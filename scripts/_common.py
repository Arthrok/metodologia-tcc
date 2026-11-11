"""Utilidades compartilhadas pelos scripts de coleta."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.collectors.base import DEFAULT_DATA_DIR  # noqa: E402
from src.search.config import DEFAULT_CONFIG_PATH  # noqa: E402

SEPARATOR = "================================="


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--family", action="append", metavar="S#",
        help="Executar apenas esta família (pode repetir). Padrão: S1–S8.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_DATA_DIR,
        help="Diretório base de dados (contém raw/ e manifests/). Padrão: data/",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--force", action="store_true", help="Ignorar cache/estado anterior.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    # Bibliotecas de terceiros ruidosas (urllib3 em DEBUG loga URLs; o
    # acl-anthology emite avisos de TeX-math irrelevantes para a coleta).
    for name in ("urllib3", "git", "acl-anthology"):
        logging.getLogger(name).setLevel(logging.ERROR)
