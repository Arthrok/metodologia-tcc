# Auditoria, Avaliação Organizacional e Síntese Transversal — MLR Engenharia de Dados em Sistemas RAG

Este documento consolida os resultados das **Etapas 4 e 5** da auditoria da base de estudos do TCC (*Engenharia de Dados em Sistemas RAG: Práticas, Desafios e Adaptações*), complementando os arquivos enriquecidos `../extracao/RESUMOS_TCC.md` (arquivo citado no registro histórico, ausente nesta cópia) e [RESUMOS_CINZENTA.md](../cinzenta/RESUMOS_CINZENTA.md).


## Parte I — Avaliação da Organização Atual e Proposta de Melhoria (Etapa 4)

### 1. Diagnóstico da estrutura atual

| Elemento | Situação observada | Pontos fortes | Fragilidades para a escrita do TCC |
|---|---|---|---|
| **Pasta `artigos/`** | 55 arquivos primários (`A01`–`A60` exceto 5 `E5`), `principal_1.pdf` (Lewis et al., 2020), `principal_2.pdf` (Gao et al., 2024), `versoes_alternativas/` (3 arquivos) e `Filtrado/auditoria_amostra.md` (0 bytes). | Padronização por código `Axx - Autor (Ano) - Título` facilita localizar o PDF; `versoes_alternativas/` preserva cópias sem duplicar a raiz. | `A37` está em `.xml` (Europe PMC) misturado com PDFs; `principal_1.pdf` e `principal_2.pdf` são referências teóricas fundacionais fora da numeração `Axx`; `Filtrado/auditoria_amostra.md` está vazio; arquivos excluídos por QA (`A01`, `A28`, `A50`) ficam misturados aos incluídos (`QA >= 4`). |
| **Pasta `cinzenta/`** | `textos/` com 126 arquivos (`CDxxx.txt/.html` e `PTxx.txt/.html`), `coleta/`, `portais/` e `RESUMOS_CINZENTA.md` (`C01`–`C37`). | Rastreabilidade completa da coleta (`devto_raw.json`, `hn_raw.json`, `triagem_titulo.csv`) e preservação dos textos baixados. | Os nomes dos arquivos em `cinzenta/textos/` usam o ID de triagem (`CD002`, `PT01`), exigindo consulta ao índice de `RESUMOS_CINZENTA.md` para saber qual é `C01`–`C37` e quais foram os 24 textos excluídos após leitura integral. |
| **Arquivos de resumo (`RESUMOS_TCC.md` e `RESUMOS_CINZENTA.md`)** | Antes da auditoria, eram fichas curtas (1 parágrafo + 2–4 excertos). Após a auditoria, cada ficha tem 14 seções padronizadas. | Mantêm separação clara entre literatura acadêmica (`Axx`) e cinzenta (`Cxx`), com IDs da Matriz Mestra (`P-...`) e notas QA/QG. | Arquivos monolíticos longos (5.182 linhas em `RESUMOS_TCC.md` e 3.146 linhas em `RESUMOS_CINZENTA.md`). Sem índice cruzado por **QP1/QP2/QP3** ou por **status de elegibilidade/QA** na própria ficha de entrada rápida. |
| **Distinção Acadêmica × Cinzenta** | Separadas em pastas e arquivos distintos. | Evita misturar evidência revisada por pares com blogs técnicos. | Na base cinzenta anterior, faltava explicitar o **nível de evidência** (estudo de caso em produção vs. experimento pessoal vs. guia opinativo vs. cenário hipotético) e o **grau de viés comercial** dentro de cada ficha (antes aparecia só em nota curta de 1 linha). |

### 2. Proposta de organização (sem destruir rastreabilidade nem mover arquivos sem necessidade)

