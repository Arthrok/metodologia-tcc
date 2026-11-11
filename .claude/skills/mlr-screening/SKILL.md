---
name: mlr-screening
description: Pré-triagem de registros acadêmicos (título, resumo, metadados) da revisão multivocal sobre engenharia de dados em RAG. Use nos lotes gerados por `scripts/review_loop.py pretriage-batches` (data/review/pretriage/batches/*.input.jsonl). Produz sugestão + prioridade por registro; não decide inclusão.
---

# Pré-triagem (passo 5)

A IA **sugere e prioriza**; toda inclusão/exclusão é decidida pelos pesquisadores
nas rodadas de dez candidatos. Registros não apresentados continuam não revisados.

## Entrada
1. `data/review/review_protocol.yaml`: QP1–QP3, PICOC, I1–I3, E1–E5, etapas S1–S8, dimensões transversais.
2. Um lote pendente: `data/review/pretriage/batches/batch_NNNN.input.jsonl` (veja `pending` em `data/review/workspace.json`).

## Para cada registro
1. Avalie I1, I2 e I3 separadamente em `assessments` (satisfied: true/false/null).
   - I1 (temporal): `temporal_status` `in_scope` satisfaz. Para `pre_cutoff`, marque
     `foundational_candidate: true` somente se o resumo indicar origem, definição ou consolidação
     de conceitos, arquiteturas ou práticas centrais de RAG.
2. `suggestion`:
   - `include`: I1–I3 sustentados pelo título/resumo e nenhum E2–E5 se aplica.
   - `exclude`: evidência textual suficiente para um critério. Informe **um** `primary_criterion`
     entre E2, E3, E4 e E5. E1 é determinístico e já foi aplicado; E2 só vale para `pre_cutoff`
     sem indício fundacional.
   - `ambiguous`: resumo ausente, critérios em conflito ou necessidade de texto completo.
3. `priority` (`alta`, `media`, `baixa`): quanto o registro tende a contribuir para QP1–QP2
   (práticas/desafios concretos de dados no ciclo de vida). Registros `pre_cutoff` com indício
   fundacional podem ter prioridade alta.
4. `evidence` e `assessments[].evidence`: trechos **copiados literalmente** do título ou do resumo.
   O importador rejeita o lote inteiro se algum trecho não for literal. Não use veículo, citações
   ou reputação como evidência.
5. `lifecycle_stages` (S1–S8) e `transverse_dimensions` (qualidade, governança, rastreabilidade,
   segurança) evidenciados no texto, não apenas a família de busca que recuperou o registro.

## Saída
Escreva `batch_NNNN.output.jsonl` ao lado do input, com uma linha JSON por registro e **todos**
os `paper_id` do lote:

```json
{"paper_id": "P-0123456789ab", "suggestion": "include|exclude|ambiguous",
 "priority": "alta|media|baixa", "primary_criterion": "E3 ou null",
 "foundational_candidate": false,
 "assessments": [{"criterion": "I2", "satisfied": true, "evidence": "trecho literal", "explanation": "razão curta"}],
 "evidence": ["trecho literal"], "justification": "síntese da sugestão",
 "lifecycle_stages": ["S2"], "transverse_dimensions": ["qualidade"],
 "model": "identificador do modelo", "model_version": null,
 "prompt_version": "mlr-screening-v2", "decided_at": "2026-09-24T12:00:00Z"}
```

`primary_criterion` é `null` para `include` e `ambiguous`; `include` exige ao menos uma evidência.
Depois rode `python scripts/review_loop.py import-pretriage` e corrija os lotes que forem rejeitados.
