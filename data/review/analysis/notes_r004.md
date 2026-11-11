# Análise assistida após a rodada r004

Esta nota sintetiza 36 fontes acadêmicas validadas. As observações se limitam aos títulos, resumos, metadados e justificativas humanas do pacote `packet_r004.json`; afirmações sobre implementação, parâmetros, causalidade ou resultados não descritos nesse material exigem consulta ao texto completo.

## 1. Padrões observados

### Fontes, ingestão e preparação (S1–S4)

O corpus reúne 10 fontes em S1, 13 em S2 e 11 em S4. As práticas recorrentes incluem integração de fontes heterogêneas, seleção e limpeza do corpus, parsing de PDFs e tabelas, preservação de layout, chunking estrutural ou semântico e enriquecimento com metadados. `P-05f05d2ab481` e `P-a00af99127ff` tratam da harmonização de dados empresariais heterogêneos; `P-03119b691be0`, `P-f728b0a66bc2`, `P-b069d8f0e835` e `P-5075f7fb2528` exploram diferentes formas de estruturar documentos complexos; `P-0cd6ed3dd6a5` aborda ruído, redundância e pré-seleção do corpus.

Os estudos indicam que decisões anteriores à indexação condicionam a recuperação. `P-d4938f96d8ae` associa chunking semântico à relevância das respostas; `P-75487430ddb8` enriquece chunks com contexto em nível de documento; e `P-f742a6093683` relaciona integridade semântica, atualidade e consistência dos dados a ações de otimização. A contribuição isolada de cada transformação deverá ser confirmada na extração dos textos completos.

### Armazenamento, indexação e disponibilização (S3–S5)

S3 é a etapa mais coberta, com 18 fontes, e S5 reúne 14. A rodada acrescentou evidência operacional sobre persistência, atualizações contínuas, concorrência entre leitura e escrita, filtragem por metadados, busca híbrida, reinicialização e escalabilidade. `P-79b99916d8ad` considera inserções e exclusões contínuas sob restrição de memória; `P-6108a118d511` avalia churn, filtros e recuperação após reinício; `P-dafca2ca704a` usa buffer e consolidação em segundo plano para reduzir WAL e atraso de replicação; e `P-2c31a6a44ef9` combina persistência distribuída, atualizações em tempo real e busca híbrida.

`P-2c1db6e3e1be` introduz construção progressiva do índice conforme a carga de consultas, enquanto `P-e33ade1826ad` discute atualização de índices em um serviço vetorial distribuído. Em conjunto, essas fontes aproximam o TCC das condições de produção, mas a comparação de custos, consistência, desempenho e aplicabilidade depende da leitura integral.

### Qualidade, segurança, governança e rastreabilidade

Qualidade aparece em 12 fontes, segurança em 13, governança em 7 e rastreabilidade em 7. Qualidade é tratada desde a preparação documental (`P-5075f7fb2528`) até a avaliação guiada por falhas reais (`P-f742a6093683`) e a observação do estado do índice (`P-423200bdcd80`). `P-0d46d780075c` acrescenta seleção ativa de novos exemplos para reagir a ruído e mudanças.

Na segurança e governança, o padrão recorrente é aplicar políticas antes ou durante a recuperação. `P-ee5a47f71db6`, `P-2a7e331ac123` e `P-43a81bdd7933` filtram o acesso conforme identidade ou papel; `P-578a6ed00cea` combina recuperação federada, políticas e exposição das fontes; `P-6cb9d57988e6`, `P-95747e099ab8` e `P-12ff196f7de4` tratam da detecção, rastreamento ou prevenção de conteúdo envenenado. As dimensões transversais, portanto, aparecem como propriedades do fluxo de dados, não apenas da resposta final.

### Uso, avaliação e feedback (S6)

S6 reúne 7 fontes. `P-3f5242546ea6` e `P-aee8c0ff3256` trazem avaliação em aplicações ou com profissionais; `P-32ac448357e4` registra respostas aceitas e rejeitadas; `P-019eda761174` audita referências antes da entrega; e `P-f742a6093683` converte resultados de avaliação em ações de melhoria sobre dados, recuperação e geração.

O conjunto sustenta avaliação e feedback como parte da operação, mas os resumos ainda não demonstram de forma suficiente como esses sinais são versionados e propagados para documentos, chunks, embeddings e índices. Essa relação exige verificação no texto completo.

### Manutenção e descarte (S7–S8)

