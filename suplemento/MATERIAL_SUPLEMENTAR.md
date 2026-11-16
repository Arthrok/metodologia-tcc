# Material suplementar — revisão multivocal de Engenharia de Dados em RAG

Arquivo complementar ao manuscrito *Engenharia de Dados em Sistemas RAG: Práticas, Desafios e Adaptações*. O corpus final contém 88 fontes e 244 evidências. Os registros de seleção, extração e auditoria estão disponíveis nos arquivos abaixo.

## Registros da revisão

Todos os registros estão em uma única planilha, [Registros_MLR.xlsx](Registros_MLR.xlsx), com uma aba por registro:

| Aba | Conteúdo |
|---|---|
| Fontes | Decisão final de cada fonte acadêmica, candidata cinzenta avaliada no texto integral e candidato priorizado do *forward snowballing*, com critério, pontuação e avaliador atribuído na auditoria |
| Cinzenta_consultas | Consultas da DEV Community, do Hacker News e dos portais, com parâmetros, data e ocorrências |
| Cinzenta_triagem | Os 210 candidatos cinzentos únicos, com pré-triagem, motivo e decisão final |
| Qualidade_QA e Qualidade_QG | Notas QA1–QA6 das acadêmicas e QG1–QG6 das 61 candidatas cinzentas |
| Evidencias | As 244 evidências válidas (179 acadêmicas e 65 cinzentas), com identificador estável (por exemplo, `C05-e02`), etapa, dimensão transversal (`31/8/7/10` nas cinzentas e `48/18/23/30` nas acadêmicas, conforme a Tabela 15 do artigo), prática, localização, excerto e as linhas das Tabelas QP1–QP3 em que aparecem |
| QP1, QP2, QP3_temas, QP3_codificacao | Vínculo entre as evidências e as Tabelas 17, 18 e 19 |
| QP3_34_temas | Correspondência entre os 34 temas iniciais e as linhas da Tabela 19 |
| Auditoria_registro e Auditoria_itens | Base documental da auditoria humana (seção 3.3.7) e lista nominal dos itens conferidos |
| Forward | Pré-triagem dos 242 citantes novos do *forward snowballing* que mencionavam RAG (os outros 158 foram excluídos por I2) |

## Classificação das Tabelas 1–4 do manuscrito

| Tabela | Papel no texto principal | Decisão |
|---|---|---|
| 1: ciclo de vida S1–S8 | Lente de codificação | Mantida no referencial |
| 2: BI/RAG | Lente de comparação contextual | Mantida no referencial |
| 3: configuração da recuperação | Lente para localizar decisões técnicas | Mantida no referencial |
| 4: falhas observáveis | Lente diagnóstica | Mantida no referencial |

## Protocolo completo de busca e seleção

As famílias acadêmicas S1–S8 e as cinzentas G1–G8 foram associadas às etapas do ciclo de vida dos dados. As strings abaixo preservam os operadores, termos e filtros registrados. O desenho metodológico, a matriz PICOC, as contagens por mecanismo, as oito rodadas de triagem e o fluxo PRISMA constam em seção de Metodologia do manuscrito.

As questões de pesquisa e a matriz PICOC foram refinadas após o rascunho inicial do protocolo operacional registrado em [config/review_protocol.yaml](../config/review_protocol.yaml). Na formulação final do artigo, a QP1 focalizou as práticas por etapa S1–S8, a QP2 examinou adaptações e desafios documentados, e a QP3 comparou os achados entre literatura acadêmica e cinzenta. Na PICOC final, a dimensão Comparação passou a explicitar essa distribuição entre os dois tipos de literatura; o contraste com BI/Analytics e outros contextos de engenharia de dados foi mantido apenas quando sustentado pelas fontes. O arquivo YAML preservou a formulação usada na triagem histórica e não substituiu as questões e a PICOC finais do manuscrito.

O *backward snowballing* recuperou 905 registros: 845 novos, 58 coincidentes com buscas diretas e 2 duplicatas internas ou registros sem metadados mínimos, descartados antes da deduplicação. O *forward snowballing* recuperou 426 citantes: 26 já no corpus e 400 novos. Dos novos, 95 foram priorizados e 305 não priorizados; nenhum foi incorporado nesta execução por corte temporal e de escopo. Consulte a aba Forward da planilha.

### Strings acadêmicas S1–S8

