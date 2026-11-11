# Análise assistida após a rodada r006

Esta nota sintetiza 47 fontes acadêmicas validadas. As observações se limitam aos títulos, resumos, metadados e justificativas humanas do pacote `packet_r006.json`; afirmações sobre implementação, parâmetros, causalidade ou resultados não descritos nesse material exigem consulta ao texto completo.

## 1. Padrões observados

### Fontes, ingestão, armazenamento e preparação (S1–S4)

O corpus reúne 10 fontes em S1, 16 em S2, 23 em S3 e 16 em S4. As práticas recorrentes incluem integração de fontes heterogêneas, parsing e OCR, preservação de estrutura, chunking, enriquecimento semântico, persistência, indexação vetorial e modelagem em grafos. `P-05f05d2ab481` e `P-a00af99127ff` integram dados empresariais heterogêneos; `P-5075f7fb2528` e `P-f728b0a66bc2` tratam de documentos complexos; `P-a2f0f78ba880` adiciona extração, normalização, deduplicação e proveniência.

A rodada r006 acrescenta evidência sobre decisões de preparação. `P-206019f44c15` mostra que o custo do chunking semântico não produz ganhos consistentes nos casos avaliados, enquanto `P-73bb4c428170` relaciona granularidade, orçamento de contexto, completude das evidências e auditabilidade. `P-dfb0b35f7ecb` modela relações hierárquicas, referências cruzadas e similaridade entre documentos regulatórios em um grafo semântico. A generalização desses resultados exige consulta aos textos completos.

### Disponibilização, uso e feedback (S5–S6)

S5 reúne 16 fontes e S6, 10. Recuperação híbrida, reranqueamento, seleção de contexto, métricas por camada e ciclos de feedback aparecem de forma recorrente. `P-0f7eddcb8eb2` otimiza a seleção de chunks sob limite de tokens; `P-f742a6093683` relaciona avaliação a ações de melhoria; `P-34502433a68a` mapeia lacunas de avaliação da recuperação, evidências e artefatos intermediários.

`P-7ca287ada16c` fortalece a conexão entre uso, feedback e manutenção: monitora falhas reais, coleta amostras negativas, classifica problemas e aplica ajustes direcionados. Esse padrão aproxima a avaliação da mudança controlada na pipeline.

### Manutenção (S7)

S7 passou de 2 para 3 fontes e atingiu o mínimo definido no protocolo. `P-0d46d780075c` seleciona exemplos para reagir a ruído e mudanças; `P-423200bdcd80` monitora replicação, divergência e atualidade do índice; `P-7ca287ada16c` implementa um ciclo MAPE e um data flywheel com feedback humano, análise de falhas e implantação gradual.

As três fontes cobrem detecção, monitoramento e melhoria contínua, mas ainda é necessário verificar nos textos completos como documentos, chunks, embeddings, índices e versões são efetivamente alterados e auditados.

### Descarte (S8)

S8 também passou de 2 para 3 fontes e atingiu o mínimo. `P-db3d0d4c1caa` descreve exclusão automatizada em solicitações DSAR, mascaramento e auditoria; `P-79b99916d8ad` suporta exclusões contínuas em um mecanismo vetorial; `P-b459a2bcbc50` organiza cache, memória de trabalho, armazenamento semântico e arquivo frio com políticas de retenção, acesso e linhagem.

O conjunto permite discutir exclusão, retenção e arquivamento. Ainda requer texto completo para confirmar propagação da remoção, limpeza de caches e réplicas, comprovação de exclusão e tratamento de logs ou artefatos derivados.

### Dimensões transversais

Qualidade aparece em 17 fontes, segurança em 16, governança em 10 e rastreabilidade em 10. `P-b459a2bcbc50` conecta retenção, controle de acesso e W3C PROV; `P-dfb0b35f7ecb` integra governança e segurança à estruturação do conhecimento regulatório; `P-73bb4c428170` trata granularidade como decisão de evidência e auditabilidade.

O padrão geral mostra que as dimensões transversais atravessam a fonte, a preparação, o armazenamento, a recuperação, o feedback, a manutenção e o descarte, em vez de aparecerem apenas na resposta gerada.

## 2. Lacunas

- **Etapas S1–S8:** nenhuma etapa permanece abaixo do mínimo quantitativo do protocolo.
- **Profundidade de S7:** apesar do mínimo atingido, ainda falta evidência detalhada sobre sincronização com sistemas de origem, CDC, invalidação de embeddings, versionamento e reconstrução de índices.
- **Profundidade de S8:** retenção e exclusão estão presentes, mas propagação da deleção, limpeza de réplicas e caches e comprovação auditável ainda precisam ser verificadas.
- **Operação contínua:** permanecem poucos trabalhos que conectam observabilidade, decisão automática, alteração da pipeline e comparação entre versões.
- **Distribuição temporal:** há 1 fonte de 2024, 16 de 2025, 28 de 2026 e 2 registradas como 2027. Os registros de 2027 precisam ter o status editorial confirmado antes da síntese final.
- **QP3:** as 47 fontes validadas continuam acadêmicas. A comparação com literatura cinzenta ainda não pode ser realizada.

## 3. Cobertura das questões de pesquisa

### QP1 — Práticas de Engenharia de Dados

O conjunto sustenta práticas de seleção e integração de fontes, parsing, OCR, chunking, enriquecimento, grafos, armazenamento e indexação, recuperação híbrida, reranqueamento, avaliação, feedback, manutenção, retenção, exclusão, controle de acesso, proveniência e auditoria. A classificação como práticas transferidas, adaptadas ou novas deverá ocorrer apenas na extração dos textos completos.

### QP2 — Desafios ao longo do ciclo de vida

Os resumos registram heterogeneidade, ruído, perda de estrutura, custo computacional, granularidade, atualidade, concorrência, latência, escalabilidade, autorização, envenenamento, avaliação, feedback, retenção e exclusão. Todas as etapas possuem ao menos três fontes, mas cobertura quantitativa não substitui a verificação qualitativa nos textos completos.

### QP3 — Literatura acadêmica versus literatura cinzenta

Ainda não pode ser respondida. A próxima expansão relevante deve priorizar documentação técnica, relatos industriais e outras fontes cinzentas, aplicando os mesmos códigos de prática, desafio, etapa e dimensão transversal.

## 4. Direções para as próximas etapas

1. Verificar os critérios formais de parada e a estabilidade temática antes de abrir nova rodada acadêmica.
2. Realizar snowballing das cinco novas fontes para completar o procedimento formal, priorizando referências de `P-7ca287ada16c` e `P-b459a2bcbc50`.
3. Iniciar a coleta e avaliação de literatura cinzenta necessária à QP3.
4. Na extração integral, detalhar como feedback altera artefatos de dados, como políticas de retenção são executadas e como exclusões são propagadas e comprovadas.
5. Confirmar o status editorial das duas fontes registradas como 2027.
6. Evitar novas rodadas dominadas por chunking genérico, hardware, RBAC, aplicações clínicas ou multimodalidade sem contribuição nova para manutenção, descarte ou operação.
