"""Normalização textual usada antes do matching local."""

from __future__ import annotations

import re
import unicodedata

# Hífens/traços Unicode que devem ser tratados como "-" (normalização trivial).
_DASHES = re.compile(r"[‐‑‒–—−­]")
_SPACES = re.compile(r"\s+")


def normalize_text(text: str | None) -> str:
    """Unicode NFKC → traços unificados → lowercase → espaços colapsados.

    Não aplica stemming nem lematização, e mantém a pontuação.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = _DASHES.sub("-", text)
    text = text.lower()
    return _SPACES.sub(" ", text).strip()
