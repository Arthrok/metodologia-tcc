import json

import pytest
import requests

from src.collectors.scopus import (
    ScopusAuthError,
    ScopusClient,
    ScopusCollector,
    ScopusError,
    ScopusQuotaError,
    ScopusRetryableError,
    parse_abstract,
    parse_search_entry,
)
from src.search import build_scopus_query, load_search_config
from src.utils.io import read_json, read_jsonl

API_KEY = "SECRET-KEY-123"
RAG = '("retrieval augmented generation" OR "retrieval-augmented generation")'


# --------------------------------------------------------------------------- #
# Fakes
# --------------------------------------------------------------------------- #

def make_response(status=200, body=None, headers=None):
    r = requests.Response()
    r.status_code = status
    r._content = json.dumps(body if body is not None else {}).encode()
    r.headers.update(headers or {})
    return r


class FakeSession:
    """Session que responde a partir de um handler(url, params) -> Response."""

    def __init__(self, handler):
        self.handler = handler
        self.headers = {}
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, dict(params or {})))
        return self.handler(url, params or {})


def entry(i, doi=True):
    e = {
        "dc:identifier": f"SCOPUS_ID:{i}",
        "eid": f"2-s2.0-{i}",
        "dc:title": f"Paper {i}",
        "dc:creator": "Doe J.",
        "prism:publicationName": "Venue",
        "prism:coverDate": "2019-05-01",
        "subtypeDescription": "Article",
        "link": [{"@ref": "scopus", "@href": f"https://www.scopus.com/{i}"}],
    }
    if doi:
        e["prism:doi"] = f"10.1/{i}"
    return e


def search_page(total, ids, cursor_next=None):
    results = {
        "opensearch:totalResults": str(total),
        "entry": [entry(i) for i in ids] if ids else [{"@_fa": "true", "error": "Result set was empty"}],
    }
    if cursor_next:
        results["cursor"] = {"@current": "x", "@next": cursor_next}
    return {"search-results": results}


def abstract_body(i, abstract="An abstract.", doi=True):
    core = {
        "dc:identifier": f"SCOPUS_ID:{i}",
        "dc:title": f"Paper {i} full title",
        "prism:coverDate": "2019-05-01",
        "prism:publicationName": "Venue",
        "subtypeDescription": "Conference Paper",
        "link": [{"@ref": "scopus", "@href": f"https://www.scopus.com/{i}"}],
    }
    if abstract is not None:
        core["dc:description"] = abstract
    if doi:
        core["prism:doi"] = f"10.1/{i}"
    return {
        "abstracts-retrieval-response": {
            "coredata": core,
            "authors": {"author": [
                {"@seq": "2", "preferred-name": {"ce:given-name": "Bob", "ce:surname": "B"}},
                {"@seq": "1", "preferred-name": {"ce:given-name": "Ann", "ce:surname": "A"}},
            ]},
            "authkeywords": {"author-keyword": [{"$": "RAG"}, {"$": "chunking"}]},
        }
    }


def paginated_handler(total, abstracts=None, page_size=200):
    ids = list(range(1, total + 1))

    def handler(url, params):
        if "/search/scopus" in url:
            start = params["start"]
            return make_response(200, search_page(total, ids[start:start + page_size]),
                                 {"X-RateLimit-Remaining": "100"})
        sid = int(url.rsplit("/", 1)[1])
        body = (abstracts or {}).get(sid, abstract_body(sid))
        return make_response(404 if body == 404 else 200, body)
    return handler


@pytest.fixture(scope="module")
def config():
    return load_search_config()


def client_for(handler, **kw):
    return ScopusClient(API_KEY, session=FakeSession(handler), sleep=lambda s: None,
                        min_interval=0, **kw)


def collector(config, tmp_path, handler, families=("S1",), **kw):
    client = client_for(handler)
    fams = [config.family(f) for f in families]
    return ScopusCollector(config, fams, data_dir=tmp_path, client=client, **kw)


# --------------------------------------------------------------------------- #
# Queries
# --------------------------------------------------------------------------- #

