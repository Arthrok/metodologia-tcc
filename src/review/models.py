"""Contratos auditáveis do loop: pré-triagem (IA), ranking da rodada (IA) e
decisão humana."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator

EXCLUSION_CRITERIA = {"E1", "E2", "E3", "E4", "E5"}
AI_EXCLUSION_CRITERIA = {"E2", "E3", "E4", "E5"}  # E1 é determinístico
STAGES = {f"S{i}" for i in range(1, 9)}
DIMENSIONS = {"qualidade", "governança", "rastreabilidade", "segurança"}


class Suggestion(str, Enum):
    INCLUDE = "include"
    EXCLUDE = "exclude"
    AMBIGUOUS = "ambiguous"


class Priority(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"


class HumanVerdict(str, Enum):
    INCLUDE = "include"
    EXCLUDE = "exclude"
    FULL_TEXT = "full_text"   # necessidade de análise do texto completo


class CriterionAssessment(BaseModel):
    criterion: str
    satisfied: bool | None
    evidence: str | None = None
    explanation: str


class Pretriage(BaseModel):
    """Pré-triagem de um registro pela skill (sugestão, nunca decisão)."""

    paper_id: str
    suggestion: Suggestion
    priority: Priority
    primary_criterion: str | None = None
    foundational_candidate: bool = False
    assessments: list[CriterionAssessment] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    justification: str
    lifecycle_stages: list[str] = Field(default_factory=list)
    transverse_dimensions: list[str] = Field(default_factory=list)
    model: str
    model_version: str | None = None
    prompt_version: str
    decided_at: datetime

    @model_validator(mode="after")
    def _check(self):
        if self.suggestion == Suggestion.EXCLUDE:
            if self.primary_criterion not in AI_EXCLUSION_CRITERIA:
                raise ValueError(f"exclude exige primary_criterion em {sorted(AI_EXCLUSION_CRITERIA)}")
        elif self.primary_criterion is not None:
            raise ValueError("primary_criterion só se aplica a exclude")
        if self.suggestion == Suggestion.INCLUDE and not self.evidence:
            raise ValueError("include exige ao menos uma evidência literal")
        if bad := set(self.lifecycle_stages) - STAGES:
            raise ValueError(f"etapas inválidas: {sorted(bad)}")
        if bad := set(self.transverse_dimensions) - DIMENSIONS:
            raise ValueError(f"dimensões inválidas: {sorted(bad)}")
        return self


class RankedCandidate(BaseModel):
    """Um dos candidatos escolhidos pela IA para a rodada."""

    paper_id: str
    rank: int = Field(ge=1)
    justification: str
    related_validated: list[str] = Field(default_factory=list)


class RoundRanking(BaseModel):
    round_id: str
    candidates: list[RankedCandidate]
    model: str
    model_version: str | None = None
    prompt_version: str
    decided_at: datetime


class HumanDecision(BaseModel):
    paper_id: str
    round_id: str | None = None
    decision: HumanVerdict
    primary_criterion: str | None = None
    foundational: bool = False       # exceção de I1 para registros anteriores ao corte vigente
    reviewer: str
    justification: str
    suggested_terms: list[str] = Field(default_factory=list)
    decided_at: datetime

    @model_validator(mode="after")
    def _check(self):
        if self.decision == HumanVerdict.EXCLUDE:
            if self.primary_criterion not in EXCLUSION_CRITERIA:
                raise ValueError(f"exclude exige primary_criterion em {sorted(EXCLUSION_CRITERIA)}")
        elif self.primary_criterion is not None:
            raise ValueError("primary_criterion só se aplica a exclude")
        if self.foundational and self.decision != HumanVerdict.INCLUDE:
            raise ValueError("foundational só se aplica a include")
        if not self.justification.strip():
            raise ValueError("justificativa obrigatória")
        return self