1. **Manter os arquivos originais e os monolitos enriquecidos como fonte canônica:** não renomear `artigos/Axx...` nem `cinzenta/textos/CDxxx` (pois `extracao/montar_extracao.py`, `cinzenta/extracao_cinzenta.py` e as âncoras dos resumos dependem desses caminhos).
2. **Criar índices leves (ou visões por arquivo/tabela) sem mover PDFs:**
   - **Tabela de Status e Uso Seguro:** separar explicitamente no topo dos resumos:
     - *Núcleo empírico acadêmico (`QA >= 4,0`, texto integral):* 52 artigos.
     - *Excluídos por QA (`< 4,0` ou `QA2=QA3=0`):* `A01`, `A28`, `A50` (usar no máximo como exemplo de lacuna ou citação conceitual com ressalva).
     - *Indisponíveis (`E5`, só resumo):* `A11`, `A27`, `A38`, `A41`, `A54` (não usar como evidência empírica).
     - *Fundacionais teóricos (fora da MLR):* `principal_1.pdf` (Lewis et al., 2020) e `principal_2.pdf` (Gao et al., 2024).
     - *Cinzenta por nível de evidência:* (i) Relato industrial em produção (`C11`, `C18`, `C19`, `C27`, `C28`, `C35`); (ii) Experimento técnico replicável (`C02`, `C05`, `C07`, `C08`, `C12`, `C13`, `C20`, `C21`, `C23`, `C24`, `C33`); (iii) Arquitetura de referência / guia sem experimento primário (`C03`, `C10`, `C04`, `C06`, `C14`, `C15`, `C22`, `C25`, `C26`, `C29`, `C30`, `C31`, `C32`, `C34`, `C36`, `C37`); (iv) Comercial/ilustrativo com ressalva forte (`C01`, `C09`, `C16`, `C17`).
3. **Preencher `artigos/Filtrado/auditoria_amostra.md`** com o registro formal da auditoria humana amostral prevista na Seção 3.3.6 de `metodologia.tex` (podendo referenciar diretamente as correções levantadas nesta auditoria).


## Parte II — Síntese Transversal (Etapa 5)

### 1. Trabalhos analisados e situação de cada resumo

- **Literatura acadêmica (`extracao/RESUMOS_TCC.md`):** **60 estudos** (`A01`–`A60`) auditados e enriquecidos.
  - **55 lidos integralmente** (54 PDFs via `pdftotext` página a página + 1 XML completo em `A37`).
  - **5 indisponíveis (`E5`, somente resumo):** `A11`, `A27`, `A38`, `A41`, `A54` — limitação explicitada em cada ficha; métricas do resumo marcadas como não verificáveis.
  - **3 alertas de qualidade (`QA < 4` / exclusão):** `A01` (`QA=3,0`, sem detalhes de dataset/LLM/embedding), `A28` (`QA=3,0`, resultados são projeções, capturas mostram `0 active` integrações), `A50` (`QA=2,0`, `QA2=QA3=0`, contém marcador não preenchido `[specify domain, e.g., academic research, customer reviews]`).
  - **1 alerta adicional identificado na auditoria:** `A57` (Sambare et al., 2026 — `QA=4,0` preliminar) apresenta contradições numéricas diretas entre texto corrido e Tabela 1, colunas idênticas em 6/7 métricas entre *Document-Based* e *LLM-based*, e erro factual sobre SQuAD 1.0; recomenda-se **rebaixar seu QA na revisão humana** ou restringi-lo a uso puramente conceitual.
  - **2 fundacionais fora da MLR:** `principal_1.pdf` (Lewis et al., 2020) e `principal_2.pdf` (Gao et al., 2024).
- **Literatura cinzenta (`cinzenta/RESUMOS_CINZENTA.md`):** **37 fontes incluídas** (`C01`–`C37`) lidas integralmente a partir de `cinzenta/textos/`, auditadas quanto a autoria, data, tipo de evidência e viés comercial.

### 2. Principais informações acrescentadas e correções factuais relevantes

A auditoria recuperou centenas de parâmetros experimentais, tabelas completas, hardware, equações e **corrigiu distorções relevantes** que existiam nos resumos curtos ou nos próprios artigos:

