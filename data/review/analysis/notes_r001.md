# Notas de análise assistida — rodada r001

Estas notas apoiam as próximas decisões dos pesquisadores e se baseiam somente
nos títulos, resumos, classificações de etapa/dimensão e justificativas humanas
das dez fontes validadas. Afirmações sobre implementação, reprodutibilidade ou
resultados além do resumo deverão ser confirmadas no texto completo.

## Padrões observados

### S1–S2: fontes e ingestão

- Integração e preparação semântica de fontes heterogêneas aparecem como uma
  preocupação central. `P-05f05d2ab481` combina aquisição corporativa,
  harmonização baseada em ontologias e recuperação; `P-0cd6ed3dd6a5` introduz
  pré-seleção do corpus para reduzir ruído, redundância e custo antes da indexação.
- A estrutura documental influencia a ingestão. `P-1034dcb2f56f` preserva a
  hierarquia de normas e converte tabelas, enquanto `P-03119b691be0` usa parsing
  orientado a esquema e múltiplas visões de PDFs.
- A qualidade da fonte também é tratada como processo contínuo:
  `P-0d46d780075c` seleciona logs para rotulação humana e incorporação à base de
  conhecimento diante de ruído e mudanças do sistema.

### S3–S4: armazenamento e preparação

- Bancos vetoriais são combinados com representações estruturadas.
  `P-03119b691be0` organiza conteúdo em banco relacional e vector store;
  `P-1034dcb2f56f` utiliza ChromaDB sobre objetos documentais estruturados.
- Chunking, embeddings e ranking são tratados como decisões de engenharia com
  efeito mensurável. `P-03e822172085` compara embeddings, RRF, concatenação,
  reranking e estratégias de chunking; `P-03119b691be0` avalia chunking
  multivisão; `P-08641889c341` inclui granularidade dos chunks entre as lições
  operacionais.
- Surgem arquiteturas de armazenamento voltadas a requisitos transversais.
  `P-09dff3480b65` mantém índices sob propriedade local em uma arquitetura
  federada; `P-12ff196f7de4` autentica índices vetoriais com árvores de Merkle e
  assinaturas digitais.

### S5–S6: disponibilização, uso e feedback

- A qualidade da recuperação é ligada diretamente à resposta final.
  `P-03e822172085` avalia Recall@10 em um chatbot implantado e
  `P-1034dcb2f56f` mede precisão e recall de contexto, fidelidade e relevância da
  resposta.
- Validação posterior à geração aparece como mecanismo operacional de qualidade
  e rastreabilidade. `P-019eda761174` normaliza referências legais, verifica
  existência e fidelidade contra fontes oficiais e aciona reescritas, apoiando-se
  em telemetria de produção.
- `P-08641889c341` acrescenta testes de usuários, revisão por especialistas e
  alinhamento a políticas, mas os detalhes do ciclo de feedback precisam ser
  confirmados no texto completo.

### S7–S8: manutenção e descarte

- S7 aparece de forma explícita apenas em `P-0d46d780075c`, por meio de
  aprendizado ativo para manter a base diante de mudanças. O fluxo de atualização
  citado por `P-08641889c341` pode acrescentar evidência, mas isso exige análise
  do texto completo.
- Nenhuma fonte validada cobre S8. Não há evidência, nesta rodada, sobre retenção,
  expiração, remoção de documentos, desindexação ou propagação de exclusões entre
  corpus, chunks, embeddings e caches.

### Dimensões transversais

- **Qualidade:** conecta ruído de OCR e seleção do corpus (`P-0cd6ed3dd6a5`),
  manutenção da base (`P-0d46d780075c`), métricas do pipeline
  (`P-1034dcb2f56f`) e auditoria de referências (`P-019eda761174`).
- **Governança:** aparece em implantação on-premises e políticas de atualização
  e privacidade (`P-08641889c341`) e em residência e propriedade federada dos
  dados (`P-09dff3480b65`).
- **Rastreabilidade:** aparece em grounding e métricas (`P-1034dcb2f56f`), na
  auditoria de referências legais (`P-019eda761174`) e na proveniência
  criptográfica (`P-12ff196f7de4`).
