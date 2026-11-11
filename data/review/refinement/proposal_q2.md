# Proposta de refinamento q2 após a rodada r003

## Síntese

Propõe-se uma única alteração conservadora na família S5: incluir a frase
`hybrid retrieval`. A estrutura `BLOCO-RAG AND BLOCO-ETAPA`, o bloco de domínio
e as demais famílias permanecem inalterados. A proposta substitui a versão
preparada após a r001, ainda não aprovada, incorporando o desempenho observado
nas três rodadas.

## Inclusão proposta

### S5 — `hybrid retrieval`

O termo vigente `hybrid search` não cobre necessariamente a formulação
`hybrid retrieval`, encontrada literalmente em fontes validadas:

- `P-019eda761174`: “domain-tuned hybrid retrieval (lexical, dense, and
  cross-encoder reranking)”;
- `P-03119b691be0`: “a hybrid neural symbolic retrieval framework”.

A família de expressões também aparece associada à combinação de recuperação
estruturada e vetorial em `P-32ac448357e4` e à arquitetura Hybrid RAG de
`P-4fbb491e1d3c`. A inclusão é aderente à disponibilização e pode ampliar a
sensibilidade da S5 sem introduzir um conceito externo ao domínio RAG.

## Termos mantidos

Não se propõe remoção ou substituição nesta versão. O termo `chunk*` possui 10
inclusões em 11 registros revisados, `knowledge source*` tem 6 em 6, `rerank*`
e `OCR` têm 4 em 4, e `user feedback` tem 2 em 2. Os desempenhos inferiores de
`vector database*` (1 inclusão em 2 revisados) e `vector index*` (2 em 3) ainda
têm amostras pequenas demais para justificar remoção.

## Lacunas sem mudança imediata nas strings

S7 e S8 permanecem abaixo do mínimo de cobertura, mas o pacote ainda não contém
um novo termo literal recorrente que satisfaça o critério metodológico de
inclusão. `freshness` produziu uma inclusão em um único registro revisado, o que
é insuficiente para medir sua precisão de forma estável. Como não há fonte
validada em S8, ampliar essa família agora exigiria sinônimos sem sustentação no
conjunto curado.

As decisões humanas também indicam que soberania de dados e multimodalidade não
devem orientar a expansão das strings: esses temas foram considerados externos
ao foco principal ou apenas complementares.

## Efeito a observar

Após eventual aprovação e coleta q2, comparar com q1:

1. número de registros recuperados exclusivamente por `hybrid retrieval`;
2. proporção de duplicatas com S4 e com `rerank*`;
3. proporção de inclusões entre os novos resultados de S5;
4. ganho de cobertura sem crescimento desproporcional de registros incidentais.

Esta proposta não altera `config/search_queries.yaml`. A aprovação da q2 e seu
registro permanecem uma decisão dos pesquisadores.
