# Análise assistida após a rodada r005

Esta nota sintetiza 42 fontes acadêmicas validadas. As observações se limitam aos títulos, resumos, metadados e justificativas humanas do pacote `packet_r005.json`; afirmações sobre implementação, parâmetros, causalidade ou resultados não descritos nesse material exigem consulta ao texto completo.

## 1. Padrões observados

### Fontes, ingestão e preparação (S1–S4)

O corpus reúne 10 fontes em S1, 16 em S2, 21 em S3 e 13 em S4. Permanecem recorrentes a integração de fontes heterogêneas, preservação da estrutura documental, chunking semântico ou hierárquico, enriquecimento de metadados e combinação de dados estruturados e não estruturados. `P-05f05d2ab481` e `P-a00af99127ff` tratam da harmonização de dados empresariais; `P-03119b691be0`, `P-f728b0a66bc2` e `P-5075f7fb2528` preservam estrutura e layout; `P-a2f0f78ba880` acrescenta extração, normalização e deduplicação contínuas de triplas com proveniência.

A rodada r005 reforça a visão de preparação como sequência de decisões dependentes. `P-8ec420ab749e` encadeia análise do corpus, seleção de chunking, arquitetura do índice e calibração de confiança. `P-291a967540dd` combina chunking multigranular, ACL em nível de chunk, recuperação híbrida e reranqueamento em uma base empresarial. Os textos completos serão necessários para separar efeitos de cada componente e verificar condições de aplicabilidade.

### Armazenamento, indexação e disponibilização (S3–S5)

S3 permanece como a etapa mais coberta, com 21 fontes, e S5 reúne 15. Os trabalhos abrangem persistência, distribuição, filtros, atualização, concorrência, busca híbrida, índices adaptativos e operação sob restrições de hardware. `P-79b99916d8ad`, `P-6108a118d511`, `P-dafca2ca704a` e `P-2c31a6a44ef9` fornecem evidência sobre inserções, exclusões, churn, reinicialização, WAL e atualização em tempo real.

`P-a650e273556d` acrescenta escala empresarial, latência, disponibilidade, custo e análise de falhas. `P-8ec420ab749e` relaciona estrutura do índice e recuperação híbrida à calibração de confiança. `P-0f7eddcb8eb2` trata a seleção do contexto como otimização sujeita a orçamento de tokens e redundância. Em conjunto, esses estudos sustentam decisões operacionais, mas a comparação entre arquiteturas e resultados exige extração dos textos completos.

### Qualidade, segurança, governança e rastreabilidade

Qualidade aparece em 16 fontes, segurança em 14, governança em 7 e rastreabilidade em 8. Qualidade atravessa preparação, recuperação, avaliação e serving. `P-f742a6093683` associa falhas observadas a ações de otimização; `P-423200bdcd80` observa atualidade e divergência do índice; `P-34502433a68a` mostra que avaliação independente da recuperação, verificação fina de evidências e análise de artefatos intermediários ainda são pouco frequentes.

Segurança e governança aparecem em controle de acesso, políticas, auditoria e integridade do corpus. `P-ee5a47f71db6`, `P-2a7e331ac123`, `P-43a81bdd7933` e `P-578a6ed00cea` restringem a recuperação conforme identidade ou política. `P-291a967540dd` adiciona permissões por chunk em um caso empresarial. `P-a2f0f78ba880` amplia rastreabilidade ao vincular triplas, segmentos-fonte e metadados.

### Uso, avaliação e feedback (S6)

S6 passou a 9 fontes. `P-3f5242546ea6`, `P-aee8c0ff3256` e `P-32ac448357e4` tratam de experiência de usuários, profissionais e ciclos de feedback. `P-f742a6093683` usa avaliação para orientar melhorias, e `P-a650e273556d` descreve feedback recursivo, métricas de produção e análise de falhas.

`P-34502433a68a` acrescenta uma síntese importante: em 157 estudos de saúde, a avaliação permanece concentrada em cenários offline, com menor presença de avaliação independente da recuperação, vínculo fino de evidências, segurança e artefatos intermediários de GraphRAG. O resumo sustenta a existência dessas lacunas, mas a adoção de métricas específicas no TCC dependerá da leitura integral.

### Manutenção e descarte (S7–S8)

