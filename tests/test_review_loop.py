import csv
from pathlib import Path

import pytest
import yaml

from src.review import HumanDecision, ReviewError, ReviewWorkspace
from src.review.analysis import coverage_analysis
from src.review.corpus import match_keys, merge_into_pool, temporal_status
from src.review.ranking import TfidfIndex
from src.search import load_search_config
from src.utils.io import read_json, read_jsonl, utc_now, write_json, write_jsonl

ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

def paper(source, sid, title, year=2025, doi=None, abstract=None, families=("S1",)):
    return {
        "id": f"{source}:{sid}", "source": source, "source_id": sid, "title": title,
        "abstract": abstract if abstract is not None else f"RAG pipeline paper about {title}.",
        "doi": doi, "authors": [], "year": year, "keywords": [],
        "search_families": list(families), "provenance": [{"source": source, "family": families[0]}],
    }


def write_collection(data: Path, source: str, records: list[dict], config, **manifest_extra):
    raw = data / "raw" / source / f"q{config.version}"
    write_jsonl(raw / "all_records.jsonl", records)
    manifest = {"source": source, "query_version": config.version,
                "query_fingerprint": config.fingerprint(), "full_run": True,
                "families": {"S1": {"status": "complete"}}, **manifest_extra}
    mdir = data / "manifests" / source
    mdir.mkdir(parents=True, exist_ok=True)
    n = len(list(mdir.glob("*.json"))) + 1
    write_json(mdir / f"2026-01-{n:02d}T000000.json", manifest)


@pytest.fixture
def setup(tmp_path):
    data = tmp_path / "data"
    config = load_search_config(ROOT / "config" / "search_queries.yaml")
    titles = [f"Topic number {i} about retrieval pipelines" for i in range(25)]
    write_collection(data, "acl", [paper("acl", f"a{i}", t) for i, t in enumerate(titles[:12])], config)
    scopus = [paper("scopus", f"s{i}", t, doi=f"10.1/{i}") for i, t in enumerate(titles[12:])]
    # Duplicata entre bases (mesmo título do ACL a0) e um registro anterior a 2024.
    scopus.append(paper("scopus", "dup", titles[0]))
    scopus.append(paper("scopus", "old", "Original RAG paper for knowledge intensive tasks", year=2020))
    write_collection(data, "scopus", scopus, config, enrichment={"status": "complete"})
    ws = ReviewWorkspace(tmp_path / "review")
    ws.init(ROOT / "config" / "review_protocol.yaml", ROOT / "config" / "search_queries.yaml", "tester")
    return ws, data, config


def pretriage_row(pid, suggestion="include", priority="alta", record=None, **kw):
    row = {
        "paper_id": pid, "suggestion": suggestion, "priority": priority,
        "primary_criterion": kw.pop("primary_criterion", "E3" if suggestion == "exclude" else None),
        "evidence": [record["title"]] if record and suggestion == "include" else [],
        "justification": "teste", "lifecycle_stages": kw.pop("stages", ["S1"]),
        "transverse_dimensions": [], "model": "test-model", "prompt_version": "mlr-screening-v2",
        "decided_at": utc_now().isoformat(),
    }
    row.update(kw)
    return row


def pretriage_all(ws, suggestion_for=lambda pid, i: "include"):
    ws.make_pretriage_batches(size=10)
    pool = ws.pool()
    for bid, batch in ws.state()["pretriage_batches"].items():
        rows = [pretriage_row(pid, suggestion_for(pid, i), record=pool[pid])
                for i, pid in enumerate(batch["paper_ids"])]
        write_jsonl(ws.root / batch["output"], rows)
    return ws.import_pretriage()