EXPECTED_QUERIES = {
    "S1": '("data source*" OR "knowledge source*" OR "source selection" OR "source curation" OR "corpus curation")',
    "S2": '("data ingestion" OR "document ingestion" OR "data extraction" OR "document parsing" OR OCR OR crawl*)',
    "S3": '("vector database*" OR "vector store*" OR "vector index*" OR "document store*" OR "embedding store*")',
    "S4": '(chunk* OR "text segment*" OR "document split*" OR "text preprocessing" OR "document preprocessing" OR "text normalization" OR "embedding generation")',
    "S5": '("retrieval strateg*" OR "hybrid search" OR rerank* OR "metadata filter*" OR "context compression")',
    "S6": '("RAG evaluation" OR "retrieval evaluation" OR observab* OR tracing OR "user feedback")',
    "S7": '(freshness OR reindex* OR "document update*" OR "corpus update*" OR "incremental update*" OR version*)',
    "S8": '("data deletion" OR "document deletion" OR deindex* OR erasure OR retention OR purge OR expiration)',
}


@pytest.mark.parametrize("fid", list(EXPECTED_QUERIES))
def test_scopus_query(config, fid):
    query = build_scopus_query(config, config.family(fid))
    assert query == f"TITLE-ABS-KEY({RAG} AND {EXPECTED_QUERIES[fid]})"
    assert "PUBYEAR" not in query


# --------------------------------------------------------------------------- #
# Cliente HTTP
# --------------------------------------------------------------------------- #

def test_client_sends_auth_headers():
    c = ScopusClient(API_KEY, inst_token="TOKEN", session=FakeSession(None))
    assert c.session.headers["X-ELS-APIKey"] == API_KEY
    assert c.session.headers["X-ELS-Insttoken"] == "TOKEN"
    assert "X-ELS-Insttoken" not in ScopusClient(API_KEY, session=FakeSession(None)).session.headers


def test_200_records_rate_limit_headers():
    headers = {"X-RateLimit-Limit": "20000", "X-RateLimit-Remaining": "19999",
               "X-RateLimit-Reset": "1760000000"}
    c = client_for(lambda u, p: make_response(200, search_page(1, [1]), headers))
    page = c.search("q")
    assert page["search-results"]["opensearch:totalResults"] == "1"
    assert c.rate_limit == {"limit": "20000", "remaining": "19999", "reset": "1760000000"}


@pytest.mark.parametrize("status", [401, 403])
def test_auth_errors_are_not_retried(status):
    body = {"service-error": {"status": {"statusCode": "AUTHENTICATION_ERROR",
                                         "statusText": "Invalid API Key"}}}
    c = client_for(lambda u, p: make_response(status, body))
    with pytest.raises(ScopusAuthError) as exc:
        c.search("q")
    assert c.request_count == 1
    assert API_KEY not in str(exc.value)


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_retryable_then_success(status):
    responses = iter([make_response(status), make_response(status),
                      make_response(200, search_page(1, [1]))])
    sleeps = []
    c = ScopusClient(API_KEY, session=FakeSession(lambda u, p: next(responses)),
                     sleep=sleeps.append, min_interval=0)
    assert c.search("q")
    assert c.request_count == 3
    assert sleeps == [1, 2]  # backoff exponencial


def test_retry_gives_up():
    c = client_for(lambda u, p: make_response(500), max_attempts=3)
    with pytest.raises(ScopusRetryableError):
        c.search("q")
    assert c.request_count == 3


def test_quota_exceeded_is_not_retried():
    c = client_for(lambda u, p: make_response(
        429, {}, {"X-ELS-Status": "QUOTA_EXCEEDED - Quota Exceeded", "X-RateLimit-Remaining": "0"}))
    with pytest.raises(ScopusQuotaError):
        c.search("q")
    assert c.request_count == 1


def test_abstract_404_returns_none():
    c = client_for(lambda u, p: make_response(404, {}))
    assert c.get_abstract("123") is None


def test_other_4xx_raises():
    c = client_for(lambda u, p: make_response(400, {"service-error": {"status": {
        "statusCode": "INVALID_INPUT", "statusText": "bad query"}}}))
    with pytest.raises(ScopusError, match="INVALID_INPUT"):
        c.search("q")


# --------------------------------------------------------------------------- #
# Normalização
# --------------------------------------------------------------------------- #

