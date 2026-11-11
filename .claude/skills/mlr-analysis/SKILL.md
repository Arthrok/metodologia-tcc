---
name: mlr-analysis
description: Análise assistida do dataset curado da revisão (passo 9) — padrões, lacunas temáticas e cobertura em relação a QP1–QP3 e às etapas S1–S8. Use sobre o pacote gerado por `scripts/review_loop.py analyze`.
---

# Análise assistida (passo 9)

Entrada: `data/review/analysis/packet_rNNN.json`, com a cobertura determinística e as fontes validadas
(título, resumo, etapas, dimensões e justificativa humana).

Produza `data/review/analysis/notes_rNNN.md` com:
1. **Padrões:** práticas e desafios recorrentes por etapa (S1–S8), sempre citando os `paper_id`.
2. **Lacunas:** etapas ou dimensões com pouca evidência (use `coverage.gaps`) e temas esperados
   pela PICOC que não aparecem.
3. **Cobertura das QPs:** o que já sustenta QP1 e QP2; para QP3, note que por enquanto só há
   literatura acadêmica.
4. **Direções para as próximas rodadas:** que tipo de fonte buscar (insumo para snowballing e
   refinamento das strings).

Baseie-se somente em títulos e resumos das validadas e sinalize quando uma afirmação exigir o
texto completo. Não classifique práticas como transferidas/adaptadas/novas nesta etapa: isso é
feito na extração, sobre o texto completo. O documento é um apoio para os pesquisadores, não um
resultado final.