| ID | Etapa | String de busca |
|---|---|---|
| S1 | Fontes | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data source*" OR "knowledge source*" OR "source selection" OR "source curation" OR "corpus curation")</code> |
| S2 | Ingestão | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data ingestion" OR "document ingestion" OR "data extraction" OR "document parsing" OR OCR OR crawl*)</code> |
| S3 | Armazenamento | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("vector database*" OR "vector store*" OR "vector index*" OR "document store*" OR "embedding store*")</code> |
| S4 | Preparação | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ( chunk* OR "text segment*" OR "document split*" OR "text preprocessing" OR "document preprocessing" OR "text normalization" OR "embedding generation")</code> |
| S5 | Disponibilização | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("retrieval strateg*" OR "hybrid search" OR rerank* OR "metadata filter*" OR "context compression")</code> |
| S6 | Uso e feedback | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("RAG evaluation" OR "retrieval evaluation" OR observab* OR tracing OR "user feedback")</code> |
| S7 | Manutenção | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND (freshness OR reindex* OR "document update*" OR "corpus update*" OR "incremental update*" OR version*)</code> |
| S8 | Descarte | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data deletion" OR "document deletion" OR deindex* OR erasure OR retention OR purge OR expiration)</code> |

### Strings da literatura cinzenta G1–G8

| ID | Etapa | String de busca |
|---|---|---|
| G1 | Fontes | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data source*" OR "knowledge source*" OR "source selection" OR "source curation" OR "corpus curation")</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G2 | Ingestão | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data ingestion" OR "document ingestion" OR "data extraction" OR "document parsing" OR OCR OR crawl*)</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G3 | Armazenamento | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("vector database*" OR "vector store*" OR "vector index*" OR "document store*" OR "embedding store*")</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G4 | Preparação | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND (chunk* OR "text segment*" OR "document split*" OR "text preprocessing" OR "document preprocessing" OR "text normalization" OR "embedding generation")</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G5 | Disponibilização | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("retrieval strateg*" OR "hybrid search" OR rerank* OR "metadata filter*" OR "context compression")</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G6 | Uso e feedback | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("RAG evaluation" OR "retrieval evaluation" OR observab* OR tracing OR "user feedback")</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G7 | Manutenção | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND (freshness OR reindex* OR "document update*" OR "corpus update*" OR "incremental update*" OR version*)</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |
| G8 | Descarte | <code>("retrieval augmented generation" OR "retrieval-augmented generation")</code><br><code>AND ("data deletion" OR "document deletion" OR deindex* OR erasure OR retention OR purge OR expiration)</code><br><code>AND ("technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices")</code> |

## Critérios completos de inclusão e exclusão

A elegibilidade foi decidida por critérios categóricos, com o motivo principal registrado para as exclusões. A data de publicação orientou o recorte temporal; para documentação continuamente atualizada sem data original, foi aceita a data explícita da última atualização. A data de acesso serviu à rastreabilidade, sem substituir essas datas. Uma fonte anterior a 2024 só podia integrar o corpus como exceção fundacional justificada e com os demais critérios atendidos.

### Inclusão (I1–I3)

| Critério | Definição |
|---|---|
| I1 — Recorte temporal | As fontes candidatas ao corpus analítico da MLR deverão ter sido publicadas a partir de 2024. Excepcionalmente, publicações anteriores poderão integrar o corpus quando apresentarem contribuição fundacional diretamente relacionada ao escopo da revisão, mediante justificativa registrada no protocolo e atendimento aos demais critérios de elegibilidade e qualidade. Publicações anteriores utilizadas exclusivamente na fundamentação teórica não integram o corpus analítico e, portanto, não constituem exceções ao recorte temporal da MLR. |
| I2 — Aderência ao escopo | a fonte deve abordar RAG de forma substantiva e apresentar relação com Engenharia de Dados, envolvendo pelo menos uma das etapas do ciclo de vida adotado ou uma de suas dimensões transversais. |
| I3 — Contribuição analisável | a fonte deve apresentar pelo menos uma prática, desafio, decisão técnica, arquitetura ou efeito relacionado às questões de pesquisa, com conteúdo suficiente para sua identificação e extração. |

### Exclusão (E1–E5)

| Critério | Definição |
|---|---|
| E1 — Duplicata ou versão redundante | registro duplicado, republicação ou versão menos completa de uma fonte já considerada. Quando houver múltiplas versões, será mantida a versão mais completa ou formalmente publicada. |
| E2 — Fora do recorte temporal | fonte publicada antes de 2024 que não apresente contribuição fundacional conforme definida em I1. |
| E3 — Fora do escopo | fonte em que RAG seja apenas incidental ou cuja contribuição não apresente relação substantiva com Engenharia de Dados, com o ciclo de vida dos dados ou com suas dimensões transversais. |
| E4 — Conteúdo insuficiente para análise | fonte predominantemente introdutória, genérica, promocional ou sem detalhamento suficiente para identificar evidências relacionadas às questões de pesquisa. |
| E5 — Conteúdo integral indisponível ou fonte derivada | fonte cujo conteúdo não esteja suficientemente disponível para análise, bem como agregadores, resumos ou republicações quando a fonte original puder ser identificada. |

