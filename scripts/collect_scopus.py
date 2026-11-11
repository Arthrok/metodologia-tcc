"""Coleta S1–S8 no Scopus (TITLE-ABS-KEY) + Abstract Retrieval (META_ABS).

Uso:
    python scripts/collect_scopus.py
    python scripts/collect_scopus.py --family S4
    python scripts/collect_scopus.py --skip-enrichment
    python scripts/collect_scopus.py --force        # ignora páginas e metadata em cache

Execuções interrompidas são retomadas automaticamente na próxima chamada.
Requer SCOPUS_API_KEY (e opcionalmente SCOPUS_INST_TOKEN) no .env.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from _common import ROOT, SEPARATOR, base_parser, setup_logging

from src.collectors.base import format_report
from src.collectors.scopus import ABSTRACT_VIEW, ScopusClient, ScopusCollector
from src.search import load_search_config


def main() -> int:
    parser = base_parser(__doc__)
    parser.add_argument("--skip-enrichment", action="store_true",
                        help="Não executar o Abstract Retrieval.")
    parser.add_argument("--abstract-view", default=ABSTRACT_VIEW,
                        help=f"View do Abstract Retrieval (padrão: {ABSTRACT_VIEW}).")
    args = parser.parse_args()
    setup_logging(args.verbose)

    load_dotenv(ROOT / ".env")
    # SCORPUS_API_KEY: nome antigo aceito temporariamente.
    api_key = os.getenv("SCOPUS_API_KEY") or os.getenv("SCORPUS_API_KEY")
    if not api_key:
        print("Erro: defina SCOPUS_API_KEY no .env", file=sys.stderr)
        return 2

    config = load_search_config(args.config)
    client = ScopusClient(api_key, inst_token=os.getenv("SCOPUS_INST_TOKEN") or None)
    collector = ScopusCollector(
        config,
        config.select(args.family),
        data_dir=args.output_dir,
        client=client,
        force=args.force,
        enrich=not args.skip_enrichment,
        abstract_view=args.abstract_view,
    )
    manifest = collector.run()

    print()
    print(SEPARATOR)
    print(format_report("SCOPUS", config, manifest))
    print(SEPARATOR)

    problems = [f"{fid}: {info['error']}" for fid, info in manifest["families"].items()
                if info["status"] != "complete"]
    if manifest["enrichment"].get("status") == "incomplete":
        problems.append(f"Abstract Retrieval: {manifest['enrichment']['error']}")
    if problems:
        print("\nATENÇÃO — coleta incompleta:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
