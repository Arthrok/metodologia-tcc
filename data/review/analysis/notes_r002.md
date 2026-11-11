# Análise assistida após a rodada r002

Esta nota sintetiza 19 fontes acadêmicas validadas. As observações se limitam aos títulos, resumos, metadados e justificativas humanas do pacote `packet_r002.json`; afirmações sobre implementação detalhada ou resultados além desse material exigem consulta ao texto completo.

## 1. Padrões observados

### Ingestão e preparação de documentos (S2–S4)

O padrão mais recorrente é a transformação de documentos heterogêneos em unidades adequadas à recuperação. Há práticas de parsing, OCR, chunking estrutural, preservação de tabelas e enriquecimento semântico em `P-1034dcb2f56f`, `P-03119b691be0`, `P-0cd6ed3dd6a5`, `P-a00af99127ff`, `P-b069d8f0e835` e `P-f728b0a66bc2`. `P-75487430ddb8` acrescenta enriquecimento dos chunks com resumos no nível do documento, enquanto `P-aad39554e020` trata a construção do contexto como uma etapa automatizada que combina normalização multimodal, estrutura documental e seleção de evidências.

Os desafios recorrentes são perda de hierarquia e relações entre páginas, ruído de OCR, formatos multimodais, fragmentação do contexto e recuperação de trechos pertencentes ao documento errado. A cobertura já permite discutir decisões concretas de preparação e seus efeitos sobre a qualidade da recuperação, mas a comparação entre alternativas ainda depende da leitura integral dos estudos experimentais.

### Armazenamento, indexação e disponibilização (S3–S5)

Os estudos combinam índices vetoriais, estruturas simbólicas ou em grafo, busca híbrida, reranqueamento e filtragem anterior à recuperação. `P-03119b691be0` e `P-f728b0a66bc2` preservam estrutura por representações neurais e simbólicas; `P-03e822172085` e `P-aad39554e020` conectam preparação do contexto e disponibilização; `P-2a7e331ac123` integra recuperação semântica e consultas estruturadas com controle de acesso; `P-09dff3480b65` e `P-423200bdcd80` acrescentam operação distribuída, residência dos dados e estado do índice.

As decisões técnicas aparecem ligadas a trade-offs entre precisão, cobertura, latência, isolamento e confiabilidade. Os resumos sustentam a existência desses trade-offs, mas a extração dos parâmetros, custos e condições de validade requer o texto completo.

### Qualidade, confiança e rastreabilidade

Qualidade é a dimensão transversal mais frequente, com sete fontes. `P-0d46d780075c` trata ruído e mudanças na base, `P-423200bdcd80` relaciona freshness, atraso de replicação e divergência entre shards à confiança do índice, e `P-019eda761174` combina validação, auditoria e redução de alucinações. `P-1034dcb2f56f`, `P-a00af99127ff` e `P-3f5242546ea6` acrescentam avaliação de recuperação, preservação estrutural e feedback de usuários.

A rastreabilidade aparece em cinco fontes. `P-12ff196f7de4` aborda proveniência verificável, `P-6cb9d57988e6` rastreia textos responsáveis por envenenamento e `P-2a7e331ac123` registra operações e confiabilidade das fontes. Isso permite relacionar qualidade do dado, origem da evidência e confiança na resposta.

### Segurança e governança

Segurança possui cinco fontes e governança três. Os mecanismos incluem isolamento e residência dos dados (`P-09dff3480b65`), controle de acesso e auditoria (`P-2a7e331ac123`), proveniência criptográfica (`P-12ff196f7de4`), prevenção do uso de conteúdo comprometido (`P-08641889c341`) e investigação de envenenamento da base (`P-6cb9d57988e6`).

O conjunto já mostra que segurança não se limita ao modelo: envolve seleção da fonte, armazenamento, autorização, integridade do corpus e rastreamento do dado recuperado. Ainda há pouca evidência sobre políticas de retenção, responsabilidades organizacionais e aplicação contínua dessas políticas ao longo do ciclo de vida.

