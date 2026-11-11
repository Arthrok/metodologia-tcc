# Análise assistida após a rodada r003

Esta nota sintetiza 27 fontes acadêmicas validadas. As observações se limitam aos títulos, resumos, metadados e justificativas humanas do pacote `packet_r003.json`; afirmações sobre detalhes de implementação, comparação de parâmetros ou resultados além desse material exigem consulta ao texto completo.

## 1. Padrões observados

### Ingestão e preparação de documentos (S2–S4)

Ingestão é a etapa com maior cobertura, com 12 fontes, seguida por preparação, com 10. O conjunto combina parsing, OCR, preservação de estrutura, chunking, enriquecimento semântico e integração de dados heterogêneos. `P-03119b691be0`, `P-b069d8f0e835`, `P-f728b0a66bc2` e `P-5075f7fb2528` comparam ou estruturam o processamento de PDFs; `P-a00af99127ff` transforma dados heterogêneos em representações prontas para IA; `P-75487430ddb8` acrescenta resumos em nível de documento aos chunks.

A rodada r003 reforça a evidência de que o desempenho do RAG depende da qualidade da preparação anterior à indexação. `P-5075f7fb2528` compara conversão, limpeza, splitting e metadados, enquanto `P-d4938f96d8ae` relata ganho de relevância ao substituir divisão fixa por chunking semântico. A extração dos efeitos isolados de cada prática e de suas condições de validade exige o texto completo.

### Armazenamento, indexação e serving (S3–S5)

Armazenamento possui 11 fontes e disponibilização, 8. Os estudos abrangem índices vetoriais e simbólicos, grafos, busca híbrida, reranqueamento, operação distribuída e filtragem por políticas. `P-09dff3480b65` e `P-423200bdcd80` tratam distribuição e estado do índice; `P-e33ade1826ad` acrescenta um banco vetorial voltado a leituras e escritas concorrentes, conectando atualização, contenção, recall e escalabilidade; `P-4fbb491e1d3c` introduz controle anterior ao reranqueamento e geração baseada em pacotes de evidências.

O corpus permite discutir o fluxo desde a preparação até o serving, mas os resumos não bastam para comparar de maneira definitiva custos de atualização, latência, consistência e desempenho entre arquiteturas. Esses dados deverão ser extraídos dos textos completos.

### Qualidade, segurança, rastreabilidade e governança

Qualidade e segurança são as dimensões transversais mais frequentes, com 10 fontes cada. Rastreabilidade aparece em 6 e governança em 4. Qualidade é relacionada a ruído e mudanças (`P-0d46d780075c`), estado e atualidade do índice (`P-423200bdcd80`), preparação documental (`P-5075f7fb2528`) e avaliação em aplicações reais (`P-aee8c0ff3256`).

Na segurança, `P-6cb9d57988e6` rastreia conteúdo envenenado e `P-95747e099ab8` propõe funções-canário para detectar ataques à base. `P-ee5a47f71db6` valida permissões nos serviços IAM das fontes, enquanto `P-4fbb491e1d3c` reúne acesso, auditoria, citações e métricas operacionais. O padrão resultante trata segurança como propriedade do fluxo de dados, abrangendo origem, autorização, integridade, recuperação e evidência apresentada ao usuário.

### Uso, avaliação e feedback (S6)

S6 passou de 3 para 6 fontes. `P-3f5242546ea6` e `P-aee8c0ff3256` trazem evidência de aplicações e avaliação por usuários ou profissionais. `P-32ac448357e4` descreve um ciclo que registra respostas aceitas e rejeitadas para ajustes supervisionados, e `P-019eda761174` relaciona validação, auditoria e qualidade das respostas.

Esse conjunto melhora a cobertura de avaliação e operação. Ainda é necessário verificar nos textos completos quais sinais de feedback efetivamente modificam documentos, metadados, chunks, embeddings, índices ou regras de recuperação. Embora `P-32ac448357e4` seja adjacente à manutenção, sua classificação atual permanece em S6 até que a extração integral confirme mudanças na pipeline de dados.

