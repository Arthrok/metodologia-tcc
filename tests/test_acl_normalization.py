from types import SimpleNamespace

import pytest

from src.collectors.acl import ACLCollector, paper_to_fields, searchable_text
from src.search import load_search_config
from src.utils.io import read_jsonl


class Markup:
    def __init__(self, text):
        self.text = text

    def as_text(self):
        return self.text


def fake_paper(full_id="2024.acl-long.1", title="A title", abstract=None, **kw):
    name = lambda first, last: SimpleNamespace(  # noqa: E731
        name=SimpleNamespace(as_first_last=lambda: f"{first} {last}")
    )
    defaults = dict(
        full_id=full_id,
        title=Markup(title),
        abstract=Markup(abstract) if abstract is not None else None,
        doi=None,
        authors=(name("Ada", "Lovelace"), name("Alan", "Turing")),
        year="2024",
        month="August",
        parent=SimpleNamespace(title=Markup("Proceedings of ACL 2024")),
        bibtype="inproceedings",
        web_url=f"https://aclanthology.org/{full_id}/",
        pdf=SimpleNamespace(url=f"https://aclanthology.org/{full_id}.pdf"),
        venue_ids=("acl",),
        bibkey="lovelace-2024-title",
        is_deleted=False,
        is_frontmatter=False,
    )
    defaults.update(kw)
    return SimpleNamespace(**defaults)


@pytest.fixture(scope="module")
def config():
    return load_search_config()


def test_paper_to_fields():
    fields = paper_to_fields(fake_paper(abstract="Some abstract."))
    assert fields["source_id"] == "2024.acl-long.1"
    assert fields["authors"] == ["Ada Lovelace", "Alan Turing"]
    assert fields["year"] == 2024
    assert fields["publication_date"] == "2024-08"
    assert fields["venue"] == "Proceedings of ACL 2024"
    assert fields["url"] == "https://aclanthology.org/2024.acl-long.1/"
    assert fields["pdf_url"] == "https://aclanthology.org/2024.acl-long.1.pdf"


def test_paper_without_pdf():
    assert paper_to_fields(fake_paper(pdf=None))["pdf_url"] is None


def test_searchable_text_falls_back_to_title():
    assert searchable_text(paper_to_fields(fake_paper(title="T"))) == "T"
    assert searchable_text(paper_to_fields(fake_paper(title="T", abstract="A"))) == "T A"


def test_match_papers_multiple_families_and_missing_abstract(config, tmp_path):
    papers = [
        fake_paper(
            "2024.a-1",
            title="Retrieval-Augmented Generation at scale",
            abstract="We study chunking and hybrid search with a vector store.",
        ),
        # Sem abstract: pesquisado só pelo título, mantido.
        fake_paper("2024.a-2", title="Chunking for Retrieval Augmented Generation"),
        # RAG sem nenhuma família.
        fake_paper("2024.a-3", title="Retrieval-augmented generation", abstract="QA."),
        # Família sem RAG.
        fake_paper("2024.a-4", title="Document ingestion", abstract="OCR pipelines."),
        # Front matter não é artigo.
        fake_paper("2024.a-0", title="Retrieval augmented generation chunking",
                   is_frontmatter=True),
        # Artigos antigos não são filtrados (E2 é aplicado depois).
        fake_paper("2015.a-5", title="retrieval augmented generation", year="2015",
                   abstract="OCR"),
    ]
    collector = ACLCollector(config, data_dir=tmp_path)
    records, stats = collector.match_papers(papers)

    by_id = {r.source_id: r for r in records}
    assert set(by_id) == {"2024.a-1", "2024.a-2", "2015.a-5"}
    assert by_id["2024.a-1"].search_families == ["S3", "S4", "S5"]
    assert [p.family for p in by_id["2024.a-1"].provenance] == ["S3", "S4", "S5"]

    no_abs = by_id["2024.a-2"]
    assert no_abs.search_families == ["S4"]
    assert no_abs.abstract_available is False
    assert no_abs.provenance[0].searched_fields == ["title"]

    assert by_id["2015.a-5"].year == 2015
    assert stats["papers_scanned"] == 5
    assert stats["frontmatter_skipped"] == 1
    assert stats["rag_candidates"] == 4

    collector.write_outputs(records, tmp_path)
    assert len(read_jsonl(tmp_path / "all_records.jsonl")) == 3
    s4 = read_jsonl(tmp_path / "S4.jsonl")
    assert {r["source_id"] for r in s4} == {"2024.a-1", "2024.a-2"}
    assert s4[0]["id"] == "acl:2024.a-1"
    assert read_jsonl(tmp_path / "S1.jsonl") == []


def test_partial_run_does_not_overwrite_all_records(config, tmp_path):
    collector = ACLCollector(config, [config.family("S4")], data_dir=tmp_path)
    collector.write_outputs([], tmp_path)
    assert not (tmp_path / "all_records.jsonl").exists()
    assert (tmp_path / "S4.jsonl").exists()