## Rubricas completas de qualidade QA e QG

Cada critério recebeu 0, 0,5 ou 1 ponto, com máximo de 6,0. Uma fonte acadêmica foi considerada adequada com pelo menos 4,0 pontos, exceto quando QA2 e QA3 receberam zero simultaneamente. Para as fontes cinzentas, exigiram-se pelo menos 4,0 pontos e QG6 acima de zero.

### Qualidade acadêmica (QA1–QA6)

| Critério | Definição |
|---|---|
| QA1 — Clareza do objetivo | o estudo apresenta claramente seu objetivo, problema ou questão investigada? |
| QA2 — Transparência metodológica | o método, experimento, estudo de caso ou procedimento empregado é descrito com detalhes suficientes para compreender a obtenção dos resultados? |
| QA3 — Fundamentação das evidências | as afirmações e conclusões relevantes são sustentadas por evidências, dados, experimentos, estudos de caso, análise ou argumentação explicitamente apresentada no trabalho? |
| QA4 — Especificidade da contribuição | o estudo descreve concretamente a prática, desafio, decisão arquitetural ou efeito observado, evitando afirmações genéricas sobre RAG? |
| QA5 — Limitações e contexto | o estudo apresenta limitações, ameaças à validade ou contexto suficiente para interpretar adequadamente os achados? |
| QA6 — Rastreabilidade técnica | é possível relacionar os resultados a artefatos, dados, configurações, componentes ou etapas do pipeline analisado? |

### Qualidade da literatura cinzenta (QG1–QG6)

| Critério | Definição |
|---|---|
| QG1 — Autoridade | a autoria, organização técnica ou responsável pela publicação é claramente identificável? |
| QG2 — Especificidade técnica | a fonte apresenta detalhamento técnico concreto para compreender a prática, arquitetura ou problema descrito? |
| QG3 — Evidência de uso | a publicação relata implementação prática, estudo de caso industrial, dados operacionais ou lições aprendidas em produção? |
| QG4 — Atualidade | o documento possui data identificável e conteúdo tecnologicamente atualizado? |
| QG5 — Transparência | a fonte descreve o contexto de aplicação, restrições ou configurações de forma transparente? |
| QG6 — Verificabilidade | as afirmações técnicas relevantes podem ser verificadas por dados, referências, exemplos, documentação ou descrição suficiente da experiência relatada? |

O registro complementar de objetividade indicou quando uma fonte cinzenta promovia produto ou serviço do próprio autor ou organização, sem alterar a pontuação. As notas finais e restrições de uso constam na aba Fontes da planilha.

## Decisões da auditoria final

A57 foi rebaixada para QA abaixo de 4,0 e excluída do corpus. A01, A11, A27, A28, A38, A41, A50 e A54 também ficaram fora da síntese. C09, C16, C17 e C21 foram incluídas com restrição de uso numérico: seus valores ilustrativos, promocionais ou não comparáveis não sustentam resultados empíricos. As decisões individuais constam em aba Fontes da planilha.

## Execução da seleção da literatura cinzenta

As três frentes (DEV Community, Hacker News e portais institucionais) resultaram em 210 candidatos únicos após a consolidação pela URL. Os 198 candidatos das APIs passaram por pré-triagem conduzida com apoio de inteligência artificial, que sugeriu classificações de elegibilidade a partir do título e da descrição; as 12 páginas dos portais, escolhidas nas buscas dirigidas, seguiram diretamente para a avaliação do texto integral. Foram excluídos 149 registros por E3 ou E4, e 61 candidatas foram encaminhadas à avaliação do texto integral. As sugestões automatizadas foram posteriormente examinadas por Eric, com apoio de uma segunda ferramenta de IA; ele foi responsável pela revisão da filtragem e pelas decisões finais de seleção. Das 61 candidatas, 37 foram incluídas e 24 excluídas (QG < 4: 9; E4: 6; E5: 3; I1: 3; QG1 = 0: 2; QG6 = 0: 1). Duas páginas inacessíveis no endereço original foram avaliadas a partir de cópias do Internet Archive.

A revisão humana foi realizada durante o processo de pesquisa, sem a produção de um registro individualizado das concordâncias e divergências em relação às sugestões automatizadas. Essa característica limita a reconstrução retrospectiva de cada decisão, embora os registros de candidatos, critérios, classificações e resultados finais tenham sido preservados. Os 65 excertos cinzentos foram verificados automaticamente contra os textos arquivados: todos constam literalmente deles. Essa verificação atesta a correspondência textual, não a adequação da etapa, da prática ou da adaptação atribuídas.

## Base documental da auditoria humana (seção 3.3.7)

