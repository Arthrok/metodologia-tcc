"""Montagem da shortlist de cada rodada.

Ordem: sugestão da pré-triagem (include > ambiguous > exclude), prioridade
(alta > media > baixa) e similaridade textual com as fontes já validadas
(relevance feedback). A IA re-ranqueia a shortlist e escolhe os candidatos
da rodada; esta ordenação só reduz o volume apresentado a ela.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from src.utils.text import normalize_text

_TOKEN = re.compile(r"[a-z][a-z0-9-]{2,}")
_STOPWORDS = set("""
the and for with this that from are was were been has have had not but can our its
their these those into over under using used use based via than such also which while
where when what how who whom whose will would should could may might must more most
other some any each both all into onto about between within without across through
paper propose proposed present presents study approach method methods results show
shows new novel however further large language model models llm llms retrieval
augmented generation rag system systems data""".split())

SUGGESTION_ORDER = {"include": 0, "ambiguous": 1, "exclude": 2, None: 3}
PRIORITY_ORDER = {"alta": 0, "media": 1, "baixa": 2, None: 3}


def tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(normalize_text(text)) if t not in _STOPWORDS]


def record_text(record: dict) -> str:
    return f"{record.get('title') or ''} {record.get('abstract') or ''}"


class TfidfIndex:
    def __init__(self, documents: dict[str, str]):
        tokenized = {pid: tokens(text) for pid, text in documents.items()}
        df = Counter(t for toks in tokenized.values() for t in set(toks))
        n = max(len(tokenized), 1)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        self.vectors = {pid: self._vector(toks) for pid, toks in tokenized.items()}

    def _vector(self, toks: list[str]) -> dict[str, float]:
        tf = Counter(toks)
        vec = {t: c * self.idf.get(t, 0.0) for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    @staticmethod
    def cosine(a: dict[str, float], b: dict[str, float]) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(v * b.get(t, 0.0) for t, v in a.items())

    def max_similarity(self, pid: str, references: list[str]) -> float:
        vec = self.vectors.get(pid, {})
        return max((self.cosine(vec, self.vectors[r]) for r in references if r in self.vectors),
                   default=0.0)


def build_shortlist(
    pool: dict[str, dict],
    pretriage: dict[str, dict],
    reviewed: set[str],
    validated: list[str],
    size: int,
) -> list[dict]:
    """Candidatos ainda não revisados e já pré-triados, ordenados para a IA."""
    candidates = [pid for pid in pool if pid not in reviewed and pid in pretriage]
    index = TfidfIndex({pid: record_text(pool[pid]) for pid in set(candidates) | set(validated)})
    scored = []
    for pid in candidates:
        pt = pretriage[pid]
        sim = index.max_similarity(pid, validated) if validated else 0.0
        scored.append({
            "paper_id": pid,
            "suggestion": pt["suggestion"],
            "priority": pt["priority"],
            "similarity_to_validated": round(sim, 4),
        })
    scored.sort(key=lambda c: (SUGGESTION_ORDER.get(c["suggestion"], 3),
                               PRIORITY_ORDER.get(c["priority"], 3),
                               -c["similarity_to_validated"], c["paper_id"]))
    for position, c in enumerate(scored[:size], 1):
        c["shortlist_position"] = position
    return scored[:size]