def rank_round(ws, round_id):
    shortlist = read_jsonl(ws.round_dir(round_id) / "shortlist.jsonl")
    n = ws._round(ws.state(), round_id)["candidates_expected"]
    ranking = {"round_id": round_id, "model": "test-model", "prompt_version": "mlr-ranking-v1",
               "decided_at": utc_now().isoformat(),
               "candidates": [{"paper_id": c["paper_id"], "rank": i + 1, "justification": "aderente"}
                              for i, c in enumerate(shortlist[:n])]}
    path = ws.round_dir(round_id) / "ranking_input.json"
    write_json(path, ranking)
    return ws.import_ranking(round_id, path)


def fill_sheet(ws, round_id, decide):
    path = ws.round_dir(round_id) / "review.csv"
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        row.update(decide(row))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return path


INCLUDE = lambda row: {"decision": "include", "justification": "Atende I1–I3.", "reviewer": "tester"}  # noqa: E731
EXCLUDE = lambda row: {"decision": "exclude", "criterion": "E3", "justification": "RAG incidental.", "reviewer": "tester"}  # noqa: E731


# --------------------------------------------------------------------------- #
# Corpus
# --------------------------------------------------------------------------- #

def test_protocol_matches_methodology():
    protocol = yaml.safe_load((ROOT / "config" / "review_protocol.yaml").read_text())
    assert protocol["scope"]["temporal_start_year"] == 2024
    assert protocol["screening"]["round_size"] == 10
    assert set(protocol["eligibility"]["exclusion"]) == {"E1", "E2", "E3", "E4", "E5"}
    assert "E2" not in protocol["screening"]["automatic_exclusions"]


def test_match_keys_doi_and_title():
    keys = match_keys({"doi": "https://doi.org/10.1/ABC", "title": "A long enough title here"})
    assert keys == ["doi:10.1/abc", "title:a long enough title here"]


def test_temporal_status_never_excludes():
    assert temporal_status(2023, 2024) == "pre_cutoff"
    assert temporal_status(2024, 2024) == "in_scope"
    assert temporal_status(None, 2024) == "unknown"


def test_merge_keeps_provenance_and_is_idempotent():
    a = paper("acl", "1", "Same title for both sources here", doi="10/x")
    b = paper("scopus", "2", "Same title for both sources here", doi="10/X", families=("S4",))
    pool, rep = merge_into_pool([], [a, b], origin="search", sync_id="s1", start_year=2025)
    assert len(pool) == 1 and rep["stats"]["duplicates_e1"] == 1
    assert pool[0]["sources"] == ["acl", "scopus"]
    assert pool[0]["search_families"] == ["S1", "S4"]
    pool, rep = merge_into_pool(pool, [a, b], origin="search", sync_id="s2", start_year=2025)
    assert len(pool) == 1 and rep["stats"]["new_papers"] == 0 and rep["stats"]["duplicates_e1"] == 0


def test_tfidf_similarity_prefers_related_text():
    idx = TfidfIndex({"v": "vector database indexing freshness", "a": "vector database freshness updates",
                      "b": "medical question answering benchmark"})
    assert idx.max_similarity("a", ["v"]) > idx.max_similarity("b", ["v"])


# --------------------------------------------------------------------------- #
# Loop
# --------------------------------------------------------------------------- #

def test_sync_dedups_and_marks_pre_cutoff(setup):
    ws, data, _ = setup
    summary = ws.sync(data)
    assert summary["new_papers"] == 25 + 1  # 25 títulos + 1 pré-2024; a duplicata é fundida
    pool = ws.pool()
    old = next(r for r in pool.values() if r["year"] == 2020)
    assert old["temporal_status"] == "pre_cutoff"  # preservado, não excluído
    assert ws.sync(data)["new_papers"] == 0          # idempotente


def test_sync_refuses_incomplete_collection(setup, tmp_path):
    ws, data, config = setup
    write_collection(data, "scopus", [], config, enrichment={"status": "incomplete", "pending": 5})
    with pytest.raises(ReviewError, match="incompleta"):
        ws.sync(data)
    assert ws.sync(data, allow_incomplete=True)["warnings"]


