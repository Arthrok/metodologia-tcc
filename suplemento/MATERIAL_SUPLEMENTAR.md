# Material suplementar — revisão multivocal de Engenharia de Dados em RAG

Arquivo complementar ao manuscrito *Engenharia de Dados em Sistemas RAG: Práticas, Desafios e Adaptações*. O corpus final contém 88 fontes e 244 evidências. Os registros de seleção, extração e auditoria estão disponíveis nos arquivos abaixo.

## Índice dos registros consolidados

- [Decisões finais do corpus](consolidado/AUDITORIA_DECISOES_CORPUS.csv): uma linha por fonte acadêmica, candidata cinzenta avaliada no texto integral e candidato priorizado do *forward snowballing*, com avaliador atribuído e decisão final.
- [Planilha de extração acadêmica](extracao/Extracao_preenchida_r009.xlsx) e [planilha da literatura cinzenta](cinzenta/Literatura_cinzenta_r009.xlsx): registro de consultas, triagem dos 210 candidatos, notas QA/QG, excertos e os 34 temas iniciais da QP3.
- Rastreabilidade entre evidências e tabelas (gerada por `scripts/rastreabilidade/gerar_rastreabilidade.py`):
  - [evidencias_244.csv](consolidado/rastreabilidade/evidencias_244.csv): as 244 evidências válidas com identificador estável (por exemplo, `C05-e02`), etapa, prática, localização e excerto;
  - [evidencia_para_tabelas.csv](consolidado/rastreabilidade/evidencia_para_tabelas.csv): em que linhas das Tabelas QP1–QP3 cada evidência aparece;
  - [qp1_vinculo_celula_evidencias.csv](consolidado/rastreabilidade/qp1_vinculo_celula_evidencias.csv), [qp2_vinculo_linha_evidencias.csv](consolidado/rastreabilidade/qp2_vinculo_linha_evidencias.csv) e [qp3_codificacao_evidencia_tema.csv](consolidado/rastreabilidade/qp3_codificacao_evidencia_tema.csv): vínculos por tabela;
  - [qp3_tabela19_frequencias.csv](consolidado/rastreabilidade/qp3_tabela19_frequencias.csv) e [qp3_correspondencia_34_temas.csv](consolidado/rastreabilidade/qp3_correspondencia_34_temas.csv): frequências da Tabela 19 e correspondência com os 34 temas da planilha;
  - [auditoria_humana_registro.csv](consolidado/rastreabilidade/auditoria_humana_registro.csv) e [auditoria_humana_itens.csv](consolidado/rastreabilidade/auditoria_humana_itens.csv): base documental das conferências declaradas na seção 3.3.7.
- Execução da literatura cinzenta: [exclusões da pré-triagem](consolidado/auditoria_cinzenta/1_pretriagem_exclusoes.csv), [inventário das 61 candidatas](consolidado/auditoria_cinzenta/2_inventario_61.csv), notas QG das [incluídas](consolidado/auditoria_cinzenta/4_qg_incluidas.csv) e [excluídas](consolidado/auditoria_cinzenta/4_qg_excluidas.csv) e [verificação literal dos 65 excertos](consolidado/auditoria_cinzenta/5_evidencias_65.csv).
- Documentos de trabalho anteriores à consolidação: [matriz de evidências](consolidado/MATRIZ_EVIDENCIAS_TCC.md), [auditoria e síntese transversal](consolidado/AUDITORIA_E_SINTESE_TRANSVERSAL.md) e [conferência da QP2 e dos casos próximos ao corte](consolidado/CONFERENCIA_QP2_E_CORTE.md). Quando divergirem dos arquivos de rastreabilidade, prevalecem estes.

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

O *backward snowballing* recuperou 905 registros: 845 novos, 58 coincidentes com buscas diretas e 2 duplicatas internas ou registros sem metadados mínimos, descartados antes da deduplicação. O *forward snowballing* recuperou 426 citantes: 26 já no corpus e 400 novos. Dos novos, 95 foram priorizados e 305 não priorizados; nenhum foi incorporado nesta execução por corte temporal e de escopo. Consulte [citantes.json](data/snowball_forward/citantes.json) e [pretriagem_forward.csv](data/snowball_forward/pretriagem_forward.csv).

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

O registro complementar de objetividade indicou quando uma fonte cinzenta promovia produto ou serviço do próprio autor ou organização, sem alterar a pontuação. As notas finais e restrições de uso constam na [auditoria do corpus](consolidado/AUDITORIA_DECISOES_CORPUS.csv).

## Decisões da auditoria final

A57 foi rebaixada para QA abaixo de 4,0 e excluída do corpus. A01, A11, A27, A28, A38, A41, A50 e A54 também ficaram fora da síntese. C09, C16, C17 e C21 foram incluídas com restrição de uso numérico: seus valores ilustrativos, promocionais ou não comparáveis não sustentam resultados empíricos. As decisões individuais constam em [AUDITORIA_DECISOES_CORPUS.csv](consolidado/AUDITORIA_DECISOES_CORPUS.csv).

## Execução da seleção da literatura cinzenta

As três frentes (DEV Community, Hacker News e portais institucionais) resultaram em 210 candidatos únicos após a consolidação pela URL. Os 198 candidatos das APIs passaram por pré-triagem conduzida com apoio de inteligência artificial, que sugeriu classificações de elegibilidade a partir do título e da descrição; as 12 páginas dos portais, escolhidas nas buscas dirigidas, seguiram diretamente para a avaliação do texto integral. Foram excluídos 149 registros por E3 ou E4, e 61 candidatas foram encaminhadas à avaliação do texto integral. As sugestões automatizadas foram posteriormente examinadas por Eric, com apoio de uma segunda ferramenta de IA; ele foi responsável pela revisão da filtragem e pelas decisões finais de seleção. Das 61 candidatas, 37 foram incluídas e 24 excluídas (QG < 4: 9; E4: 6; E5: 3; I1: 3; QG1 = 0: 2; QG6 = 0: 1). Duas páginas inacessíveis no endereço original foram avaliadas a partir de cópias do Internet Archive.

A revisão humana foi realizada durante o processo de pesquisa, sem a produção de um registro individualizado das concordâncias e divergências em relação às sugestões automatizadas. Essa característica limita a reconstrução retrospectiva de cada decisão, embora os registros de candidatos, critérios, classificações e resultados finais tenham sido preservados. As notas QG da planilha mantêm a marcação de sugestão do modelo. Os 65 excertos cinzentos foram verificados automaticamente contra os textos arquivados: todos constam literalmente deles. Essa verificação atesta a correspondência textual, não a adequação da etapa, da prática ou da adaptação atribuídas.

## Base documental da auditoria humana (seção 3.3.7)

A [divisão nominal](consolidado/AUDITORIA_DECISOES_CORPUS.csv) atribuiu 115 registros a Eric (41 cinzentos, 20 acadêmicos e 54 do *forward snowballing*) e 101 a Arthur (20 cinzentos, 40 acadêmicos e 41 do *forward snowballing*). Os 20 casos próximos dos cortes QA=4,0/4,5 e QG=4,0/4,5 (seis acadêmicos e 14 cinzentos) e as fontes de cada adaptação da Tabela 18 estão listados em [auditoria_humana_itens.csv](consolidado/rastreabilidade/auditoria_humana_itens.csv), com avaliador atribuído, decisão final e evidências. O [registro de base documental](consolidado/rastreabilidade/auditoria_humana_registro.csv) indica, para cada afirmação da seção 3.3.7, o arquivo que a documenta e o que ele não documenta. Os efeitos da conferência estão registrados no arquivo de decisões: o rebaixamento de A57 e a restrição de uso numérico de C09, C16, C17 e C21. A conferência não produziu registro individualizado do que foi confirmado ou alterado em cada nota, excerto ou adaptação.

## Rastreabilidade entre evidências e Tabelas QP1–QP3

Cada evidência válida recebeu o identificador `<fonte>-e<NN>`, na ordem da ficha de extração. Na QP1 (Tabela 17), cada ID de uma célula remete às evidências da fonte codificadas na etapa da linha; o gerador recusa célula sem essa evidência. Na QP2 (Tabela 18), cada linha remete às evidências que sustentam a adaptação. Na QP3 (Tabela 19), cada tema remete às evidências codificadas nele, segundo a definição operacional abaixo; uma evidência pode integrar mais de um tema. A codificação final foi consolidada com apoio do modelo de linguagem a partir das fichas de extração e pode ser conferida pelo identificador de cada evidência.

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

As fichas e localizações dos excertos constam na [matriz de evidências](consolidado/MATRIZ_EVIDENCIAS_TCC.md) e na [conferência da QP2 e dos casos próximos ao corte](consolidado/CONFERENCIA_QP2_E_CORTE.md).

## Tabela integral QP1 anterior à compactação editorial

Versão histórica, gerada antes da codificação final das evidências. Para o vínculo entre evidências e a tabela publicada, consulte a seção de rastreabilidade acima.