- **Correções críticas na literatura acadêmica:**
  - `A31` (Chen et al., 2025): o resumo anterior afirmava acurácia comparável ao GPT-4, mas a Tabela 2 (p. 3) compara apenas `RAG` vs. `No-RAG` com `Mistral-7B` (GPT-4 gerou apenas perfis sintéticos).
  - `A39` (Jomraj et al., 2025): o resumo citava *"eCFR"*, ausente do PDF (usa documentos da FDA); além disso, na Tabela 1 (p. 3), triplas foram **piores** que o baseline em Section Overlap `@0.50` e `@0.60`, vencendo apenas em `@0.75`.
  - `A10` (Legado et al., 2026): o resumo citava *"RAGAS"*, mas o artigo não nomeia RAGAS; o PDF tem contradição interna entre *"five unseen benchmark queries"* e *Q1–Q30*, e não entrega ablação de embeddings nem análise de *Taglish* prometidas na introdução.
  - `A52` (Bati et al., 2026): afirma redução de alucinações no resumo/conclusão, mas a Seção V não reporta nenhuma métrica quantitativa de geração/alucinação (apenas recuperação em 46 consultas).
  - `A30` (Yang et al., 2026): `58% -> 89,3%` é especificamente **Retrieval Hit@5** (`87/150 -> 134/150`), não acurácia global de QA.
  - `A16` (Paidi, 2026): divergência interna entre `-27,4% FIR at high staleness` (texto) vs. Tabela II (`0,48 -> 0,28`, ou `-41,7%` na Tabela VI; `-27,4%` é o $\Delta$ médio em *Medium staleness* na Tabela III).
  - `A45` (Yerneni, 2025): alega *"10x reduction"* em alucinação, mas `12,9% -> 4,6%` é `~2,8×`.
  - `A44` (Jovanovski et al., 2026): avalia **7 normas centrais** (ISO/IEC 27000–27006), não toda a família de 97 documentos.
  - `A48` (Bennani e Moslonka, 2026): 3 páginas (não 4) e modelo exato `Ministral-8B-Instruct-2410`.
  - `A43` (Shukla et al., 2026): veículo corrigido para `Volume 5: Industry Track, pp. 438–454`.
  - `A59` (Merola e Singh, 2026): *Contextual Retrieval* (RQ#2) rodou em apenas **20% do NFCorpus** (50 consultas) por limite de 20 GB VRAM; *Late Chunking* colapsou com `BGE-M3` (`0,246 -> 0,070` NDCG@5).

- **Correções críticas e avaliação de viés na literatura cinzenta:**
  - `C36` (Choong / Elastic, 2024): pesos `70%/15%/10%/5%` não são ponderação na busca (S5), mas **Composite Multi-Field Embedding em tempo de indexação (S4/S3)** somado em um único vetor `primary_embedding`.
  - `C02` (Shastri, 2026): embora não testado em 15M docs, executou experimento real no SQuAD v2 (1.200 perguntas, `tinyroberta-squad2`), reduzindo *unsupported-answer rate* de `100% -> 11,6%` ao custo de cobertura (`100% -> 80,3%`).
  - `C07` (Temitayo, 2026): omitia toda a segunda metade com experimento LangGraph (Self-RAG 38% sucesso vs. Query Decomposition 100% vs. HyDE 100%).
  - `C09` (Trpevski, 2026): código `HybridRetriever` declara RRF na docstring, mas implementa soma ponderada linear (`0.6*v + 0.4*b`).
  - `C16` (Decompressed, 2026) e `C17` (Bhaumik, 2026): números são **cenários ilustrativos/marketing** (C16 promove CLI `dcp`; C17 tem links de afiliado Bright Data), não medições de produção.
  - `C21` (Mixedbread, 2025): benchmark OHR v2 comparou OCRs e Ground-truth usando **apenas BM25 lexical** contra o store multimodal proprietário.
  - `C35` (Uber, 2025): `+27%` respostas aceitáveis e `-60%` orientações incorretas são **variações relativas** sobre golden set de 100+ consultas em 40+ docs.

### 3. Lacunas ainda não cobertas pela coleção

1. **Propagação coordenada do descarte (S8) pela cadeia de artefatos derivados:** nenhum estudo acadêmico mede ponta a ponta a remoção coordenada entre `documento -> texto extraído -> chunks -> embeddings -> índice ANN -> caches -> traces -> datasets de avaliação`. `A24`, `A32`, `A34`, `A35` tratam apenas da exclusão no índice vetorial (tombstones/compactação/MVCC); `C01` e `C10` propõem *crypto-shredding* e políticas de retenção na cinzenta, sem validação independente.
2. **Qualidade formal e SLAs das fontes (S1):** poucos estudos formalizam contratos de dados, donos, cadência e critérios de admissibilidade na origem (`A03`, `A08`, `A26` apontam o problema; `C04` e `C17` propõem manifestos na cinzenta, sem avaliação empírica).
3. **Custo de construção e atualização incremental de Knowledge Graphs (S4/S7):** `A05`, `A06`, `A17`, `A39`, `A44` e `C26` mostram ganhos ou arquiteturas com grafos, mas `A23` (>10h em DGX Spark para 20.055 entidades) e `A44` expõem que o custo de atualização incremental de grafos em produção contínua permanece pouco medido.
4. **Migração de modelos de *embedding* e compatibilidade de versões (S7):** na literatura acadêmica aparece apenas indiretamente (`A40`, `A60`); na cinzenta aparece em post-mortems/guias (`C06`, `C16`), faltando estudos empíricos controlados sobre estratégias de *re-embedding* sem indisponibilidade.
5. **Corrupção de caracteres e idiomas não-ingleses em *parsing* (S2):** apenas `A23` registra corrupção do `"ç"` em português e `A10` menciona *Taglish* (sem medir). A quase totalidade dos benchmarks é em inglês (ou chinês em `A53`).

### 4. Convergências e divergências entre os trabalhos

| Tema | Convergência | Divergência / Condição de contorno |
|---|---|---|
| **Engenharia de dados vs. tamanho do LLM** | Forte convergência (`A09`, `A15`, `A23`, `A26`, `A44`, `A46`, `A52`): preparação, *parsing* preservando estrutura e escolha do *embedding* dominam o desempenho mais do que escalar o LLM. | Em `A47` (modelos pequenos), mesmo com todos os fatos recuperados, `20,05%` ainda falham na geração. |
| ***Chunking* estrutural vs. semântico** | Preservar hierarquia/estrutura e tabelas vence de forma consistente (`A06`, `A12`, `A15`, `A17`, `A23`, `A51`, `A52`, `A55`, `C20`, `C33`, `C35`). | *Chunking* semântico não compensa o custo na maioria dos corpora (`A46`, `A48`, `A53`, `C24`), mas ajudou em material didático com fórmulas (`A21`) e em caso industrial específico (`A30`, `C09`). `A40` explica: funciona em prosa, falha em tabelas. |
| **Busca híbrida (BM25 + Densa) e *Reranking*** | Maioria relata ganho com busca híbrida/RRF (`A22`, `A30`, `A34`, `A40`, `C03`, `C15`, `C28`, `C35`) e com *reranker* ajustado ao domínio (`C18`, `C19`). | BM25 degradou precisão/recall em `A09` e `A18` e perdeu para vetorial pura em `C07`. Cross-encoder genérico reduziu Recall@10 em `A09`, piorou F1 e somou `5,98 s/query` em `A47`, e não trouxe ganho com +3× latência em `C07`. |
| **Banco vetorial dedicado vs. integrado** | Integrar vetores ao banco operacional/lakehouse reduz *dual-write* e acelera buscas com filtros de permissão/metadados (`A32`, `A35`, `A58`, `C05`, `C11`, `C32`). Em pequena escala (<500k chunks), busca exata basta (`A29`, `A40`, `C03`, `C22`). | Índices HNSW dedicados continuam relevantes em alta escala pura sem filtros complexos, mas sofrem explosão de latência de cauda (>10.000× em `A36`) sob filtros pouco seletivos se não houver *attribute pushdown* (`A32`) ou otimizador pré/pós-filtro (`A34`). |

### 5. Evidências relacionadas às perguntas de pesquisa (QP1, QP2, QP3)

- **QP1 (Distribuição no ciclo de vida):** Forte concentração acadêmica em **Preparação (S4)** e **Disponibilização (S5)**, seguidas por **Armazenamento (S3)**, **Uso e feedback (S6)**, **Manutenção (S7)** e **Ingestão (S2)**. **Fontes (S1)** e **Descarte (S8)** são as menos cobertas.
- **QP2 (Adaptações e desafios):** Evidências sólidas de adaptação de práticas clássicas de Engenharia de Dados/BI/ML para RAG: arquitetura Medallion (`A23`), *snapshots/time-travel* em lakehouse para controle de versão e retenção na recuperação (`A58`), *data mesh* federado (`A02`, `A33`), otimizadores de consulta pré/pós-filtro (`A34`, `A32`), ETL batch para *traces* (`A43`), aprendizado ativo para curadoria (`A03`) e linhagem W3C PROV (`A45`). Desafios centrais: latência de cauda em busca filtrada (`A36`), custo de OCR (`A13`, `C21`), obsolescência e mistura de versões (`A03`, `A16`, `A30`, `A58`), e vazamento por controle de acesso pós-recuperação (`A22`, `A25`, `A31`, `C30`).
- **QP3 (Acadêmica × Cinzenta):**
  - *Exclusivas ou mais detalhadas na acadêmica:* internos de índices ANN (cracking `A29`, two-tier WAL `A35`, quantização 2 estágios `A24`, amplificação de latência `A36`), métricas intrínsecas de *chunk* (`A49`, `A53`), seleção sob orçamento de tokens como ILP/DP (`A42`, `A15`), e protocolos criptográficos/forenses formais (`A07`, `A19`).
  - *Exclusivas ou mais detalhadas na cinzenta:* operação de pipeline (ingestão idempotente com hash/checkpoint `C06`, `C12`), *post-mortem* de troca de *embedding* (`C16`), sincronização de ACLs (`C30`), políticas práticas de retenção/redação de PII por camada (`C10`, `C14`), e SLOs operacionais (`C14`, `C18`, `C19`).
  - *Ressalva metodológica para QP3:* frequência de menção na cinzenta não equivale a força empírica — apenas uma minoria (`C18`, `C19`, `C28`, `C35`, `C05`, `C11`) traz medições reais de produção.

### 6. Práticas, desafios, ferramentas e artefatos recorrentes

- **Ferramentas recorrentes:** `PyMuPDF`, `pdfplumber`, `Docling`, `MinerU`, `Unstructured` (parsing); `pgvector`, `Milvus`, `Qdrant`, `ChromaDB`, `FAISS`, `OpenSearch`, `Elasticsearch`, `Apache Iceberg` (armazenamento); `BGE-M3`, `text-embedding-3-small/large`, `mxbai-embed-large` (embeddings); `bge-reranker-v2-m3`, `FlashRank` (reranking); `RAGAS`, `LangSmith`, `OpenTelemetry` (avaliação e observabilidade).
- **Artefatos críticos:** documento bruto, Markdown intermediário, *chunk* com caminho hierárquico, metadados de versão/ACL/validade, *embedding* versionado, índice ANN/BM25, cache, *trace* de consulta e *golden set* de avaliação.

### 7. Oportunidades de fortalecimento do referencial teórico e da metodologia (sem alterar `sigconf.tex` agora)

1. **Em `metodologia.tex` (Seção 3.3.5 / QA):** registrar na revisão humana o rebaixamento de `A57` (contradições internas graves) e confirmar a exclusão de `A01`, `A28`, `A50`, além de manter os 5 `E5` (`A11`, `A27`, `A38`, `A41`, `A54`) estritamente fora da síntese empírica.
2. **Em `metodologia.tex` (Seção 3.3.5 / QG):** na literatura cinzenta, além da marcação binária de viés comercial (6 fontes mencionadas em `metodologia.tex`), vale distinguir na tabela de síntese **relato empírico de produção** vs. **experimento controlado próprio** vs. **cenário ilustrativo/guia**, evitando que `C16` ou `C17` tenham o mesmo peso argumentativo de `C18`, `C19` ou `C35`.
3. **Em `referencial.tex` (Seção 2.3 / Tabela 3):** os achados de `A16` (incerteza do estado do índice), `A36` (amplificação de latência em busca filtrada) e `A59` (colapso de *Late Chunking* em certos embedders) oferecem exemplos concretos para enriquecer a discussão sobre a cadeia de artefatos derivados e recuperabilidade.

### 8. Sugestões de pesquisas complementares

1. **Estudo empírico sobre propagação de exclusão (S8) em pipelines RAG:** medir o tempo, custo e taxa de vazamento residual quando um documento é excluído/revogado entre lakehouse/SQL, índice vetorial, índice BM25, caches semânticos e *traces*.
2. **Benchmark controlado de migração de *embeddings* (S7):** comparar *dual-index shadow rollout* vs. reindexação em lotes sob restrições de latência e orçamento em produção.
3. **Avaliação de *parsing* e *chunking* em corpora em língua portuguesa (S2/S4):** investigar sistematicamente a corrupção de diacríticos (`ç`, acentos) e tabelas em PDFs regulatórios/jurídicos brasileiros, estendendo a observação pontual de `A23`.
