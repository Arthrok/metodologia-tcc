"""Infraestrutura comum aos coletores."""

from __future__ import annotations

import logging
from pathlib import Path

from src.models import PaperRecord
from src.search import SearchConfig, SearchFamily
from src.search.config import PROJECT_ROOT
from src.utils.io import run_timestamp, utc_now, write_json

DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


def raw_version_dir(data_dir: Path, source: str, query_version: int) -> Path:
    """Resultados brutos de uma versão das strings: data/raw/<base>/q<versão>/."""
    return Path(data_dir) / "raw" / source / f"q{query_version}"


class BaseCollector:
    source: str = ""

    def __init__(
        self,
        config: SearchConfig,
        families: list[SearchFamily] | None = None,
        data_dir: Path | str = DEFAULT_DATA_DIR,
    ):
        self.config = config
        self.families = families if families is not None else list(config.families.values())
        self.data_dir = Path(data_dir)
        self.started_at = utc_now()
        self.log = logging.getLogger(self.source)

    @property
    def source_dir(self) -> Path:
        return self.data_dir / "raw" / self.source

    @property
    def raw_dir(self) -> Path:
        return raw_version_dir(self.data_dir, self.source, self.config.version)

    def query_info(self) -> dict:
        return {"query_version": self.config.version,
                "query_fingerprint": self.config.fingerprint()}

    @property
    def manifest_dir(self) -> Path:
        return self.data_dir / "manifests" / self.source

    def write_manifest(self, manifest: dict) -> Path:
        path = self.manifest_dir / f"{run_timestamp(self.started_at)}.json"
        write_json(path, manifest)
        self.log.info("Manifest: %s", path)
        return path


def family_counts(records: list[PaperRecord], families: list[SearchFamily]) -> dict[str, int]:
    return {
        f.id: sum(1 for r in records if f.id in r.search_families) for f in families
    }


def format_report(title: str, config: SearchConfig, manifest: dict) -> str:
    """Bloco do relatório final (seção 36 do plano) a partir de um manifest."""
    lines = [title, ""]
    families = manifest.get("families", {})
    for fid, family in config.families.items():
        info = families.get(fid)
        if info is None:
            count = "—"
        else:
            count = f"{info.get('total_results', 0):03d}"
            if info.get("status") not in (None, "complete"):
                count += f"  [{info['status'].upper()}]"
        lines.append(f"{fid} {family.label:<20}{count}")
    lines += [
        "",
        f"Total de ocorrências: {manifest.get('total_occurrences', 0):03d}",
        f"Papers únicos: {manifest.get('unique_papers', 0):03d}",
    ]
    return "\n".join(lines)