def test_sync_refuses_collection_from_other_query_version(setup):
    ws, data, config = setup
    manifest_dir = data / "manifests" / "acl"
    for m in manifest_dir.glob("*.json"):
        doc = read_json(m)
        doc["query_fingerprint"] = "outra"
        write_json(m, doc)
    with pytest.raises(ReviewError, match="não corresponde"):
        ws.sync(data)


def test_protocol_update_reclassifies_and_invalidates_pretriage(setup, tmp_path):
    ws, data, _ = setup
    ws.sync(data)
    ws.make_pretriage_batches(size=100)
    batch = next(iter(ws.state()["pretriage_batches"].values()))
    pool = ws.pool()
    old = next(pid for pid, record in pool.items() if record["year"] == 2020)
    rows = [pretriage_row(pid, record=pool[pid]) for pid in batch["paper_ids"]]
    old_index = next(i for i, row in enumerate(rows) if row["paper_id"] == old)
    rows[old_index] = pretriage_row(old, "exclude", primary_criterion="E2")
    write_jsonl(ws.root / batch["output"], rows)
    assert ws.import_pretriage()["imported"] == ["batch_0001"]
    assert old in ws.pretriage()

    proposed = yaml.safe_load((ROOT / "config" / "review_protocol.yaml").read_text())
    proposed["version"] = 4
    proposed["scope"]["temporal_start_year"] = 2020
    protocol_path = tmp_path / "protocol-v4.yaml"
    protocol_path.write_text(yaml.safe_dump(proposed, allow_unicode=True, sort_keys=False))
    summary = ws.update_protocol(protocol_path, "tester", "Teste de migração do corte.")

    assert summary["changed_records"] == 1
    assert summary["invalidated_pretriage"] == 1
    assert ws.pool()[old]["temporal_status"] == "in_scope"
    assert old not in ws.pretriage()
    report = read_json(ws.root / summary["report"])
    assert report["invalidated_pretriage"][0]["paper_id"] == old
    created = ws.make_pretriage_batches(size=100)
    assert created["created"] == ["batch_0002"]
    refreshed = read_jsonl(ws.root / ws.state()["pretriage_batches"]["batch_0002"]["input"])
    assert refreshed[0]["paper_id"] == old
    assert refreshed[0]["temporal_status"] == "in_scope"


def test_provisional_snowball_seeds_are_deterministic_and_in_scope(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws)
    seeds, policy = ws.snowball_seeds("pretriage-high")
    repeated, repeated_policy = ws.snowball_seeds("pretriage-high")

    assert list(seeds) == list(repeated)
    assert policy == repeated_policy
    assert policy["source"] == "provisional_ai_pretriage"
    assert all(record["temporal_status"] == "in_scope" for record in seeds.values())
    assert all(ws.pretriage()[pid]["priority"] == "alta" for pid in seeds)

    acl_seeds, acl_policy = ws.snowball_seeds("pretriage-high", "acl")
    assert acl_seeds
    assert all("acl" in record["sources"] for record in acl_seeds.values())
    assert acl_policy["origin_filter"] == "acl"
    assert acl_policy["eligible_before_origin_filter"] == len(seeds)
    assert acl_policy["eligible_after_origin_filter"] == len(acl_seeds)


def test_pretriage_rejects_non_verbatim_evidence(setup):
    ws, data, _ = setup
    ws.sync(data)
    ws.make_pretriage_batches(size=100)
    batch = next(iter(ws.state()["pretriage_batches"].values()))
    rows = [pretriage_row(pid, record=ws.pool()[pid]) for pid in batch["paper_ids"]]
    rows[0]["evidence"] = ["texto que não está no resumo"]
    write_jsonl(ws.root / batch["output"], rows)
    result = ws.import_pretriage()
    assert result["imported"] == [] and "não literal" in next(iter(result["rejected"].values()))[0]
    assert ws.pretriage() == {}


