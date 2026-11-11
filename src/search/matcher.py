"""Matcher local das famílias S1–S8 (usado no ACL Anthology).

As buscas têm sempre a forma

    (DOMÍNIO_1 OR DOMÍNIO_2) AND (TERMO_1 OR TERMO_2 OR ...)

então não há parser booleano: cada termo vira uma regex e o AND entre os
blocos é feito explicitamente.

Regras:
- frases são sequências de palavras contíguas (tolerando apenas variação de
  espaços), nunca "palavra AND palavra em qualquer posição";
- "*" no fim de uma palavra é prefix matching (``chunk*`` → chunk, chunking);
- sem "*", o termo precisa terminar em limite de palavra (``OCR`` não casa
  ``ocrs``);
- o texto e os termos passam pela mesma normalização (``normalize_text``).
"""

from __future__ import annotations

import re
from functools import lru_cache

from src.search.config import SearchConfig, SearchFamily
from src.utils.text import normalize_text


@lru_cache(maxsize=None)
def compile_term(term: str) -> re.Pattern[str]:
    words = normalize_text(term).split(" ")
    parts = []
    for word in words:
        if word.endswith("*"):
            parts.append(re.escape(word[:-1]) + r"\w*")
        else:
            parts.append(re.escape(word))
    pattern = r"(?<!\w)" + r"\s+".join(parts)
    if not words[-1].endswith("*"):
        pattern += r"(?!\w)"
    return re.compile(pattern)


def matches_term(normalized_text: str, term: str) -> bool:
    return compile_term(term).search(normalized_text) is not None


def matches_any(normalized_text: str, terms: list[str]) -> bool:
    return any(matches_term(normalized_text, t) for t in terms)


def matched_terms(normalized_text: str, terms: list[str]) -> list[str]:
    return [t for t in terms if matches_term(normalized_text, t)]


class FamilyMatcher:
    """Aplica o bloco de domínio uma vez e depois cada família."""

    def __init__(self, config: SearchConfig, families: list[SearchFamily] | None = None):
        self.config = config
        self.families = families if families is not None else list(config.families.values())

    def matches_domain(self, normalized_text: str) -> bool:
        return matches_any(normalized_text, self.config.domain_terms)

    def matches_family(self, normalized_text: str, family: SearchFamily) -> bool:
        return self.matches_domain(normalized_text) and matches_any(
            normalized_text, family.terms
        )

    def match(self, text: str) -> dict[str, list[str]]:
        """Retorna {família: termos casados} para as famílias satisfeitas."""
        normalized = normalize_text(text)
        if not self.matches_domain(normalized):
            return {}
        return self.match_families(normalized)

    def match_families(self, normalized_text: str) -> dict[str, list[str]]:
        """Só o segundo bloco; o chamador já verificou o domínio."""
        result = {}
        for family in self.families:
            hits = matched_terms(normalized_text, family.terms)
            if hits:
                result[family.id] = hits
        return result
