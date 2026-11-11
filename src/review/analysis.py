"""Passo 9: análise de cobertura do dataset curado (parte determinística).

Gera contagens e lacunas objetivas; a identificação de padrões e lacunas
temáticas é feita pela skill `mlr-analysis` sobre o pacote gerado aqui, e
revisada pelos pesquisadores.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from src.utils.io import utc_now, write_json


def coverage_analysis(workspace) -> dict:
    protocol = workspace.protocol()
    pool, pretriage, decisions = workspace.pool(), workspace.pretriage(), workspace.current_decisions()
    validated = workspace.validated()
    stages = protocol["lifecycle_stages"]
    dimensions = protocol["transverse_dimensions"]
    minimum = protocol["stopping"]["min_includes_per_stage"]

    stage_counts = Counter(s for p in validated for s in pretriage.get(p, {}).get("lifecycle_stages", []))
    dim_counts = Counter(d for p in validated for d in pretriage.get(p, {}).get("transverse_dimensions", []))
    # Etapa atribuída pela IA vs família de busca que recuperou o paper.
    family_counts = Counter(f for p in validated for f in pool[p].get("search_families", []))

    return {
        "generated_at": utc_now().isoformat(),
        "validated_total": len(validated),
        "foundational_included": sum(1 for p in validated if decisions[p].get("foundational")),
        "by_lifecycle_stage": {s: {"label": label, "validated": stage_counts.get(s, 0),
                                   "retrieved_by_family": family_counts.get(s, 0)}
                               for s, label in stages.items()},
        "by_transverse_dimension": {d: dim_counts.get(d, 0) for d in dimensions},
        "by_year": dict(sorted(Counter(pool[p].get("year") for p in validated).items(),
                               key=lambda kv: kv[0] or 0)),
        "by_source": dict(Counter(s for p in validated for s in pool[p].get("sources", []))),
        "by_origin": dict(Counter(o for p in validated for o in pool[p].get("origins", []))),
        "top_venues": Counter(pool[p].get("venue") for p in validated).most_common(10),
        "gaps": {
            "stages_below_minimum": [s for s in stages if stage_counts.get(s, 0) < minimum],
            "dimensions_without_evidence": [d for d in dimensions if not dim_counts.get(d)],
        },
        "decisions": {
            "include": len(validated),
            "exclude_by_criterion": dict(Counter(d["primary_criterion"] for d in decisions.values()
                                                 if d["decision"] == "exclude")),
            "full_text_pending": sum(1 for d in decisions.values() if d["decision"] == "full_text"),
        },
    }


def write_analysis(workspace) -> tuple[Path, Path]:
    """Salva a análise e o pacote de entrada da skill mlr-analysis."""
    state = workspace.state()
    tag = state["rounds"][-1]["round_id"] if state["rounds"] else "r000"
    analysis = coverage_analysis(workspace)
    out = workspace.root / "analysis"
    analysis_path = out / f"coverage_{tag}.json"
    write_json(analysis_path, analysis)

    pool, pretriage, decisions = workspace.pool(), workspace.pretriage(), workspace.current_decisions()
    packet = {
        "after_round": tag,
        "research_questions": workspace.protocol()["research_questions"],
        "coverage": analysis,
        "validated": [
            {"paper_id": p, "title": pool[p].get("title"), "abstract": pool[p].get("abstract"),
             "year": pool[p].get("year"), "venue": pool[p].get("venue"),
             "lifecycle_stages": pretriage.get(p, {}).get("lifecycle_stages", []),
             "transverse_dimensions": pretriage.get(p, {}).get("transverse_dimensions", []),
             "human_justification": decisions[p]["justification"]}
            for p in workspace.validated()
        ],
    }
    packet_path = out / f"packet_{tag}.json"
    write_json(packet_path, packet)
    return analysis_path, packet_path
