"""Gera os dados do site de material complementar (docs/assets/data/triagem.json).

Junta as 80 decisões humanas versionadas, o ranqueamento de cada rodada e a pré-triagem com os
metadados bibliográficos do pool local (título, autores, ano, veículo, DOI). Os resumos da Scopus
não são copiados: o site publica só a referência e as justificativas já versionadas no repositório.

Uso: python scripts/build_pages_data.py   (requer data/review/pool.jsonl, regenerado por `sync`)
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "data" / "review"
OUT = ROOT / "docs" / "assets" / "data" / "triagem.json"


def _list(value) -> list:
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = ast.literal_eval(value)
        return list(parsed) if isinstance(parsed, (list, tuple)) else [parsed]
    except (ValueError, SyntaxError):
        return [value]


def main() -> None:
    decisions = [json.loads(line) for line in (REVIEW / "decisions.jsonl").open(encoding="utf-8")]
    ids = {d["paper_id"] for d in decisions}

    ranking: dict[str, dict] = {}
    for path in sorted((REVIEW / "rounds").glob("r*/ranking.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for cand in data["candidates"]:
            ranking[cand["paper_id"]] = {"rank": cand["rank"], "justification": cand["justification"]}

    pretriage: dict[str, dict] = {}
    for line in (REVIEW / "pretriage" / "pretriage.jsonl").open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["paper_id"] in ids:
            pretriage[rec["paper_id"]] = rec

    pool: dict[str, dict] = {}
    for line in (REVIEW / "pool.jsonl").open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["review_id"] in ids:
            pool[rec["review_id"]] = rec

    missing = ids - pool.keys()
    if missing:
        raise SystemExit(f"registros ausentes do pool: {sorted(missing)}")

    rows = []
    for d in decisions:
        pid = d["paper_id"]
        meta = pool[pid]
        pre = pretriage.get(pid, {})
        authors = _list(meta.get("authors"))
        rows.append({
            "id": pid,
            "round": d["round_id"],
            "rank": ranking.get(pid, {}).get("rank"),
            "decision": d["decision"],
            "criterion": d["primary_criterion"],
            "justification": d["justification"],
            "ai_justification": ranking.get(pid, {}).get("justification"),
            "title": meta.get("title"),
            "authors": authors[:3] + (["et al."] if len(authors) > 3 else []),
            "year": meta.get("year"),
            "venue": meta.get("venue"),
            "doi": meta.get("doi"),
            "url": meta.get("url"),
            "sources": _list(meta.get("sources")),
            "origins": _list(meta.get("origins")),
            "families": _list(meta.get("search_families")),
            "stages": pre.get("lifecycle_stages", []),
            "dimensions": pre.get("transverse_dimensions", []),
        })

    rows.sort(key=lambda r: (r["round"], r["rank"] or 99))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # Cópia em JS para a página abrir também direto do disco (file://), sem servidor.
    OUT.with_suffix(".js").write_text(
        "window.TRIAGEM = " + json.dumps(rows, ensure_ascii=False) + ";\n", encoding="utf-8"
    )
    print(f"{len(rows)} registros -> {OUT.relative_to(ROOT)} (+ .js)")


if __name__ == "__main__":
    main()
