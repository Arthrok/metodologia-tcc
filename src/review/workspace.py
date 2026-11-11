"""Loop incremental da revisão (Figura: coleta → triagem → validação → análise
→ snowballing → refinamento das strings → nova coleta).

Estrutura em ``data/review/``::

    workspace.json            estado global (versões das strings, syncs, rodadas)
    pool.jsonl                registros consolidados (nunca perdem proveniência)
    queries/q<N>.yaml         snapshot de cada versão aprovada das strings
    syncs/<id>.json           o que cada sincronização adicionou/fundiu (E1)
    pretriage/batches/        lotes para a skill (input) e respostas (output)
    pretriage/pretriage.jsonl pré-triagens aceitas (sugestão + prioridade)
    decisions.jsonl           decisões humanas (append-only)
    rounds/r<NNN>/            shortlist, contexto, ranking da IA, planilha de revisão
    audits/a<NNN>/            auditoria amostral da pré-triagem
    refinement/               pacotes para sugestão de novas strings

Princípio: a IA só sugere e prioriza; toda inclusão/exclusão é humana.
"""

from __future__ import annotations

import csv
import random
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from src.collectors.base import raw_version_dir
from src.review.corpus import merge_into_pool, temporal_status
from src.review.models import HumanDecision, HumanVerdict, Pretriage, RoundRanking
from src.review.ranking import build_shortlist
from src.search import FamilyMatcher, build_canonical_query, load_search_config
from src.utils.io import read_json, read_jsonl, utc_now, write_json, write_jsonl
from src.utils.text import normalize_text

PRETRIAGE_PROMPT = "mlr-screening-v2"
RANKING_PROMPT = "mlr-ranking-v1"

REVIEW_COLUMNS = [
    "rank", "paper_id", "title", "year", "temporal_status", "venue", "doi", "url",
    "abstract", "ai_suggestion", "ai_priority", "ai_criterion", "ai_justification",
    "ai_rank_justification", "decision", "criterion", "foundational", "justification",
    "reviewer", "suggested_terms",
]


class ReviewError(Exception):
    pass


def _latest_manifest(data_dir: Path, source: str, query_version: int) -> tuple[Path, dict] | None:
    for path in sorted((data_dir / "manifests" / source).glob("*.json"), reverse=True):
        manifest = read_json(path)
        if manifest.get("query_version") == query_version and manifest.get("full_run", True):
            return path, manifest
    return None


def _collection_problems(manifest: dict) -> list[str]:
    problems = [f"{fid}: {info.get('status')}" for fid, info in manifest.get("families", {}).items()
                if info.get("status") != "complete"]
    enrichment = manifest.get("enrichment")
    if enrichment and enrichment.get("status") not in ("complete", None):
        problems.append(f"abstracts: {enrichment.get('status')} "
                        f"({enrichment.get('pending', '?')} pendentes)")
    return problems


def evidence_is_verbatim(evidence: str, record: dict) -> bool:
    haystack = normalize_text(f"{record.get('title') or ''} {record.get('abstract') or ''}")
    return normalize_text(evidence).strip(" .\"'…") in haystack


