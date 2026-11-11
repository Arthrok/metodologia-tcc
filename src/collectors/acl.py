"""Coletor ACL Anthology: matching local S1–S8 sobre os metadados oficiais.

O ACL Anthology não é uma API de busca como o Scopus. Os metadados oficiais
(repositório GitHub acl-org/acl-anthology) são carregados via pacote
``acl-anthology`` e percorridos UMA vez; cada paper é testado contra o bloco
de domínio (RAG) e depois contra cada família.

Adaptação registrada no manifest: campos pesquisados = title + abstract
(não é TITLE-ABS-KEY). Papers sem abstract são pesquisados apenas pelo título
e mantidos com ``abstract_available = false``.
"""

from __future__ import annotations

import subprocess
from importlib.metadata import version
from pathlib import Path
from typing import Any

from src.collectors.base import BaseCollector, family_counts
from src.models import PaperRecord, SearchProvenance
from src.search import FamilyMatcher, build_canonical_query
from src.utils.io import utc_now, write_jsonl
from src.utils.text import normalize_text

SEARCHED_FIELDS = ["title", "abstract"]
SEARCH_MODE = "local_metadata_matching"
ACL_REPO_URL = "https://github.com/acl-org/acl-anthology.git"

_MONTHS = {
    m: i
    for i, names in enumerate(
        [
            ("january", "jan"), ("february", "feb"), ("march", "mar"),
            ("april", "apr"), ("may",), ("june", "jun"), ("july", "jul"),
            ("august", "aug"), ("september", "sep", "sept"), ("october", "oct"),
            ("november", "nov"), ("december", "dec"),
        ],
        start=1,
    )
    for m in names
}


def _text(value: Any) -> str | None:
    """MarkupText → texto simples."""
    if value is None:
        return None
    text = value.as_text() if hasattr(value, "as_text") else str(value)
    text = text.strip()
    return text or None


def _parse_month(month: str | None) -> int | None:
    if not month:
        return None
    token = month.strip().lower().split()[0].rstrip(".,")
    if token.isdigit() and 1 <= int(token) <= 12:
        return int(token)
    return _MONTHS.get(token.split("-")[0])


def paper_to_fields(paper: Any) -> dict[str, Any]:
    """Extrai os campos do PaperRecord de um ``acl_anthology.Paper``."""
    year = int(paper.year) if str(paper.year).isdigit() else None
    month = _parse_month(paper.month)
    publication_date = None
    if year:
        publication_date = f"{year}-{month:02d}" if month else str(year)

    pdf = paper.pdf
    return {
        "source_id": paper.full_id,
        "title": _text(paper.title) or "",
        "abstract": _text(paper.abstract),
        "doi": paper.doi or None,
        "authors": [ns.name.as_first_last() for ns in paper.authors],
        "year": year,
        "publication_date": publication_date,
        "venue": _text(paper.parent.title),
        "document_type": str(paper.bibtype),
        "url": paper.web_url,
        "pdf_url": pdf.url if pdf is not None else None,
        "extra": {
            "venue_ids": list(paper.venue_ids),
            "bibkey": paper.bibkey,
            "is_deleted": bool(paper.is_deleted),
        },
    }


def searchable_text(fields: dict[str, Any]) -> str:
    """title + abstract; só title quando não há abstract."""
    if fields["abstract"]:
        return f"{fields['title']} {fields['abstract']}"
    return fields["title"]