A divisão nominal (aba Fontes) atribuiu 115 registros a Eric (41 cinzentos, 20 acadêmicos e 54 do *forward snowballing*) e 101 a Arthur (20 cinzentos, 40 acadêmicos e 41 do *forward snowballing*). Os 20 casos próximos dos cortes QA=4,0/4,5 e QG=4,0/4,5 (seis acadêmicos e 14 cinzentos) e as fontes de cada adaptação da Tabela 18 estão listados na aba Auditoria_itens, com avaliador atribuído, decisão final e evidências. A aba Auditoria_registro indica, para cada afirmação da seção 3.3.7, o arquivo que a documenta e o que ele não documenta. Os efeitos da conferência estão registrados no arquivo de decisões: o rebaixamento de A57 e a restrição de uso numérico de C09, C16, C17 e C21. A conferência não produziu registro individualizado do que foi confirmado ou alterado em cada nota, excerto ou adaptação.

## Rastreabilidade entre evidências e Tabelas QP1–QP3

Cada evidência válida recebeu o identificador `<fonte>-e<NN>`, na ordem da ficha de extração. Na QP1 (Tabela 17), cada ID de uma célula remete às evidências da fonte codificadas na etapa da linha; nenhuma célula cita fonte sem evidência na etapa. Na QP2 (Tabela 18), cada linha remete às evidências que sustentam a adaptação. Na QP3 (Tabela 19), cada tema remete às evidências codificadas nele, segundo a definição operacional abaixo; uma evidência pode integrar mais de um tema. A codificação final foi consolidada com apoio do modelo de linguagem a partir das fichas de extração e pode ser conferida pelo identificador de cada evidência.

### Tabela 19: temas, definições e frequências

A frequência conta as fontes com ao menos uma evidência codificada no tema; não mede eficácia.

| ID | Tema | Definição operacional | Presença | Fontes acad./cinz. | Evidências |
|---|---|---|---|---|---|
| T01 | Medallion para documentos RAG | Camadas Bronze/Silver/Gold aplicadas a artefatos documentais do pipeline RAG | Acadêmica | 1/0 | 1 |
| T02 | Índices federados por domínio | Índices e documentos mantidos por domínio ou instituição, com roteamento federado | Acadêmica | 2/0 | 3 |
| T03 | Pré/pós-filtro na busca vetorial | Decisão sobre onde e como aplicar filtros de atributos na busca vetorial (pré/pós-filtro, pushdown, varredura iterativa, seletividade) | Ambas | 6/1 | 7 |
| T04 | Autorização antes da geração | Controle de acesso aplicado na recuperação ou antes do prompt (ACL, RBAC/ABAC/PBAC, IAM da fonte, finalidade) | Ambas | 7/4 | 14 |
| T05 | Linhagem e traces por resposta | Registro de proveniência ou trace que liga fonte, trecho, rota e resposta | Ambas | 6/1 | 8 |
| T06 | Chunking estrutural e contexto | Preservação de estrutura, tabelas e hierarquia ou inclusão de contexto e metadados do documento no chunk | Ambas | 15/5 | 25 |
| T07 | Retenção por artefato e mascaramento de PII | Minimização, redação ou mascaramento de dados pessoais e prazos de retenção por artefato ou camada | Ambas | 4/2 | 8 |
| T08 | Índices ANN, WAL e latência filtrada | Mecanismos internos de construção, atualização, compactação e manutenção de índices ANN | Acadêmica | 6/0 | 14 |
| T09 | Métricas intrínsecas de chunk | Medidas da qualidade do fragmento independentes da resposta final | Acadêmica | 3/0 | 3 |
| T10 | Orçamento formal de contexto | Seleção ou dimensionamento do contexto sob orçamento explícito de tokens | Acadêmica | 4/0 | 4 |
| T11 | Defasagem de estado entre índices, fontes e permissões | Divergência entre o estado do índice e o da fonte ou das permissões, e sua ressincronização | Ambas | 3/2 | 7 |
| T12 | Exclusão em índices e derivados | Remoção de documentos ou dados de índices e derivados (tombstone, purge, compactação, eliminação criptográfica, verificação) | Ambas | 7/3 | 11 |
| T13 | Ingestão idempotente e retomável | Ingestão ou reprocessamento controlado por hash de conteúdo, checkpoints e filas de falha | Cinzenta | 0/2 | 2 |
| T14 | Migração de embedding e troca de versão | Troca de modelo de embedding, índice ou configuração com validação, versão e rollback | Ambas | 4/2 | 7 |

### Correspondência com os 34 temas da planilha de extração

A planilha da literatura cinzenta (aba QP3) registrou 34 temas iniciais, com fontes atribuídas no nível da fonte. Dezessete deles foram agregados nas linhas da Tabela 19; três linhas (T01–T03) são temas novos, desdobrados das adaptações da QP2; os 17 restantes foram tratados no texto da QP1 e da QP2 ou permanecem só neste suplemento. As frequências da planilha e as da Tabela 19 diferem porque a tabela recodificou evidência a evidência, com as definições acima, e porque A57 deixou o corpus.

