"""Pool consolidado da revisão: deduplicação (E1) e marcação temporal.

O pool cresce a cada sincronização (novas versões das strings, snowballing)
e nunca perde registros nem proveniência. O recorte temporal apenas marca os
registros: anteriores a 2024 são preservados como potencialmente fundacionais
e decididos pelos pesquisadores (I1/E2).
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any

MERGED_FIELDS = ("title", "abstract", "doi", "authors", "year", "publication_date",
                 "venue", "document_type", "keywords", "url", "pdf_url")


def normalized_title(title: str) -> str:
    text = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def normalized_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        doi = doi.removeprefix(prefix)
    return doi or None


def match_keys(record: dict[str, Any]) -> list[str]:
    """Chaves de deduplicação: DOI (preferida) e título normalizado."""
    keys = []
    if doi := normalized_doi(record.get("doi")):
        keys.append(f"doi:{doi}")
    if title := normalized_title(record.get("title") or ""):
        # Títulos muito curtos geram falsos pares; só entram com DOI ausente.
        if len(title.split()) >= 4 or not keys:
            keys.append(f"title:{title}")
    return keys


def canonical_key(record: dict[str, Any]) -> str:
    return match_keys(record)[0]


def review_id(key: str) -> str:
    return "P-" + hashlib.sha256(key.encode()).hexdigest()[:12]


def temporal_status(year: int | None, start_year: int) -> str:
    if year is None:
        return "unknown"
    return "in_scope" if year >= start_year else "pre_cutoff"


def _richness(record: dict[str, Any]) -> tuple:
    return (bool(record.get("abstract")), len(record.get("abstract") or ""),
            bool(record.get("doi")), len(record.get("authors") or []))


def _new_entry(record: dict, key: str, origin: str, sync_id: str, start_year: int) -> dict:
    entry = {"review_id": review_id(key), "canonical_key": key}
    entry.update({f: record.get(f) for f in MERGED_FIELDS})
    entry.update({
        "sources": [record["source"]],
        "source_records": [record["id"]],
        "search_families": sorted(record.get("search_families", [])),
        "query_versions": sorted(set(record.get("_query_versions", []))),
        "origins": [origin],
        "provenance": list(record.get("provenance", [])),
        "first_seen": sync_id,
        "temporal_status": temporal_status(record.get("year"), start_year),
    })
    return entry


def _merge(entry: dict, record: dict, origin: str, start_year: int) -> bool:
    """Funde `record` em `entry`. Retorna True se for uma nova versão do mesmo trabalho."""
    is_new_version = record["id"] not in entry["source_records"]
    if is_new_version:
        entry["source_records"].append(record["id"])
    if _richness(record) > _richness(entry):
        for f in MERGED_FIELDS:
            if record.get(f) not in (None, "", []):
                entry[f] = record[f]
        entry["temporal_status"] = temporal_status(entry.get("year"), start_year)
    entry["sources"] = sorted(set(entry["sources"]) | {record["source"]})
    entry["search_families"] = sorted(set(entry["search_families"]) | set(record.get("search_families", [])))
    entry["query_versions"] = sorted(set(entry["query_versions"]) | set(record.get("_query_versions", [])))
    entry["origins"] = sorted(set(entry["origins"]) | {origin})
    seen = {(p.get("source"), p.get("family"), p.get("executed_query"), p.get("seed")) for p in entry["provenance"]}
    for p in record.get("provenance", []):
        if (p.get("source"), p.get("family"), p.get("executed_query"), p.get("seed")) not in seen:
            entry["provenance"].append(p)
    return is_new_version


def merge_into_pool(
    pool: list[dict], records: list[dict], *, origin: str, sync_id: str, start_year: int,
) -> tuple[list[dict], dict]:
    """Adiciona `records` ao pool. Duplicatas entre bases são registradas como E1."""
    index: dict[str, dict] = {}
    for entry in pool:
        for key in match_keys(entry):
            index.setdefault(key, entry)

    added, duplicates, already = [], [], 0
    for record in records:
        keys = match_keys(record)
        if not keys:
            continue
        entry = next((index[k] for k in keys if k in index), None)
        if entry is None:
            entry = _new_entry(record, keys[0], origin, sync_id, start_year)
            pool.append(entry)
            added.append(entry)
        elif record["id"] in entry["source_records"]:
            _merge(entry, record, origin, start_year)
            already += 1
        else:
            _merge(entry, record, origin, start_year)
            duplicates.append({
                "review_id": entry["review_id"], "kept": entry["source_records"][0],
                "merged": record["id"], "criterion": "E1",
                "match_key": next(k for k in keys if k in index), "sync": sync_id,
            })
        for key in match_keys(entry):
            index.setdefault(key, entry)

    stats = {"input_records": len(records), "new_papers": len(added),
             "duplicates_e1": len(duplicates), "already_in_pool": already}
    return pool, {"stats": stats, "added": [e["review_id"] for e in added], "duplicates": duplicates}