```latex
\begin{longtable}{p{3.1cm}p{3.1cm}lp{2.1cm}lp{1.8cm}}
\caption{QP1: práticas e menções por etapa; fichas e localizações na matriz de evidências.}\label{tab:qp1-sintese}\\
\toprule
\textbf{Prática} & \textbf{Finalidade} & \textbf{Etapa} & \textbf{IDs validados} & \textbf{Tipo} & \textbf{Localização} \\
\midrule
\endfirsthead
\toprule
\textbf{Prática} & \textbf{Finalidade} & \textbf{Etapa} & \textbf{IDs validados} & \textbf{Tipo} & \textbf{Localização} \\
\midrule
\endhead
Propriedade e armazenamento locais de documentos e índices por domínio (federação) & Arquitetura em três camadas: nós locais, gateways regionais, roteamento/inferência na nuvem & S3 & A02 & Acadêmica & p.1 (Resumo/Introdução) \\
Catálogo de metadados dos índices (domínio, modelo de embedding, latência) e aplicação local de políticas & Roteador com escore custo-sensível (relevância − latência) treinado em logs & S3 & A02 & Acadêmica & p.3 (Gateways) \\
Catálogo de metadados dos índices (domínio, modelo de embedding, latência) e aplicação local de políticas & Roteador com escore custo-sensível (relevância − latência) treinado em logs & S5 & A02 & Acadêmica & p.3 (Gateways) \\
Compressão (PQ) e ruído de privacidade diferencial em embeddings trocados entre fronteiras & σ de ruído DP configurável (0,3–0,5) & S4 & A02 & Acadêmica & p.4–5 \\
Compressão (PQ) e ruído de privacidade diferencial em embeddings trocados entre fronteiras & σ de ruído DP configurável (0,3–0,5) & S5 & A02 & Acadêmica & p.4–5 \\
Propagar proveniência e metadados com os trechos; mascaramento pós-geração; logs para monitoramento & Logs usados também para treinar o roteador & S5 & A02 & Acadêmica & p.4 \\
Propagar proveniência e metadados com os trechos; mascaramento pós-geração; logs para monitoramento & Logs usados também para treinar o roteador & S6 & A02 & Acadêmica & p.4 \\
Reconhecer a obsolescência da base de conhecimento quando o sistema-fonte muda & Base de conhecimento dinâmica que cresce durante a operação & S7 & A03 & Acadêmica & p.1 (Introdução) \\
Semente pequena e verificada manualmente da base de conhecimento & Iniciar com 10 exemplos verificados em vez de seleção não supervisionada (aleatória/cluster) & S1 & A03 & Acadêmica & p.3 (Active Learning) \\
Atualização incremental da base guiada pela incerteza do LLM, com rotulação humana seletiva (humano no laço) & Limiares de seleção (st) e de rotulação (lt) sobre a incerteza & S6 & A03 & Acadêmica & p.3 \\
Atualização incremental da base guiada pela incerteza do LLM, com rotulação humana seletiva (humano no laço) & Limiares de seleção (st) e de rotulação (lt) sobre a incerteza & S7 & A03 & Acadêmica & p.3 \\
Ponderação por campo (resumo > texto integral) e filtragem por metadados na recuperação & BM25 por campo + filtros de metadados + embeddings de domínio + reranking com limiar & S4 & A04 & Acadêmica & p.2 (Seção 3.1) \\
Ponderação por campo (resumo > texto integral) e filtragem por metadados na recuperação & BM25 por campo + filtros de metadados + embeddings de domínio + reranking com limiar & S5 & A04 & Acadêmica & p.2 (Seção 3.1) \\
Armazenamento estruturado por fragmento com metadados temporais, separado do índice vetorial & Separar legislação (banco relacional) de jurisprudência/editorial (índice vetorial/léxico) & S3 & A04 & Acadêmica & p.2–3 (Seção 3.1 e Etapa 3) \\
Normalização canônica e validação das citações da resposta contra fontes oficiais (auditoria pós-geração) & Status por referência + reescrita limitada a 2 iterações para controlar latência & S6 & A04 & Acadêmica & p.3 (Etapas 2–3) \\
Trilhas de auditoria por resposta e mascaramento de dados pessoais (LGPD) & Transformar alucinação silenciosa em aviso explícito por referência & S6 & A04 & Acadêmica & p.4 \\
Pré-seleção do corpus antes da indexação (pre-targeting) em vez de indexação integral & Filtragem positiva (perguntas simples) ou negativa (multi-hop) conforme o tipo de pergunta & S1 & A05 & Acadêmica & p.1 (Introdução) e p.3 \\
Pré-seleção do corpus antes da indexação (pre-targeting) em vez de indexação integral & Filtragem positiva (perguntas simples) ou negativa (multi-hop) conforme o tipo de pergunta & S3 & A05 & Acadêmica & p.1 (Introdução) e p.3 \\
Estimar a qualidade do OCR por heurística antes de indexar & Heurística de palavras suspeitas (longas, dígitos misturados, caracteres não franceses) & S2 & A05 & Acadêmica & p.4 \\
Remoção de documentos de baixa densidade informacional antes da indexação & Limiar de proporção de stopwords; exclusão de documentos sempre mal ranqueados & S1 & A05 & Acadêmica & p.5 \\
Remoção de documentos de baixa densidade informacional antes da indexação & Limiar de proporção de stopwords; exclusão de documentos sempre mal ranqueados & S4 & A05 & Acadêmica & p.5 \\
Calibração de limiares de filtragem por coleção & — & S1 & A05 & Acadêmica & p.6 (Discussão) \\
Chunking multivisão (página, seção, tamanho fixo) + elementos paratextuais & Manter várias granularidades em paralelo & S4 & A06 & Acadêmica & p.1 (Introdução) \\
Pipeline de parsing orientado a esquema relacional fixo, com enriquecimento de metadados por APIs externas & Banco relacional (DuckDB) como representação canônica do documento & S2 & A06 & Acadêmica & p.2 (Seção 2.2) \\
Ligação 1:1 entre vetor e registro de origem e metadados de filtragem por documento/página & Coleções separadas por modelo de codificação e modalidade & S3 & A06 & Acadêmica & p.3 (Seção 2.3) \\
Ligação 1:1 entre vetor e registro de origem e metadados de filtragem por documento/página & Coleções separadas por modelo de codificação e modalidade & S5 & A06 & Acadêmica & p.3 (Seção 2.3) \\
Índice vetorial autenticado (Merkle + assinaturas) com versionamento do corpus à prova de adulteração & Cada chunk assinado e incluído em árvore de Merkle comprometida por versão & S3 & A07 & Acadêmica & p.1–2 (Contribuições) \\
Índice vetorial autenticado (Merkle + assinaturas) com versionamento do corpus à prova de adulteração & Cada chunk assinado e incluído em árvore de Merkle comprometida por versão & S7 & A07 & Acadêmica & p.1–2 (Contribuições) \\
Contrato de admissibilidade: só liberar resposta com evidência verificada; caso contrário, abster-se & Política de verificação parcial (descarta chunks não verificados, responde com os verificados) & S5 & A07 & Acadêmica & p.1 e p.6 (Tabela III) \\
Contrato de admissibilidade: só liberar resposta com evidência verificada; caso contrário, abster-se & Política de verificação parcial (descarta chunks não verificados, responde com os verificados) & S6 & A07 & Acadêmica & p.1 e p.6 (Tabela III) \\
Validação semântica do conteúdo na ingestão, antes do commit do corpus & Combinar proveniência criptográfica com verificação semântica (trabalho futuro) & S2 & A07 & Acadêmica & p.4 e p.9 \\
Inventário de dados, responsáveis pela atualização, cadência de atualização e procedimentos de rollback & Equipe designada para curar fontes, acompanhar métricas e confirmar respostas & S1 & A08 & Acadêmica & p.3 (Segurança e governança) \\
Inventário de dados, responsáveis pela atualização, cadência de atualização e procedimentos de rollback & Equipe designada para curar fontes, acompanhar métricas e confirmar respostas & S7 & A08 & Acadêmica & p.3 (Segurança e governança) \\
Chunking semântico (não por contagem de caracteres) para listas e tabelas & Chunking semântico + reranking para páginas longas & S4 & A08 & Acadêmica & p.4 (Lições) e p.5 \\
Curadoria de fontes canônicas para fechar lacunas de cobertura & Nomear fontes canônicas; páginas sem PDF exigem extração manual (p.3) & S1 & A08 & Acadêmica & p.5 \\
Curadoria de fontes canônicas para fechar lacunas de cobertura & Nomear fontes canônicas; páginas sem PDF exigem extração manual (p.3) & S7 & A08 & Acadêmica & p.5 \\
Console administrativo para upload, reindexação e rollback; logs mínimos e amostragem semanal de respostas & Observabilidade básica (tempos + logs mínimos) basta para detectar regressões (p.4) & S6 & A08 & Acadêmica & p.5 (Passos de escala) \\
Console administrativo para upload, reindexação e rollback; logs mínimos e amostragem semanal de respostas & Observabilidade básica (tempos + logs mínimos) basta para detectar regressões (p.4) & S7 & A08 & Acadêmica & p.5 (Passos de escala) \\
Diagnosticar o gargalo pela métrica de recuperação (gap Recall@10 × Recall@50) antes de mexer no gerador & Priorizar melhorias de recuperação/reranking & S5 & A09 & Acadêmica & p.1 e p.6 (Resultados) \\
Diagnosticar o gargalo pela métrica de recuperação (gap Recall@10 × Recall@50) antes de mexer no gerador & Priorizar melhorias de recuperação/reranking & S6 & A09 & Acadêmica & p.1 e p.6 (Resultados) \\
Chunking com consciência de layout e escolha de tamanho de chunk por experimento & Chunks de 2048 tokens; parser com consciência de layout & S2 & A09 & Acadêmica & p.3 (Datasets) e p.4 (Seção 4.3) \\
Chunking com consciência de layout e escolha de tamanho de chunk por experimento & Chunks de 2048 tokens; parser com consciência de layout & S4 & A09 & Acadêmica & p.3 (Datasets) e p.4 (Seção 4.3) \\
Fusão de rankings (RRF) entre modelos de embedding; teste de reranking por cross-encoder × LLM & Combinar dois embeddings densos; reranking por LLM sobre top-50 & S5 & A09 & Acadêmica & p.5 (Tabelas 3–4) \\
Usar falhas de reranking como casos de avaliação para ajustar o prompt (ciclo de feedback) & Meta-prompting com exemplos difíceis do conjunto de treino & S6 & A09 & Acadêmica & p.6 \\
Filtro de chunks ruidosos e deduplicação por identificador da regra antes da vetorização & Chunking recursivo com sobreposição; regra mínima de 10 palavras; chave (rule\_id, texto) & S4 & A10 & Acadêmica & p.3 (Pré-processamento) \\
Preservar a hierarquia do documento e converter tabelas para Markdown & Pipeline de pré-processamento orientado à estrutura & S2 & A10 & Acadêmica & p.1 (Resumo) \\
Preservar a hierarquia do documento e converter tabelas para Markdown & Pipeline de pré-processamento orientado à estrutura & S4 & A10 & Acadêmica & p.1 (Resumo) \\
Avaliação separada de recuperação e geração com métricas RAGAS & — & S6 & A10 & Acadêmica & p.1 e Conclusão \\
Normalização de codificação, chunking com sobreposição e resumo por documento com metadados indexado junto aos chunks & Dois níveis de representação (chunk fino + resumo do documento) & S2 & A12 & Acadêmica & p.4 (Texto simples) \\
Normalização de codificação, chunking com sobreposição e resumo por documento com metadados indexado junto aos chunks & Dois níveis de representação (chunk fino + resumo do documento) & S4 & A12 & Acadêmica & p.4 (Texto simples) \\
Extração de imagens e tabelas por prompts de domínio com saída em esquema estruturado & Processadores específicos por tipo de artefato & S2 & A12 & Acadêmica & p.6 e p.9 (Resultados) \\
Extração de imagens e tabelas por prompts de domínio com saída em esquema estruturado & Processadores específicos por tipo de artefato & S4 & A12 & Acadêmica & p.6 e p.9 (Resultados) \\
Filtragem por etiquetas de proveniência (seção, página) após a busca top-k & k=10 e similaridade mínima & S5 & A12 & Acadêmica & p.8 (Política de recuperação) \\
Busca sistemática em grade da configuração da cadeia (embedding, chunk, sobreposição, busca, reranking) & Padrão recomendado: Gemini Embeddings + MMR + cross-encoder; sobreposição de 10–15\% & S4 & A12 & Acadêmica & p.10–11 e p.28 (Apêndice) \\
Busca sistemática em grade da configuração da cadeia (embedding, chunk, sobreposição, busca, reranking) & Padrão recomendado: Gemini Embeddings + MMR + cross-encoder; sobreposição de 10–15\% & S5 & A12 & Acadêmica & p.10–11 e p.28 (Apêndice) \\
— & Automação do pipeline de preparação & S2 & A12 & Acadêmica & p.1–2 (Introdução) \\
Avaliar parser e chunker em conjunto como parte da qualidade do pipeline & Experimento fatorial completo parser × chunker & S2 & A13 & Acadêmica & p.1–2 (Introdução) \\
Avaliar parser e chunker em conjunto como parte da qualidade do pipeline & Experimento fatorial completo parser × chunker & S4 & A13 & Acadêmica & p.1–2 (Introdução) \\
Considerar custo de parsing (tempo por página) na escolha do parser & Parsers leves frequentemente equivalem aos complexos & S2 & A13 & Acadêmica & p.7 (RQ2c) \\
Sobreposição moderada de chunks (25\%) e evitar granularidade excessiva & 512 tokens com 25\% de sobreposição & S4 & A13 & Acadêmica & p.8 (Tabela 9) e p.9 (RQ3b) \\
Escolher o recuperador conforme o tipo de conteúdo/consulta (texto × tabela) & E5 para texto; ColBERT para tabelas; SPLADE como compromisso & S5 & A13 & Acadêmica & p.6–7 (Tabela 6) \\
Limpeza de ruído de OCR e deduplicação na origem & Tesseract/easyOCR + limpeza por regex & S2 & A14 & Acadêmica & p.12 (6.1–6.2) \\
Limpeza de ruído de OCR e deduplicação na origem & Tesseract/easyOCR + limpeza por regex & S4 & A14 & Acadêmica & p.12 (6.1–6.2) \\
Calibrar tamanho de chunk e usar filtro por metadados (tipo de documento) para reduzir o espaço de busca & Chunks de 200–500 tokens; filtro por tipo de documento & S3 & A14 & Acadêmica & p.12 (6.1) \\
Calibrar tamanho de chunk e usar filtro por metadados (tipo de documento) para reduzir o espaço de busca & Chunks de 200–500 tokens; filtro por tipo de documento & S4 & A14 & Acadêmica & p.12 (6.1) \\
Calibrar tamanho de chunk e usar filtro por metadados (tipo de documento) para reduzir o espaço de busca & Chunks de 200–500 tokens; filtro por tipo de documento & S5 & A14 & Acadêmica & p.12 (6.1) \\
Manutenção contínua de conectores/scrapers de ingestão & Feeds semiestruturados e manutenção regular de scripts & S2 & A14 & Acadêmica & p.12 (6.2) \\
Manutenção contínua de conectores/scrapers de ingestão & Feeds semiestruturados e manutenção regular de scripts & S7 & A14 & Acadêmica & p.12 (6.2) \\
Registrar perguntas, respostas e avaliações dos usuários e usá-las para ajustar a recuperação e o chunking & Armazenamento leve (SQLite) de interações & S6 & A14 & Acadêmica & p.12 (6.2) \\
Hospedagem própria por conformidade; citar a fonte (arquivo e link) na resposta; tratar desbalanceamento de fontes & Reranking para diversidade; ocultar fontes em domínios sensíveis & S1 & A14 & Acadêmica & p.12 (6.2–6.3) \\
Hospedagem própria por conformidade; citar a fonte (arquivo e link) na resposta; tratar desbalanceamento de fontes & Reranking para diversidade; ocultar fontes em domínios sensíveis & S3 & A14 & Acadêmica & p.12 (6.2–6.3) \\
Hospedagem própria por conformidade; citar a fonte (arquivo e link) na resposta; tratar desbalanceamento de fontes & Reranking para diversidade; ocultar fontes em domínios sensíveis & S5 & A14 & Acadêmica & p.12 (6.2–6.3) \\
Metadados estruturais por unidade de evidência (documento, página, modalidade, título pai, tabela, parte) & Esquema de metadados que permite reconstruir objetos multipartes & S3 & A15 & Acadêmica & p.3 (Ingestão) \\
Metadados estruturais por unidade de evidência (documento, página, modalidade, título pai, tabela, parte) & Esquema de metadados que permite reconstruir objetos multipartes & S4 & A15 & Acadêmica & p.3 (Ingestão) \\
Chunking de tabelas por linha com ID estável, faixa de linhas e contexto (título e texto anterior) & Fallback para chunking por tokens mantendo o tipo 'tabela' & S4 & A15 & Acadêmica & p.4 (Tabelas) \\
Filtrar segmentos de baixa informação e normalizar texto antes de indexar & Regras heurísticas de filtragem & S4 & A15 & Acadêmica & p.4 \\
Empacotamento do contexto sob orçamento de tokens, com expansão por grafo e poda intermodal & Seleção de segmentos com penalidade para chunks irrelevantes & S5 & A15 & Acadêmica & p.1 (Resumo) e p.6 \\
Tratar o estado do índice (atraso, divergência, frescor) como dimensão de qualidade monitorada & Middleware ISUQ com escore de confiança do índice (ICS) & S3 & A16 & Acadêmica & p.1 (Introdução) \\
Tratar o estado do índice (atraso, divergência, frescor) como dimensão de qualidade monitorada & Middleware ISUQ com escore de confiança do índice (ICS) & S7 & A16 & Acadêmica & p.1 (Introdução) \\
Ações de recuperação automáticas guiadas pelo estado do índice (refresh de shard, renormalização, busca mais ampla) & Limiar θ=0,40 (23\% das consultas roteadas para recuperação) & S5 & A16 & Acadêmica & p.4 \\
Ações de recuperação automáticas guiadas pelo estado do índice (refresh de shard, renormalização, busca mais ampla) & Limiar θ=0,40 (23\% das consultas roteadas para recuperação) & S7 & A16 & Acadêmica & p.4 \\
Propagar o sinal de confiança da fonte/índice até a geração & Token de confiança no prompt do sistema & S5 & A16 & Acadêmica & p.4 \\
Propagar o sinal de confiança da fonte/índice até a geração & Token de confiança no prompt do sistema & S6 & A16 & Acadêmica & p.4 \\
Dependência de metadados operacionais do índice (timestamps de replicação) & — & S3 & A16 & Acadêmica & p.5–6 (Limitações) \\
Representar a estrutura e as dependências entre páginas na ingestão (grafo do documento) & Grafo simbólico + índice neural lado a lado & S2 & A17 & Acadêmica & p.1 (Introdução) \\
Representar a estrutura e as dependências entre páginas na ingestão (grafo do documento) & Grafo simbólico + índice neural lado a lado & S4 & A17 & Acadêmica & p.1 (Introdução) \\
Deslocar o custo de estruturação para a ingestão offline & Pré-computar o grafo; recuperação dinâmica sem top-k fixo & S3 & A17 & Acadêmica & p.7 (Latência) \\
Deslocar o custo de estruturação para a ingestão offline & Pré-computar o grafo; recuperação dinâmica sem top-k fixo & S5 & A17 & Acadêmica & p.7 (Latência) \\
Extração de elementos (texto, tabelas, figuras) por modelo multimodal & OCR tradicional ou modelos menores podem baratear o parsing inicial & S2 & A17 & Acadêmica & p.10 (Limitações) \\
Medir a falha de recuperação do documento errado (DRM) como métrica de qualidade & Métrica DRM + precisão/recall por caractere & S4 & A18 & Acadêmica & p.3 \\
Enriquecer cada chunk com resumo do documento de origem (metadado sintético) & Chunking recursivo + prefixo de resumo; só recuperação densa & S4 & A18 & Acadêmica & p.5 (Pipeline) \\
Avaliar busca híbrida (BM25 + densa) contra as métricas de falha & Manter apenas a recuperação densa & S5 & A18 & Acadêmica & p.6 e p.12 (Apêndice B) \\
Preferir resumos genéricos a resumos especializados para guiar o recuperador & Resumo genérico & S4 & A18 & Acadêmica & p.9 (Conclusão) \\
Forense de dados: rastrear até a fonte e o pipeline de coleta comprometidos & Priorizar rastreamento a defesas cada vez mais complexas & S1 & A19 & Acadêmica & p.2 (Introdução) \\
Forense de dados: rastrear até a fonte e o pipeline de coleta comprometidos & Priorizar rastreamento a defesas cada vez mais complexas & S2 & A19 & Acadêmica & p.2 (Introdução) \\
Feedback do usuário como gatilho de investigação da base & Recuperação iterativa + LLM juiz com prompt específico & S6 & A19 & Acadêmica & p.3 (Cenário) \\
Remoção de textos envenenados da base (descarte) com verificação da correção & Remover, reenviar a consulta e comparar; inserir textos benignos quando o erro é do modelo & S7 & A19 & Acadêmica & p.8 e p.10 \\
Remoção de textos envenenados da base (descarte) com verificação da correção & Remover, reenviar a consulta e comparar; inserir textos benignos quando o erro é do modelo & S8 & A19 & Acadêmica & p.8 e p.10 \\
Pipeline de ingestão com metadados, OCR de fallback e proveniência por chunk (arquivo, página, id) & Chroma + SQLite em paralelo & S2 & A20 & Acadêmica & p.1 (Resumo) e p.3 \\
Pipeline de ingestão com metadados, OCR de fallback e proveniência por chunk (arquivo, página, id) & Chroma + SQLite em paralelo & S3 & A20 & Acadêmica & p.1 (Resumo) e p.3 \\
Roteamento por tipo de pergunta entre dados estruturados (SQL) e não estruturados (vetorial) & Rota SQL / híbrida + validador LLM + checagem de fatos & S5 & A20 & Acadêmica & p.1 (Resumo) \\
Registrar feedback com rota, evidência e resposta aceita como dataset de melhoria & Corpus de fine-tuning supervisionado crescente & S6 & A20 & Acadêmica & Conclusão (p.6–7) \\
— & — & S4 & A20 & Acadêmica & p.7 (Limitações) \\
Chunking semântico por limiar de similaridade em vez de divisão fixa por caracteres & Chunks de tamanho variável (até 2.187 caracteres) conforme a densidade semântica & S4 & A21 & Acadêmica & p.3–4 (Tabela III, Fig. 3) \\
Fronteira de privacidade por arquitetura: processar documentos localmente e enviar à nuvem só metadados de esquema & Especialização de modelos por tipo de dado & S3 & A21 & Acadêmica & p.1 e p.5 \\
Fronteira de privacidade por arquitetura: processar documentos localmente e enviar à nuvem só metadados de esquema & Especialização de modelos por tipo de dado & S5 & A21 & Acadêmica & p.1 e p.5 \\
Validação de segurança das consultas geradas antes de tocar no banco & Lista de bloqueio + autocorreção limitada a 2 chamadas & S5 & A21 & Acadêmica & p.3 \\
Controle de acesso antes da recuperação (policy-first) e refiltragem após a fusão & Filtro compilado de papel, inquilino, região e contexto; RBAC/ABAC; zero trust & S5 & A22 & Acadêmica & p.1 e p.4 (Algoritmo 1) \\
Registrar, por passagem, postagem léxica, vetor e metadados/ACL, com versão e ID para rollback & Três artefatos derivados por passagem & S3 & A22 & Acadêmica & p.3 (Ingestão) \\
Registrar, por passagem, postagem léxica, vetor e metadados/ACL, com versão e ID para rollback & Três artefatos derivados por passagem & S7 & A22 & Acadêmica & p.3 (Ingestão) \\
Trace imutável por requisição ligando política, evidências, versões e saída & Registro append-only com hashes & S6 & A22 & Acadêmica & p.3–4 \\
Desempate por atualidade e manutenção da qualidade dos metadados de permissão & Freshness no ranking; red team e monitoramento contínuo & S5 & A22 & Acadêmica & p.3 e p.5 \\
Desempate por atualidade e manutenção da qualidade dos metadados de permissão & Freshness no ranking; red team e monitoramento contínuo & S7 & A22 & Acadêmica & p.3 e p.5 \\
Avaliar ferramentas de conversão pela acurácia final do RAG, não por métricas de fidelidade de parsing & Benchmark ponta a ponta com 21 configurações & S2 & A23 & Acadêmica & p.1 (Resumo) e p.21 (4.1) \\
Avaliar ferramentas de conversão pela acurácia final do RAG, não por métricas de fidelidade de parsing & Benchmark ponta a ponta com 21 configurações & S4 & A23 & Acadêmica & p.1 (Resumo) e p.21 (4.1) \\
Divisão hierárquica com caminho da seção (breadcrumb) prefixado ao chunk & Docling + divisão hierárquica + descrição de imagens & S4 & A23 & Acadêmica & p.18 \\
Arquitetura em camadas Bronze/Silver/Gold para artefatos do pipeline RAG & Separação de ingestão, transformação e indexação; troca por um parâmetro de configuração & S2 & A23 & Acadêmica & p.4 \\
Arquitetura em camadas Bronze/Silver/Gold para artefatos do pipeline RAG & Separação de ingestão, transformação e indexação; troca por um parâmetro de configuração & S3 & A23 & Acadêmica & p.4 \\
Restrição de privacidade como critério de escolha de ferramenta de ingestão & Apenas ferramentas locais & S2 & A23 & Acadêmica & p.3 e p.20–21 \\
Atualização contínua do banco vetorial sob leitura concorrente & Índice IVF de dois estágios com parâmetros de inserção separados & S3 & A24 & Acadêmica & p.1 (Introdução) \\
Atualização contínua do banco vetorial sob leitura concorrente & Índice IVF de dois estágios com parâmetros de inserção separados & S7 & A24 & Acadêmica & p.1 (Introdução) \\
Exclusão lógica (tombstone) seguida de remoção física por compactação & Checagem de tombstone no filtro; difusão da exclusão a todos os IndexWorkers & S8 & A24 & Acadêmica & p.4 e p.7 \\
Reconstrução periódica do índice quando a distribuição dos dados muda & Rebuild recomendado após mudanças significativas & S7 & A24 & Acadêmica & p.4 e p.17 \\
Delegar a autorização ao IAM nativo de cada fonte, validando cada documento em tempo real & Sem fusão de políticas; verificação por documento contra o provedor & S5 & A25 & Acadêmica & p.1–3 (Introdução) \\
Identificador persistente por recurso ligando chunks à origem e ao IAM, para atualização e exclusão & UUID global + ID local de origem & S2 & A25 & Acadêmica & p.4–5 (Ingestão) \\
Identificador persistente por recurso ligando chunks à origem e ao IAM, para atualização e exclusão & UUID global + ID local de origem & S8 & A25 & Acadêmica & p.4–5 (Ingestão) \\
Separar o armazenamento de vetores (estáveis) do de metadados (voláteis) & Vector store + metadata store ligados pelo resourceID & S3 & A25 & Acadêmica & p.6 \\
Separar o armazenamento de vetores (estáveis) do de metadados (voláteis) & Vector store + metadata store ligados pelo resourceID & S7 & A25 & Acadêmica & p.6 \\
Evitar índices separados por papel (filtragem estática) & Filtragem dinâmica com cache TTL (futuro) para reduzir latência & S3 & A25 & Acadêmica & p.14 (Discussão) \\
Evitar índices separados por papel (filtragem estática) & Filtragem dinâmica com cache TTL (futuro) para reduzir latência & S7 & A25 & Acadêmica & p.14 (Discussão) \\
Medir o impacto do nível de permissão na qualidade da resposta & — & S6 & A25 & Acadêmica & p.11 (Tabela 5) \\
Seleção e coleta de dados, chunking e escolha de embedding como trabalho central & Chunk nem pequeno demais (fragmenta) nem grande demais (sobrecarrega o gerador) (p.9) & S1 & A26 & Acadêmica & p.1 (Resumo) e p.8 \\
Seleção e coleta de dados, chunking e escolha de embedding como trabalho central & Chunk nem pequeno demais (fragmenta) nem grande demais (sobrecarrega o gerador) (p.9) & S2 & A26 & Acadêmica & p.1 (Resumo) e p.8 \\
Seleção e coleta de dados, chunking e escolha de embedding como trabalho central & Chunk nem pequeno demais (fragmenta) nem grande demais (sobrecarrega o gerador) (p.9) & S4 & A26 & Acadêmica & p.1 (Resumo) e p.8 \\
Qualidade dos dados como requisito explícito do sistema RAG & — & S1 & A26 & Acadêmica & p.6 \\
Ontologia/grafo para desambiguar entidades e abreviações & Grafo de conhecimento com ontologia em vez de banco vetorial & S4 & A26 & Acadêmica & p.8 \\
Rodar benchmark de novo após mudanças nos dados ou componentes (teste de regressão) & — & S6 & A26 & Acadêmica & p.7 \\
Rodar benchmark de novo após mudanças nos dados ou componentes (teste de regressão) & — & S7 & A26 & Acadêmica & p.7 \\
Avaliação manual predominante & — & S6 & A26 & Acadêmica & p.1 e p.9 \\
Avaliação manual predominante & — & S7 & A26 & Acadêmica & p.1 e p.9 \\
Decidir quando e como indexar cada dataset conforme o uso esperado & Índice adaptativo (cracking) que cresce com as consultas & S3 & A29 & Acadêmica & p.1 (Introdução) \\
Escolher a estratégia de índice pelo volume de consultas (força bruta, índice pequeno, índice grande) & CrackIVF com custo quase mínimo em todas as escalas & S3 & A29 & Acadêmica & p.9 \\
Escolher a estratégia de índice pelo volume de consultas (força bruta, índice pequeno, índice grande) & CrackIVF com custo quase mínimo em todas as escalas & S5 & A29 & Acadêmica & p.9 \\
Manutenção de índices ANN diante de mudanças na distribuição dos dados (split/merge locais) & — & S7 & A29 & Acadêmica & p.12 (Trabalhos relacionados) \\
Metadados temporais e de proveniência para distinguir versões coexistentes de um dado & Enriquecimento de metadados; critério de validade temporal na avaliação & S4 & A30 & Acadêmica & p.3–4 \\
Metadados temporais e de proveniência para distinguir versões coexistentes de um dado & Enriquecimento de metadados; critério de validade temporal na avaliação & S7 & A30 & Acadêmica & p.3–4 \\
Avaliar a camada de dados (validade de metadados, integridade e densidade dos chunks) separadamente da recuperação e da geração & Avaliação em dois níveis (triagem barata + juiz LLM fino) & S6 & A30 & Acadêmica & p.1 (Resumo) e p.7 \\
Mapear cada falha diagnosticada para uma ação de otimização na camada correspondente & Busca híbrida BM25+densa; reranking; chunking semântico & S4 & A30 & Acadêmica & p.1 e p.13–14 (Tabela 3) \\
Mapear cada falha diagnosticada para uma ação de otimização na camada correspondente & Busca híbrida BM25+densa; reranking; chunking semântico & S5 & A30 & Acadêmica & p.1 e p.13–14 (Tabela 3) \\
Ingestão automatizada com limpeza inteligente e vetorização dinâmica em ciclo fechado & — & S2 & A30 & Acadêmica & p.3–4 e p.11 \\
Filtrar documentos recuperados conforme as permissões do usuário antes da geração & Níveis de acesso por perfil (AL1/AL2) & S5 & A31 & Acadêmica & p.1 (Resumo/Introdução) \\
Resposta orientada quando a informação é restrita (encaminhar a quem tem permissão) & — & S6 & A31 & Acadêmica & p.3 (Discussão) \\
Armazenamento vetorial integrado ao banco operacional (multimodelo) em vez de banco vetorial isolado & Arquitetura de armazenamento compartilhado (LindormDFS) & S3 & A32 & Acadêmica & p.1 e p.4 (3.1) \\
Inserção e exclusão de vetores em tempo real para manter o frescor & Busca de centróide otimizada no caminho de escrita & S7 & A32 & Acadêmica & p.8 e p.12 (5.5.1) \\
Inserção e exclusão de vetores em tempo real para manter o frescor & Busca de centróide otimizada no caminho de escrita & S8 & A32 & Acadêmica & p.8 e p.12 (5.5.1) \\
Particionamento temporal de tabelas vetoriais com metadados de índice compartilhados & Reuso de centróides e codebooks & S3 & A32 & Acadêmica & p.9 (4.6.1) \\
Particionamento temporal de tabelas vetoriais com metadados de índice compartilhados & Reuso de centróides e codebooks & S7 & A32 & Acadêmica & p.9 (4.6.1) \\
Busca vetorial filtrada por atributos (pré/pós-filtro, pushdown) & Pushdown de atributos & S5 & A32 & Acadêmica & p.12 (5.5.2) \\
Particionar índices de modo a refletir a proveniência (instituição, departamento) em recuperação federada & Árvore hierárquica de recuperadores & S3 & A33 & Acadêmica & p.4 \\
Controle de acesso por políticas (PBAC) em cada recuperador, com sobre-busca para compensar documentos negados & Ponto de decisão de política por folha & S5 & A33 & Acadêmica & p.5 \\
Escolher armazenamento vetorial com CRUD por causa de dados que mudam com frequência & Qdrant; filtros por paciente via NER & S3 & A33 & Acadêmica & p.4 \\
Escolher armazenamento vetorial com CRUD por causa de dados que mudam com frequência & Qdrant; filtros por paciente via NER & S7 & A33 & Acadêmica & p.4 \\
Reconhecer a degradação do índice com atualizações (centróides desatualizados) & Manutenção incremental do índice & S7 & A34 & Acadêmica & p.3 \\
Delta-store para inserções/exclusões em tempo real e monitor de qualidade que dispara reindexação & Armazenamento relacional com ACID; reindexação por gatilho & S7 & A34 & Acadêmica & p.4 \\
Delta-store para inserções/exclusões em tempo real e monitor de qualidade que dispara reindexação & Armazenamento relacional com ACID; reindexação por gatilho & S8 & A34 & Acadêmica & p.4 \\
Otimizador de consulta híbrida que escolhe pré ou pós-filtro pela seletividade estimada & Estimativa de seletividade de atributos & S5 & A34 & Acadêmica & p.7 e p.10 \\
Considerar o custo de log/replicação das atualizações do índice vetorial em bancos relacionais & Buffer de inserção + merge em lote por partição & S3 & A35 & Acadêmica & p.1 (Introdução) \\
Considerar o custo de log/replicação das atualizações do índice vetorial em bancos relacionais & Buffer de inserção + merge em lote por partição & S7 & A35 & Acadêmica & p.1 (Introdução) \\
Desacoplar a visibilidade dos novos vetores da atualização da estrutura do índice & Merge a cada 1.000 inserções & S7 & A35 & Acadêmica & p.3 \\
Exclusão por tombstone com reconstrução de partição acima de um limiar, respeitando MVCC & Proposta (não avaliada) & S8 & A35 & Acadêmica & p.9 (Limitações) \\
Avaliar o banco vetorial sob cargas realistas (filtros, churn, restart) em vez de benchmarks estáticos & Oráculo de verdade com filtros (bitmap + FAISS flat adaptativo) & S5 & A36 & Acadêmica & p.1 (Introdução) \\
Avaliar o banco vetorial sob cargas realistas (filtros, churn, restart) em vez de benchmarks estáticos & Oráculo de verdade com filtros (bitmap + FAISS flat adaptativo) & S7 & A36 & Acadêmica & p.1 (Introdução) \\
Monitorar a seletividade dos filtros de metadados e permissão & Controles de operador para trocar acurácia por latência & S5 & A36 & Acadêmica & p.1 e p.5 \\
Monitorar a cadência de compactação e dimensionar pelo pior caso transitório & Provisionamento pelo pior caso & S7 & A36 & Acadêmica & p.5 \\
Monitorar a cadência de compactação e dimensionar pelo pior caso transitório & Provisionamento pelo pior caso & S8 & A36 & Acadêmica & p.5 \\
Checagem de prontidão no nível de consulta após restart & — & S6 & A36 & Acadêmica & p.1 (Takeaways) e p.6 \\
Checagem de prontidão no nível de consulta após restart & — & S7 & A36 & Acadêmica & p.1 (Takeaways) e p.6 \\
Avaliação por camada (recuperação separada de geração) e verificação fina de evidência & — & S6 & A37 & Acadêmica & Resumo (Resultados) \\
Reportar a unidade e a granularidade de recuperação (chunk/documento) junto da avaliação & — & S4 & A37 & Acadêmica & Discussão \\
Reportar a unidade e a granularidade de recuperação (chunk/documento) junto da avaliação & — & S6 & A37 & Acadêmica & Discussão \\
Avaliar a construção do grafo e os artefatos intermediários (nós, caminhos, subgrafos) & — & S4 & A37 & Acadêmica & Resumo (Resultados) \\
Avaliar a construção do grafo e os artefatos intermediários (nós, caminhos, subgrafos) & — & S6 & A37 & Acadêmica & Resumo (Resultados) \\
Salvaguardas de avaliação (concordância entre avaliadores; controle de viés do juiz LLM) & — & S6 & A37 & Acadêmica & Resumo (Resultados) \\
Extração contínua de triplas com normalização, deduplicação e proveniência até a seção de origem & Índice vetorial unificado (tripla + texto de origem + metadados) & S2 & A39 & Acadêmica & p.1 (Resumo) e p.1–2 (2.1) \\
Extração contínua de triplas com normalização, deduplicação e proveniência até a seção de origem & Índice vetorial unificado (tripla + texto de origem + metadados) & S4 & A39 & Acadêmica & p.1 (Resumo) e p.1–2 (2.1) \\
Esquema mínimo com canonicalização de entidades em vez de ontologia rígida & Canonicalização e ligação de entidades & S4 & A39 & Acadêmica & p.2 (2.4) \\
Atualização incremental do grafo e do índice & Curadoria iterativa e supervisão fraca & S7 & A39 & Acadêmica & p.3 \\
Sequência de otimização: análise do corpus → chunking → índice → busca híbrida → calibração & Processo de implantação repetível & S4 & A40 & Acadêmica & p.1 (Resumo/Introdução) \\
Sequência de otimização: análise do corpus → chunking → índice → busca híbrida → calibração & Processo de implantação repetível & S5 & A40 & Acadêmica & p.1 (Resumo/Introdução) \\
Chunking por estrutura (títulos, tabelas, itens numerados) com lógica por tipo de elemento & Chunking por estrutura em corpora técnicos e regulatórios & S4 & A40 & Acadêmica & p.3 \\
Escolher o índice pela frequência de atualização; pré-filtro por metadados como isolamento entre inquilinos & HNSW para ingestão contínua; pré-filtro obrigatório & S3 & A40 & Acadêmica & p.4–5 \\
Escolher o índice pela frequência de atualização; pré-filtro por metadados como isolamento entre inquilinos & HNSW para ingestão contínua; pré-filtro obrigatório & S5 & A40 & Acadêmica & p.4–5 \\
Gatilhos de reavaliação (mudança de distribuição, de prompt ou de embedding) e registro versionado de configuração & Calibração por campo após 3–5 lotes de correções & S7 & A40 & Acadêmica & p.6–7 \\
Seleção de contexto como otimização sob orçamento de tokens (mochila/ILP) em vez de top-k & ILP binário (relevância × custo em tokens) & S5 & A42 & Acadêmica & p.1 (Resumo) e p.3 \\
Extração com preservação de estrutura (Markdown) + chunking por estrutura & Extração com Azure Document Intelligence & S2 & A42 & Acadêmica & p.3 \\
Extração com preservação de estrutura (Markdown) + chunking por estrutura & Extração com Azure Document Intelligence & S4 & A42 & Acadêmica & p.3 \\
Restrições de diversidade por documento-fonte na montagem do contexto & Diversidade adaptativa (futuro): não impor sempre & S5 & A42 & Acadêmica & p.4 (Trabalhos futuros) \\
Trace por resposta com fonte, rota, latências, consulta reescrita, resultados de recuperação, prompts e guardrails & Arquitetura de captura de respostas e feedback & S6 & A43 & Acadêmica & p.10–11 (Apêndice, Fig. 3) \\
Pipeline batch agendado (cron + PySpark + data lake) para dados de feedback e traces & Janela de 4 h & S6 & A43 & Acadêmica & p.11 \\
Pipeline batch agendado (cron + PySpark + data lake) para dados de feedback e traces & Janela de 4 h & S7 & A43 & Acadêmica & p.11 \\
Tratar o viés e a escassez do feedback e remover PII antes de reutilizar os dados & Dados sintéticos (5 mil exemplos) para complementar & S6 & A43 & Acadêmica & p.3 \\
Implantação gradual (canário) com procedimento de rollback e monitoramento pós-deploy & Promoção e reversão de configuração com KPIs (acurácia, latência, feedback) & S7 & A43 & Acadêmica & p.5 (Learnings) \\
Limpeza estrutural de PDFs normativos e metadados por cláusula para rastreabilidade & Segmentação por cláusula/parágrafo & S2 & A44 & Acadêmica & p.6 \\
Limpeza estrutural de PDFs normativos e metadados por cláusula para rastreabilidade & Segmentação por cláusula/parágrafo & S4 & A44 & Acadêmica & p.6 \\
Grafo com relações tipadas (referência cruzada, hierarquia, similaridade) ligado aos chunks de origem, com deduplicação & Recuperação híbrida local+global no grafo & S4 & A44 & Acadêmica & p.4 \\
Priorizar o modelo de embedding e calibrar o tamanho do chunk com a janela de contexto & Chunks pequenos/médios + janela grande & S4 & A44 & Acadêmica & p.11 \\
Priorizar o modelo de embedding e calibrar o tamanho do chunk com a janela de contexto & Chunks pequenos/médios + janela grande & S5 & A44 & Acadêmica & p.11 \\
— & Futuro: atualização incremental do grafo & S7 & A44 & Acadêmica & p.13 \\
Minimização e mascaramento na escrita, TTL de retenção e consentimento por item, filtro por finalidade na leitura & Motor de políticas com regras GDPR / EU AI Act / NIST / ISO 42001 executáveis & S2 & A45 & Acadêmica & p.3 (Plano de governança) \\
Minimização e mascaramento na escrita, TTL de retenção e consentimento por item, filtro por finalidade na leitura & Motor de políticas com regras GDPR / EU AI Act / NIST / ISO 42001 executáveis & S5 & A45 & Acadêmica & p.3 (Plano de governança) \\
Minimização e mascaramento na escrita, TTL de retenção e consentimento por item, filtro por finalidade na leitura & Motor de políticas com regras GDPR / EU AI Act / NIST / ISO 42001 executáveis & S8 & A45 & Acadêmica & p.3 (Plano de governança) \\
Armazenamento em camadas com política de retenção por camada e arquivo frio imutável para retenção legal & Promoção e expiração entre camadas & S3 & A45 & Acadêmica & p.3 (Camadas) \\
Armazenamento em camadas com política de retenção por camada e arquivo frio imutável para retenção legal & Promoção e expiração entre camadas & S8 & A45 & Acadêmica & p.3 (Camadas) \\
Linhagem padronizada (W3C PROV) por operação e pacote de evidências assinado por resposta & Log assíncrono para não pesar na latência & S6 & A45 & Acadêmica & p.3 e p.5 \\
— & — & S8 & A45 & Acadêmica & p.5 (Limitações) \\
Avaliar o custo-benefício do chunking semântico frente ao fixo antes de adotá-lo & Chunking fixo com sobreposição como baseline competitivo & S4 & A46 & Acadêmica & p.1 (Resumo) \\
Priorizar a escolha do modelo de embedding sobre a sofisticação do chunking & — & S4 & A46 & Acadêmica & p.4 \\
Balancear tamanho do chunk entre recall e precisão (F1) & Métrica F1 para escolher o tamanho & S4 & A46 & Acadêmica & p.9 (Apêndice D) \\
Escolher a granularidade do chunk pela completude da evidência recuperada & Chunks de 256 tokens com busca híbrida & S4 & A47 & Acadêmica & p.1 (Resumo) e p.11 \\
Ajustar o orçamento de contexto antes de ajustar a sobreposição & Sem sobreposição & S4 & A47 & Acadêmica & p.12 e p.15 (Discussão) \\
Ajustar o orçamento de contexto antes de ajustar a sobreposição & Sem sobreposição & S5 & A47 & Acadêmica & p.12 e p.15 (Discussão) \\
Pré-computar e amortizar embeddings; avaliar se o reranking compensa o custo por consulta & — & S3 & A47 & Acadêmica & p.15 \\
Pré-computar e amortizar embeddings; avaliar se o reranking compensa o custo por consulta & — & S5 & A47 & Acadêmica & p.15 \\
Avaliar separadamente recuperação (completude da evidência) e geração, com condições-oráculo & Comparar com contexto-ouro e fatos-ouro & S6 & A47 & Acadêmica & p.3 e p.17 \\
Padrões de produção: sem sobreposição; chunking por sentença & Estudo ponta a ponta para padronizar defaults & S4 & A48 & Acadêmica & p.1 (Resumo) e p.2 \\
Ajustar o orçamento de contexto ao objetivo da tarefa & Política de preencher até o orçamento (sem k fixo) & S5 & A48 & Acadêmica & p.1–2 \\
Medir a taxa de abstenção como indicador de confiabilidade & — & S6 & A48 & Acadêmica & p.1 (Setup) e Conclusão \\
Métricas intrínsecas de qualidade de chunk e seleção da estratégia por documento & Seleção guiada por métricas + chunkers novos (regex por LLM; split-then-merge) & S4 & A49 & Acadêmica & p.1 (Resumo) \\
Pós-processamento de chunks: dividir os grandes e fundir os minúsculos & Limites de 100–1.100 tokens & S4 & A49 & Acadêmica & p.6 e p.17 (Tabela 7) \\
— & Custo amortizado na indexação & S4 & A49 & Acadêmica & p.9 (Limitações) \\
— & Custo amortizado na indexação & S7 & A49 & Acadêmica & p.9 (Limitações) \\
Casos de avaliação com evidência densa para avaliar decisões de chunking & HiCBench com cortes hierárquicos anotados & S6 & A51 & Acadêmica & p.1 (Introdução, Fig. 1) \\
Estruturação hierárquica do documento + recuperação que funde filhos no pai (Auto-Merge) & HC200 + Auto-Merge & S4 & A51 & Acadêmica & p.4 \\
Estruturação hierárquica do documento + recuperação que funde filhos no pai (Auto-Merge) & HC200 + Auto-Merge & S5 & A51 & Acadêmica & p.4 \\
Comparar configurações de chunking sob o mesmo orçamento de tokens & Orçamento de 4.096 tokens & S6 & A51 & Acadêmica & p.6–7 \\
Chunking por delimitadores do domínio com injeção de metadados hierárquicos (Lei, Capítulo, Seção, título) no texto do chunk & Carimbo semântico determinístico & S4 & A52 & Acadêmica & p.3 (Ingestão) \\
Recuperação pai-filho e busca ampla seguida de reranking & k=60 + cross-encoder (FlashRank) & S5 & A52 & Acadêmica & p.1 (Resumo) e p.3 \\
Estruturação prévia da fonte (JSON com seções) como pré-requisito & Futuro: extração automática de hierarquia & S1 & A52 & Acadêmica & p.5 (Discussão) \\
Estruturação prévia da fonte (JSON com seções) como pré-requisito & Futuro: extração automática de hierarquia & S4 & A52 & Acadêmica & p.5 (Discussão) \\
Métricas diretas de qualidade do chunking (clareza de fronteira, independência entre chunks) & BC e CS correlacionadas com o desempenho do QA & S4 & A53 & Acadêmica & p.1 (Resumo) e p.3 \\
Métricas diretas de qualidade do chunking (clareza de fronteira, independência entre chunks) & BC e CS correlacionadas com o desempenho do QA & S6 & A53 & Acadêmica & p.1 (Resumo) e p.3 \\
— & Chunking guiado por LLM & S4 & A53 & Acadêmica & p.8 \\
Gerar regras de corte (regex) com modelos pequenos roteados por granularidade, em vez de reescrever o texto & Mistura de chunkers com ativação esparsa & S4 & A53 & Acadêmica & p.5 e p.14–15 \\
Chunking estrutural guiado pela árvore sintática (split-then-merge) & max\_chunk\_size 2.000 caracteres & S4 & A55 & Acadêmica & p.1 (Resumo/Introdução) \\
Fundir unidades pequenas para não inflar o índice & Etapa de merge obrigatória & S3 & A55 & Acadêmica & p.4 (Ablações) \\
Fundir unidades pequenas para não inflar o índice & Etapa de merge obrigatória & S4 & A55 & Acadêmica & p.4 (Ablações) \\
Preservar metadados estruturais (arquivo, classe, função) nos chunks & — & S4 & A55 & Acadêmica & p.1–2 (Vantagem 3) \\
Indexar várias granularidades contíguas por sentença e escolher a granularidade na consulta & Embeddings multigranulares em uma passada (máscara de padrões de chunk) & S4 & A56 & Acadêmica & p.1 (Resumo/Introdução) \\
Indexar várias granularidades contíguas por sentença e escolher a granularidade na consulta & Embeddings multigranulares em uma passada (máscara de padrões de chunk) & S5 & A56 & Acadêmica & p.1 (Resumo/Introdução) \\
Integrar o RAG ao lakehouse governado (tabelas Iceberg, catálogo, contratos de dados, evolução de esquema) & Embeddings no nível da partição Iceberg; metadados no Glue & S3 & A58 & Acadêmica & p.1 (Resumo/Introdução) \\
Planejamento de recuperação guiado por linhagem: seleção de snapshot válido e exclusão de partições expiradas ou sem acesso antes da busca vetorial & Política prevalece sobre a versão mais recente (ex.: partição Retention:Expired é excluída) & S5 & A58 & Acadêmica & p.3 (Planejador) \\
Planejamento de recuperação guiado por linhagem: seleção de snapshot válido e exclusão de partições expiradas ou sem acesso antes da busca vetorial & Política prevalece sobre a versão mais recente (ex.: partição Retention:Expired é excluída) & S8 & A58 & Acadêmica & p.3 (Planejador) \\
Metadados de linhagem por chunk (tabela, partição, versão do esquema, política) propagados até a resposta & Reprodução por manifests de snapshot do Iceberg & S4 & A58 & Acadêmica & p.3 e p.6 \\
Metadados de linhagem por chunk (tabela, partição, versão do esquema, política) propagados até a resposta & Reprodução por manifests de snapshot do Iceberg & S6 & A58 & Acadêmica & p.3 e p.6 \\
Usar metadados de governança como sinal ativo de recuperação (remove versões obsoletas e duplicadas) & — & S7 & A58 & Acadêmica & p.6 (Discussão) \\
Enriquecer o chunk com contexto do documento (contextual retrieval) × embedar o documento antes de dividir (late chunking) & Escolha conforme o orçamento computacional & S4 & A59 & Acadêmica & p.1 (Resumo) e p.4–6 \\
— & — & S4 & A59 & Acadêmica & p.12 (Conclusão) \\
Metadados estruturados (empresa, ano, seção, tipo de formulário) como sinal de recuperação embutido, não só como filtro & Prefixo de metadados ou embedding unificado & S4 & A60 & Acadêmica & p.1 (Resumo/Introdução) \\
Metadados estruturados (empresa, ano, seção, tipo de formulário) como sinal de recuperação embutido, não só como filtro & Prefixo de metadados ou embedding unificado & S5 & A60 & Acadêmica & p.1 (Resumo/Introdução) \\
Embeddings de metadados separados e fundidos (unified) para evitar reindexação quando os metadados mudam & Dual encoder com soma de vetores num índice único & S7 & A60 & Acadêmica & p.3 e p.5 \\
Escolher campos de metadados por poder de desambiguação (global: empresa/ano; local: seção) & — & S4 & A60 & Acadêmica & p.12–13 (Ablação) \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S1 & C04, C17*, C29 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S2 & C06, C10, C12, C31, C34, C35 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S3 & C03, C05, C11, C22 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S4 & C02, C08, C29, C32, C33, C35, C36 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S5 & C04, C05, C08, C15, C18, C19, C28, C30 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S6 & C02, C03, C13, C14, C23 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S7 & C06, C11, C12, C16*, C28 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
Práticas registradas nas fichas da matriz de evidências & Excertos e localizações nas fichas da matriz de evidências & S8 & C01, C05, C10, C12 & Cinzenta & Matriz de evidências; * = uso numérico restrito \\
\bottomrule
\end{longtable}

```