def test_pretriage_rejects_e2_for_in_scope_record(setup):
    ws, data, _ = setup
    ws.sync(data)
    ws.make_pretriage_batches(size=100)
    batch = next(iter(ws.state()["pretriage_batches"].values()))
    pool = ws.pool()
    rows = [pretriage_row(pid, record=pool[pid]) for pid in batch["paper_ids"]]
    in_scope = next(i for i, r in enumerate(rows) if pool[r["paper_id"]]["temporal_status"] == "in_scope")
    rows[in_scope] = pretriage_row(rows[in_scope]["paper_id"], "exclude", primary_criterion="E2")
    write_jsonl(ws.root / batch["output"], rows)
    assert ws.import_pretriage()["rejected"]


def test_round_requires_exactly_ten_and_human_decisions(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws)
    rnd = ws.new_round()
    assert rnd["candidates_expected"] == 10
    with pytest.raises(ReviewError, match="feche a rodada"):
        ws.new_round()

    bad = {"round_id": "r001", "model": "m", "prompt_version": "v", "decided_at": utc_now().isoformat(),
           "candidates": [{"paper_id": c["paper_id"], "rank": i + 1, "justification": "x"}
                          for i, c in enumerate(read_jsonl(ws.round_dir("r001") / "shortlist.jsonl")[:9])]}
    write_json(ws.root / "bad.json", bad)
    with pytest.raises(ReviewError, match="exatamente 10"):
        ws.import_ranking("r001", ws.root / "bad.json")

    rnd = rank_round(ws, "r001")
    assert len(rnd["candidates"]) == 10
    with pytest.raises(ReviewError, match="faltam decisões"):
        ws.close_round("r001")

    ws.import_review_sheet("r001", fill_sheet(ws, "r001", INCLUDE))
    closed = ws.close_round("r001")
    assert closed["result"]["include"] == 10
    assert closed["result"]["ai_pretriage_agreement"] == 1.0
    assert len(ws.validated()) == 10


def test_unpresented_records_stay_unreviewed(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws, lambda pid, i: "exclude" if i % 2 else "include")
    rank_round(ws, ws.new_round()["round_id"])
    ws.import_review_sheet("r001", fill_sheet(ws, "r001", EXCLUDE))
    ws.close_round("r001")
    status = ws.status()
    assert status["human_reviewed"] == 10
    assert status["unreviewed"] == status["pool"] - 10  # não apresentados ≠ excluídos
    # Próxima rodada só traz não revisados.
    ws.new_round()
    shortlist = {c["paper_id"] for c in read_jsonl(ws.round_dir("r002") / "shortlist.jsonl")}
    assert not shortlist & set(ws.current_decisions())


def test_pre_cutoff_include_requires_foundational(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws)
    old = next(pid for pid, r in ws.pool().items() if r["temporal_status"] == "pre_cutoff")
    ws.new_round()
    shortlist = read_jsonl(ws.round_dir("r001") / "shortlist.jsonl")
    ids = [old] + [c["paper_id"] for c in shortlist if c["paper_id"] != old][:9]
    write_json(ws.root / "rk.json", {
        "round_id": "r001", "model": "m", "prompt_version": "v", "decided_at": utc_now().isoformat(),
        "candidates": [{"paper_id": p, "rank": i + 1, "justification": "x"} for i, p in enumerate(ids)]})
    if old not in {c["paper_id"] for c in shortlist}:
        pytest.skip("registro antigo fora da shortlist")
    ws.import_ranking("r001", ws.root / "rk.json")
    decision = dict(paper_id=old, round_id="r001", decision="include", reviewer="t",
                    justification="Artigo original de RAG.", decided_at=utc_now())
    with pytest.raises(ReviewError, match="foundational"):
        ws.record_decision(HumanDecision(**decision))
    ws.record_decision(HumanDecision(**decision, foundational=True))
    with pytest.raises(ReviewError, match="E2"):
        ws.record_decision(HumanDecision(paper_id=ids[1], round_id="r001", decision="exclude",
                                         primary_criterion="E2", reviewer="t", justification="x",
                                         decided_at=utc_now()))


