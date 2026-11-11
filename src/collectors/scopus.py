"""Coletor Scopus: Scopus Search (S1–S8) + Abstract Retrieval (META_ABS).

Fluxo:

    Scopus Search (por família, paginado, páginas brutas salvas)
        ↓
    Scopus IDs das S1–S8
        ↓
    IDs únicos → Abstract Retrieval (cache em raw/scopus/metadata/)
        ↓
    PaperRecord (records.jsonl por família + all_records.jsonl)

Nenhum filtro temporal é aplicado. Execuções interrompidas são retomadas a
partir da última página salva (``state.json`` de cada família).
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import requests
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt

from src.collectors.base import BaseCollector
from src.models import PaperRecord, SearchProvenance
from src.search import SearchFamily, build_canonical_query, build_scopus_query
from src.utils.io import read_json, utc_now, write_json, write_jsonl

log = logging.getLogger("scopus")

BASE_URL = "https://api.elsevier.com/content"
SEARCH_VIEW = "STANDARD"
PAGE_SIZE = 200          # máximo por chamada no view STANDARD
OFFSET_LIMIT = 5000      # limite de start+count sem cursor
ABSTRACT_VIEW = "META_ABS"
SEARCHED_FIELDS = ["title", "abstract", "keywords"]
ADAPTER = "TITLE-ABS-KEY"

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
RATE_LIMIT_HEADERS = {
    "X-RateLimit-Limit": "limit",
    "X-RateLimit-Remaining": "remaining",
    "X-RateLimit-Reset": "reset",
}


# --------------------------------------------------------------------------- #
# Erros
# --------------------------------------------------------------------------- #

class ScopusError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class ScopusAuthError(ScopusError):
    """401/403: chave inválida, sem entitlement ou fora da rede institucional."""


class ScopusQuotaError(ScopusError):
    """Quota semanal esgotada — não adianta tentar novamente."""


class ScopusRetryableError(ScopusError):
    def __init__(self, message: str, status: int | None = None, retry_after: float | None = None):
        super().__init__(message, status)
        self.retry_after = retry_after


class ScopusIncompleteError(ScopusError):
    """A execução não conseguiu coletar o universo completo de resultados."""


# --------------------------------------------------------------------------- #
# Cliente HTTP
# --------------------------------------------------------------------------- #

def _error_detail(response: requests.Response) -> str:
    try:
        body = response.json()
        err = body.get("service-error", {}).get("status", {})
        if err:
            return f"{err.get('statusCode', '')}: {err.get('statusText', '')}".strip(": ")
        return str(body.get("error-response", body))[:300]
    except ValueError:
        return response.text[:300]


def _exponential_wait(retry_state) -> float:
    exc = retry_state.outcome.exception()
    if isinstance(exc, ScopusRetryableError) and exc.retry_after:
        return min(exc.retry_after, 120.0)
    return min(2 ** (retry_state.attempt_number - 1), 60.0)  # 1, 2, 4, 8, ...


class ScopusClient:
    def __init__(
        self,
        api_key: str,
        inst_token: str | None = None,
        session: requests.Session | None = None,
        base_url: str = BASE_URL,
        timeout: float = 60.0,
        max_attempts: int = 6,
        min_interval: float = 0.15,
        sleep: Callable[[float], None] = time.sleep,
    ):
        if not api_key:
            raise ScopusAuthError("SCOPUS_API_KEY não definida.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.min_interval = min_interval
        self.sleep = sleep
        self.session = session or requests.Session()
        self.session.headers.update({"X-ELS-APIKey": api_key, "Accept": "application/json"})
        if inst_token:
            self.session.headers["X-ELS-Insttoken"] = inst_token
        self.uses_inst_token = bool(inst_token)
        # Proxy vindo de HTTPS_PROXY (ex.: túnel SOCKS para a rede institucional),
        # registrado sem credenciais.
        proxy = requests.utils.get_environ_proxies(f"{self.base_url}/").get("https")
        self.proxy = requests.utils.urldefragauth(proxy) if proxy else None
        self.rate_limit: dict[str, str] = {}
        self.request_count = 0
        self._last_request = 0.0
        self._retrying = Retrying(
            retry=retry_if_exception_type(
                (ScopusRetryableError, requests.ConnectionError, requests.Timeout)
            ),
            wait=_exponential_wait,
            stop=stop_after_attempt(max_attempts),
            sleep=sleep,
            reraise=True,
            before_sleep=lambda rs: log.warning(
                "[SCOPUS] Tentativa %d falhou (%s); nova tentativa em %.0fs",
                rs.attempt_number, rs.outcome.exception(), rs.next_action.sleep,
            ),
        )

    def _throttle(self) -> None:
        # Requisições sequenciais com intervalo mínimo (sem paralelismo).
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_interval:
            self.sleep(self.min_interval - elapsed)
        self._last_request = time.monotonic()

    def _record_rate_limit(self, response: requests.Response) -> None:
        for header, key in RATE_LIMIT_HEADERS.items():
            if header in response.headers:
                self.rate_limit[key] = response.headers[header]
        if self.rate_limit:
            log.debug("[SCOPUS] Rate limit: %s", self.rate_limit)

    def _request_once(self, path: str, params: dict[str, Any]) -> requests.Response:
        self._throttle()
        self.request_count += 1
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        self._record_rate_limit(response)

        status = response.status_code
        if status == 200 or status == 404:
            return response
        detail = _error_detail(response)
        if status in (401, 403):
            raise ScopusAuthError(f"HTTP {status} — {detail}", status)
        if status == 429:
            els_status = response.headers.get("X-ELS-Status", "")
            if "QUOTA_EXCEEDED" in els_status.upper() or self.rate_limit.get("remaining") == "0":
                raise ScopusQuotaError(
                    f"HTTP 429 — quota esgotada (reset: {self.rate_limit.get('reset')}). {detail}",
                    status,
                )
            retry_after = response.headers.get("Retry-After")
            raise ScopusRetryableError(
                f"HTTP 429 — {detail}", status,
                float(retry_after) if retry_after and retry_after.isdigit() else None,
            )
        if status in RETRYABLE_STATUS:
            raise ScopusRetryableError(f"HTTP {status} — {detail}", status)
        raise ScopusError(f"HTTP {status} — {detail}", status)

    def _get(self, path: str, params: dict[str, Any]) -> requests.Response:
        return self._retrying(self._request_once, path, params)

    def search(
        self,
        query: str,
        *,
        start: int | None = 0,
        cursor: str | None = None,
        count: int = PAGE_SIZE,
        view: str = SEARCH_VIEW,
    ) -> dict:
        params: dict[str, Any] = {"query": query, "view": view, "count": count}
        if cursor is not None:
            params["cursor"] = cursor
        else:
            params["start"] = start
        response = self._get("/search/scopus", params)
        if response.status_code == 404:
            raise ScopusError(f"HTTP 404 — {_error_detail(response)}", 404)
        return response.json()

    def get_references(
        self, scopus_id: str, start: int | None = None, count: int | None = None
    ) -> dict | None:
        """Referências de um documento (Abstract Retrieval, view REF, paginado)."""
        params: dict[str, Any] = {"view": "REF"}
        if start is not None:
            params["startref"] = start
        if count is not None:
            params["refcount"] = count
        response = self._get(f"/abstract/scopus_id/{scopus_id}", params)
        if response.status_code == 404:
            return None
        return response.json()

    def get_abstract(self, scopus_id: str, view: str = ABSTRACT_VIEW) -> dict | None:
        """Abstract Retrieval. Retorna None se o registro não existir (404)."""
        response = self._get(f"/abstract/scopus_id/{scopus_id}", {"view": view})
        if response.status_code == 404:
            return None
        return response.json()


# --------------------------------------------------------------------------- #
# Normalização
# --------------------------------------------------------------------------- #

def _as_list(value: Any) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _as_text(value: Any) -> str | None:
    """Texto de campos Scopus que podem vir como str, {"$": ...} ou listas."""
    if value is None:
        return None
    if isinstance(value, str):
        text = value
    elif isinstance(value, dict):
        if "$" in value:
            text = str(value["$"])
        else:
            text = " ".join(filter(None, (_as_text(v) for k, v in value.items()
                                          if not k.startswith("@"))))
    elif isinstance(value, list):
        text = " ".join(filter(None, (_as_text(v) for v in value)))
    else:
        text = str(value)
    text = " ".join(text.split())
    return text or None


def _year(date: str | None) -> int | None:
    if date and len(date) >= 4 and date[:4].isdigit():
        return int(date[:4])
    return None


def _scopus_link(links: Any) -> str | None:
    for link in _as_list(links):
        if link.get("@ref") == "scopus":
            return link.get("@href")
    return None


def search_results(page: dict) -> dict:
    return page.get("search-results", {})


def total_results(page: dict) -> int:
    return int(search_results(page).get("opensearch:totalResults") or 0)


def page_entries(page: dict) -> list[dict]:
    """Entradas válidas de uma página (resultado vazio vem como entry com 'error')."""
    return [e for e in search_results(page).get("entry", []) if "error" not in e]


def next_cursor(page: dict) -> str | None:
    return (search_results(page).get("cursor") or {}).get("@next")


def parse_search_entry(entry: dict) -> dict[str, Any]:
    """Campos do PaperRecord a partir de uma entrada do Scopus Search (STANDARD)."""
    scopus_id = entry["dc:identifier"].removeprefix("SCOPUS_ID:")
    cover_date = entry.get("prism:coverDate")
    creator = entry.get("dc:creator")
    return {
        "source_id": scopus_id,
        "title": entry.get("dc:title") or "",
        "abstract": None,
        "doi": entry.get("prism:doi") or None,
        "authors": [creator] if creator else [],
        "year": _year(cover_date),
        "publication_date": cover_date,
        "venue": entry.get("prism:publicationName"),
        "document_type": entry.get("subtypeDescription"),
        "url": _scopus_link(entry.get("link")),
        "pdf_url": None,
        "extra": {
            "eid": entry.get("eid"),
            "aggregation_type": entry.get("prism:aggregationType"),
            "cited_by_count": entry.get("citedby-count"),
            "open_access": entry.get("openaccessFlag"),
            "enrichment": "not_enriched",
        },
    }


def _author_name(author: dict) -> str | None:
    preferred = author.get("preferred-name") or {}
    given = preferred.get("ce:given-name") or author.get("ce:given-name")
    surname = preferred.get("ce:surname") or author.get("ce:surname")
    if given and surname:
        return f"{given} {surname}"
    return surname or author.get("ce:indexed-name")


def parse_abstract(response: dict) -> dict[str, Any]:
    """Campos do PaperRecord a partir do Abstract Retrieval (META_ABS)."""
    root = response.get("abstracts-retrieval-response", {})
    core = root.get("coredata", {})

    authors_raw = _as_list((root.get("authors") or {}).get("author"))
    if not authors_raw:
        authors_raw = _as_list((core.get("dc:creator") or {}).get("author"))
    authors_raw.sort(key=lambda a: int(a.get("@seq", 0) or 0))
    authors = [n for n in (_author_name(a) for a in authors_raw) if n]

    keywords = [
        k for k in (_as_text(kw) for kw in _as_list((root.get("authkeywords") or {}).get("author-keyword")))
        if k
    ]
    cover_date = core.get("prism:coverDate")
    return {
        "title": _as_text(core.get("dc:title")),
        "abstract": _as_text(core.get("dc:description")),
        "doi": core.get("prism:doi"),
        "authors": authors,
        "keywords": keywords,
        "year": _year(cover_date),
        "publication_date": cover_date,
        "venue": core.get("prism:publicationName"),
        "document_type": core.get("subtypeDescription"),
        "url": _scopus_link(core.get("link")),
    }


def merge_fields(search_fields: dict[str, Any], abstract_fields: dict[str, Any]) -> dict[str, Any]:
    """Metadados do Abstract Retrieval sobrescrevem os da busca quando presentes."""
    merged = {**search_fields, "extra": dict(search_fields["extra"])}
    for key, value in abstract_fields.items():
        if value not in (None, "", []):
            merged[key] = value
    return merged


# --------------------------------------------------------------------------- #
# Coletor
# --------------------------------------------------------------------------- #

@dataclass
class FamilyResult:
    family: SearchFamily
    executed_query: str
    status: str = "pending"           # complete | incomplete | failed
    total_reported: int = 0
    total_collected: int = 0
    pages: int = 0
    mode: str = "offset"              # offset | cursor
    started_at: str | None = None
    completed_at: str | None = None
    reused: bool = False              # já estava completa em disco
    error: str | None = None
    entries: list[dict] = field(default_factory=list)


class ScopusCollector(BaseCollector):
    source = "scopus"

    def __init__(
        self,
        *args,
        client: ScopusClient,
        force: bool = False,
        enrich: bool = True,
        abstract_view: str = ABSTRACT_VIEW,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.client = client
        self.force = force
        self.enrich = enrich
        self.abstract_view = abstract_view

    @property
    def metadata_dir(self) -> Path:
        # Compartilhado entre versões das strings: um abstract por Scopus ID.
        return self.source_dir / "metadata"

    # ---- Search ----------------------------------------------------------- #

    def family_dir(self, family_id: str) -> Path:
        return self.raw_dir / family_id

    def _reset_family(self, fdir: Path) -> None:
        for path in fdir.glob("page_*.json"):
            path.unlink()
        for name in ("state.json", "records.jsonl"):
            (fdir / name).unlink(missing_ok=True)

    def _save_page(self, fdir: Path, number: int, page: dict, state: dict) -> None:
        write_json(fdir / f"page_{number:04d}.json", page)
        state["pages_done"] = number
        state["entries_collected"] += len(page_entries(page))
        state["next_cursor"] = next_cursor(page)
        write_json(fdir / "state.json", state)

    def search_family(self, family: SearchFamily) -> FamilyResult:
        query = build_scopus_query(self.config, family)
        result = FamilyResult(family=family, executed_query=query)
        fdir = self.family_dir(family.id)
        state_path = fdir / "state.json"

        self.log.info("[SCOPUS] Starting %s", family.id)
        self.log.info("[SCOPUS] Query: %s", query)

        if self.force:
            self._reset_family(fdir)

        state = read_json(state_path) if state_path.exists() else None
        if state and state["query"] != query:
            result.status = "failed"
            result.error = (
                f"{state_path} pertence a outra query ({state['query']!r}). "
                "Use --force para descartar a coleta anterior."
            )
            self.log.error("[SCOPUS] %s", result.error)
            return result

        if state is None:
            state = {
                "family": family.id,
                "query": query,
                "view": SEARCH_VIEW,
                "count": PAGE_SIZE,
                "mode": "offset",
                "total_results": None,
                "pages_done": 0,
                "entries_collected": 0,
                "next_cursor": None,
                "complete": False,
                "started_at": utc_now().isoformat(),
                "completed_at": None,
            }
        elif state["complete"]:
            self.log.info("[SCOPUS] %s já coletada em %s — reutilizando páginas salvas",
                          family.id, state["completed_at"])
            result.reused = True
        elif state["pages_done"]:
            self.log.info("[SCOPUS] Retomando %s a partir da página %d",
                          family.id, state["pages_done"] + 1)

        try:
            if not state["complete"]:
                self._collect_pages(fdir, state)
        except (ScopusError, requests.RequestException) as exc:
            result.error = f"{type(exc).__name__}: {exc}"
            self.log.error("[SCOPUS] %s interrompida: %s", family.id, result.error)

        entries = []
        for n in range(1, state["pages_done"] + 1):
            entries.extend(page_entries(read_json(fdir / f"page_{n:04d}.json")))

        result.entries = entries
        result.total_reported = state["total_results"] or 0
        result.total_collected = len(entries)
        result.pages = state["pages_done"]
        result.mode = state["mode"]
        result.started_at = state["started_at"]
        result.completed_at = state["completed_at"]
        if state["complete"]:
            result.status = "complete"
        else:
            result.status = "incomplete" if state["pages_done"] else "failed"
            if result.error is None:
                result.error = "Coleta não concluída."
        self.log.info("[SCOPUS] %s %s: %d/%d", family.id, result.status,
                      result.total_collected, result.total_reported)
        return result

    def _collect_pages(self, fdir: Path, state: dict) -> None:
        query, count = state["query"], state["count"]

        if state["total_results"] is None:
            first = self.client.search(query, start=0, count=count)
            total = total_results(first)
            state["total_results"] = total
            self.log.info("[SCOPUS] Total reported: %d", total)
            if total > OFFSET_LIMIT:
                self.log.warning(
                    "[SCOPUS] %d resultados > %d: usando cursor pagination", total, OFFSET_LIMIT
                )
                state["mode"] = "cursor"
                first = self._cursor_search(query, "*", count)
            self._save_page(fdir, 1, first, state)
            self._log_page(state)

        total = state["total_results"]
        while state["entries_collected"] < total:
            number = state["pages_done"] + 1
            if state["mode"] == "cursor":
                if not state["next_cursor"]:
                    break
                page = self._cursor_search(query, state["next_cursor"], count)
            else:
                page = self.client.search(query, start=state["pages_done"] * count, count=count)
            if not page_entries(page):
                break
            self._save_page(fdir, number, page, state)
            self._log_page(state)

        if state["entries_collected"] < total:
            raise ScopusIncompleteError(
                f"API parou de retornar registros: {state['entries_collected']} de {total} "
                "coletados. A execução NÃO cobre o universo completo."
            )
        state["complete"] = True
        state["completed_at"] = utc_now().isoformat()
        write_json(fdir / "state.json", state)

    def _cursor_search(self, query: str, cursor: str, count: int) -> dict:
        try:
            return self.client.search(query, cursor=cursor, count=count)
        except ScopusQuotaError:
            raise
        except ScopusError as exc:
            raise ScopusIncompleteError(
                f"Mais de {OFFSET_LIMIT} resultados e cursor pagination indisponível "
                f"({exc}). A execução NÃO cobre o universo completo."
            ) from exc

    def _log_page(self, state: dict) -> None:
        total = state["total_results"] or 0
        pages_total = max(1, -(-total // state["count"]))
        self.log.info("[SCOPUS] Page %d/%d: %d/%d", state["pages_done"], pages_total,
                      state["entries_collected"], total)

    # ---- Enrichment ------------------------------------------------------- #

    def enrich_ids(self, scopus_ids: list[str]) -> dict:
        """Abstract Retrieval para IDs únicos, reaproveitando o cache."""
        stats = {"view": self.abstract_view, "unique_ids": len(scopus_ids), "cached": 0,
                 "fetched": 0, "not_found": 0, "pending": 0, "status": "complete",
                 "error": None}
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        for i, sid in enumerate(scopus_ids, 1):
            path = self.metadata_dir / f"{sid}.json"
            if path.exists() and not self.force:
                stats["cached"] += 1
                continue
            try:
                response = self.client.get_abstract(sid, view=self.abstract_view)
            except (ScopusError, requests.RequestException) as exc:
                stats["status"] = "incomplete"
                stats["error"] = f"{type(exc).__name__}: {exc}"
                stats["pending"] = len(scopus_ids) - i + 1
                self.log.error("[SCOPUS] Abstract Retrieval interrompido em %s: %s",
                               sid, stats["error"])
                if isinstance(exc, ScopusAuthError):
                    self.log.error(
                        "[SCOPUS] O view %s pode exigir SCOPUS_INST_TOKEN ou rede institucional.",
                        self.abstract_view,
                    )
                break
            if response is None:
                # Cacheado como "não encontrado" para não consultar novamente.
                write_json(path, {"_not_found": True, "scopus_id": sid,
                                  "retrieved_at": utc_now().isoformat()})
                stats["not_found"] += 1
            else:
                write_json(path, response)
                stats["fetched"] += 1
            if i % 50 == 0:
                self.log.info("[SCOPUS] Abstract Retrieval %d/%d", i, len(scopus_ids))
        self.log.info("[SCOPUS] Abstract Retrieval: %d em cache, %d consultados, %d não encontrados",
                      stats["cached"], stats["fetched"], stats["not_found"])
        return stats

    def _load_metadata(self, scopus_id: str) -> tuple[str, dict | None]:
        path = self.metadata_dir / f"{scopus_id}.json"
        if not path.exists():
            return "not_enriched", None
        data = read_json(path)
        if data.get("_not_found"):
            return "not_found", None
        return self.abstract_view, data

    # ---- Normalização e saída -------------------------------------------- #

    def build_records(self, results: list[FamilyResult]) -> list[PaperRecord]:
        records: dict[str, PaperRecord] = {}
        for res in results:
            family = res.family
            provenance = SearchProvenance(
                source=self.source,
                family=family.id,
                stage=family.stage,
                canonical_query=build_canonical_query(self.config, family),
                executed_query=res.executed_query,
                searched_fields=SEARCHED_FIELDS,
                retrieved_at=res.started_at or self.started_at,
            )
            for entry in res.entries:
                fields = parse_search_entry(entry)
                sid = fields["source_id"]
                if sid not in records:
                    enrichment, metadata = self._load_metadata(sid)
                    if metadata is not None:
                        fields = merge_fields(fields, parse_abstract(metadata))
                    fields["extra"]["enrichment"] = enrichment
                    records[sid] = PaperRecord(
                        source=self.source, retrieved_at=self.started_at, **fields
                    )
                records[sid].add_occurrence(provenance)
        return list(records.values())

    def write_outputs(self, records: list[PaperRecord], results: list[FamilyResult]) -> None:
        for res in results:
            subset = [r for r in records if res.family.id in r.search_families]
            write_jsonl(self.family_dir(res.family.id) / "records.jsonl", subset)
        write_jsonl(self.raw_dir / "all_records.jsonl", records)

    def _families_on_disk(self) -> list[SearchFamily]:
        """Famílias não executadas agora, mas já coletadas por completo antes."""
        selected = {f.id for f in self.families}
        found = []
        for family in self.config.families.values():
            state_path = self.family_dir(family.id) / "state.json"
            if family.id in selected or not state_path.exists():
                continue
            state = read_json(state_path)
            if state.get("complete") and state["query"] == build_scopus_query(self.config, family):
                found.append(family)
        return found

    def run(self) -> dict:
        results = [self.search_family(f) for f in self.families]

        # Consolida também famílias completas de execuções anteriores (sem requisições).
        executed = {r.family.id for r in results}
        saved_force, self.force = self.force, False
        for family in self._families_on_disk():
            self.log.info("[SCOPUS] Incluindo %s coletada anteriormente", family.id)
            results.append(self.search_family(family))
        self.force = saved_force
        results.sort(key=lambda r: list(self.config.families).index(r.family.id))

        unique_ids = list(dict.fromkeys(
            parse_search_entry(e)["source_id"] for r in results for e in r.entries
        ))
        enrichment = {"status": "skipped", "view": self.abstract_view,
                      "unique_ids": len(unique_ids)}
        if self.enrich:
            enrichment = self.enrich_ids(unique_ids)

        records = self.build_records(results)
        self.write_outputs(records, results)

        manifest = {
            "source": self.source,
            "executed_at": self.started_at.isoformat(),
            "finished_at": utc_now().isoformat(),
            **self.query_info(),
            "search_fields": SEARCHED_FIELDS,
            "adapter": ADAPTER,
            "search_view": SEARCH_VIEW,
            "page_size": PAGE_SIZE,
            "temporal_filter": None,
            "auth": {"api_key": "SCOPUS_API_KEY (valor omitido)",
                     "inst_token": self.client.uses_inst_token,
                     "proxy": self.client.proxy},
            "families": {
                r.family.id: {
                    "stage": r.family.stage,
                    "label": r.family.label,
                    "canonical_query": build_canonical_query(self.config, r.family),
                    "executed_query": r.executed_query,
                    "executed_in_this_run": r.family.id in executed and not r.reused,
                    "status": r.status,
                    "error": r.error,
                    "pagination_mode": r.mode,
                    "pages": r.pages,
                    "total_results_reported": r.total_reported,
                    "total_results_collected": r.total_collected,
                    "total_results": r.total_collected,
                    "collection_started_at": r.started_at,
                    "collection_completed_at": r.completed_at,
                    "raw_dir": str(self.family_dir(r.family.id)),
                }
                for r in results
            },
            "enrichment": enrichment,
            "total_occurrences": sum(r.total_collected for r in results),
            "unique_papers": len(records),
            "abstracts_available": sum(1 for r in records if r.abstract_available),
            "requests_made": self.client.request_count,
            "rate_limit": self.client.rate_limit,
            "output_file": str(self.raw_dir / "all_records.jsonl"),
        }
        self.write_manifest(manifest)
        return manifest