S7 permanece com apenas 2 fontes. `P-0d46d780075c` reage a ruído e mudanças por aprendizagem ativa, e `P-423200bdcd80` monitora atraso de replicação, divergência entre shards e perda de atualidade. Há estudos adjacentes sobre atualização de índices em S3 e S5, mas a classificação como manutenção depende de evidência explícita sobre sincronização, versionamento, reindexação, invalidação ou reconstrução.

S8 passou de nenhuma evidência para 2 fontes. `P-db3d0d4c1caa` descreve exclusão automatizada em solicitações DSAR, mascaramento e auditoria imutável; `P-79b99916d8ad` oferece suporte contínuo a exclusões em um mecanismo vetorial atualizável. A cobertura ainda não permite explicar todo o descarte, especialmente propagação da exclusão para chunks, embeddings, caches, réplicas e logs, verificação da remoção e aplicação de políticas de retenção.

## 2. Lacunas

- **S7 — Manutenção:** 2 fontes, abaixo do mínimo do protocolo. Faltam evidências diretas sobre sincronização com sistemas de origem, atualização incremental, invalidação de embeddings, detecção de obsolescência, versionamento e critérios de reconstrução.
- **S8 — Descarte:** 2 fontes, também abaixo do mínimo. A rodada introduziu DSAR e exclusão vetorial, mas permanecem pouco cobertas retenção, expiração, propagação da exclusão entre artefatos derivados, desativação de fontes e auditoria da remoção.
- **Operação contínua:** há métricas de atualidade, latência, recall, churn e WAL, porém ainda são escassos os trabalhos que conectam esses sinais a decisões automatizadas e versionadas sobre a pipeline.
- **Governança do ciclo completo:** controle de acesso tem boa presença relativa, mas responsabilidades, políticas de atualização e descarte e rastreabilidade entre versões continuam menos desenvolvidas.
- **Distribuição temporal:** 22 das 36 fontes são de 2026, 13 de 2025 e apenas 1 de 2024. O recorte recente foi respeitado, mas a concentração pode refletir a novidade do tema e deverá ser considerada na síntese.
- **QP3:** as 36 fontes validadas continuam sendo literatura acadêmica; ainda não há base para comparar literatura acadêmica e cinzenta.

## 3. Cobertura das questões de pesquisa

### QP1 — Práticas de Engenharia de Dados

O corpus sustenta práticas de seleção e integração de fontes, parsing, OCR, chunking, enriquecimento semântico e de metadados, persistência e indexação vetorial, busca híbrida, atualização de índices, avaliação, feedback, controle de acesso, auditoria, proveniência, detecção de envenenamento e descarte. A classificação como práticas transferidas, adaptadas ou novas deverá ocorrer somente na extração dos textos completos.

### QP2 — Desafios ao longo do ciclo de vida

Os resumos registram desafios de heterogeneidade, ruído, perda de estrutura, consistência de entidades e números, atualidade, concorrência entre leitura e escrita, custo de atualização, latência de cauda, recuperação após reinício, escalabilidade, autorização, envenenamento, avaliação e exclusão. A cobertura é forte entre S1 e S6, mas permanece insuficiente em S7 e S8.

### QP3 — Literatura acadêmica versus literatura cinzenta

Ainda não pode ser respondida. As 36 fontes validadas são acadêmicas. A comparação exigirá incorporar fontes cinzentas e aplicar a elas os mesmos códigos de prática, desafio, etapa e dimensão transversal.

## 4. Direções para a rodada r005

1. Priorizar snowballing a partir de `P-db3d0d4c1caa`, `P-79b99916d8ad`, `P-423200bdcd80`, `P-0d46d780075c`, `P-dafca2ca704a` e `P-6108a118d511`, sem excluir as demais fontes validadas do procedimento formal.
2. Para S7, buscar sincronização com fontes, CDC, atualização incremental, reindexação, invalidação de embeddings, deriva ou obsolescência do corpus, versionamento e reconstrução de índices.
3. Para S8, buscar retenção, expiração, direito ao esquecimento, deleção propagada, remoção de embeddings, limpeza de caches e réplicas, desativação de fontes e comprovação auditável da exclusão.
4. Favorecer estudos que associem observabilidade a uma ação automática na pipeline, com métricas por versão e comparação entre estados antes e depois da mudança.
5. Buscar relatos industriais e documentação técnica para iniciar a cobertura de literatura cinzenta necessária à QP3.
6. Evitar repetir comparações genéricas de bancos vetoriais ou chunking quando não acrescentarem manutenção, descarte, governança, avaliação operacional ou evidência de produção.
