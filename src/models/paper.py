"""Modelo comum de artigo entregue por todos os coletores."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, computed_field


class SearchProvenance(BaseModel):
    """Uma ocorrência: o artigo foi recuperado por (base, família)."""

    source: str
    family: str
    stage: str

    canonical_query: str
    executed_query: str

    searched_fields: list[str]
    matched_terms: list[str] | None = None
    # Snowballing: paper validado a partir do qual este registro foi encontrado.
    seed: str | None = None

    retrieved_at: datetime


class PaperRecord(BaseModel):
    source: str
    source_id: str

    title: str
    abstract: str | None = None

    doi: str | None = None
    authors: list[str] = Field(default_factory=list)

    year: int | None = None
    publication_date: str | None = None

    venue: str | None = None
    document_type: str | None = None
    keywords: list[str] = Field(default_factory=list)

    url: str | None = None
    pdf_url: str | None = None

    search_families: list[str] = Field(default_factory=list)
    provenance: list[SearchProvenance] = Field(default_factory=list)

    retrieved_at: datetime

    # Campos específicos da base que não pertencem ao modelo comum.
    extra: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def id(self) -> str:
        return f"{self.source}:{self.source_id}"

    @computed_field
    @property
    def abstract_available(self) -> bool:
        return bool(self.abstract and self.abstract.strip())

    def add_occurrence(self, provenance: SearchProvenance) -> None:
        if provenance.family not in self.search_families:
            self.search_families.append(provenance.family)
            self.search_families.sort()
        self.provenance.append(provenance)