def test_parse_search_entry_without_doi():
    fields = parse_search_entry(entry(7, doi=False))
    assert fields["source_id"] == "7"
    assert fields["doi"] is None
    assert fields["year"] == 2019
    assert fields["url"] == "https://www.scopus.com/7"
    assert fields["extra"]["eid"] == "2-s2.0-7"


def test_parse_abstract():
    fields = parse_abstract(abstract_body(7))
    assert fields["abstract"] == "An abstract."
    assert fields["authors"] == ["Ann A", "Bob B"]
    assert fields["keywords"] == ["RAG", "chunking"]
    assert fields["doi"] == "10.1/7"


def test_parse_abstract_missing_abstract_and_doi():
    fields = parse_abstract(abstract_body(7, abstract=None, doi=False))
    assert fields["abstract"] is None
    assert fields["doi"] is None


def test_parse_abstract_single_author_as_dict():
    body = abstract_body(7)
    body["abstracts-retrieval-response"]["authors"]["author"] = {
        "@seq": "1", "ce:indexed-name": "Solo S."}
    assert parse_abstract(body)["authors"] == ["Solo S."]


# --------------------------------------------------------------------------- #
# Coletor
# --------------------------------------------------------------------------- #

def test_pagination_collects_all_pages(config, tmp_path):
    c = collector(config, tmp_path, paginated_handler(450))
    manifest = c.run()

    fam = manifest["families"]["S1"]
    assert fam["status"] == "complete"
    assert fam["pages"] == 3
    assert fam["total_results_reported"] == 450
    assert fam["total_results_collected"] == 450
    assert fam["executed_query"].startswith("TITLE-ABS-KEY(")
    assert manifest["temporal_filter"] is None

    starts = [p["start"] for u, p in c.client.session.calls if "search" in u]
    assert starts == [0, 200, 400]
    assert all(p["count"] == 200 and p["view"] == "STANDARD"
               for u, p in c.client.session.calls if "search" in u)

    fdir = tmp_path / "raw" / "scopus" / "q1" / "S1"
    assert sorted(p.name for p in fdir.glob("page_*.json")) == [
        "page_0001.json", "page_0002.json", "page_0003.json"]
    records = read_jsonl(fdir / "records.jsonl")
    assert len(records) == 450
    assert records[0]["abstract"] == "An abstract."
    assert records[0]["year"] == 2019  # nenhum filtro temporal
    assert manifest["enrichment"]["fetched"] == 450

    text = json.dumps(manifest)
    assert API_KEY not in text


def test_empty_result(config, tmp_path):
    c = collector(config, tmp_path, paginated_handler(0))
    manifest = c.run()
    fam = manifest["families"]["S1"]
    assert fam["status"] == "complete"
    assert fam["total_results_collected"] == 0
    assert manifest["unique_papers"] == 0


def test_same_paper_in_two_families_keeps_both_occurrences(config, tmp_path):
    c = collector(config, tmp_path, paginated_handler(3), families=("S2", "S4"))
    manifest = c.run()
    assert manifest["total_occurrences"] == 6
    assert manifest["unique_papers"] == 3
    # Abstract Retrieval uma vez por ID único.
    abstract_calls = [u for u, p in c.client.session.calls if "/abstract/" in u]
    assert len(abstract_calls) == 3
    rec = read_jsonl(tmp_path / "raw" / "scopus" / "q1" / "all_records.jsonl")[0]
    assert rec["search_families"] == ["S2", "S4"]
    assert [p["family"] for p in rec["provenance"]] == ["S2", "S4"]


def test_total_over_5000_uses_cursor(config, tmp_path):
    total = 5001

    def handler(url, params):
        if "cursor" not in params:
            return make_response(200, search_page(total, list(range(1, 201))))
        if params["cursor"] == "*":
            return make_response(200, search_page(total, list(range(1, 201)), "c1"))
        # Simula o resto em uma única "página" grande para o teste.
        return make_response(200, search_page(total, list(range(201, total + 1)), "c2"))

    c = collector(config, tmp_path, handler, enrich=False)
    manifest = c.run()
    fam = manifest["families"]["S1"]
    assert fam["pagination_mode"] == "cursor"
    assert fam["status"] == "complete"
    assert fam["total_results_collected"] == total