def git_commit(repo_path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_anthology(repo_path: Path | None = None, update: bool = True):
    """Carrega o Anthology a partir do repositório oficial.

    Retorna (anthology, caminho_do_repositório).
    """
    from acl_anthology import Anthology
    from acl_anthology.config import dirs

    if repo_path is None:
        repo_path = dirs.user_data_path / "git" / "acl-org-acl-anthology-git"
    repo_path = Path(repo_path)

    if update or not (repo_path / "data").exists():
        anthology = Anthology.from_repo(repo_url=ACL_REPO_URL, path=repo_path, verbose=False)
    else:
        anthology = Anthology(datadir=repo_path / "data", verbose=False)
    return anthology, repo_path


class ACLCollector(BaseCollector):
    source = "acl"

    def __init__(self, *args, repo_path: Path | None = None, update: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo_path = repo_path
        self.update = update

    def match_papers(self, papers) -> tuple[list[PaperRecord], dict[str, int]]:
        """Uma única passagem pelo corpus aplicando S1–S8."""
        matcher = FamilyMatcher(self.config, self.families)
        queries = {f.id: build_canonical_query(self.config, f) for f in self.families}
        stats = {"papers_scanned": 0, "frontmatter_skipped": 0, "rag_candidates": 0,
                 "without_abstract_scanned": 0, "without_abstract_matched": 0}
        records: list[PaperRecord] = []

        for paper in papers:
            if paper.is_frontmatter:
                # Front matter de volume não é um artigo.
                stats["frontmatter_skipped"] += 1
                continue
            stats["papers_scanned"] += 1
            if stats["papers_scanned"] % 20000 == 0:
                self.log.info("[ACL] Papers scanned: %d", stats["papers_scanned"])

            fields = paper_to_fields(paper)
            if not fields["abstract"]:
                stats["without_abstract_scanned"] += 1

            normalized = normalize_text(searchable_text(fields))
            if not matcher.matches_domain(normalized):
                continue
            stats["rag_candidates"] += 1

            hits = matcher.match_families(normalized)
            if not hits:
                continue

            record = PaperRecord(source=self.source, retrieved_at=self.started_at, **fields)
            searched = SEARCHED_FIELDS if fields["abstract"] else ["title"]
            for family in self.families:
                if family.id not in hits:
                    continue
                record.add_occurrence(SearchProvenance(
                    source=self.source,
                    family=family.id,
                    stage=family.stage,
                    canonical_query=queries[family.id],
                    executed_query=queries[family.id],
                    searched_fields=searched,
                    matched_terms=hits[family.id],
                    retrieved_at=self.started_at,
                ))
            if not record.abstract_available:
                stats["without_abstract_matched"] += 1
            records.append(record)

        return records, stats

    @property
    def is_full_run(self) -> bool:
        return {f.id for f in self.families} == set(self.config.families)

    def write_outputs(self, records: list[PaperRecord], output_dir: Path) -> None:
        # Com --family, all_records.jsonl não é sobrescrito por um subconjunto.
        if self.is_full_run:
            write_jsonl(output_dir / "all_records.jsonl", records)
        for family in self.families:
            subset = [r for r in records if family.id in r.search_families]
            write_jsonl(output_dir / f"{family.id}.jsonl", subset)

    def run(self) -> dict:
        self.log.info("[ACL] Loading Anthology")
        anthology, repo_path = load_anthology(self.repo_path, self.update)
        commit = git_commit(repo_path)
        self.log.info("[ACL] Repository %s @ %s", repo_path, commit or "unknown")

        records, stats = self.match_papers(anthology.papers())
        counts = family_counts(records, self.families)

        self.log.info("[ACL] Papers scanned: %d", stats["papers_scanned"])
        self.log.info("[ACL] RAG candidates: %d", stats["rag_candidates"])
        for fid, n in counts.items():
            self.log.info("[ACL] %s: %d", fid, n)

        self.write_outputs(records, self.raw_dir)

        manifest = {
            "source": self.source,
            "executed_at": self.started_at.isoformat(),
            "finished_at": utc_now().isoformat(),
            "full_run": self.is_full_run,
            **self.query_info(),
            "search_fields": SEARCHED_FIELDS,
            "search_fields_note": (
                "Registros sem abstract são pesquisados apenas pelo título "
                "(abstract_available=false)."
            ),
            "search_mode": SEARCH_MODE,
            "text_normalization": "unicode NFKC, traços unicode→'-', lowercase, espaços colapsados; sem stemming",
            "temporal_filter": None,
            "acl_package_version": version("acl-anthology"),
            "acl_repository_url": ACL_REPO_URL,
            "acl_repository_commit": commit,
            "acl_repository_path": str(repo_path),
            "stats": stats,
            "families": {
                f.id: {
                    "stage": f.stage,
                    "label": f.label,
                    "canonical_query": build_canonical_query(self.config, f),
                    "total_results": counts[f.id],
                    "status": "complete",
                    "output_file": str(self.raw_dir / f"{f.id}.jsonl"),
                }
                for f in self.families
            },
            "total_occurrences": sum(counts.values()),
            "unique_papers": len(records),
            "output_file": str(self.raw_dir / "all_records.jsonl") if self.is_full_run else None,
        }
        self.write_manifest(manifest)
        return manifest
