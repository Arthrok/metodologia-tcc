"""Carregamento das famílias S1–S8 e geração das queries por base."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "search_queries.yaml"


class SearchFamily(BaseModel):
    id: str
    stage: str
    label: str
    terms: list[str] = Field(min_length=1)


class SearchConfig(BaseModel):
    version: int = 1
    domain_terms: list[str] = Field(min_length=1)
    families: dict[str, SearchFamily]

    def family(self, family_id: str) -> SearchFamily:
        try:
            return self.families[family_id]
        except KeyError:
            valid = ", ".join(self.families)
            raise KeyError(f"Família desconhecida: {family_id} (válidas: {valid})") from None

    def fingerprint(self) -> str:
        """Hash do conteúdo das buscas (independe de formatação/comentários do YAML)."""
        payload = {"domain": self.domain_terms,
                   "families": {f.id: f.terms for f in self.families.values()}}
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def select(self, family_ids: list[str] | None) -> list[SearchFamily]:
        if not family_ids:
            return list(self.families.values())
        return [self.family(f.upper()) for f in family_ids]


def load_search_config(path: Path | str = DEFAULT_CONFIG_PATH) -> SearchConfig:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    families = {
        fid: SearchFamily(id=fid, **spec) for fid, spec in raw["families"].items()
    }
    return SearchConfig(
        version=raw.get("version", 1),
        domain_terms=raw["domain"]["terms"],
        families=families,
    )


def format_term(term: str) -> str:
    """Frases (com espaço ou hífen) vão entre aspas; palavras simples não."""
    if " " in term or "-" in term:
        return f'"{term}"'
    return term


def _or_block(terms: list[str]) -> str:
    return "(" + " OR ".join(format_term(t) for t in terms) + ")"


def build_canonical_query(config: SearchConfig, family: SearchFamily) -> str:
    """String booleana conforme a Tabela 2 do TCC."""
    return f"{_or_block(config.domain_terms)} AND {_or_block(family.terms)}"


def build_scopus_query(config: SearchConfig, family: SearchFamily) -> str:
    """Adaptação Scopus: a query canônica aplicada ao campo TITLE-ABS-KEY.

    No Scopus, frases entre aspas duplas são "loose phrases" e aceitam
    wildcard (*), portanto a sintaxe canônica é preservada sem alterações.
    """
    return f"TITLE-ABS-KEY({build_canonical_query(config, family)})"