def test_total_over_5000_without_cursor_is_explicit_error(config, tmp_path):
    def handler(url, params):
        if "cursor" in params:
            return make_response(400, {"service-error": {"status": {
                "statusCode": "INVALID_INPUT", "statusText": "cursor not allowed"}}})
        return make_response(200, search_page(6000, list(range(1, 201))))

    c = collector(config, tmp_path, handler, enrich=False)
    manifest = c.run()
    fam = manifest["families"]["S1"]
    assert fam["status"] == "failed"
    assert "NÃO cobre o universo completo" in fam["error"]
    assert fam["total_results_reported"] == 6000
    assert fam["total_results_collected"] == 0


def test_resume_after_interruption(config, tmp_path):
    base = paginated_handler(450)
    fail = {"on": True}

    def flaky(url, params):
        if "search" in url and params.get("start") == 400 and fail["on"]:
            return make_response(400, {})
        return base(url, params)

    c1 = collector(config, tmp_path, flaky, enrich=False)
    m1 = c1.run()
    assert m1["families"]["S1"]["status"] == "incomplete"
    assert m1["families"]["S1"]["total_results_collected"] == 400
    state = read_json(tmp_path / "raw" / "scopus" / "q1" / "S1" / "state.json")
    assert state["pages_done"] == 2 and not state["complete"]

    fail["on"] = False
    c2 = collector(config, tmp_path, flaky, enrich=False)
    m2 = c2.run()
    assert m2["families"]["S1"]["status"] == "complete"
    assert m2["families"]["S1"]["total_results_collected"] == 450
    starts = [p["start"] for u, p in c2.client.session.calls if "search" in u]
    assert starts == [400]  # retomou na página 3


def test_completed_family_is_reused_without_requests(config, tmp_path):
    collector(config, tmp_path, paginated_handler(10)).run()
    c = collector(config, tmp_path, paginated_handler(10))
    manifest = c.run()
    assert c.client.session.calls == []
    assert manifest["families"]["S1"]["total_results_collected"] == 10
    assert manifest["enrichment"]["cached"] == 10


def test_force_ignores_cache(config, tmp_path):
    collector(config, tmp_path, paginated_handler(10)).run()
    c = collector(config, tmp_path, paginated_handler(10), force=True)
    c.run()
    assert len([u for u, p in c.client.session.calls if "/abstract/" in u]) == 10
    assert len([u for u, p in c.client.session.calls if "search" in u]) == 1


def test_missing_abstract_and_404_metadata(config, tmp_path):
    handler = paginated_handler(3, abstracts={1: abstract_body(1, abstract=None, doi=False), 2: 404})
    c = collector(config, tmp_path, handler)
    manifest = c.run()
    by_id = {r["source_id"]: r for r in read_jsonl(tmp_path / "raw" / "scopus" / "q1" / "all_records.jsonl")}
    assert by_id["1"]["abstract"] is None
    assert by_id["1"]["abstract_available"] is False
    assert by_id["1"]["doi"] == "10.1/1"  # DOI da busca preservado
    assert by_id["2"]["extra"]["enrichment"] == "not_found"
    assert by_id["2"]["title"] == "Paper 2"
    assert manifest["enrichment"]["not_found"] == 1
    # 404 fica em cache: nova execução não consulta de novo.
    c2 = collector(config, tmp_path, handler)
    c2.run()
    assert c2.client.session.calls == []


def test_enrichment_auth_error_is_reported(config, tmp_path):
    base = paginated_handler(3)

    def handler(url, params):
        if "/abstract/" in url:
            return make_response(401, {})
        return base(url, params)

    manifest = collector(config, tmp_path, handler).run()
    assert manifest["families"]["S1"]["status"] == "complete"
    assert manifest["enrichment"]["status"] == "incomplete"
    assert manifest["enrichment"]["pending"] == 3
    assert manifest["unique_papers"] == 3


def test_query_version_layout_and_shared_metadata_cache(config, tmp_path):
    manifest = collector(config, tmp_path, paginated_handler(3)).run()
    assert manifest["query_version"] == config.version
    assert manifest["query_fingerprint"] == config.fingerprint()
    assert (tmp_path / "raw" / "scopus" / f"q{config.version}" / "S1" / "page_0001.json").exists()
    # Cache de abstracts fica fora da versão (reaproveitado entre versões das strings).
    assert len(list((tmp_path / "raw" / "scopus" / "metadata").glob("*.json"))) == 3
