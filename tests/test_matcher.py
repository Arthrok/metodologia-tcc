import pytest

from src.search import FamilyMatcher, build_canonical_query, load_search_config
from src.search.matcher import matches_term
from src.utils.text import normalize_text


@pytest.fixture(scope="module")
def config():
    return load_search_config()


@pytest.fixture(scope="module")
def matcher(config):
    return FamilyMatcher(config)


def m(text: str, term: str) -> bool:
    return matches_term(normalize_text(text), term)


# --- Configuração -----------------------------------------------------------

def test_config_has_eight_families(config):
    assert list(config.families) == [f"S{i}" for i in range(1, 9)]


def test_canonical_query_matches_tcc_table(config):
    assert build_canonical_query(config, config.family("S2")) == (
        '("retrieval augmented generation" OR "retrieval-augmented generation") AND '
        '("data ingestion" OR "document ingestion" OR "data extraction" OR '
        '"document parsing" OR OCR OR crawl*)'
    )


# --- RAG --------------------------------------------------------------------

@pytest.mark.parametrize(
    "text",
    [
        "Retrieval-Augmented Generation",
        "retrieval augmented generation",
        "RETRIEVAL   AUGMENTED\nGENERATION",
        "Retrieval–Augmented Generation",  # en dash
    ],
)
def test_rag_matches(matcher, text):
    assert matcher.matches_domain(normalize_text(text))


@pytest.mark.parametrize(
    "text",
    ["retrieval generation", "retrieval-augmented generator", "augmented retrieval generation"],
)
def test_rag_does_not_match(matcher, text):
    assert not matcher.matches_domain(normalize_text(text))


# --- Wildcard ---------------------------------------------------------------

@pytest.mark.parametrize("text", ["chunk", "chunks", "chunking", "chunked", "Chunking."])
def test_wildcard_chunk(text):
    assert m(text, "chunk*")


def test_wildcard_requires_word_start():
    assert not m("unchunked", "chunk*")


@pytest.mark.parametrize("text", ["observable", "observability", "observability-related"])
def test_wildcard_observab(text):
    assert m(text, "observab*")


@pytest.mark.parametrize("text", ["version", "versions", "versioning"])
def test_wildcard_version(text):
    assert m(text, "version*")


# --- Phrase -----------------------------------------------------------------

@pytest.mark.parametrize("text", ["vector database", "vector databases", "Vector  Databases"])
def test_phrase_with_wildcard(text):
    assert m(text, "vector database*")


def test_phrase_is_contiguous():
    assert not m("data from the ingestion layer", "data ingestion")
    assert not m("ingestion of data", "data ingestion")
    assert m("robust data ingestion pipelines", "data ingestion")


def test_term_without_wildcard_needs_word_boundary():
    assert m("uses OCR.", "OCR")
    assert not m("ocrs", "OCR")
    assert not m("tracings", "tracing")
    assert not m("datas ingestion", "data ingestion")


def test_mixed_wildcard_phrase():
    assert m("retrieval strategies", "retrieval strateg*")
    assert m("retrieval strategy", "retrieval strateg*")
    assert not m("retrieval and strategy", "retrieval strateg*")


# --- AND entre blocos -------------------------------------------------------

def test_family_without_rag_is_not_returned(matcher):
    assert matcher.match("This paper proposes document ingestion for search.") == {}


def test_family_with_rag_is_returned(matcher):
    result = matcher.match("Retrieval augmented generation using document ingestion.")
    assert "S2" in result
    assert result["S2"] == ["document ingestion"]


def test_multiple_families(matcher):
    text = (
        "A retrieval-augmented generation system with chunking, "
        "a vector database and reranking."
    )
    assert set(matcher.match(text)) == {"S3", "S4", "S5"}


def test_rag_only_matches_no_family(matcher):
    assert matcher.match("Retrieval-augmented generation for QA.") == {}
