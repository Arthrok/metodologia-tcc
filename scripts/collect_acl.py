"""Coleta S1–S8 no ACL Anthology (matching local sobre title + abstract).

Uso:
    python scripts/collect_acl.py
    python scripts/collect_acl.py --family S4
    python scripts/collect_acl.py --no-update      # não faz git pull do repositório
"""

from __future__ import annotations

from pathlib import Path

from _common import SEPARATOR, base_parser, setup_logging

from src.collectors.acl import ACLCollector
from src.collectors.base import format_report
from src.search import load_search_config


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument(
        "--repo-path", type=Path, default=None,
        help="Clone local do acl-org/acl-anthology (padrão: diretório de dados do usuário).",
    )
    parser.add_argument(
        "--no-update", action="store_true",
        help="Usar o snapshot local sem atualizar o repositório.",
    )
    args = parser.parse_args()
    setup_logging(args.verbose)

    # A coleta ACL é local e sempre sobrescreve os resultados; --force não
    # altera o comportamento.
    config = load_search_config(args.config)
    collector = ACLCollector(
        config,
        config.select(args.family),
        data_dir=args.output_dir,
        repo_path=args.repo_path,
        update=not args.no_update,
    )
    manifest = collector.run()

    print()
    print(SEPARATOR)
    print(format_report("ACL ANTHOLOGY", config, manifest))
    print(SEPARATOR)


if __name__ == "__main__":
    main()
