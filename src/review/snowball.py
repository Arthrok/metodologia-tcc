"""Passo 10: snowballing retrospectivo (referências) e progressivo (citações)
via Scopus, a partir de fontes validadas ou de sementes provisórias cuja
política de seleção fica registrada no manifest.

Saída em ``data/raw/snowball/``:

    candidates.jsonl       PaperRecords candidatos (entram no pool no próximo sync)
    state.json             sementes já processadas por direção
    raw/<seed>/            respostas brutas (REF e REFEID)

Os candidatos não passam pelas strings de busca (Wohlin, 2014): seguem para a
mesma pré-triagem e rodadas de revisão humana. Nenhum filtro temporal é
aplicado aqui; anteriores ao recorte podem ser fundacionais.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.collectors.scopus import (
    ScopusClient, ScopusError, _as_list, merge_fields, page_entries, parse_abstract,
    parse_search_entry, total_results,
)
from src.models import PaperRecord, SearchProvenance
from src.review.corpus import normalized_doi
from src.utils.io import read_json, read_jsonl, run_timestamp, utc_now, write_json, write_jsonl

log = logging.getLogger("snowball")

# A resposta inicial sem parâmetros traz até 40 itens. Páginas adicionais do
# serviço institucional aceitam no máximo 10 referências por chamada.
REF_PAGE = 10
# O nível básico da Scopus Search limita ``count`` a 25; níveis institucionais
# aceitam páginas maiores, mas 25 mantém a coleta portável e integral.
CITING_PAGE = 25
BACKWARD, FORWARD = "backward", "forward"


def parse_references(response: dict) -> tuple[int, list[str]]:
    """(total de referências, Scopus IDs) de uma página da view REF."""
    refs = (response.get("abstracts-retrieval-response") or {}).get("references") or {}
    total = int(refs.get("@total-references") or 0)
    ids = []
    for ref in _as_list(refs.get("reference")):
        sid = ref.get("scopus-id") or (ref.get("scopus-eid") or "").removeprefix("2-s2.0-")
        if sid:
            ids.append(str(sid))
    return total, ids


class ScopusSnowball:
    def __init__(self, client: ScopusClient, data_dir: Path):
        self.client = client
        self.data_dir = Path(data_dir)
        self.dir = self.data_dir / "raw" / "snowball"
        self.metadata_dir = self.data_dir / "raw" / "scopus" / "metadata"  # cache compartilhado
        self.started_at = utc_now()
        self.stats = {"requests_before": client.request_count, "seeds": 0, "unresolved_seeds": [],
                      "references": 0, "citing": 0, "metadata_fetched": 0, "metadata_cached": 0,
                      "errors": []}

    # ---- sementes ---------------------------------------------------------- #

    def resolve_scopus_id(self, record: dict) -> str | None:
        for rid in record.get("source_records", []):
            if rid.startswith("scopus:"):
                return rid.split(":", 1)[1]
        doi = normalized_doi(record.get("doi"))
        if not doi:
            return None
        page = self.client.search(f"DOI({doi})", start=0, count=1)
        entries = page_entries(page)
        return parse_search_entry(entries[0])["source_id"] if entries else None

    # ---- coleta ------------------------------------------------------------ #

    def references(self, seed_pid: str, sid: str) -> list[str]:
        response = self.client.get_references(sid)
        if response is None:
            return []
        write_json(self.dir / "raw" / seed_pid / "ref_0001.json", response)
        total, ids = parse_references(response)
        refs = (response.get("abstracts-retrieval-response") or {}).get("references") or {}
        returned = len(_as_list(refs.get("reference")))

        # ``startref`` é baseado em 1 (zero funciona como alias da primeira
        # posição). Contamos também referências não resolvidas, pois elas
        # ocupam posições apesar de não produzirem Scopus ID.
        while returned < total:
            start = returned + 1
            count = min(REF_PAGE, total - returned)
            response = None
            while count:
                try:
                    response = self.client.get_references(sid, start=start, count=count)
                    break
                except ScopusError as exc:
                    if (exc.status == 400 and
                            "startref' or 'refcount" in str(exc)):
                        count -= 1
                        continue
                    raise
            if response is None:
                break
            write_json(self.dir / "raw" / seed_pid / f"ref_{start:04d}.json", response)
            refs = (response.get("abstracts-retrieval-response") or {}).get("references") or {}
            raw_page = _as_list(refs.get("reference"))
            if not raw_page:
                break
            _, page_ids = parse_references(response)
            ids.extend(page_ids)
            returned += len(raw_page)
        return ids

    def citing(self, seed_pid: str, sid: str) -> list[str]:
        query = f"REFEID(2-s2.0-{sid})"
        ids, start, total = [], 0, None
        while total is None or start < total:
            page = self.client.search(query, start=start, count=CITING_PAGE)
            write_json(self.dir / "raw" / seed_pid / f"citing_{start // CITING_PAGE + 1:04d}.json", page)
            total = total_results(page)
            entries = page_entries(page)
            if not entries:
                break
            ids.extend(parse_search_entry(e)["source_id"] for e in entries)
            start += CITING_PAGE
        return ids

    def metadata(self, sid: str) -> dict | None:
        path = self.metadata_dir / f"{sid}.json"
        if path.exists():
            self.stats["metadata_cached"] += 1
            data = read_json(path)
            return None if data.get("_not_found") else data
        response = self.client.get_abstract(sid)
        self.stats["metadata_fetched"] += 1
        write_json(path, response if response is not None else
                   {"_not_found": True, "scopus_id": sid, "retrieved_at": utc_now().isoformat()})
        return response

    def to_record(self, sid: str, provenance: SearchProvenance) -> PaperRecord | None:
        data = self.metadata(sid)
        if data is None:
            return None
        base = {"source_id": sid, "title": "", "abstract": None, "doi": None, "authors": [],
                "year": None, "publication_date": None, "venue": None, "document_type": None,
                "url": None, "pdf_url": None, "extra": {"enrichment": "META_ABS"}}
        fields = merge_fields(base, parse_abstract(data))
        if not fields["title"]:
            return None
        record = PaperRecord(source="scopus", retrieved_at=self.started_at, **fields)
        record.add_occurrence(provenance)
        return record

    # ---- execução ---------------------------------------------------------- #

    def run(self, seeds: dict[str, dict], directions=(BACKWARD, FORWARD),
            max_seeds: int | None = None, seed_selection: dict | None = None) -> dict:
        state_path = self.dir / "state.json"
        state = read_json(state_path) if state_path.exists() else {"done": {}}
        candidates = {r["source_id"]: PaperRecord.model_validate(r)
                      for r in read_jsonl(self.dir / "candidates.jsonl")} \
            if (self.dir / "candidates.jsonl").exists() else {}
        pending = [(pid, rec) for pid, rec in seeds.items()
                   if any(d not in state["done"].get(pid, {}) for d in directions)]
        if max_seeds is not None:
            pending = pending[:max_seeds]
        selected_seed_ids = [pid for pid, _ in pending]

        for pid, rec in pending:
            self.stats["seeds"] += 1
            try:
                sid = self.resolve_scopus_id(rec)
                if sid is None:
                    self.stats["unresolved_seeds"].append(pid)
                    state["done"][pid] = {d: {"status": "unresolved"} for d in directions}
                    continue
                for direction in directions:
                    if direction in state["done"].get(pid, {}):
                        continue
                    found = self.references(pid, sid) if direction == BACKWARD else self.citing(pid, sid)
                    self.stats["references" if direction == BACKWARD else "citing"] += len(found)
                    prov = SearchProvenance(
                        source="scopus", family="SB-B" if direction == BACKWARD else "SB-F",
                        stage="snowballing",
                        canonical_query=f"{direction} snowballing de {pid}",
                        executed_query=(f"abstract/scopus_id/{sid}?view=REF" if direction == BACKWARD
                                        else f"REFEID(2-s2.0-{sid})"),
                        searched_fields=[], seed=pid, retrieved_at=self.started_at,
                    )
                    for cid in dict.fromkeys(found):
                        if cid in candidates:
                            candidates[cid].add_occurrence(prov)
                        elif (record := self.to_record(cid, prov)) is not None:
                            candidates[cid] = record
                    state["done"].setdefault(pid, {})[direction] = {
                        "status": "complete", "scopus_id": sid, "found": len(found),
                        "at": utc_now().isoformat()}
                    write_json(state_path, state)
                    write_jsonl(self.dir / "candidates.jsonl", candidates.values())
            except ScopusError as exc:
                # Erros de acesso/quota interrompem: o restante é retomado na próxima execução.
                self.stats["errors"].append(f"{pid}: {type(exc).__name__}: {exc}")
                log.error("[SNOWBALL] %s interrompido: %s", pid, exc)
                break

        write_json(state_path, state)
        write_jsonl(self.dir / "candidates.jsonl", candidates.values())
        manifest = {
            "source": "snowball", "backend": "scopus", "executed_at": self.started_at.isoformat(),
            "finished_at": utc_now().isoformat(), "directions": list(directions),
            "method": {"backward": "Abstract Retrieval view=REF", "forward": "Scopus Search REFEID()"},
            "seed_selection": seed_selection or {"source": "human_validated"},
            "seeds_available": len(seeds), "seed_ids_selected": selected_seed_ids,
            "search_strings_applied": False, "temporal_filter": None,
            **{k: v for k, v in self.stats.items() if k != "requests_before"},
            "requests_made": self.client.request_count - self.stats["requests_before"],
            "seeds_pending": len([1 for pid in seeds
                                  if any(d not in state["done"].get(pid, {}) for d in directions)]),
            "candidates_total": len(candidates),
            "rate_limit": self.client.rate_limit, "proxy": self.client.proxy,
        }
        write_json(self.data_dir / "manifests" / "snowball" / f"{run_timestamp(self.started_at)}.json", manifest)
        return manifest