def test_full_text_can_be_resolved_outside_round(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws)
    rank_round(ws, ws.new_round()["round_id"])
    ws.import_review_sheet("r001", fill_sheet(ws, "r001", lambda r: {
        "decision": "full_text", "justification": "Precisa do texto completo.", "reviewer": "t"}))
    ws.close_round("r001")
    pid = ws._round(ws.state(), "r001")["candidates"][0]
    ws.record_decision(HumanDecision(paper_id=pid, decision="include", reviewer="t",
                                     justification="Texto completo confirma I2.", decided_at=utc_now()))
    assert pid in ws.validated()
    other = next(p for p in ws.pool() if p not in ws.current_decisions())
    with pytest.raises(ReviewError, match="full_text"):
        ws.record_decision(HumanDecision(paper_id=other, decision="include", reviewer="t",
                                         justification="x", decided_at=utc_now()))


def test_audit_sample_is_reproducible_and_measures_agreement(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws, lambda pid, i: "exclude")
    audit = ws.new_audit(size=5)
    assert len(audit["paper_ids"]) == 5 and audit["seed"].endswith("a001")
    path = ws.root / audit["sheet"]
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for i, row in enumerate(rows):
        row.update(human_agrees="sim" if i else "não", reviewer="t")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    result = ws.import_audit("a001", path)["result"]
    assert result["agreement"] == 0.8
    assert result["possible_false_negatives"] == 1


def test_query_versions_and_refinement(setup, tmp_path):
    ws, data, config = setup
    ws.sync(data)
    pretriage_all(ws)
    rank_round(ws, ws.new_round()["round_id"])
    ws.import_review_sheet("r001", fill_sheet(ws, "r001", INCLUDE))
    ws.close_round("r001")

    packet = read_json(ws.refinement_packet())
    assert len(packet["validated_references"]) == 10
    assert packet["current_query_version"] == 1

    # Alterar strings sem incrementar a versão é recusado.
    changed = yaml.safe_load((ROOT / "config" / "search_queries.yaml").read_text())
    changed["families"]["S7"]["terms"].append("stale index*")
    q = tmp_path / "q.yaml"
    q.write_text(yaml.safe_dump(changed, allow_unicode=True))
    with pytest.raises(ReviewError, match="incremente"):
        ws.register_queries(q, "tester", "adiciona termo")
    changed["version"] = 2
    q.write_text(yaml.safe_dump(changed, allow_unicode=True))
    ws.register_queries(q, "tester", "Termo recorrente nas validadas.")
    assert ws.current_query_version() == 2
    assert ws.state()["query_versions"]["2"]["registered_after_round"] == "r001"
    # Sync exige coleta da nova versão.
    with pytest.raises(ReviewError, match="q2"):
        ws.sync(data)


def test_stopping_indicators_and_analysis(setup):
    ws, data, _ = setup
    ws.sync(data)
    pretriage_all(ws)
    for n in range(1, 3):
        rid = ws.new_round()["round_id"]
        rank_round(ws, rid)
        ws.import_review_sheet(rid, fill_sheet(ws, rid, INCLUDE if n == 1 else EXCLUDE))
        ws.close_round(rid)
    stopping = ws.status()["stopping"]
    assert stopping["low_new_relevant"]["met"] is False   # janela de 3 ainda não completa
    assert stopping["coverage"]["validated_by_stage"]["S1"] == 10
    assert stopping["coverage"]["met"] is False           # S2–S8 sem evidências
    analysis = coverage_analysis(ws)
    assert analysis["validated_total"] == 10
    assert "S8" in analysis["gaps"]["stages_below_minimum"]
