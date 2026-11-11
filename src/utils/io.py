"""Leitura/escrita de JSON e JSONL (escritas atômicas)."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from pydantic import BaseModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def run_timestamp(dt: datetime | None = None) -> str:
    """Nome de arquivo de manifest: 2026-09-23T200000."""
    return (dt or utc_now()).strftime("%Y-%m-%dT%H%M%S")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_json(path: Path, data: Any) -> None:
    _atomic_write(Path(path), json.dumps(data, ensure_ascii=False, indent=2, default=str) + "\n")


def read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _to_line(item: BaseModel | dict) -> str:
    if isinstance(item, BaseModel):
        return item.model_dump_json()
    return json.dumps(item, ensure_ascii=False, default=str)


def write_jsonl(path: Path, items: Iterable[BaseModel | dict]) -> int:
    lines = [_to_line(i) for i in items]
    _atomic_write(Path(path), "".join(line + "\n" for line in lines))
    return len(lines)


def read_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]