- **Segurança:** inclui privacidade e execução local (`P-08641889c341`),
  isolamento e residência (`P-09dff3480b65`) e defesa contra envenenamento do
  corpus (`P-12ff196f7de4`).

## Lacunas

- A cobertura mínima de três fontes ainda não foi atingida em S6 (duas), S7
  (uma) e S8 (zero). S8 é a lacuna mais clara e não pode ser inferida a partir
  das fontes atuais.
- Todas as dimensões transversais possuem alguma evidência, mas governança tem
  somente duas fontes; faltam estudos sobre catálogo, ownership, políticas de
  acesso, lineage e conformidade ao longo de todo o pipeline.
- As dez fontes são de 2025–2026. Ainda não há fonte de 2024 nem fonte anterior
  incluída como fundacional, o que limita a observação da evolução temporal.
- O conjunto validado contém somente literatura acadêmica. A presença em ACL e
  Scopus representa proveniência de indexação, não literatura cinzenta.
- Os resumos permitem identificar práticas e desafios, mas não sustentam ainda
  avaliação de qualidade metodológica, extração detalhada nem classificação das
  práticas como transferidas, adaptadas ou novas.

## Cobertura das questões de pesquisa

### QP1 — práticas de Engenharia de Dados em RAG

O conjunto já sustenta a identificação preliminar de práticas de integração e
harmonização semântica (`P-05f05d2ab481`), pré-seleção de corpus
(`P-0cd6ed3dd6a5`), parsing e chunking estruturais (`P-03119b691be0`,
`P-1034dcb2f56f`), recuperação híbrida e reranking (`P-03e822172085`),
manutenção ativa da base (`P-0d46d780075c`), distribuição de índices
(`P-09dff3480b65`) e mecanismos de validação, proveniência e segurança
(`P-019eda761174`, `P-12ff196f7de4`). A classificação dessas práticas como
transferidas, adaptadas ou novas deve aguardar a extração dos textos completos.

### QP2 — desafios ao longo do ciclo de vida

Há evidências preliminares de heterogeneidade e dispersão das fontes
(`P-05f05d2ab481`), perda de estrutura documental (`P-03119b691be0`), ruído de
OCR e custo de indexação (`P-0cd6ed3dd6a5`), ruído e mudança contínua
(`P-0d46d780075c`), relevância insuficiente da recuperação
(`P-03e822172085`), normalização e fidelidade de referências
(`P-019eda761174`), centralização, residência e isolamento dos dados
(`P-09dff3480b65`) e envenenamento do corpus (`P-12ff196f7de4`). Faltam
evidências sobre descarte e ainda há pouca cobertura de manutenção e feedback.

### QP3 — literatura acadêmica e literatura cinzenta

QP3 ainda não pode ser respondida. Todas as fontes validadas são acadêmicas;
ACL e Scopus são bases de indexação. Será necessário coletar e selecionar
literatura cinzenta segundo um protocolo explícito antes de comparar
convergências, divergências e lacunas.

## Direções para as próximas rodadas

1. Priorizar candidatos sobre S8: retenção, expiração, remoção de documentos,
   direito ao apagamento, desindexação e propagação de deleções em vector stores.
2. Reforçar S7 com estudos de atualização incremental, detecção de drift,
   versionamento de corpus e embeddings, reindexação e monitoramento de freshness.
3. Ampliar S6 com telemetria, feedback humano, aprendizado a partir do uso e
   mecanismos que transformem feedback em atualização controlada do corpus.
4. Buscar governança aplicada de ponta a ponta: catálogo, ownership, lineage,
   controle de acesso, isolamento entre tenants e auditoria de políticas.
5. Na seleção dos candidatos de snowballing já coletados, priorizar os que
   acrescentem S6–S8 em vez de repetir estudos de chunking e recuperação.
6. Resolver metodologicamente a coleta de literatura cinzenta necessária à QP3
   antes de alterar as strings ou misturar novos tipos de fonte ao corpus acadêmico.