| Tema da planilha | Etapa | Acad./cinz. (planilha) | Acad./cinz. (corpus final) | Linha da Tabela 19 |
|---|---|---|---|---|
| Curadoria, inventário e confiabilidade das fontes | S1 | 6/4 | 6/4 | — |
| Monitorar mudança e obsolescência das fontes | S1/S7 | 3/2 | 3/2 | — |
| Qualidade da extração (OCR/parsing) medida pelo efeito no RAG | S2 | 4/4 | 4/4 | — |
| Preservar tabelas e estrutura na extração e no chunking | S2/S4 | 12/4 | 12/4 | T06 Chunking estrutural e contexto |
| Ingestão idempotente e retomável (hash, checkpoint) | S2 | 0/2 | 0/2 | T13 Ingestão idempotente e retomável |
| Redação/mascaramento de PII e minimização | S2/Seg. | 5/2 | 5/2 | T07 Retenção por artefato e mascaramento de PII |
| Vetores no banco já existente (relacional/OLAP/lakehouse) | S3 | 3/3 | 3/3 | — |
| Dispensar índice ANN conforme escala e uso | S3 | 2/2 | 2/2 | — |
| Grafo de conhecimento construído dos documentos | S3/S4 | 6/1 | 6/1 | — |
| Deduplicação e filtro de ruído/baixa informação | S4 | 5/4 | 5/4 | — |
| Enriquecer o chunk com contexto e metadados do documento | S4 | 10/5 | 9/5 | T06 Chunking estrutural e contexto |
| Chunking semântico | S4 | 4/3 | 4/3 | — |
| Tamanho/granularidade do chunk definido por experimento | S4 | 11/3 | 11/3 | — |
| Métricas intrínsecas de qualidade do chunk | S4 | 3/0 | 3/0 | T09 Métricas intrínsecas de chunk |
| Busca híbrida e fusão de rankings (RRF) | S5 | 4/4 | 4/4 | — |
| Reranking (genérico ou ajustado ao domínio) | S5 | 3/4 | 3/4 | — |
| Controle de acesso na recuperação (ACL/políticas) | S5 | 5/5 | 5/5 | T04 Autorização antes da geração |
| Seleção do contexto sob orçamento de tokens | S5 | 4/0 | 4/0 | T10 Orçamento formal de contexto |
| Diversidade de fontes no contexto | S5 | 1/1 | 1/1 | — |
| Conjunto de avaliação próprio e métricas por camada | S6 | 7/4 | 7/4 | — |
| Validar o avaliador automático (LLM-juiz) | S6 | 1/1 | 1/1 | — |
| Rastreamento por requisição e observabilidade da recuperação | S6 | 4/1 | 4/1 | T05 Linhagem e traces por resposta |
| Feedback de uso realimentando dados e recuperação | S6 | 6/1 | 6/1 | — |
| Atualização incremental e consistência durante a atualização | S7 | 7/3 | 7/3 | T08 Índices ANN, WAL e latência filtrada |
| Manutenção estrutural do índice ANN (reconstrução, split/merge) | S7 | 5/0 | 5/0 | T08 Índices ANN, WAL e latência filtrada |
| Sincronização entre índices/armazenamentos e defasagem | S7 | 2/2 | 2/2 | T11 Defasagem de estado entre índices, fontes e permissões |
| Versionamento do corpus/índice e rollback | S7 | 6/1 | 6/1 | T14 Migração de embedding e troca de versão |
| Migração do modelo de embedding (re-embedding) | S7 | 2/1 | 2/1 | T14 Migração de embedding e troca de versão |
| Exclusão em índices vetoriais (tombstone, compactação, purge) | S8 | 5/2 | 5/2 | T12 Exclusão em índices e derivados |
| Exclusão verificável e direito ao esquecimento | S8 | 2/2 | 2/2 | T12 Exclusão em índices e derivados |
| Retenção por tipo de artefato (logs, prompts, camadas) | S8 | 1/2 | 1/2 | T07 Retenção por artefato e mascaramento de PII |
| Integridade do índice e da linhagem (Merkle, assinaturas) | S3/S6 | 2/1 | 2/1 | T05 Linhagem e traces por resposta |
| Conteúdo indexado como vetor de ataque (envenenamento, injeção) | Seg. | 1/1 | 1/1 | — |
| Custo como critério de decisão de dados | S2–S5 | 3/3 | 3/3 | — |

## Lista completa das 88 fontes finais