class ReviewWorkspace:
    def __init__(self, root: Path):
        self.root = Path(root)

    # ------------------------------------------------------------------ #
    # Estado
    # ------------------------------------------------------------------ #

    @property
    def state_path(self) -> Path:
        return self.root / "workspace.json"

    def state(self) -> dict:
        if not self.state_path.exists():
            raise ReviewError(f"workspace não inicializado em {self.root} (use init)")
        return read_json(self.state_path)

    def _save(self, state: dict) -> None:
        state["updated_at"] = utc_now().isoformat()
        write_json(self.state_path, state)

    def protocol(self) -> dict:
        return yaml.safe_load((self.root / "review_protocol.yaml").read_text(encoding="utf-8"))

    def pool(self) -> dict[str, dict]:
        path = self.root / "pool.jsonl"
        return {r["review_id"]: r for r in read_jsonl(path)} if path.exists() else {}

    def pretriage(self) -> dict[str, dict]:
        path = self.root / "pretriage" / "pretriage.jsonl"
        return {r["paper_id"]: r for r in read_jsonl(path)} if path.exists() else {}

    def decisions(self) -> list[dict]:
        path = self.root / "decisions.jsonl"
        return read_jsonl(path) if path.exists() else []

    def current_decisions(self) -> dict[str, dict]:
        """Última decisão humana de cada paper."""
        return {d["paper_id"]: d for d in self.decisions()}

    def validated(self) -> list[str]:
        return [pid for pid, d in self.current_decisions().items() if d["decision"] == "include"]

    def snowball_seeds(self, source: str, origin: str = "any") -> tuple[dict[str, dict], dict]:
        """Seleciona sementes com política explícita e ordem determinística."""
        pool = self.pool()

        def apply_origin(ids: list[str], policy: dict) -> tuple[dict[str, dict], dict]:
            if origin not in {"any", "acl", "scopus"}:
                raise ReviewError(f"origem de sementes desconhecida: {origin}")
            before = len(ids)
            if origin != "any":
                ids = [pid for pid in ids if origin in set(pool[pid].get("sources", []))]
            return ({pid: pool[pid] for pid in ids}, {
                **policy,
                "origin_filter": origin,
                "eligible_before_origin_filter": before,
                "eligible_after_origin_filter": len(ids),
            })

        if source == "validated":
            ids = self.validated()
            return apply_origin(
                ids, {"source": "human_validated", "criteria": ["decision=include"]})
        if source != "pretriage-high":
            raise ReviewError(f"fonte de sementes desconhecida: {source}")

        decisions = self.current_decisions()
        candidates = []
        for pid, pt in self.pretriage().items():
            if pt["suggestion"] != "include" or pt["priority"] != "alta":
                continue
            if pool[pid].get("temporal_status") != "in_scope":
                continue
            if pid in decisions and decisions[pid]["decision"] != "include":
                continue
            tags = set(pt.get("lifecycle_stages", [])) | set(pt.get("transverse_dimensions", []))
            candidates.append((pid, pt, tags))

        selected: list[tuple[str, dict, set[str]]] = []
        uncovered = {f"S{i}" for i in range(1, 9)}
        uncovered |= {"qualidade", "governança", "rastreabilidade", "segurança"}
        remaining = candidates[:]
        while remaining:
            remaining.sort(key=lambda item: (
                -len(item[2] & uncovered), -len(item[2]), item[0]))
            chosen = remaining.pop(0)
            selected.append(chosen)
            uncovered -= chosen[2]
        ids = [pid for pid, _, _ in selected]
        models = sorted({pt["model"] for _, pt, _ in selected})
        return apply_origin(ids, {
            "source": "provisional_ai_pretriage",
            "criteria": ["suggestion=include", "priority=alta", "temporal_status=in_scope"],
            "ordering": "greedy coverage of lifecycle stages and transverse dimensions, then paper_id",
            "models": models,
        })

    def current_query_version(self) -> int:
        return max(int(v) for v in self.state()["query_versions"])

    # ------------------------------------------------------------------ #
    # Inicialização e versões das strings
    # ------------------------------------------------------------------ #

    def init(self, protocol_path: Path, queries_path: Path, reviewer: str) -> dict:
        if self.state_path.exists():
            raise ReviewError(f"workspace já existe em {self.root}")
        self.root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(protocol_path, self.root / "review_protocol.yaml")
        protocol = self.protocol()
        state = {
            "created_at": utc_now().isoformat(),
            "protocol_version": protocol["version"],
            "query_versions": {},
            "syncs": [],
            "rounds": [],
            "open_round": None,
            "audits": [],
            "pretriage_batches": {},
            "protocol_changes": [],
        }
        self._save(state)
        self.register_queries(queries_path, reviewer, "Strings iniciais do protocolo (Tabela 2).")
        return self.state()

    def update_protocol(self, protocol_path: Path, reviewer: str, justification: str) -> dict:
        """Versiona o protocolo e migra marcações derivadas sem apagar o histórico bruto."""
        state = self.state()
        if state.get("open_round"):
            raise ReviewError("feche a rodada aberta antes de alterar o protocolo")
        current = self.protocol()
        proposed = yaml.safe_load(Path(protocol_path).read_text(encoding="utf-8"))
        old_version = int(state.get("protocol_version", current["version"]))
        new_version = int(proposed["version"])
        if new_version <= old_version:
            raise ReviewError(f"versão do protocolo deve ser maior que {old_version}")

        old_start = int(current["scope"]["temporal_start_year"])
        new_start = int(proposed["scope"]["temporal_start_year"])
        pool = self.pool()
        changed = []
        for pid, record in pool.items():
            before = record.get("temporal_status")
            after = temporal_status(record.get("year"), new_start)
            if before != after:
                changed.append({"paper_id": pid, "year": record.get("year"),
                                "before": before, "after": after})

        decided = set(self.current_decisions())
        if affected := sorted(decided & {r["paper_id"] for r in changed}):
            raise ReviewError(
                f"{len(affected)} decisões humanas seriam afetadas pelo novo corte; "
                "faça a migração manual dessas decisões")

        protocols = self.root / "protocols"
        protocols.mkdir(parents=True, exist_ok=True)
        old_snapshot = protocols / f"v{old_version}.yaml"
        if not old_snapshot.exists():
            shutil.copy2(self.root / "review_protocol.yaml", old_snapshot)
        new_snapshot = protocols / f"v{new_version}.yaml"
        shutil.copy2(protocol_path, new_snapshot)
        shutil.copy2(protocol_path, self.root / "review_protocol.yaml")

        for item in changed:
            pool[item["paper_id"]]["temporal_status"] = item["after"]
        if pool:
            write_jsonl(self.root / "pool.jsonl", pool.values())

        accepted = self.pretriage()
        invalidated = []
        for item in changed:
            if previous := accepted.pop(item["paper_id"], None):
                invalidated.append({"paper_id": item["paper_id"], "previous": previous})
        if (self.root / "pretriage" / "pretriage.jsonl").exists():
            write_jsonl(self.root / "pretriage" / "pretriage.jsonl", accepted.values())

        pending_inputs_updated = 0
        for batch in state["pretriage_batches"].values():
            if batch["status"] != "pending":
                continue
            write_jsonl(self.root / batch["input"],
                        [self.screening_packet(pool[pid]) for pid in batch["paper_ids"]])
            pending_inputs_updated += 1

        report = {
            "from_version": old_version, "to_version": new_version,
            "old_temporal_start_year": old_start, "new_temporal_start_year": new_start,
            "reviewer": reviewer, "justification": justification,
            "changed_records": changed, "invalidated_pretriage": invalidated,
            "pending_inputs_updated": pending_inputs_updated,
            "executed_at": utc_now().isoformat(),
        }
        report_path = protocols / f"migration-v{new_version}.json"
        write_json(report_path, report)
        summary = {
            "from_version": old_version, "to_version": new_version,
            "old_temporal_start_year": old_start, "new_temporal_start_year": new_start,
            "changed_records": len(changed),
            "invalidated_pretriage": len(invalidated),
            "pending_inputs_updated": pending_inputs_updated,
            "reviewer": reviewer, "justification": justification,
            "report": str(report_path.relative_to(self.root)),
            "executed_at": report["executed_at"],
        }
        state["protocol_version"] = new_version
        state.setdefault("protocol_changes", []).append(summary)
        self._save(state)
        return summary

    def register_queries(self, queries_path: Path, reviewer: str, justification: str) -> dict:
        """Registra uma versão aprovada pelos pesquisadores (passo 11 → passo 2)."""
        state = self.state()
        config = load_search_config(queries_path)
        versions = state["query_versions"]
        if str(config.version) in versions:
            if versions[str(config.version)]["fingerprint"] != config.fingerprint():
                raise ReviewError(
                    f"q{config.version} já registrada com outro conteúdo: incremente `version` "
                    "no search_queries.yaml ao alterar as strings")
            return state
        if versions and config.version <= self.current_query_version():
            raise ReviewError(f"version deve ser maior que q{self.current_query_version()}")
        if any(v["fingerprint"] == config.fingerprint() for v in versions.values()):
            raise ReviewError("conteúdo idêntico a uma versão já registrada")
        snapshot = self.root / "queries" / f"q{config.version}.yaml"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(queries_path, snapshot)
        versions[str(config.version)] = {
            "fingerprint": config.fingerprint(),
            "approved_by": reviewer,
            "justification": justification,
            "registered_at": utc_now().isoformat(),
            "registered_after_round": state["rounds"][-1]["round_id"] if state["rounds"] else None,
            "snapshot": str(snapshot.relative_to(self.root)),
            "queries": {f.id: build_canonical_query(config, f) for f in config.families.values()},
        }
        self._save(state)
        return state

    # ------------------------------------------------------------------ #
    # Passo 4: sincronizar coletas (e candidatos do snowballing) no pool
    # ------------------------------------------------------------------ #

    def sync(self, data_dir: Path, allow_incomplete: bool = False) -> dict:
        state = self.state()
        protocol = self.protocol()
        version = self.current_query_version()
        fingerprint = state["query_versions"][str(version)]["fingerprint"]
        sync_id = f"sync{len(state['syncs']) + 1:03d}"
        pool = list(self.pool().values())
        start_year = protocol["scope"]["temporal_start_year"]

        report = {"sync_id": sync_id, "executed_at": utc_now().isoformat(),
                  "query_version": version, "collections": {}, "warnings": []}
        for source in protocol["scope"]["sources"]:
            found = _latest_manifest(data_dir, source, version)
            if found is None:
                raise ReviewError(f"sem coleta completa de {source} para q{version}; "
                                  f"rode scripts/collect_{source}.py")
            path, manifest = found
            if manifest.get("query_fingerprint") != fingerprint:
                raise ReviewError(f"coleta {path.name} de {source} não corresponde às strings q{version}")
            problems = _collection_problems(manifest)
            if problems and not allow_incomplete:
                raise ReviewError(f"coleta de {source} incompleta ({'; '.join(problems)}). "
                                  "Complete a coleta ou use --allow-incomplete")
            if problems:
                report["warnings"].append(f"{source}: {'; '.join(problems)}")
            records = read_jsonl(raw_version_dir(data_dir, source, version) / "all_records.jsonl")
            for r in records:
                r["_query_versions"] = [version]
            pool, merged = merge_into_pool(pool, records, origin="search",
                                           sync_id=sync_id, start_year=start_year)
            report["collections"][source] = {"manifest": str(path), **merged["stats"],
                                             "duplicates": merged["duplicates"],
                                             "added": merged["added"]}

        snowball = data_dir / "raw" / "snowball" / "candidates.jsonl"
        if snowball.exists():
            pool, merged = merge_into_pool(pool, read_jsonl(snowball), origin="snowball",
                                           sync_id=sync_id, start_year=start_year)
            report["collections"]["snowball"] = {"file": str(snowball), **merged["stats"],
                                                 "duplicates": merged["duplicates"],
                                                 "added": merged["added"]}

        write_jsonl(self.root / "pool.jsonl", pool)
        write_json(self.root / "syncs" / f"{sync_id}.json", report)
        summary = {
            "sync_id": sync_id, "executed_at": report["executed_at"], "query_version": version,
            "new_papers": sum(c["new_papers"] for c in report["collections"].values()),
            "pool_size": len(pool), "warnings": report["warnings"],
            "after_round": state["rounds"][-1]["round_id"] if state["rounds"] else None,
        }
        state["syncs"].append(summary)
        self._save(state)
        return summary

    # ------------------------------------------------------------------ #
    # Passo 5: pré-triagem pela skill, em lotes
    # ------------------------------------------------------------------ #

    @property
    def batches_dir(self) -> Path:
        return self.root / "pretriage" / "batches"

    @staticmethod
    def screening_packet(record: dict) -> dict:
        return {
            "paper_id": record["review_id"], "title": record.get("title"),
            "abstract": record.get("abstract"), "abstract_available": bool(record.get("abstract")),
            "year": record.get("year"), "temporal_status": record.get("temporal_status"),
            "venue": record.get("venue"), "document_type": record.get("document_type"),
            "keywords": record.get("keywords") or [], "search_families": record.get("search_families"),
            "origins": record.get("origins"),
        }

    def make_pretriage_batches(self, size: int | None = None) -> dict:
        state = self.state()
        size = size or self.protocol()["screening"]["pretriage_batch_size"]
        done = set(self.pretriage())
        pending = {bid: b for bid, b in state["pretriage_batches"].items() if b["status"] == "pending"}
        queued = {pid for b in pending.values() for pid in b["paper_ids"]}
        todo = [r for pid, r in self.pool().items() if pid not in done and pid not in queued]
        created = []
        n = len(state["pretriage_batches"])
        for i in range(0, len(todo), size):
            n += 1
            bid = f"batch_{n:04d}"
            chunk = todo[i:i + size]
            write_jsonl(self.batches_dir / f"{bid}.input.jsonl", [self.screening_packet(r) for r in chunk])
            state["pretriage_batches"][bid] = {
                "status": "pending", "created_at": utc_now().isoformat(),
                "paper_ids": [r["review_id"] for r in chunk],
                "input": str((self.batches_dir / f"{bid}.input.jsonl").relative_to(self.root)),
                "output": str((self.batches_dir / f"{bid}.output.jsonl").relative_to(self.root)),
            }
            created.append(bid)
        self._save(state)
        return {"created": created, "pending_total": len(pending) + len(created),
                "records_in_new_batches": len(todo)}

    def import_pretriage(self) -> dict:
        state = self.state()
        pool = self.pool()
        accepted = self.pretriage()
        imported, errors = [], {}
        for bid, batch in sorted(state["pretriage_batches"].items()):
            output = self.root / batch["output"]
            if batch["status"] != "pending" or not output.exists():
                continue
            problems, parsed = [], []
            expected = set(batch["paper_ids"])
            for i, row in enumerate(read_jsonl(output), 1):
                try:
                    pt = Pretriage.model_validate(row)
                except ValueError as exc:
                    problems.append(f"linha {i}: {exc}")
                    continue
                if pt.paper_id not in expected:
                    problems.append(f"linha {i}: {pt.paper_id} não pertence ao lote")
                    continue
                record = pool[pt.paper_id]
                quotes = list(pt.evidence) + [a.evidence for a in pt.assessments if a.evidence]
                if bad := [q for q in quotes if not evidence_is_verbatim(q, record)]:
                    problems.append(f"linha {i} ({pt.paper_id}): evidência não literal: {bad[0][:80]!r}")
                if pt.primary_criterion == "E2" and record.get("temporal_status") != "pre_cutoff":
                    problems.append(f"linha {i} ({pt.paper_id}): E2 sugerido para registro no recorte")
                parsed.append(pt)
            if missing := expected - {p.paper_id for p in parsed}:
                problems.append(f"{len(missing)} registros do lote sem resposta")
            if problems:
                errors[bid] = problems
                continue
            for pt in parsed:
                accepted[pt.paper_id] = pt.model_dump(mode="json")
            batch["status"] = "imported"
            batch["imported_at"] = utc_now().isoformat()
            imported.append(bid)
        write_jsonl(self.root / "pretriage" / "pretriage.jsonl", accepted.values())
        self._save(state)
        return {"imported": imported, "rejected": errors, "pretriaged": len(accepted),
                "pool": len(pool),
                "suggestions": dict(Counter(p["suggestion"] for p in accepted.values()))}

    # ------------------------------------------------------------------ #
    # Passos 5–7: rodadas de dez candidatos
    # ------------------------------------------------------------------ #

    def round_dir(self, round_id: str) -> Path:
        return self.root / "rounds" / round_id

    def _round(self, state: dict, round_id: str) -> dict:
        for r in state["rounds"]:
            if r["round_id"] == round_id:
                return r
        raise ReviewError(f"rodada {round_id} não existe")

    def new_round(self) -> dict:
        state = self.state()
        if state["open_round"]:
            raise ReviewError(f"feche a rodada {state['open_round']} antes de abrir outra")
        protocol = self.protocol()["screening"]
        pool, pretriage = self.pool(), self.pretriage()
        reviewed = set(self.current_decisions())
        validated = self.validated()
        shortlist = build_shortlist(pool, pretriage, reviewed, validated, protocol["shortlist_size"])
        if not shortlist:
            raise ReviewError("nenhum candidato pré-triado e não revisado; rode a pré-triagem")

        round_id = f"r{len(state['rounds']) + 1:03d}"
        rdir = self.round_dir(round_id)
        write_jsonl(rdir / "shortlist.jsonl", [
            {**c, "record": self.screening_packet(pool[c["paper_id"]]),
             "pretriage": pretriage[c["paper_id"]]} for c in shortlist])
        decisions = self.current_decisions()
        write_jsonl(rdir / "validated_references.jsonl", [
            {"paper_id": pid, "title": pool[pid].get("title"), "abstract": pool[pid].get("abstract"),
             "year": pool[pid].get("year"), "human_justification": decisions[pid]["justification"],
             "lifecycle_stages": pretriage.get(pid, {}).get("lifecycle_stages", [])}
            for pid in validated])
        n = min(protocol["round_size"], len(shortlist))
        state["rounds"].append({
            "round_id": round_id, "status": "awaiting_ai_ranking",
            "opened_at": utc_now().isoformat(), "query_version": self.current_query_version(),
            "shortlist_size": len(shortlist), "candidates_expected": n,
            "validated_before": len(validated),
            "unreviewed_pretriaged": sum(1 for p in pretriage if p not in reviewed),
            "unreviewed_without_pretriage": sum(1 for p in pool if p not in reviewed and p not in pretriage),
        })
        state["open_round"] = round_id
        self._save(state)
        return state["rounds"][-1]

    def import_ranking(self, round_id: str, ranking_path: Path) -> dict:
        state = self.state()
        rnd = self._round(state, round_id)
        if rnd["status"] != "awaiting_ai_ranking":
            raise ReviewError(f"{round_id} não aguarda ranking (status: {rnd['status']})")
        ranking = RoundRanking.model_validate(read_json(ranking_path))
        if ranking.round_id != round_id:
            raise ReviewError(f"ranking é de {ranking.round_id}, não de {round_id}")
        shortlist = {c["paper_id"]: c for c in read_jsonl(self.round_dir(round_id) / "shortlist.jsonl")}
        ids = [c.paper_id for c in ranking.candidates]
        if len(ids) != rnd["candidates_expected"]:
            raise ReviewError(f"esperados exatamente {rnd['candidates_expected']} candidatos, vieram {len(ids)}")
        if len(set(ids)) != len(ids):
            raise ReviewError("paper_id repetido no ranking")
        if unknown := [i for i in ids if i not in shortlist]:
            raise ReviewError(f"candidatos fora da shortlist: {unknown}")
        if sorted(c.rank for c in ranking.candidates) != list(range(1, len(ids) + 1)):
            raise ReviewError("ranks devem ser 1..N sem repetição")

        write_json(self.round_dir(round_id) / "ranking.json", ranking.model_dump(mode="json"))
        rows = []
        for c in sorted(ranking.candidates, key=lambda c: c.rank):
            rec, pt = shortlist[c.paper_id]["record"], shortlist[c.paper_id]["pretriage"]
            full = self.pool()[c.paper_id]
            rows.append({
                "rank": c.rank, "paper_id": c.paper_id, "title": rec["title"], "year": rec["year"],
                "temporal_status": rec["temporal_status"], "venue": rec["venue"],
                "doi": full.get("doi") or "", "url": full.get("url") or "",
                "abstract": rec["abstract"] or "", "ai_suggestion": pt["suggestion"],
                "ai_priority": pt["priority"], "ai_criterion": pt.get("primary_criterion") or "",
                "ai_justification": pt["justification"], "ai_rank_justification": c.justification,
            })
        self._write_review_sheet(self.round_dir(round_id) / "review.csv", rows)
        rnd.update(status="awaiting_human_review", ranked_at=utc_now().isoformat(),
                   candidates=[c.paper_id for c in sorted(ranking.candidates, key=lambda c: c.rank)],
                   ranking_model=ranking.model)
        self._save(state)
        return rnd

    @staticmethod
    def _write_review_sheet(path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=REVIEW_COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k, "") for k in REVIEW_COLUMNS})

    def record_decision(self, decision: HumanDecision) -> dict:
        state = self.state()
        pool = self.pool()
        record = pool.get(decision.paper_id)
        if record is None:
            raise ReviewError(f"{decision.paper_id} não está no pool")
        current = self.current_decisions().get(decision.paper_id)
        if decision.round_id:
            rnd = self._round(state, decision.round_id)
            if rnd["status"] != "awaiting_human_review":
                raise ReviewError(f"{decision.round_id} não está em revisão humana")
            if decision.paper_id not in rnd["candidates"]:
                raise ReviewError(f"{decision.paper_id} não é candidato de {decision.round_id}")
        elif not current or current["decision"] != HumanVerdict.FULL_TEXT.value:
            raise ReviewError("fora de uma rodada só é possível resolver papers marcados full_text")

        pre = record.get("temporal_status") == "pre_cutoff"
        if decision.decision == HumanVerdict.INCLUDE and pre and not decision.foundational:
            raise ReviewError("inclusão anterior ao recorte exige --foundational (exceção de I1) com justificativa")
        if decision.primary_criterion == "E2" and not pre:
            raise ReviewError("E2 só se aplica a registros anteriores ao recorte temporal")
        path = self.root / "decisions.jsonl"
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(decision.model_dump_json() + "\n")
        return decision.model_dump(mode="json")

    def import_review_sheet(self, round_id: str, csv_path: Path, default_reviewer: str | None = None) -> dict:
        recorded, skipped = [], []
        with open(csv_path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not (row.get("decision") or "").strip():
                    skipped.append(row["paper_id"])
                    continue
                reviewer = (row.get("reviewer") or "").strip() or default_reviewer
                if not reviewer:
                    raise ReviewError(f"{row['paper_id']}: preencha a coluna reviewer")
                decision = HumanDecision(
                    paper_id=row["paper_id"], round_id=round_id,
                    decision=row["decision"].strip().lower(),
                    primary_criterion=(row.get("criterion") or "").strip().upper() or None,
                    foundational=(row.get("foundational") or "").strip().lower() in ("1", "true", "sim", "x", "yes"),
                    reviewer=reviewer, justification=(row.get("justification") or "").strip(),
                    suggested_terms=[t.strip() for t in (row.get("suggested_terms") or "").split(";") if t.strip()],
                    decided_at=utc_now(),
                )
                self.record_decision(decision)
                recorded.append(row["paper_id"])
        return {"recorded": len(recorded), "blank": skipped}

    def close_round(self, round_id: str) -> dict:
        state = self.state()
        rnd = self._round(state, round_id)
        if rnd["status"] != "awaiting_human_review":
            raise ReviewError(f"{round_id} não está em revisão humana")
        decisions = {d["paper_id"]: d for d in self.decisions() if d.get("round_id") == round_id}
        if missing := [p for p in rnd["candidates"] if p not in decisions]:
            raise ReviewError(f"faltam decisões humanas para {len(missing)} candidatos: {missing}")
        pretriage = self.pretriage()
        equivalent = {"include": "include", "exclude": "exclude", "ambiguous": "full_text"}
        agree = sum(equivalent[pretriage[p]["suggestion"]] == decisions[p]["decision"] for p in rnd["candidates"])
        verdicts = Counter(decisions[p]["decision"] for p in rnd["candidates"])
        rnd.update(
            status="closed", closed_at=utc_now().isoformat(),
            result={
                "include": verdicts.get("include", 0), "exclude": verdicts.get("exclude", 0),
                "full_text": verdicts.get("full_text", 0),
                "exclusion_criteria": dict(Counter(decisions[p]["primary_criterion"] for p in rnd["candidates"]
                                                   if decisions[p]["decision"] == "exclude")),
                "precision_at_round": verdicts.get("include", 0) / len(rnd["candidates"]),
                "ai_pretriage_agreement": agree / len(rnd["candidates"]),
                "validated_total": len(self.validated()),
            },
        )
        state["open_round"] = None
        self._save(state)
        return rnd

    # ------------------------------------------------------------------ #
    # Auditoria amostral da pré-triagem (controle de qualidade da IA)
    # ------------------------------------------------------------------ #

    def new_audit(self, size: int | None = None) -> dict:
        state = self.state()
        protocol = self.protocol()["screening"]
        size = size or protocol["audit_sample_size"]
        reviewed = set(self.current_decisions())
        audited = {p for a in state["audits"] for p in a["paper_ids"]}
        candidates = sorted(p for p in self.pretriage() if p not in reviewed and p not in audited)
        audit_id = f"a{len(state['audits']) + 1:03d}"
        seed = f"{protocol['random_seed']}-{audit_id}"
        sample = random.Random(seed).sample(candidates, min(size, len(candidates)))
        pool, pretriage = self.pool(), self.pretriage()
        path = self.root / "audits" / audit_id / "audit.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        columns = ["paper_id", "title", "year", "abstract", "ai_suggestion", "ai_priority",
                   "ai_criterion", "ai_justification", "human_agrees", "human_suggestion",
                   "reviewer", "comment"]
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns)
            writer.writeheader()
            for pid in sample:
                r, pt = pool[pid], pretriage[pid]
                writer.writerow({"paper_id": pid, "title": r.get("title"), "year": r.get("year"),
                                 "abstract": r.get("abstract") or "", "ai_suggestion": pt["suggestion"],
                                 "ai_priority": pt["priority"], "ai_criterion": pt.get("primary_criterion") or "",
                                 "ai_justification": pt["justification"]})
        state["audits"].append({"audit_id": audit_id, "seed": seed, "created_at": utc_now().isoformat(),
                                "paper_ids": sample, "status": "open", "sheet": str(path.relative_to(self.root))})
        self._save(state)
        return state["audits"][-1]

    def import_audit(self, audit_id: str, csv_path: Path) -> dict:
        state = self.state()
        audit = next((a for a in state["audits"] if a["audit_id"] == audit_id), None)
        if audit is None:
            raise ReviewError(f"auditoria {audit_id} não existe")
        rows = {}
        with open(csv_path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                agrees = (row.get("human_agrees") or "").strip().lower()
                if agrees:
                    if agrees not in ("sim", "nao", "não", "yes", "no"):
                        raise ReviewError(f"{row['paper_id']}: human_agrees deve ser sim/não")
                    if not (row.get("reviewer") or "").strip():
                        raise ReviewError(f"{row['paper_id']}: preencha reviewer")
                    rows[row["paper_id"]] = {
                        "paper_id": row["paper_id"], "agrees": agrees in ("sim", "yes"),
                        "ai_suggestion": row["ai_suggestion"],
                        "human_suggestion": (row.get("human_suggestion") or "").strip() or None,
                        "reviewer": row["reviewer"].strip(), "comment": row.get("comment") or "",
                    }
        if missing := [p for p in audit["paper_ids"] if p not in rows]:
            raise ReviewError(f"faltam {len(missing)} linhas preenchidas na auditoria")
        write_jsonl(self.root / "audits" / audit_id / "verdicts.jsonl", rows.values())
        by_suggestion: dict[str, list[bool]] = {}
        for r in rows.values():
            by_suggestion.setdefault(r["ai_suggestion"], []).append(r["agrees"])
        audit.update(status="closed", closed_at=utc_now().isoformat(), result={
            "agreement": sum(r["agrees"] for r in rows.values()) / len(rows) if rows else None,
            "agreement_by_suggestion": {k: sum(v) / len(v) for k, v in by_suggestion.items()},
            # IA sugeriu excluir e o humano discordou: possível falso negativo.
            "possible_false_negatives": sum(1 for r in rows.values()
                                            if r["ai_suggestion"] == "exclude" and not r["agrees"]),
        })
        self._save(state)
        return audit

    # ------------------------------------------------------------------ #
    # Passo 11: pacote para sugestão de novas strings
    # ------------------------------------------------------------------ #

    def refinement_packet(self) -> Path:
        state = self.state()
        version = self.current_query_version()
        config = load_search_config(self.root / "queries" / f"q{version}.yaml")
        matcher = FamilyMatcher(config)
        pool, decisions, pretriage = self.pool(), self.current_decisions(), self.pretriage()

        term_stats: dict[tuple[str, str], Counter] = {}
        for pid, d in decisions.items():
            text = normalize_text(f"{pool[pid].get('title') or ''} {pool[pid].get('abstract') or ''}")
            for family, terms in matcher.match_families(text).items():
                for term in terms:
                    term_stats.setdefault((family, term), Counter())[d["decision"]] += 1
        terms = [{"family": f, "term": t, "reviewed": sum(c.values()), "included": c["include"],
                  "precision_observed": c["include"] / sum(c.values())}
                 for (f, t), c in term_stats.items()]
        terms.sort(key=lambda x: (x["precision_observed"], -x["reviewed"]))

        packet = {
            "generated_at": utc_now().isoformat(),
            "after_round": state["rounds"][-1]["round_id"] if state["rounds"] else None,
            "current_query_version": version,
            "current_queries": state["query_versions"][str(version)]["queries"],
            "domain_terms": config.domain_terms,
            "families": {f.id: {"label": f.label, "terms": f.terms} for f in config.families.values()},
            "validated_references": [
                {"paper_id": pid, "title": pool[pid].get("title"), "abstract": pool[pid].get("abstract"),
                 "keywords": pool[pid].get("keywords") or [], "search_families": pool[pid].get("search_families"),
                 "lifecycle_stages": pretriage.get(pid, {}).get("lifecycle_stages", []),
                 "human_justification": decisions[pid]["justification"]}
                for pid in self.validated()],
            "excluded_examples": [
                {"paper_id": pid, "title": pool[pid].get("title"), "criterion": d["primary_criterion"],
                 "human_justification": d["justification"]}
                for pid, d in decisions.items() if d["decision"] == "exclude"],
            "reviewer_suggested_terms": dict(Counter(t for d in decisions.values() for t in d.get("suggested_terms", []))),
            "term_performance": terms,
        }
        name = f"packet_q{version}_{packet['after_round'] or 'r000'}.json"
        path = self.root / "refinement" / name
        write_json(path, packet)
        return path

    # ------------------------------------------------------------------ #
    # Status e critérios de parada
    # ------------------------------------------------------------------ #

    def status(self) -> dict[str, Any]:
        state = self.state()
        protocol = self.protocol()
        pool, pretriage, decisions = self.pool(), self.pretriage(), self.current_decisions()
        verdicts = Counter(d["decision"] for d in decisions.values())
        return {
            "query_version": self.current_query_version(),
            "pool": len(pool),
            "pool_by_temporal_status": dict(Counter(r["temporal_status"] for r in pool.values())),
            "pool_without_abstract": sum(1 for r in pool.values() if not r.get("abstract")),
            "pretriaged": len(pretriage),
            "pretriage_suggestions": dict(Counter(p["suggestion"] for p in pretriage.values())),
            "pending_batches": sum(1 for b in state["pretriage_batches"].values() if b["status"] == "pending"),
            "human_reviewed": len(decisions),
            "human_decisions": dict(verdicts),
            "unreviewed": len(pool) - len(decisions),
            "rounds_closed": sum(1 for r in state["rounds"] if r["status"] == "closed"),
            "open_round": state["open_round"],
            "stopping": self.stopping_indicators(state, protocol, pretriage),
        }

    def stopping_indicators(self, state: dict, protocol: dict, pretriage: dict) -> dict:
        cfg = protocol["stopping"]
        window = cfg["window_rounds"]
        closed = [r for r in state["rounds"] if r["status"] == "closed"]
        recent = closed[-window:]

        includes_recent = sum(r["result"]["include"] for r in recent)
        low_yield = len(recent) == window and includes_recent <= cfg["max_includes_in_window"]

        last_query = max(state["query_versions"].values(), key=lambda v: v["registered_at"])
        after = last_query["registered_after_round"]
        rounds_since = (len(closed) - next((i + 1 for i, r in enumerate(closed) if r["round_id"] == after), 0))
        stable = rounds_since >= cfg["min_rounds_since_query_change"]

        validated = self.validated()
        stage_counts = Counter(s for pid in validated for s in pretriage.get(pid, {}).get("lifecycle_stages", []))
        dims = Counter(d for pid in validated for d in pretriage.get(pid, {}).get("transverse_dimensions", []))
        stages = protocol["lifecycle_stages"]
        coverage_ok = all(stage_counts.get(s, 0) >= cfg["min_includes_per_stage"] for s in stages)

        # Saturação: as inclusões da janela não trouxeram etapa ou dimensão nova.
        decisions = self.decisions()
        recent_ids = {r["round_id"] for r in recent}
        recent_inc = {d["paper_id"] for d in decisions if d.get("round_id") in recent_ids and d["decision"] == "include"}
        before = [p for p in validated if p not in recent_inc]
        themes = lambda ids: {x for p in ids for x in pretriage.get(p, {}).get("lifecycle_stages", [])
                              + pretriage.get(p, {}).get("transverse_dimensions", [])}
        new_themes = sorted(themes(recent_inc) - themes(before))
        saturated = len(recent) == window and not new_themes

        return {
            "note": "Indicadores para apoiar a decisão dos pesquisadores; não encerram o loop sozinhos.",
            "query_stabilization": {"met": stable, "rounds_since_last_query_version": rounds_since,
                                    "required": cfg["min_rounds_since_query_change"]},
            "low_new_relevant": {"met": low_yield, "includes_in_last_rounds": includes_recent,
                                 "window": window, "max": cfg["max_includes_in_window"]},
            "thematic_saturation": {"met": saturated, "new_themes_in_window": new_themes},
            "coverage": {"met": coverage_ok, "validated_by_stage": {s: stage_counts.get(s, 0) for s in stages},
                         "validated_by_dimension": dict(dims), "min_per_stage": cfg["min_includes_per_stage"]},
        }