### Manutenção e descarte (S7–S8)

S7 permanece com apenas duas fontes. `P-0d46d780075c` usa aprendizagem ativa para lidar com ruído e mudanças na base, e `P-423200bdcd80` mede incerteza associada a replicação, divergência e atualização do índice. Não há cobertura suficiente de reindexação incremental, invalidação de embeddings, sincronização com as fontes, detecção de obsolescência ou critérios de reconstrução do índice.

S8 continua sem fonte validada. Não há evidência sobre retenção, expiração, exclusão propagada de documentos e chunks, remoção de embeddings, desativação de fontes, direito ao esquecimento ou auditoria do descarte.

## 2. Lacunas

- **S7 — Manutenção:** 2 fontes, ainda abaixo do mínimo do protocolo. O feedback cresceu em S6, mas falta evidência de sua conversão em atualização controlada da base e dos índices.
- **S8 — Descarte:** nenhuma fonte. É a lacuna mais clara do ciclo de vida.
- **Governança:** aumentou para 4 fontes, principalmente por controle de acesso. Permanecem pouco cobertas retenção, responsabilidades, políticas de atualização e descarte.
- **Avaliação operacional:** há novos estudos com métricas de auditoria, latência, grounding e feedback, mas falta evidência sobre versionamento de datasets, comparação reprodutível entre versões da pipeline e observabilidade contínua.
- **QP3:** todas as 27 fontes validadas são acadêmicas; ainda não é possível comparar literatura acadêmica e cinzenta.

## 3. Cobertura das questões de pesquisa

### QP1 — Práticas de Engenharia de Dados

O conjunto sustenta práticas de seleção e integração de fontes, OCR e parsing, chunking estrutural e semântico, enriquecimento de metadados, embeddings, indexação, busca híbrida, reranqueamento, serving vetorial, feedback, controle de acesso, auditoria, proveniência e detecção de envenenamento. A classificação como práticas transferidas, adaptadas ou novas deve ser feita somente na extração do texto completo.

### QP2 — Desafios ao longo do ciclo de vida

Os resumos registram desafios de heterogeneidade, ruído, perda de estrutura, fragmentação, qualidade de metadados, concorrência entre leitura e escrita, latência, escalabilidade, atualização do índice, autorização, envenenamento, auditoria e incorporação do feedback. A cobertura é ampla entre S1 e S6, porém permanece insuficiente em S7 e inexistente em S8.

### QP3 — Literatura acadêmica versus literatura cinzenta

Ainda não pode ser respondida. As 27 fontes validadas são acadêmicas. A comparação exigirá incorporar literatura cinzenta e aplicar os mesmos códigos de prática, desafio, etapa e dimensão transversal.

## 4. Direções para a rodada r004

1. Priorizar S8 com termos e fontes relacionados a retenção, expiração, exclusão, remoção de embeddings, propagação de deleções, desativação de fontes e direito ao esquecimento em RAG.
2. Em S7, buscar atualização incremental, reindexação, sincronização, invalidação de embeddings, detecção de documentos obsoletos, deriva do corpus e reconstrução de índices.
3. Favorecer estudos em que feedback ou métricas operacionais alterem concretamente a pipeline de dados, com versionamento e comparação entre estados.
4. Buscar observabilidade de dados e índices, incluindo freshness, lineage, qualidade contínua, métricas por versão e auditoria de mudanças.
5. Manter o foco principal em pipelines textuais. Usar multimodalidade apenas quando trouxer uma prática indispensável ainda não coberta.
6. Evitar ampliar o escopo para soberania de dados ou repetir comparações genéricas de chunking sem contribuição nova para manutenção, avaliação ou governança.
7. No snowballing, priorizar `P-0d46d780075c`, `P-423200bdcd80`, `P-32ac448357e4`, `P-4fbb491e1d3c`, `P-e33ade1826ad` e `P-95747e099ab8` como sementes temáticas, sem excluir as demais fontes validadas do procedimento formal.
