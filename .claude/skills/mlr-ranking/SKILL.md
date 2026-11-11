---
name: mlr-ranking
description: Re-ranqueia a shortlist de uma rodada da revisão e escolhe exatamente os dez candidatos de maior aderência para revisão humana, considerando as fontes já validadas. Use após `scripts/review_loop.py round-new`.
---

# Ranking da rodada (passos 5–6)

## Entrada (`data/review/rounds/rNNN/`)
- `shortlist.jsonl`: candidatos não revisados, com registro, pré-triagem e similaridade às validadas.
- `validated_references.jsonl`: fontes já incluídas pelos pesquisadores (pode estar vazio na primeira rodada).
- `data/review/review_protocol.yaml`: QP, PICOC e critérios.
- `candidates_expected` da rodada em `data/review/workspace.json`, normalmente 10.

## Como escolher
1. Priorize aderência a QP1–QP2 e I2–I3: práticas, desafios e decisões técnicas de dados concretos
   em sistemas RAG.
2. Use as fontes validadas como referência do que os pesquisadores consideram relevante. Prefira
   candidatos que ampliem a cobertura (etapas S1–S8 ou dimensões pouco representadas) em vez de
   repetir o mesmo tema.
3. Registros `pre_cutoff` só entram se houver indício fundacional.
4. Não descarte ninguém: quem não for escolhido continua não revisado para rodadas futuras.

## Saída
Escreva `data/review/rounds/rNNN/ranking.input.json`:

```json
{"round_id": "r001",
 "candidates": [{"paper_id": "P-...", "rank": 1,
                 "justification": "por que está entre os 10 (aderência e evidência do resumo)",
                 "related_validated": ["P-... validada relacionada"]}],
 "model": "identificador do modelo", "model_version": null,
 "prompt_version": "mlr-ranking-v1", "decided_at": "2026-09-24T12:00:00Z"}
```

Exatamente `candidates_expected` itens, ranks 1..N sem repetição e somente `paper_id` da shortlist.
Depois rode `python scripts/review_loop.py round-rank rNNN data/review/rounds/rNNN/ranking.input.json`.
Os pesquisadores preenchem `rounds/rNNN/review.csv`.