| Código | Tipo | Ano | Título | Decisão |
|---|---|---:|---|---|
| A02 | Acadêmica | 2026 | Distributed RAG Framework for Enterprise Systems | Adequada |
| A03 | Acadêmica | 2025 | EagerLog: Active Learning Enhanced Retrieval Augmented Generation for Log-based Anomaly Detection | Adequada |
| A04 | Acadêmica | 2026 | Grounded in Law: A Multi-Stage Anti-Hallucination Pipeline for Legal RAG Systems in Brazilian Portuguese | Adequada |
| A05 | Acadêmica | 2026 | How to Efficiently Explore Noisy Historical Data? Leveraging Corpus Pre-Targeting to Enhance Graph-based RAG | Adequada |
| A06 | Acadêmica | 2025 | NeuSym-RAG: Hybrid Neural Symbolic Retrieval with Multiview Structuring for PDF Question Answering | Adequada |
| A07 | Acadêmica | 2025 | Proof-Carrying Answers: A Systematic Protocol for Verifiable Retrieval-Augmented Generation with Cryptographic Provenance | Adequada |
| A08 | Acadêmica | 2025 | PUENYAI Bot: A Retrieval-Augmented LLM Chatbot for University Information Services | Adequada |
| A09 | Acadêmica | 2026 | Retrieval Enhancements for RAG: Insights from a Deployed Customer Support Chatbot | Adequada |
| A10 | Acadêmica | 2026 | Structure-Aware Retrieval-Augmented Generation for Regulatory Compliance: A Chatbot for the DOLE OSHS Handbook | Adequada |
| A12 | Acadêmica | 2026 | A RAG data pipeline transforming heterogeneous data into AI-ready format for autonomous building performance discovery | Adequada |
| A13 | Acadêmica | 2026 | Empirical Evaluation of PDF Parsing and Chunking for Financial Question Answering with RAG | Adequada |
| A14 | Acadêmica | 2026 | Engineering RAG Systems for Real-World Applications: Design, Development, and Evaluation | Adequada |
| A15 | Acadêmica | 2026 | Hallucination in Retrieval-Augmented Generation is a Context Construction Problem: A Constraint-Driven Cross-Modal Framework | Adequada |
| A16 | Acadêmica | 2026 | Index-State Uncertainty Quantification for Trustworthy Retrieval-Augmented Generation in Distributed Enterprise Search | Adequada |
| A17 | Acadêmica | 2026 | LAD-RAG: Layout-aware Dynamic RAG for Visually-Rich Document Understanding | Adequada |
| A18 | Acadêmica | 2025 | Towards Reliable Retrieval in RAG Systems for Large Legal Datasets | Adequada |
| A19 | Acadêmica | 2025 | Traceback of Poisoning Attacks to Retrieval-Augmented Generation | Adequada |
| A20 | Acadêmica | 2025 | A Hybrid SQL-RAG-LLM Question Answering System for Plastic Waste Management | Adequada |
| A21 | Acadêmica | 2026 | An LLM-Powered Intelligent Assistant for Learning Management Systems Using RAG and NL2SQL Pipelines | Adequada |
| A22 | Acadêmica | 2026 | Enterprise Search Portals: Hybrid RAG at Scale for Compliance-Sensitive Knowledge Work | Adequada |
| A23 | Acadêmica | 2026 | From PDF to RAG-Ready: Evaluating Document Conversion Frameworks for Domain-Specific Question Answering | Adequada |
| A24 | Acadêmica | 2025 | HAKES: Scalable Vector Database for Embedding Search Service | Adequada |
| A25 | Acadêmica | 2025 | Permission-Aware RAG: Identity and Access Management (IAM)-Based Access Filtering in Multi-Resource Environments | Adequada |
| A26 | Acadêmica | 2025 | Retrieval-Augmented Generation in Industry: An Interview Study on Use Cases, Requirements, Challenges, and Evaluation | Adequada |
| A29 | Acadêmica | 2025 | Cracking Vector Search Indexes | Adequada |
| A30 | Acadêmica | 2026 | Efficacy Evaluation and Optimization of RAG Knowledge Bases in the Oil and Gas Industry Using an LLM-as-a-Judge Mechanism | Adequada |
| A31 | Acadêmica | 2025 | Integrating Access Control with Retrieval-Augmented Generation: A Proof of Concept for Managing Sensitive Patient Profiles | Adequada |
| A32 | Acadêmica | 2026 | LindormVector: A Distributed Vector Engine on a Cloud-Native Multi-Model NoSQL Database | Adequada |
| A33 | Acadêmica | 2024 | MediRAG: Secure Question Answering for Healthcare Data | Adequada |
| A34 | Acadêmica | 2025 | MicroNN: An On-device Disk-resident Updatable Vector Database | Adequada |
| A35 | Acadêmica | 2026 | TTVI: A Two-Tier Vector Index for Low-WAL Approximate Nearest Neighbor Search in Databases | Adequada |
| A36 | Acadêmica | 2026 | Vector Databases Under Realistic Workloads: Filtered Search, Churn, and Warm-Restart Behavior | Adequada |
| A37 | Acadêmica | 2026 | Evaluation Methods for Inference-Time Retrieval-Augmented and Graph Retrieval-Augmented Large Language Models in Health Care: Scoping Review | Adequada |
| A39 | Acadêmica | 2025 | RAGulating Compliance: A Multi-Agent Schema-Light Knowledge Graph for Regulatory Compliance QA | Adequada |
| A40 | Acadêmica | 2026 | Retrieval-Augmented Generation At Enterprise Scale: Chunking Strategies, Vector Index Optimization, And Confidence-Calibrated Retrieval For Mission-Critical LLM Applications | Adequada |
| A42 | Acadêmica | 2026 | Token-Budget-Aware Context Selection for RAG Via Integer Linear Programming | Adequada |
| A43 | Acadêmica | 2026 | Adaptive Data Flywheel: Applying MAPE Control Loops to AI Agent Improvement | Adequada |
| A44 | Acadêmica | 2026 | An Empirical Study of Knowledge Graph-Enhanced RAG for Information Security Compliance | Adequada |
| A45 | Acadêmica | 2025 | Enterprise Memory Architecture for Agentic AI (EMA2): A Policy-Aware, Provenance-First, Multi-Tier Memory Stack for Long-Horizon Agents | Adequada |
| A46 | Acadêmica | 2025 | Is Semantic Chunking Worth the Computational Cost? | Adequada |
| A47 | Acadêmica | 2026 | Retrieval Granularity as Evidence Design in Small-Model RAG Question Answering: A Diagnostic HotpotQA Study | Adequada |
| A48 | Acadêmica | 2026 | A Systematic Analysis of Chunking Strategies for Reliable Question Answering | Adequada |
| A49 | Acadêmica | 2026 | Adaptive Chunking: Optimizing Chunking-Method Selection for RAG | Adequada |
| A51 | Acadêmica | 2026 | HiChunk: Evaluating and Enhancing Retrieval Augmented Generation with Hierarchical Chunking | Adequada |
| A52 | Acadêmica | 2026 | Mitigating Context Loss in Legal RAG: A Metadata-Aware Chunking Strategy for Hierarchical Indian Statutes | Adequada |
| A53 | Acadêmica | 2025 | MoC: Mixtures of Text Chunking Learners for Retrieval-Augmented Generation System | Adequada |
| A55 | Acadêmica | 2025 | cAST: Enhancing Code Retrieval-Augmented Generation with Structural Chunking via Abstract Syntax Tree | Adequada |
| A56 | Acadêmica | 2026 | FreeChunker: A Cross-Granularity Chunking Framework | Adequada |
| A58 | Acadêmica | 2026 | Policy-Aware RAG on the Lakehouse: Lineage-Driven Retrieval Over Apache Iceberg on S3 to Reduce Hallucination and Cost | Adequada |
| A59 | Acadêmica | 2026 | Reconstructing Context: Evaluating Advanced Chunking Strategies for Retrieval-Augmented Generation | Adequada |
| A60 | Acadêmica | 2026 | Utilizing Metadata for Better Retrieval-Augmented Generation | Adequada |
| C01 | Cinzenta | 2026 | Solving the Erasure / Receipt Trilemma in AI Memory and RAG | Incluída |
| C02 | Cinzenta | 2026 | How to Make RAG Show Its Evidence: Claim Verification at 15M-Document Scale | Incluída |
| C03 | Cinzenta | 2026 | RAG Retrieval Strategies on a 50k-Document Dataset: BM25 vs Dense vs Hybrid | Incluída |
| C04 | Cinzenta | 2026 | RAG Has a Routing Problem: Knowing Which Knowledge Source to Trust | Incluída |
| C05 | Cinzenta | 2026 | We Deleted Our Vector Database. Postgres Was Faster. | Incluída |
| C06 | Cinzenta | 2026 | Building a Production RAG Pipeline with n8n, Qdrant, and Gemini: A Step-by-Step Walkthrough | Incluída |
| C07 | Cinzenta | 2026 | Building a Production-Grade Hybrid RAG System | Incluída |
| C08 | Cinzenta | 2026 | My RAG Pipeline Got Hijacked by Retrieved Text: An Accidental Prompt Injection | Incluída |
| C09 | Cinzenta | 2026 | We cut RAG costs 5x without losing quality | Incluída com restrição (sem uso de números ilustrativos/marketing) |
| C10 | Cinzenta | 2026 | Data Privacy in RAG Redaction and Retention [2026 Playbook] | Incluída |
| C11 | Cinzenta | 2026 | Lessons We Learned Building a RAG Assistant Without a Separate Vector Database | Incluída |
| C12 | Cinzenta | 2026 | RAG Series (19): Incremental Updates — Keeping the Knowledge Base Fresh | Incluída |
| C13 | Cinzenta | 2026 | Building a RAG Evaluation Harness That Actually Catches Problems | Incluída |
| C14 | Cinzenta | 2026 | Observability for AI Systems with OpenTelemetry | Incluída |
| C15 | Cinzenta | 2026 | 15 Engineering Decisions Behind RAG Hybrid Search | Incluída |
| C16 | Cinzenta | 2026 | I Updated My Embedding Model and My RAG Broke: A Post-Mortem | Incluída com restrição (sem uso de números ilustrativos/marketing) |
| C17 | Cinzenta | 2026 | Monitor RAG Data Source Quality | Incluída com restrição (sem uso de números ilustrativos/marketing) |
| C18 | Cinzenta | 2025 | We built a world‑class reranker for RAG | Incluída |
| C19 | Cinzenta | 2025 | LLM Rerankers for RAG: A Practical Guide | Incluída |
| C20 | Cinzenta | 2025 | OCR and RAG for Tables | Incluída |
| C21 | Cinzenta | 2025 | The Ceiling: How OCR Quality Limits RAG Performance | Incluída com restrição (sem uso de números ilustrativos/marketing) |
| C22 | Cinzenta | 2025 | Roaming RAG – RAG without the vector DB | Incluída |
| C23 | Cinzenta | 2025 | Evaluating the evaluators: know your RAG metrics | Incluída |
| C24 | Cinzenta | 2024 | Exploring Semantic Chunking for RAG | Incluída |
| C25 | Cinzenta | 2024 | Is your RAG Reranker not helping? This might be why | Incluída |
| C26 | Cinzenta | 2024 | Scaling LLM Data Extraction: Challenges, Design Decisions, and Solutions | Incluída |
| C27 | Cinzenta | 2024 | Breaking up is hard to do: Chunking in RAG applications | Incluída |
| C28 | Cinzenta | 2024 | Better RAG Results with Reciprocal Rank Fusion and Hybrid Search | Incluída |
| C29 | Cinzenta | 2025/2026 | Design and develop a RAG solution (série: preparation / chunking / enrichment / embedding / information retrieval / LLM evaluation) | Incluída |
| C30 | Cinzenta | 2025 | Authorizing access to data with RAG implementations | Incluída |
| C31 | Cinzenta | 2025/2026 | RAG-capable generative AI application using Vertex AI | Incluída |
| C32 | Cinzenta | 2026 | RAG data pipeline (fundamentals + build an unstructured data pipeline) | Incluída |
| C33 | Cinzenta | 2025 | Finding the Best Chunking Strategy for Accurate AI Responses | Incluída |
| C34 | Cinzenta | 2024 | RAG Cookbook — chunking and data ingestion | Incluída |
| C35 | Cinzenta | 2025 | Enhanced Agentic-RAG: What If Chatbots Could Deliver Near-Human Precision? | Incluída |
| C36 | Cinzenta | 2024 | Advanced RAG techniques part 1: data processing | Incluída |
| C37 | Cinzenta | 2025 | Chunking Strategies for LLM Applications | Incluída |