S7 e S8 continuam com apenas 2 fontes cada. Em S7, `P-0d46d780075c` reage a ruído e mudanças por aprendizagem ativa, enquanto `P-423200bdcd80` monitora replicação, divergência entre shards e perda de atualidade. Os novos artigos mencionam processos contínuos, feedback e atualização, mas suas classificações atuais permanecem em outras etapas porque os resumos não descrevem de forma suficiente reindexação, invalidação, sincronização ou reconstrução.

Em S8, `P-db3d0d4c1caa` descreve exclusão automatizada em DSAR, mascaramento e auditoria, e `P-79b99916d8ad` suporta exclusões contínuas em um mecanismo vetorial. Ainda faltam retenção, expiração, propagação da exclusão para artefatos derivados, limpeza de caches e réplicas e comprovação auditável da remoção.

## 2. Lacunas

- **S7 — Manutenção:** 2 fontes, abaixo do mínimo do protocolo. Faltam estudos explícitos sobre sincronização com fontes, CDC, atualização incremental, invalidação de embeddings, deriva do corpus, versionamento e reconstrução de índices.
- **S8 — Descarte:** 2 fontes, também abaixo do mínimo. Permanecem pouco cobertas retenção, expiração, desativação de fontes, deleção propagada e verificação da remoção.
- **Operação contínua:** aumentou a evidência sobre escala, latência, confiança e avaliação, mas ainda são raros os trabalhos que conectam métricas a ações automatizadas e versionadas sobre a base.
- **Governança do ciclo completo:** controle de acesso está bem representado, enquanto responsabilidades sobre atualização, retenção e descarte continuam menos desenvolvidas.
- **Distribuição temporal:** há 1 fonte de 2024, 14 de 2025, 25 de 2026 e 2 registradas como 2027. Os registros de 2027 devem ter seu status de publicação confirmado no texto completo ou nos metadados editoriais antes da síntese final.
- **QP3:** as 42 fontes validadas continuam sendo acadêmicas; ainda não há base para comparar literatura acadêmica e cinzenta.

## 3. Cobertura das questões de pesquisa

### QP1 — Práticas de Engenharia de Dados

O corpus sustenta práticas de seleção e integração de fontes, parsing, OCR, chunking, enriquecimento semântico e de metadados, persistência e indexação, recuperação híbrida, reranqueamento, calibração de confiança, seleção otimizada de contexto, feedback, controle de acesso, auditoria, proveniência, detecção de envenenamento e descarte. A classificação como práticas transferidas, adaptadas ou novas deverá ocorrer apenas durante a extração dos textos completos.

### QP2 — Desafios ao longo do ciclo de vida

Os resumos registram heterogeneidade, ruído, perda de estrutura, consistência, atualidade, concorrência, custo de atualização, latência, escalabilidade, autorização, envenenamento, avaliação, confiança e exclusão. A cobertura é forte entre S1 e S6, mas permanece insuficiente em S7 e S8.

### QP3 — Literatura acadêmica versus literatura cinzenta

Ainda não pode ser respondida. As 42 fontes validadas são acadêmicas. A comparação depende da incorporação de documentação técnica, relatos industriais e outras fontes cinzentas avaliadas pelos mesmos códigos.

## 4. Direções para a rodada r006

1. Priorizar snowballing das fontes que descrevem atualização contínua, feedback e operação empresarial, especialmente `P-a2f0f78ba880`, `P-a650e273556d`, `P-423200bdcd80`, `P-0d46d780075c`, `P-db3d0d4c1caa` e `P-79b99916d8ad`.
2. Para S7, buscar sincronização, CDC, reindexação, invalidação de embeddings, versionamento, detecção de obsolescência e reconstrução do índice.
3. Para S8, buscar retenção, expiração, direito ao esquecimento, deleção propagada, limpeza de caches e réplicas, desativação de fontes e auditoria da remoção.
4. Favorecer trabalhos em que feedback, observabilidade ou avaliação produzam mudanças verificáveis na pipeline e permitam comparar versões.
5. Evitar novos artigos centrados apenas em RBAC, hardware vetorial, chunking genérico ou aplicações finais que repitam práticas já bem representadas.
6. Iniciar a busca e avaliação de literatura cinzenta para tornar QP3 respondível.
