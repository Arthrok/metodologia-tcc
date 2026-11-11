---
name: mlr-refinement
description: Sugere ajustes nas strings de busca S1–S8 (inclusão, remoção ou substituição de termos) a partir das fontes validadas e do desempenho observado dos termos (passo 11). Use sobre o pacote de `scripts/review_loop.py refine`; os pesquisadores aprovam antes de qualquer uso.
---

# Refinamento das strings (passo 11)

Entrada: `data/review/refinement/packet_q<N>_rNNN.json`, com as strings vigentes, as validadas,
exemplos excluídos, os termos sugeridos pelos revisores e `term_performance` (precisão observada
de cada termo entre os registros revisados).

Produza `data/review/refinement/proposal_q<N+1>.md` e um rascunho `proposal_q<N+1>.yaml` no formato
de `config/search_queries.yaml`, com `version: N+1`.

Regras:
1. Preserve a estrutura `BLOCO-RAG AND BLOCO-ETAPA` e as oito famílias.
2. Cada alteração precisa de uma justificativa rastreável:
   - **inclusão:** termo recorrente nas validadas (cite `paper_id` e o trecho literal) ausente das strings;
   - **remoção/substituição:** termo com baixa precisão observada e volume suficiente (cite os números
     de `term_performance`), ou ambíguo (ex.: "retention" no sentido de memória do modelo).
3. Seja conservador: poucos termos por versão, para que o efeito de cada mudança seja mensurável.
4. Não altere `config/search_queries.yaml`. Os pesquisadores revisam a proposta, editam o arquivo
   oficial, rodam as coletas da nova versão e registram com
   `python scripts/review_loop.py register-queries --reviewer ... --justification ...`.
