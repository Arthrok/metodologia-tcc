"""Relatório final da coleta acadêmica a partir dos manifests mais recentes.

Uso:
    python scripts/report.py
    python scripts/report.py --output-dir data
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import SEPARATOR

from src.collectors.base import DEFAULT_DATA_DIR, format_report
from src.search import load_search_config
from src.search.config import DEFAULT_CONFIG_PATH
from src.utils.io import read_json

SOURCES = [("scopus", "SCOPUS"), ("acl", "ACL ANTHOLOGY")]


def latest_manifest(data_dir: Path, source: str) -> Path | None:
    manifests = sorted((data_dir / "manifests" / source).glob("*.json"))
    return manifests[-1] if manifests else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args()
    config = load_search_config(args.config)

    print(SEPARATOR)
    print("ACADEMIC COLLECTION")
    print(SEPARATOR)
    for source, title in SOURCES:
        print()
        path = latest_manifest(args.output_dir, source)
        if path is None:
            print(f"{title}\n\n(sem manifest)")
            continue
        manifest = read_json(path)
        print(format_report(title, config, manifest))
        print(f"Manifest: {path}")
        print()
    print(SEPARATOR)


if __name__ == "__main__":
    main()
