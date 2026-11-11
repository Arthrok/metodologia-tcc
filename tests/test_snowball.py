from src.collectors.scopus import ScopusAuthError, ScopusError
from src.review.snowball import FORWARD, ScopusSnowball, parse_references
from src.utils.io import read_json, read_jsonl


def abstract(sid, year=2024):
    return {"abstracts-retrieval-response": {"coredata": {
        "dc:identifier": f"SCOPUS_ID:{sid}", "dc:title": f"Paper {sid}",
        "dc:description": f"Abstract {sid}", "prism:coverDate": f"{year}-01-01",
        "prism:doi": f"10.9/{sid}"}}}


def refs_page(total, ids):
    return {"abstracts-retrieval-response": {"references": {
        "@total-references": str(total), "reference": [{"scopus-id": i} for i in ids]}}}


class FakeClient:
    def __init__(self, refs, citing, fail_on=None, reported_totals=None):
        self.refs, self.citing_ids, self.fail_on = refs, citing, fail_on
        self.reported_totals = reported_totals or {}
        self.request_count, self.rate_limit, self.proxy = 0, {}, None
        self.calls = []

    def get_references(self, sid, start=None, count=None):
        self.request_count += 1
        self.calls.append(("ref", sid, start))
        if sid == self.fail_on:
            raise ScopusAuthError("HTTP 401", 401)
        ids = self.refs.get(sid, [])
        total = self.reported_totals.get(sid, len(ids))
        if start is None:
            return refs_page(total, ids[:40])
        if start - 1 + count > len(ids):
            raise ScopusError("HTTP 400 — INVALID_INPUT: 'startref' or 'refcount' parameter missing or invalid", 400)
        return refs_page(total, ids[start - 1:start - 1 + count])

    def search(self, query, start=0, count=200):
        self.request_count += 1
        self.calls.append(("search", query, start))
        if query.startswith("DOI("):
            return {"search-results": {"opensearch:totalResults": "1",
                                       "entry": [{"dc:identifier": "SCOPUS_ID:900"}]}}
        sid = query.removeprefix("REFEID(2-s2.0-").rstrip(")")
        ids = self.citing_ids.get(sid, [])
        entries = [{"dc:identifier": f"SCOPUS_ID:{i}"} for i in ids[start:start + count]]
        return {"search-results": {"opensearch:totalResults": str(len(ids)),
                                   "entry": entries or [{"error": "Result set was empty"}]}}

    def get_abstract(self, sid, view="META_ABS"):
        self.request_count += 1
        self.calls.append(("abs", sid))
        return abstract(sid, year=2019 if sid == "old" else 2025)


def seed(pid, sid=None, doi=None):
    return {"review_id": pid, "source_records": [f"scopus:{sid}"] if sid else [f"acl:{pid}"], "doi": doi}


def test_parse_references():
    assert parse_references(refs_page(2, ["1", "2"])) == (2, ["1", "2"])


def test_backward_and_forward_with_pagination_and_cache(tmp_path):
    refs = {"100": [str(i) for i in range(1, 46)] + ["old"]}  # 46 refs → 40 + 6
    client = FakeClient(refs, {"100": ["c1", "c2", "1"]})
    manifest = ScopusSnowball(client, tmp_path).run({"P-1": seed("P-1", "100")})

    assert [c for c in client.calls if c[0] == "ref"] == [("ref", "100", None), ("ref", "100", 41)]
    candidates = {r["source_id"]: r for r in read_jsonl(tmp_path / "raw" / "snowball" / "candidates.jsonl")}
    assert len(candidates) == 48  # 46 referências + 2 citantes novos ("1" aparece nos dois)
    both = candidates["1"]
    assert {p["family"] for p in both["provenance"]} == {"SB-B", "SB-F"}
    assert all(p["seed"] == "P-1" for p in both["provenance"])
    assert candidates["old"]["year"] == 2019  # sem filtro temporal no snowballing
    assert manifest["search_strings_applied"] is False
    assert manifest["seed_selection"]["source"] == "human_validated"
    assert manifest["seed_ids_selected"] == ["P-1"]
    assert manifest["seeds_pending"] == 0

    # Nova execução: semente já processada, sem requisições.
    client2 = FakeClient(refs, {})
    ScopusSnowball(client2, tmp_path).run({"P-1": seed("P-1", "100")})
    assert client2.calls == []


def test_seed_resolved_by_doi_and_error_resumes(tmp_path):
    client = FakeClient({"900": ["a"]}, {}, fail_on="900")
    manifest = ScopusSnowball(client, tmp_path).run({"P-2": seed("P-2", doi="10.1/x")})
    assert ("search", "DOI(10.1/x)", 0) in client.calls
    assert manifest["errors"] and manifest["seeds_pending"] == 1
    state = read_json(tmp_path / "raw" / "snowball" / "state.json")
    assert "P-2" not in state["done"] or "backward" not in state["done"]["P-2"]

    ok = FakeClient({"900": ["a"]}, {})
    manifest = ScopusSnowball(ok, tmp_path).run({"P-2": seed("P-2", doi="10.1/x")})
    assert manifest["seeds_pending"] == 0 and manifest["candidates_total"] == 1


def test_forward_paginates_with_basic_service_limit(tmp_path):
    citing = {"100": [str(i) for i in range(30)]}
    client = FakeClient({}, citing)
    manifest = ScopusSnowball(client, tmp_path).run(
        {"P-1": seed("P-1", "100")}, directions=(FORWARD,))

    calls = [call for call in client.calls if call[0] == "search"]
    assert calls == [
        ("search", "REFEID(2-s2.0-100)", 0),
        ("search", "REFEID(2-s2.0-100)", 25),
    ]
    assert manifest["citing"] == 30
    assert manifest["candidates_total"] == 30


def test_backward_tolerates_unresolved_reference_in_reported_total(tmp_path):
    refs = {"100": [str(i) for i in range(42)]}
    client = FakeClient(refs, {}, reported_totals={"100": 43})
    manifest = ScopusSnowball(client, tmp_path).run(
        {"P-1": seed("P-1", "100")}, directions=("backward",))

    assert manifest["references"] == 42
    assert manifest["candidates_total"] == 42
    assert manifest["errors"] == []


def test_unresolved_seed_is_recorded(tmp_path):
    client = FakeClient({}, {})
    manifest = ScopusSnowball(client, tmp_path).run({"P-3": seed("P-3")})
    assert manifest["unresolved_seeds"] == ["P-3"]