## Cronograma original

O cronograma abaixo registra o planejamento histórico do semestre 2026.2.

| Mês | Frente de trabalho | Atividades principais |
|---|---|---|
| Julho e agosto | Planejamento da MLR | Definição do protocolo, das famílias de busca e dos critérios de seleção; preparação das strings para fontes acadêmicas e cinzentas. |
| Setembro | Busca e triagem acadêmicas | Coleta na Scopus e na ACL Anthology (23/09) e consolidação dos manifestos (24/09); pré-triagem pelo modelo de linguagem, oito rodadas de decisão humana (25 a 27/09) e *backward snowballing*. |
| Outubro | Estratégia da literatura cinzenta | Definição das frentes de recuperação, dos critérios de seleção dos portais e da rastreabilidade das consultas. |
| Novembro | Avaliação, busca cinzenta e extração | Obtenção dos textos integrais, aplicação de E5 e avaliação de qualidade das fontes acadêmicas; recuperação e seleção da literatura cinzenta (13/11) e avaliação de qualidade; extração das evidências e conferência das sugestões do modelo pelos pesquisadores. |
| Dezembro | Síntese, discussão e redação | Organização das práticas por etapa, análise das adaptações e desafios e comparação entre literatura acadêmica e cinzenta para responder à QP3; discussão das convergências, divergências, lacunas e limites da revisão e revisão final da monografia. |

As localizações e os excertos de cada evidência constam da aba Evidencias.