## Tabela integral QP2 anterior à compactação editorial

Versão histórica, gerada antes da codificação final das evidências. Para o vínculo entre evidências e a tabela publicada, consulte a seção de rastreabilidade acima.

```latex
\begin{longtable}{p{3cm}p{2.5cm}p{3cm}p{2.5cm}p{1.7cm}}
\caption{QP2: adaptações candidatas; base comparativa e excertos cinzentos requerem conferência.}\label{tab:qp2-sintese}\\
\toprule
\textbf{Adaptação} & \textbf{Base BI/ED/ML} & \textbf{Mudança para RAG} & \textbf{Requisito/desafio} & \textbf{IDs} \\
\midrule
\endfirsthead
\toprule
\textbf{Adaptação} & \textbf{Base BI/ED/ML} & \textbf{Mudança para RAG} & \textbf{Requisito/desafio} & \textbf{IDs} \\
\midrule
\endhead
Propriedade e armazenamento locais de documentos e índices por domínio (federação) & Base de comparação nas fichas da matriz de evidências & Arquitetura em três camadas: nós locais, gateways regionais, roteamento/inferência na nuvem & Centralização em um único índice vetorial complica residência de dados, isolamento e conformidade (GDPR/CCPA) e aumenta o raio de impacto de vazamentos & A02 \\
Catálogo de metadados dos índices (domínio, modelo de embedding, latência) e aplicação local de políticas & Base de comparação nas fichas da matriz de evidências & Roteador com escore custo-sensível (relevância − latência) treinado em logs & Encaminhar consultas a muitos índices heterogêneos sem difundir tudo & A02 \\
Semente pequena e verificada manualmente da base de conhecimento & Base de comparação nas fichas da matriz de evidências & Iniciar com 10 exemplos verificados em vez de seleção não supervisionada (aleatória/cluster) & Ruído na base contamina a recuperação & A03 \\
Atualização incremental da base guiada pela incerteza do LLM, com rotulação humana seletiva (humano no laço) & Base de comparação nas fichas da matriz de evidências & Limiares de seleção (st) e de rotulação (lt) sobre a incerteza & Custo de rotulação humana × atualidade da base & A03 \\
Armazenamento estruturado por fragmento com metadados temporais, separado do índice vetorial & Base de comparação nas fichas da matriz de evidências & Separar legislação (banco relacional) de jurisprudência/editorial (índice vetorial/léxico) & Citações exigem precisão em nível de fragmento & A04 \\
Trilhas de auditoria por resposta e mascaramento de dados pessoais (LGPD) & Base de comparação nas fichas da matriz de evidências & Transformar alucinação silenciosa em aviso explícito por referência & Conformidade legal e confiança do profissional & A04 \\
Remoção de documentos de baixa densidade informacional antes da indexação & Base de comparação nas fichas da matriz de evidências & Limiar de proporção de stopwords; exclusão de documentos sempre mal ranqueados & Textos repetitivos ou procedimentais diluem a recuperação & A05 \\
Chunking multivisão (página, seção, tamanho fixo) + elementos paratextuais & Base de comparação nas fichas da matriz de evidências & Manter várias granularidades em paralelo & Chunking de tamanho fixo perde estrutura e tabelas espalhadas & A06 \\
Pipeline de parsing orientado a esquema relacional fixo, com enriquecimento de metadados por APIs externas & Base de comparação nas fichas da matriz de evidências & Banco relacional (DuckDB) como representação canônica do documento & PDF semiestruturado com layout rico & A06 \\
Índice vetorial autenticado (Merkle + assinaturas) com versionamento do corpus à prova de adulteração & Base de comparação nas fichas da matriz de evidências & Cada chunk assinado e incluído em árvore de Merkle comprometida por versão & Envenenamento do corpus por documentos maliciosos & A07 \\
Chunking semântico (não por contagem de caracteres) para listas e tabelas & Base de comparação nas fichas da matriz de evidências & Chunking semântico + reranking para páginas longas & Tabelas e listas partidas entre chunks & A08 \\
Console administrativo para upload, reindexação e rollback; logs mínimos e amostragem semanal de respostas & Base de comparação nas fichas da matriz de evidências & Observabilidade básica (tempos + logs mínimos) basta para detectar regressões (p.4) & Sem console administrativo, a manutenção da base depende de engenheiros & A08 \\
Chunking com consciência de layout e escolha de tamanho de chunk por experimento & Base de comparação nas fichas da matriz de evidências & Chunks de 2048 tokens; parser com consciência de layout & Documentos longos e tabelas em PDFs & A09 \\
Preservar a hierarquia do documento e converter tabelas para Markdown & Base de comparação nas fichas da matriz de evidências & Pipeline de pré-processamento orientado à estrutura & Tabelas e numeração hierárquica de regras & A10 \\
Normalização de codificação, chunking com sobreposição e resumo por documento com metadados indexado junto aos chunks & Base de comparação nas fichas da matriz de evidências & Dois níveis de representação (chunk fino + resumo do documento) & Passagens longas excedem o contexto do modelo de embedding; codificações ruidosas distorcem a tokenização & A12 \\
Busca sistemática em grade da configuração da cadeia (embedding, chunk, sobreposição, busca, reranking) & Base de comparação nas fichas da matriz de evidências & Padrão recomendado: Gemini Embeddings + MMR + cross-encoder; sobreposição de 10–15\% & Trade-off recall × acurácia × latência × tamanho do índice & A12 \\
Avaliar parser e chunker em conjunto como parte da qualidade do pipeline & Base de comparação nas fichas da matriz de evidências & Experimento fatorial completo parser × chunker & PDF é feito para leitura humana: tabelas desalinhadas, colunas fundidas, legendas separadas & A13 \\
Sobreposição moderada de chunks (25\%) e evitar granularidade excessiva & Base de comparação nas fichas da matriz de evidências & 512 tokens com 25\% de sobreposição & Chunking granular aumenta armazenamento e custo de indexação sem ganho consistente & A13 \\
Calibrar tamanho de chunk e usar filtro por metadados (tipo de documento) para reduzir o espaço de busca & Base de comparação nas fichas da matriz de evidências & Chunks de 200–500 tokens; filtro por tipo de documento & Escalabilidade do índice e latência & A14 \\
Registrar perguntas, respostas e avaliações dos usuários e usá-las para ajustar a recuperação e o chunking & Base de comparação nas fichas da matriz de evidências & Armazenamento leve (SQLite) de interações & Identificar falhas em produção & A14 \\
Hospedagem própria por conformidade; citar a fonte (arquivo e link) na resposta; tratar desbalanceamento de fontes & Base de comparação nas fichas da matriz de evidências & Reranking para diversidade; ocultar fontes em domínios sensíveis & GDPR; confiança; viés por tipo de documento & A14 \\
Metadados estruturais por unidade de evidência (documento, página, modalidade, título pai, tabela, parte) & Base de comparação nas fichas da matriz de evidências & Esquema de metadados que permite reconstruir objetos multipartes & Evidência multimodal e tabelas fragmentadas & A15 \\
Deslocar o custo de estruturação para a ingestão offline & Base de comparação nas fichas da matriz de evidências & Pré-computar o grafo; recuperação dinâmica sem top-k fixo & Métodos que varrem páginas na consulta são caros & A17 \\
Enriquecer cada chunk com resumo do documento de origem (metadado sintético) & Base de comparação nas fichas da matriz de evidências & Chunking recursivo + prefixo de resumo; só recuperação densa & Contexto global perdido no chunking & A18 \\
Forense de dados: rastrear até a fonte e o pipeline de coleta comprometidos & Base de comparação nas fichas da matriz de evidências & Priorizar rastreamento a defesas cada vez mais complexas & Defesas na inferência são contornadas por ataques adaptativos & A19 \\
Remoção de textos envenenados da base (descarte) com verificação da correção & Base de comparação nas fichas da matriz de evidências & Remover, reenviar a consulta e comparar; inserir textos benignos quando o erro é do modelo & Risco de remover texto benigno; erros que não vêm da base & A19 \\
Roteamento por tipo de pergunta entre dados estruturados (SQL) e não estruturados (vetorial) & Base de comparação nas fichas da matriz de evidências & Rota SQL / híbrida + validador LLM + checagem de fatos & RAG vetorial falha em perguntas numéricas e agregadas & A20 \\
Registrar feedback com rota, evidência e resposta aceita como dataset de melhoria & Base de comparação nas fichas da matriz de evidências & Corpus de fine-tuning supervisionado crescente & Feedback ainda não integrado a um ciclo ativo (declarado) & A20 \\
Chunking semântico por limiar de similaridade em vez de divisão fixa por caracteres & Base de comparação nas fichas da matriz de evidências & Chunks de tamanho variável (até 2.187 caracteres) conforme a densidade semântica & Divisão fixa separa unidades lógicas (fórmula e derivação) & A21 \\
Fronteira de privacidade por arquitetura: processar documentos localmente e enviar à nuvem só metadados de esquema & Base de comparação nas fichas da matriz de evidências & Especialização de modelos por tipo de dado & Residência de dados institucionais × qualidade de modelos em nuvem & A21 \\
Controle de acesso antes da recuperação (policy-first) e refiltragem após a fusão & Base de comparação nas fichas da matriz de evidências & Filtro compilado de papel, inquilino, região e contexto; RBAC/ABAC; zero trust & Vazamento de conteúdo restrito para o prompt & A22 \\
Registrar, por passagem, postagem léxica, vetor e metadados/ACL, com versão e ID para rollback & Base de comparação nas fichas da matriz de evidências & Três artefatos derivados por passagem & Manter coerência entre índices léxico e vetorial e permissões & A22 \\
Desempate por atualidade e manutenção da qualidade dos metadados de permissão & Base de comparação nas fichas da matriz de evidências & Freshness no ranking; red team e monitoramento contínuo & Política antiga semanticamente próxima mas inválida; ACLs desatualizadas causam bloqueios indevidos & A22 \\
Avaliar ferramentas de conversão pela acurácia final do RAG, não por métricas de fidelidade de parsing & Base de comparação nas fichas da matriz de evidências & Benchmark ponta a ponta com 21 configurações & Métricas de parsing não preveem desempenho no RAG & A23 \\
Divisão hierárquica com caminho da seção (breadcrumb) prefixado ao chunk & Base de comparação nas fichas da matriz de evidências & Docling + divisão hierárquica + descrição de imagens & Tabelas e estrutura perdidas no chunking básico & A23 \\
Arquitetura em camadas Bronze/Silver/Gold para artefatos do pipeline RAG & Base de comparação nas fichas da matriz de evidências & Separação de ingestão, transformação e indexação; troca por um parâmetro de configuração & Reprodutibilidade e troca de ferramentas & A23 \\
Atualização contínua do banco vetorial sob leitura concorrente & Base de comparação nas fichas da matriz de evidências & Índice IVF de dois estágios com parâmetros de inserção separados & Índices de grafo têm construção cara e contenção em escrita & A24 \\
Delegar a autorização ao IAM nativo de cada fonte, validando cada documento em tempo real & Base de comparação nas fichas da matriz de evidências & Sem fusão de políticas; verificação por documento contra o provedor & Fontes com modelos de autorização heterogêneos (RBAC, ABAC, custom) & A25 \\
Identificador persistente por recurso ligando chunks à origem e ao IAM, para atualização e exclusão & Base de comparação nas fichas da matriz de evidências & UUID global + ID local de origem & Recursos mudam (nome, local, permissão) ao longo do tempo & A25 \\
Ontologia/grafo para desambiguar entidades e abreviações & Base de comparação nas fichas da matriz de evidências & Grafo de conhecimento com ontologia em vez de banco vetorial & Abreviações ambíguas e documentos quase idênticos & A26 \\
Rodar benchmark de novo após mudanças nos dados ou componentes (teste de regressão) & Base de comparação nas fichas da matriz de evidências & — & Prioridade moderada; ofuscada por 'aprendizado contínuo' & A26 \\
Decidir quando e como indexar cada dataset conforme o uso esperado & Base de comparação nas fichas da matriz de evidências & Índice adaptativo (cracking) que cresce com as consultas & Custo inicial de indexação não compensa para dados raramente consultados & A29 \\
Metadados temporais e de proveniência para distinguir versões coexistentes de um dado & Base de comparação nas fichas da matriz de evidências & Enriquecimento de metadados; critério de validade temporal na avaliação & Várias versões do mesmo dado no corpus geram respostas obsoletas & A30 \\
Ingestão automatizada com limpeza inteligente e vetorização dinâmica em ciclo fechado & Base de comparação nas fichas da matriz de evidências & — & PDFs com layouts complexos, tabelas multipágina; semântica em imagens técnicas (sísmica, P\&ID) que o OCR não captura & A30 \\
Filtrar documentos recuperados conforme as permissões do usuário antes da geração & Base de comparação nas fichas da matriz de evidências & Níveis de acesso por perfil (AL1/AL2) & LLMs não têm controle de acesso nativo; risco de vazamento de dados de pacientes & A31 \\
Armazenamento vetorial integrado ao banco operacional (multimodelo) em vez de banco vetorial isolado & Base de comparação nas fichas da matriz de evidências & Arquitetura de armazenamento compartilhado (LindormDFS) & Trade-off desempenho × integração/consistência & A32 \\
Particionamento temporal de tabelas vetoriais com metadados de índice compartilhados & Base de comparação nas fichas da matriz de evidências & Reuso de centróides e codebooks & Custo de treinar índices para cada nova partição & A32 \\
Particionar índices de modo a refletir a proveniência (instituição, departamento) em recuperação federada & Base de comparação nas fichas da matriz de evidências & Árvore hierárquica de recuperadores & Prontuários distribuídos entre instituições e regulação (HIPAA) que restringe o compartilhamento & A33 \\
Controle de acesso por políticas (PBAC) em cada recuperador, com sobre-busca para compensar documentos negados & Base de comparação nas fichas da matriz de evidências & Ponto de decisão de política por folha & Políticas dependem de atributos variáveis do usuário, não só do documento & A33 \\
Delta-store para inserções/exclusões em tempo real e monitor de qualidade que dispara reindexação & Base de comparação nas fichas da matriz de evidências & Armazenamento relacional com ACID; reindexação por gatilho & Manter consistência e recall com escrita contínua & A34 \\
Considerar o custo de log/replicação das atualizações do índice vetorial em bancos relacionais & Base de comparação nas fichas da matriz de evidências & Buffer de inserção + merge em lote por partição & Atualização fina do índice gera WAL alto e atraso de replicação & A35 \\
Desacoplar a visibilidade dos novos vetores da atualização da estrutura do índice & Base de comparação nas fichas da matriz de evidências & Merge a cada 1.000 inserções & Buffer grande aumenta o custo de busca; inserções concentradas sobrecarregam partições & A35 \\
Avaliar o banco vetorial sob cargas realistas (filtros, churn, restart) em vez de benchmarks estáticos & Base de comparação nas fichas da matriz de evidências & Oráculo de verdade com filtros (bitmap + FAISS flat adaptativo) & Benchmarks sem filtro e estáticos escondem degradações de produção & A36 \\
Monitorar a cadência de compactação e dimensionar pelo pior caso transitório & Base de comparação nas fichas da matriz de evidências & Provisionamento pelo pior caso & Manutenção em segundo plano compete com as consultas & A36 \\
Avaliação por camada (recuperação separada de geração) e verificação fina de evidência & Base de comparação nas fichas da matriz de evidências & — & Avaliação ponta a ponta esconde de onde vem a falha & A37 \\
Extração contínua de triplas com normalização, deduplicação e proveniência até a seção de origem & Base de comparação nas fichas da matriz de evidências & Índice vetorial unificado (tripla + texto de origem + metadados) & Jargão e referências cruzadas geram triplas ausentes ou ruidosas & A39 \\
Esquema mínimo com canonicalização de entidades em vez de ontologia rígida & Base de comparação nas fichas da matriz de evidências & Canonicalização e ligação de entidades & Vocabulário fragmentado & A39 \\
Sequência de otimização: análise do corpus → chunking → índice → busca híbrida → calibração & Base de comparação nas fichas da matriz de evidências & Processo de implantação repetível & Configurações padrão degradam com o crescimento do corpus & A40 \\
Chunking por estrutura (títulos, tabelas, itens numerados) com lógica por tipo de elemento & Base de comparação nas fichas da matriz de evidências & Chunking por estrutura em corpora técnicos e regulatórios & Chunk fixo corta obrigações; semântico falha em tabelas & A40 \\
Escolher o índice pela frequência de atualização; pré-filtro por metadados como isolamento entre inquilinos & Base de comparação nas fichas da matriz de evidências & HNSW para ingestão contínua; pré-filtro obrigatório & IVF exige retreino com adições; pós-filtro arrisca vazamento entre inquilinos & A40 \\
Extração com preservação de estrutura (Markdown) + chunking por estrutura & Base de comparação nas fichas da matriz de evidências & Extração com Azure Document Intelligence & — & A42 \\
Trace por resposta com fonte, rota, latências, consulta reescrita, resultados de recuperação, prompts e guardrails & Base de comparação nas fichas da matriz de evidências & Arquitetura de captura de respostas e feedback & Diagnosticar falhas por componente do pipeline & A43 \\
Tratar o viés e a escassez do feedback e remover PII antes de reutilizar os dados & Base de comparação nas fichas da matriz de evidências & Dados sintéticos (5 mil exemplos) para complementar & Feedback escasso, enviesado e com dados pessoais & A43 \\
Grafo com relações tipadas (referência cruzada, hierarquia, similaridade) ligado aos chunks de origem, com deduplicação & Base de comparação nas fichas da matriz de evidências & Recuperação híbrida local+global no grafo & Chunks independentes fragmentam relações entre cláusulas & A44 \\
Priorizar o modelo de embedding e calibrar o tamanho do chunk com a janela de contexto & Base de comparação nas fichas da matriz de evidências & Chunks pequenos/médios + janela grande & Trade-off precisão semântica × capacidade de síntese & A44 \\
Minimização e mascaramento na escrita, TTL de retenção e consentimento por item, filtro por finalidade na leitura & Base de comparação nas fichas da matriz de evidências & Motor de políticas com regras GDPR / EU AI Act / NIST / ISO 42001 executáveis & Pipelines RAG raramente codificam limitação de finalidade, retenção ou linhagem verificável & A45 \\
Armazenamento em camadas com política de retenção por camada e arquivo frio imutável para retenção legal & Base de comparação nas fichas da matriz de evidências & Promoção e expiração entre camadas & Diferentes tempos de vida e obrigações para dados de memória & A45 \\
Escolher a granularidade do chunk pela completude da evidência recuperada & Base de comparação nas fichas da matriz de evidências & Chunks de 256 tokens com busca híbrida & Unidades muito finas perdem evidência; muito grandes trazem distratores & A47 \\
Padrões de produção: sem sobreposição; chunking por sentença & Base de comparação nas fichas da matriz de evidências & Estudo ponta a ponta para padronizar defaults & Chunking decidido por regra de bolso & A48 \\
Pós-processamento de chunks: dividir os grandes e fundir os minúsculos & Base de comparação nas fichas da matriz de evidências & Limites de 100–1.100 tokens & Fragmentos quase vazios (0–4 tokens) ocupam vagas do top-k & A49 \\
Estruturação hierárquica do documento + recuperação que funde filhos no pai (Auto-Merge) & Base de comparação nas fichas da matriz de evidências & HC200 + Auto-Merge & Chunks semânticos têm granularidade irregular & A51 \\
Chunking por delimitadores do domínio com injeção de metadados hierárquicos (Lei, Capítulo, Seção, título) no texto do chunk & Base de comparação nas fichas da matriz de evidências & Carimbo semântico determinístico & Chunking por janela separa provisos e exceções da seção que os governa & A52 \\
Recuperação pai-filho e busca ampla seguida de reranking & Base de comparação nas fichas da matriz de evidências & k=60 + cross-encoder (FlashRank) & Top-k padrão 'enterra' a seção correta & A52 \\
Chunking estrutural guiado pela árvore sintática (split-then-merge) & Base de comparação nas fichas da matriz de evidências & max\_chunk\_size 2.000 caracteres & Chunking por linhas quebra funções e classes & A55 \\
Preservar metadados estruturais (arquivo, classe, função) nos chunks & Base de comparação nas fichas da matriz de evidências & — & — & A55 \\
Integrar o RAG ao lakehouse governado (tabelas Iceberg, catálogo, contratos de dados, evolução de esquema) & Base de comparação nas fichas da matriz de evidências & Embeddings no nível da partição Iceberg; metadados no Glue & RAG como silo sem governança: alucinação, baixa reprodutibilidade, custo com embeddings redundantes & A58 \\
Metadados de linhagem por chunk (tabela, partição, versão do esquema, política) propagados até a resposta & Base de comparação nas fichas da matriz de evidências & Reprodução por manifests de snapshot do Iceberg & Reproduzir e auditar respostas & A58 \\
Enriquecer o chunk com contexto do documento (contextual retrieval) × embedar o documento antes de dividir (late chunking) & Base de comparação nas fichas da matriz de evidências & Escolha conforme o orçamento computacional & Chunks isolados perdem contexto global & A59 \\
Metadados estruturados (empresa, ano, seção, tipo de formulário) como sinal de recuperação embutido, não só como filtro & Base de comparação nas fichas da matriz de evidências & Prefixo de metadados ou embedding unificado & Documentos repetitivos com linguagem idêntica entre empresas e anos & A60 \\
Otimizador de consultas SQL para escolha pré vs. pós-filtro em busca vetorial híbrida & Base de comparação nas fichas da matriz de evidências & Adapta estimativa de seletividade (F\_filters < F\_IVF) para decidir entre filtragem prévia ou varredura vetorial. & Excertos cinzentos nas fichas da matriz de evidências & A34, C05 \\
Controle de acesso (RBAC/ABAC/IAM) deslocado para pré-recuperação, sobre-busca (fetch\_k > k) ou verificação de escopos na fonte (C30) & Base de comparação nas fichas da matriz de evidências & Adapta autorização de linha/tabela para impedir que o LLM receba chunks restritos no contexto. & Excertos cinzentos nas fichas da matriz de evidências & A22, A25, A33, C30 \\
Linhagem W3C PROV e OpenTelemetry para traces de recuperação (5 fases) e Evidence Packs & Base de comparação nas fichas da matriz de evidências & Adapta proveniência de workflows e tracing de microsserviços para registrar chunks, escores, filtros, versão de índice e prompts. & Excertos cinzentos nas fichas da matriz de evidências & A43, A45, C14 \\
Chunking estrutural/hierárquico/AST e enriquecimento contextual (SAC, Semantic Stamp, breadcrumb) & Base de comparação nas fichas da matriz de evidências & Adapta pré-processamento textual para preservar hierarquia (tabelas, seções, AST) dentro da janela de embedding/contexto. & Excertos cinzentos nas fichas da matriz de evidências & A18, A23, A51, A52, A55, A59, A60, C20, C33 \\
Mascaramento de PII na ingestão preservando tokens (PERSON\_1) e matriz de retenção de 10 artefatos & Base de comparação nas fichas da matriz de evidências & Adapta redação de PII para não destruir coesão referencial no chunk e diferencia TTL entre vault, vetor, prompt e audit log. & Excertos cinzentos nas fichas da matriz de evidências & A04, A45, C10 \\
\bottomrule
\end{longtable}

```