### Uso, feedback e manutenção (S6–S7)

Uso e feedback possuem três fontes. `P-3f5242546ea6` é a evidência mais direta por envolver avaliação com usuários e lições de aplicações reais; `P-1034dcb2f56f` e `P-019eda761174` complementam com avaliação operacional, qualidade e rastreabilidade. A cobertura ainda é pequena para práticas de incorporação sistemática do feedback em mudanças no corpus, índices ou regras de recuperação.

Manutenção possui apenas duas fontes. `P-0d46d780075c` aborda ruído e mudanças no sistema, enquanto `P-423200bdcd80` mede atraso de replicação, divergência entre shards e perda de atualidade. Ainda faltam estudos sobre reindexação incremental, invalidação de embeddings, detecção de documentos obsoletos, atualização de metadados e critérios para reconstrução do índice.

## 2. Lacunas

- **S7 — Manutenção:** 2 fontes, abaixo do mínimo de cobertura definido pelo protocolo. A evidência está concentrada em observabilidade e estado do índice.
- **S8 — Descarte:** nenhuma fonte. Não há evidência validada sobre exclusão de documentos e chunks, expiração, retenção, direito ao esquecimento, remoção propagada em índices vetoriais, desativação de fontes ou auditoria do descarte.
- **Governança:** embora exista evidência, são apenas 3 fontes e o foco atual está mais em controle técnico do que em políticas, papéis e responsabilização.
- **Feedback fechado:** há avaliação de usuários, mas pouca evidência sobre como o feedback altera dados, metadados, chunks, embeddings ou políticas de recuperação.
- **QP3:** o conjunto contém somente literatura acadêmica; ainda não é possível comparar convergências e divergências com literatura cinzenta.

## 3. Cobertura das questões de pesquisa

### QP1 — Práticas de Engenharia de Dados

O conjunto sustenta práticas de seleção e curadoria de fontes, OCR e parsing, chunking, enriquecimento semântico, criação de embeddings, indexação vetorial e simbólica, busca híbrida, reranqueamento, filtragem por metadados, controle de acesso, auditoria, proveniência e monitoramento de freshness. A classificação dessas práticas como transferidas, adaptadas ou novas deve permanecer para a etapa de extração sobre o texto completo.

### QP2 — Desafios ao longo do ciclo de vida

Os resumos registram desafios de heterogeneidade documental, ruído, perda de estrutura, fragmentação do contexto, recuperação do documento errado, latência, escalabilidade, atualização do índice, residência dos dados, autorização, envenenamento e rastreabilidade. S7 ainda tem evidência limitada e S8 permanece sem evidência.

### QP3 — Literatura acadêmica versus literatura cinzenta

Ainda não pode ser respondida. As 19 fontes validadas são acadêmicas. A comparação exige a futura incorporação e extração da literatura cinzenta com os mesmos códigos de práticas, desafios, etapas e dimensões transversais.

## 4. Direções para a rodada r003

1. Priorizar candidatos diretamente relacionados a S8: retenção, exclusão, expiração, remoção de embeddings, direito ao esquecimento e desativação de fontes.
2. Em S7, buscar reindexação incremental, detecção de obsolescência, sincronização de fontes, atualização de embeddings e monitoramento de deriva do corpus.
3. Em S6, favorecer estudos em que feedback humano ou métricas operacionais alterem efetivamente a pipeline de dados.
4. Ampliar governança com políticas de acesso, retenção, proveniência, auditoria e responsabilidades organizacionais.
5. Evitar repetir estudos genéricos de chunking ou RAG jurídico, salvo quando apresentarem uma prática ou comparação ainda não coberta.
6. Usar no snowballing as fontes de manutenção, observabilidade, proveniência e envenenamento como sementes prioritárias, sem excluir as demais fontes incluídas da rodada.
