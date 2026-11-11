"""Loop incremental da revisão: coleta → pré-triagem → rodadas de 10 →
validação humana → análise → snowballing → refinamento das strings.

Fluxo típico (ver também .claude/skills/mlr-*):

    review_loop.py init --reviewer arthur
    review_loop.py protocol-update --reviewer arthur --justification "..."
    review_loop.py sync                         # coletas q<N> (+ snowball) → pool
    review_loop.py pretriage-batches            # lotes para a skill mlr-screening
    review_loop.py import-pretriage
    review_loop.py round-new                    # shortlist para a skill mlr-ranking
    review_loop.py round-rank r001 ranking.json # 10 candidatos → rounds/r001/review.csv
    review_loop.py round-review r001 rounds/r001/review.csv
    review_loop.py round-close r001
    review_loop.py analyze                      # passo 9 (+ skill mlr-analysis)
    review_loop.py snowball                     # passo 10 (Scopus)
    review_loop.py refine                       # passo 11 (+ skill mlr-refinement)
    review_loop.py register-queries --reviewer arthur --justification "..."
    review_loop.py status                       # inclui critérios de parada
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from _common import ROOT, setup_logging

from src.review import HumanDecision, ReviewError, ReviewWorkspace
from src.review.analysis import write_analysis
from src.utils.io import utc_now

DEFAULT_WORKSPACE = ROOT / "data" / "review"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    p.add_argument("--data-dir", type=Path, default=ROOT / "data")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("init", help="cria o workspace e registra as strings iniciais (q1)")
    c.add_argument("--protocol", type=Path, default=ROOT / "config" / "review_protocol.yaml")
    c.add_argument("--queries", type=Path, default=ROOT / "config" / "search_queries.yaml")
    c.add_argument("--reviewer", required=True)

    c = sub.add_parser("protocol-update", help="versiona o protocolo e migra o recorte temporal")
    c.add_argument("--protocol", type=Path, default=ROOT / "config" / "review_protocol.yaml")
    c.add_argument("--reviewer", required=True)
    c.add_argument("--justification", required=True)

    c = sub.add_parser("sync", help="consolida a coleta da versão atual (+ snowball) no pool")
    c.add_argument("--allow-incomplete", action="store_true",
                   help="aceita coleta com abstracts pendentes (registrado como aviso)")

    c = sub.add_parser("pretriage-batches", help="gera lotes para a skill mlr-screening")
    c.add_argument("--size", type=int)
    sub.add_parser("import-pretriage", help="valida e importa as respostas dos lotes")

    sub.add_parser("round-new", help="abre rodada: shortlist para a skill mlr-ranking")
    c = sub.add_parser("round-rank", help="importa o ranking da IA (exatamente 10 candidatos)")
    c.add_argument("round")
    c.add_argument("ranking", type=Path)
    c = sub.add_parser("round-review", help="importa a planilha de revisão humana da rodada")
    c.add_argument("round")
    c.add_argument("sheet", type=Path)
    c.add_argument("--reviewer", help="revisor padrão para linhas sem a coluna reviewer")
    c = sub.add_parser("decide", help="registra uma decisão humana individual")
    c.add_argument("paper_id")
    c.add_argument("decision", choices=["include", "exclude", "full_text"])
    c.add_argument("--round", help="rodada (omitir só para resolver papers full_text)")
    c.add_argument("--criterion", choices=["E1", "E2", "E3", "E4", "E5"])
    c.add_argument("--foundational", action="store_true", help="exceção de I1 (registro anterior ao corte vigente)")
    c.add_argument("--reviewer", required=True)
    c.add_argument("--justification", required=True)
    c.add_argument("--suggest-term", action="append", default=[])
    c = sub.add_parser("round-close", help="fecha a rodada após as 10 decisões humanas")
    c.add_argument("round")

    c = sub.add_parser("audit-new", help="amostra aleatória da pré-triagem para auditoria humana")
    c.add_argument("--size", type=int)
    c = sub.add_parser("audit-import", help="importa a planilha de auditoria preenchida")
    c.add_argument("audit")
    c.add_argument("sheet", type=Path)

    sub.add_parser("analyze", help="passo 9: cobertura do dataset curado + pacote para mlr-analysis")

    c = sub.add_parser("snowball", help="passo 10: referências e citações (Scopus) das validadas")
    c.add_argument("--direction", choices=["backward", "forward", "both"], default="both")
    c.add_argument("--max-seeds", type=int)
    c.add_argument("--seed-source", choices=["validated", "pretriage-high"], default="validated",
                   help="validated usa inclusões humanas; pretriage-high usa sementes provisórias "
                        "e registra a política no manifest")
    c.add_argument("--seed-origin", choices=["any", "acl", "scopus"], default="any",
                   help="restringe sementes à proveniência indicada; o filtro fica no manifest")

    sub.add_parser("refine", help="passo 11: pacote para a skill mlr-refinement")
    c = sub.add_parser("register-queries", help="registra nova versão aprovada das strings")
    c.add_argument("--queries", type=Path, default=ROOT / "config" / "search_queries.yaml")
    c.add_argument("--reviewer", required=True)
    c.add_argument("--justification", required=True)

    sub.add_parser("status", help="progresso e indicadores de parada")
    return p


def run_snowball(ws: ReviewWorkspace, args) -> dict:
    from dotenv import load_dotenv

    from src.collectors.scopus import ScopusClient
    from src.review.snowball import BACKWARD, FORWARD, ScopusSnowball

    load_dotenv(ROOT / ".env")
    api_key = os.getenv("SCOPUS_API_KEY") or os.getenv("SCORPUS_API_KEY")
    client = ScopusClient(api_key, inst_token=os.getenv("SCOPUS_INST_TOKEN") or None)
    seeds, seed_selection = ws.snowball_seeds(args.seed_source, args.seed_origin)
    directions = {"backward": (BACKWARD,), "forward": (FORWARD,), "both": (BACKWARD, FORWARD)}[args.direction]
    return ScopusSnowball(client, args.data_dir).run(
        seeds, directions, args.max_seeds, seed_selection=seed_selection)


def main() -> int:
    args = parser().parse_args()
    setup_logging(False)
    ws = ReviewWorkspace(args.workspace)

    try:
        cmd = args.command
        if cmd == "init":
            result = ws.init(args.protocol, args.queries, args.reviewer)
        elif cmd == "protocol-update":
            result = ws.update_protocol(args.protocol, args.reviewer, args.justification)
        elif cmd == "sync":
            result = ws.sync(args.data_dir, args.allow_incomplete)
        elif cmd == "pretriage-batches":
            result = ws.make_pretriage_batches(args.size)
        elif cmd == "import-pretriage":
            result = ws.import_pretriage()
        elif cmd == "round-new":
            result = ws.new_round()
        elif cmd == "round-rank":
            result = ws.import_ranking(args.round, args.ranking)
        elif cmd == "round-review":
            result = ws.import_review_sheet(args.round, args.sheet, args.reviewer)
        elif cmd == "decide":
            result = ws.record_decision(HumanDecision(
                paper_id=args.paper_id, round_id=args.round, decision=args.decision,
                primary_criterion=args.criterion, foundational=args.foundational,
                reviewer=args.reviewer, justification=args.justification,
                suggested_terms=args.suggest_term, decided_at=utc_now()))
        elif cmd == "round-close":
            result = ws.close_round(args.round)
        elif cmd == "audit-new":
            result = ws.new_audit(args.size)
        elif cmd == "audit-import":
            result = ws.import_audit(args.audit, args.sheet)
        elif cmd == "analyze":
            analysis, packet = write_analysis(ws)
            result = {"analysis": str(analysis), "packet_for_mlr_analysis": str(packet)}
        elif cmd == "snowball":
            result = run_snowball(ws, args)
        elif cmd == "refine":
            result = {"packet_for_mlr_refinement": str(ws.refinement_packet())}
        elif cmd == "register-queries":
            result = ws.register_queries(args.queries, args.reviewer, args.justification)["query_versions"]
        else:
            result = ws.status()
    except (ReviewError, ValueError, FileNotFoundError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