## Tabela integral QP3 anterior à compactação editorial

Versão histórica, gerada antes da codificação final das evidências. Para o vínculo entre evidências e a tabela publicada, consulte a seção de rastreabilidade acima.

```latex
\begin{longtable}{p{4.2cm}lrrp{4cm}}
\caption{QP3: frequência de fontes por tema (não mede eficácia); força indicada por tipo de evidência.}\label{tab:qp3-sintese}\\
\toprule
\textbf{Tema} & \textbf{Presença} & \textbf{N acad.} & \textbf{N cinz.} & \textbf{Tipo de evidência} \\
\midrule
\endfirsthead
\toprule
\textbf{Tema} & \textbf{Presença} & \textbf{N acad.} & \textbf{N cinz.} & \textbf{Tipo de evidência} \\
\midrule
\endhead
Arquitetura Medallion (Bronze/Silver/Gold) para conversão PDF → Markdown estruturado & Acadêmica & 1 & 0 & EE:1 \\
Lakehouse (Iceberg + snapshots + time-travel) como filtro pré-recuperação de versão e retenção & Acadêmica & 1 & 0 & EE:1 \\
Data Mesh / propriedade por domínio em índices vetoriais federados & Acadêmica & 2 & 0 & EE:3 \\
Particionamento temporal (DW) em tabelas vetoriais com metadados de índice compartilhados & Acadêmica & 1 & 0 & EP:2 \\
Otimizador de consultas SQL para escolha pré vs. pós-filtro em busca vetorial híbrida & Ambas & 1 & 1 & EE:1, EP:2 \\
Controle de acesso (RBAC/ABAC/IAM) deslocado para pré-recuperação ou sobre-busca (fetch\_k > k) & Ambas & 3 & 1 & EE:4, GP:1 \\
Aprendizado ativo (ML) para curadoria incremental da base RAG guiada por incerteza do LLM & Acadêmica & 1 & 0 & EE:1 \\
Linhagem W3C PROV e OpenTelemetry para traces de recuperação (5 fases) e Evidence Packs & Ambas & 2 & 1 & EP:2, GP:1, PC:2 \\
Testes de qualidade de dados como métricas intrínsecas de chunk (Boundary Clarity, Stickiness, RC/ICC/DCC) & Acadêmica & 2 & 0 & EE:2 \\
Chunking estrutural/hierárquico/AST e enriquecimento contextual (SAC, Semantic Stamp, breadcrumb) & Ambas & 7 & 2 & EE:2 \\
Mascaramento de PII na ingestão preservando tokens (PERSON\_1) e matriz de retenção de 10 artefatos & Ambas & 2 & 1 & EP:2, GP:1, PC:2 \\
\bottomrule
\end{longtable}

```
