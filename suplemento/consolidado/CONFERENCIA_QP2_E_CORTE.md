# Conferência de QP2 e notas de corte

> **Atualização (16/11/2026).** Este documento foi gerado antes da consolidação dos excertos cinzentos. Os 65 excertos cinzentos individuais estão em `rastreabilidade/evidencias_244.csv`, e o vínculo de cada adaptação da Tabela QP2 com suas evidências está em `rastreabilidade/qp2_vinculo_linha_evidencias.csv`; quando houver divergência, prevalecem esses arquivos. O otimizador que escolhe pré ou pós-filtro pela seletividade estimada é de A34 (A34-e03); C05 contribui com busca filtrada por metadados e varredura iterativa no pgvector (C05-e01, C05-e02).

Os excertos acadêmicos abaixo vêm dos lotes JSON. A matriz e a auditoria não contêm os excertos originais individuais das 37 fontes cinzentas. As menções cinzentas permanecem pendentes de conferência textual; não foram inventadas citações.

Corpus: 51 acadêmicas + 37 cinzentas = 88 fontes.
Excertos acadêmicos válidos: 179; adaptações acadêmicas marcadas: 79.

## Adaptações acadêmicas com excerto original

### 1. A02 — Propriedade e armazenamento locais de documentos e índices por domínio (federação)
- Localização: p.1 (Resumo/Introdução)
- Etapa: S3
- Decisão/mudança: Arquitetura em três camadas: nós locais, gateways regionais, roteamento/inferência na nuvem
- Desafio: Centralização em um único índice vetorial complica residência de dados, isolamento e conformidade (GDPR/CCPA) e aumenta o raio de impacto de vazamentos
- Excerto original: "allows each domain to retain ownership of its documents and indexes while participating in a federated retrieval architecture ... raw documents never leave their local administrative boundaries"

### 2. A02 — Catálogo de metadados dos índices (domínio, modelo de embedding, latência) e aplicação local de políticas
- Localização: p.3 (Gateways)
- Etapa: S3; S5
- Decisão/mudança: Roteador com escore custo-sensível (relevância − latência) treinado em logs
- Desafio: Encaminhar consultas a muitos índices heterogêneos sem difundir tudo
- Excerto original: "maintain lightweight catalogs of node capabilities (such as supported domains, embedding models, and latency profiles) ... They also enforce local policy decisions and rate limits"

### 3. A03 — Semente pequena e verificada manualmente da base de conhecimento
- Localização: p.3 (Active Learning)
- Etapa: S1
- Decisão/mudança: Iniciar com 10 exemplos verificados em vez de seleção não supervisionada (aleatória/cluster)
- Desafio: Ruído na base contamina a recuperação
- Excerto original: "our knowledge source begins with ten log sequences that can be easily verified by humans to ensure they are noise-free"

### 4. A03 — Atualização incremental da base guiada pela incerteza do LLM, com rotulação humana seletiva (humano no laço)
- Localização: p.3
- Etapa: S6; S7
- Decisão/mudança: Limiares de seleção (st) e de rotulação (lt) sobre a incerteza
- Desafio: Custo de rotulação humana × atualidade da base
- Excerto original: "When the uncertainty uc is low ... add the current log sequence ... directly to the knowledge source ... [when high] we perform manual annotation ... before adding it"

### 5. A04 — Armazenamento estruturado por fragmento com metadados temporais, separado do índice vetorial
- Localização: p.2–3 (Seção 3.1 e Etapa 3)
- Etapa: S3
- Decisão/mudança: Separar legislação (banco relacional) de jurisprudência/editorial (índice vetorial/léxico)
- Desafio: Citações exigem precisão em nível de fragmento
- Excerto original: "legislation and its fragments are served from a dedicated structured store ... a relational legislation database with fragment-level entries and temporal metadata"

### 6. A04 — Trilhas de auditoria por resposta e mascaramento de dados pessoais (LGPD)
- Localização: p.4
- Etapa: S6
- Decisão/mudança: Transformar alucinação silenciosa em aviso explícito por referência
- Desafio: Conformidade legal e confiança do profissional
- Excerto original: "the system operates under Brazil's LGPD with NER-based PII masking. Audit traces provide a governance layer by recording cited authorities, resolution status, and supporting official excerpts"

### 7. A05 — Remoção de documentos de baixa densidade informacional antes da indexação
- Localização: p.5
- Etapa: S1; S4
- Decisão/mudança: Limiar de proporção de stopwords; exclusão de documentos sempre mal ranqueados
- Desafio: Textos repetitivos ou procedimentais diluem a recuperação
- Excerto original: "we consider a document to be low in informational content if stop words account for more than 20% of its text, in which case the document is filtered out"

### 8. A06 — Chunking multivisão (página, seção, tamanho fixo) + elementos paratextuais
- Localização: p.1 (Introdução)
- Etapa: S4
- Decisão/mudança: Manter várias granularidades em paralelo
- Desafio: Chunking de tamanho fixo perde estrutura e tabelas espalhadas
- Excerto original: "the most widely utilized scheme to segment documents into chunks is based on a fixed length ... this common practice neglects the intrinsic structure of sections and the salient features of paratextual tables and figures"

### 9. A06 — Pipeline de parsing orientado a esquema relacional fixo, com enriquecimento de metadados por APIs externas
- Localização: p.2 (Seção 2.2)
- Etapa: S2
- Decisão/mudança: Banco relacional (DuckDB) como representação canônica do documento
- Desafio: PDF semiestruturado com layout rico
- Excerto original: "1) Querying scholar APIs ... to obtain the metadata ... 2) Splitting the text based on different granularities ... 3) Leveraging OCR models to extract non-textual elements ... 4) Asking LLMs or VLMs to generate concise summaries ... We handcraft the DB schema in advance"

### 10. A07 — Índice vetorial autenticado (Merkle + assinaturas) com versionamento do corpus à prova de adulteração
- Localização: p.1–2 (Contribuições)
- Etapa: S3; S7
- Decisão/mudança: Cada chunk assinado e incluído em árvore de Merkle comprometida por versão
- Desafio: Envenenamento do corpus por documentos maliciosos
- Excerto original: "Cryptographic binding between semantic embeddings and source documents ... Tamper-evident corpus versioning with atomic updates"

### 11. A08 — Chunking semântico (não por contagem de caracteres) para listas e tabelas
- Localização: p.4 (Lições) e p.5
- Etapa: S4
- Decisão/mudança: Chunking semântico + reranking para páginas longas
- Desafio: Tabelas e listas partidas entre chunks
- Excerto original: "Source structure dominates: long, weakly segmented pages and dense tables degrade retrieval ... Granularity mismatches—long list pages or dense tables split across chunks cause the model to miss the row"

### 12. A08 — Console administrativo para upload, reindexação e rollback; logs mínimos e amostragem semanal de respostas
- Localização: p.5 (Passos de escala)
- Etapa: S6; S7
- Decisão/mudança: Observabilidade básica (tempos + logs mínimos) basta para detectar regressões (p.4)
- Desafio: Sem console administrativo, a manutenção da base depende de engenheiros
- Excerto original: "name canonical sources, owners, and update cadence; add a small admin console for upload, re-index, and rollback; (2) Observability—retain minimal query logs and timings; sample responses weekly"

### 13. A09 — Chunking com consciência de layout e escolha de tamanho de chunk por experimento
- Localização: p.3 (Datasets) e p.4 (Seção 4.3)
- Etapa: S2; S4
- Decisão/mudança: Chunks de 2048 tokens; parser com consciência de layout
- Desafio: Documentos longos e tabelas em PDFs
- Excerto original: "PDF text chunking was done using LLMSherpa as it's layout-aware chunking helps preserve structural coherence (e.g., sections, tables) ... models utilizing 2048-token segments consistently demonstrated superior performance compared to 512-token"

### 14. A10 — Preservar a hierarquia do documento e converter tabelas para Markdown
- Localização: p.1 (Resumo)
- Etapa: S2; S4
- Decisão/mudança: Pipeline de pré-processamento orientado à estrutura
- Desafio: Tabelas e numeração hierárquica de regras
- Excerto original: "integrates a structure-aware preprocessing pipeline ... The processed knowledge base contained 1,343 document objects, including structured text chunks and Markdown-converted tables"

### 15. A12 — Normalização de codificação, chunking com sobreposição e resumo por documento com metadados indexado junto aos chunks
- Localização: p.4 (Texto simples)
- Etapa: S2; S4
- Decisão/mudança: Dois níveis de representação (chunk fino + resumo do documento)
- Desafio: Passagens longas excedem o contexto do modelo de embedding; codificações ruidosas distorcem a tokenização
- Excerto original: "each document is normalized to a unicode representation and stripped of control characters ... a sliding-window chunker that yields overlapping one-thousand-token segments ... a LLM to generate a brief summary that describes the document's meta information (e.g., file type, size, location) ... Both the fine-grained chunks and the summary are embedded"

### 16. A12 — Busca sistemática em grade da configuração da cadeia (embedding, chunk, sobreposição, busca, reranking)
- Localização: p.10–11 e p.28 (Apêndice)
- Etapa: S4; S5
- Decisão/mudança: Padrão recomendado: Gemini Embeddings + MMR + cross-encoder; sobreposição de 10–15%
- Desafio: Trade-off recall × acurácia × latência × tamanho do índice
- Excerto original: "we tested four chat models ..., two embedding models ..., and eight chunking configurations ... Overlap helps when answers straddle chunk boundaries. Too much overlap inflates the index ... Ten to fifteen percent often balances both goals"

### 17. A13 — Avaliar parser e chunker em conjunto como parte da qualidade do pipeline
- Localização: p.1–2 (Introdução)
- Etapa: S2; S4
- Decisão/mudança: Experimento fatorial completo parser × chunker
- Desafio: PDF é feito para leitura humana: tabelas desalinhadas, colunas fundidas, legendas separadas
- Excerto original: "If parsing produces incorrect structure (e.g., misaligned tables or merged columns) or chunking disrupts logical units (e.g., splitting tables or detaching figures from captions), the retrieval component may fail"

### 18. A13 — Sobreposição moderada de chunks (25%) e evitar granularidade excessiva
- Localização: p.8 (Tabela 9) e p.9 (RQ3b)
- Etapa: S4
- Decisão/mudança: 512 tokens com 25% de sobreposição
- Desafio: Chunking granular aumenta armazenamento e custo de indexação sem ganho consistente
- Excerto original: "neural splitting explodes the corpus to more than eight chunks per page, increasing indexing cost by a factor of four ... 25% overlap produces the strongest retrieval on both datasets ... lifts MRR from 0.529 (no overlap) to 0.658"

### 19. A14 — Calibrar tamanho de chunk e usar filtro por metadados (tipo de documento) para reduzir o espaço de busca
- Localização: p.12 (6.1)
- Etapa: S3; S4; S5
- Decisão/mudança: Chunks de 200–500 tokens; filtro por tipo de documento
- Desafio: Escalabilidade do índice e latência
- Excerto original: "Token chunk sizes between 200–500 struck a practical balance between retrieval relevance and query latency. Smaller chunks bloated the index ... With large corpora (>10k embeddings), FAISS latency increased noticeably. Metadata filtering by document type reduced search time"

### 20. A14 — Registrar perguntas, respostas e avaliações dos usuários e usá-las para ajustar a recuperação e o chunking
- Localização: p.12 (6.2)
- Etapa: S6
- Decisão/mudança: Armazenamento leve (SQLite) de interações
- Desafio: Identificar falhas em produção
- Excerto original: "We used SQLite to log user questions, responses, and ratings ... This lightweight store helped identify system failures ... User ratings and comments exposed weak spots, guiding adjustments to retrieval settings and chunk sizes"

### 21. A14 — Hospedagem própria por conformidade; citar a fonte (arquivo e link) na resposta; tratar desbalanceamento de fontes
- Localização: p.12 (6.2–6.3)
- Etapa: S1; S3; S5
- Decisão/mudança: Reranking para diversidade; ocultar fontes em domínios sensíveis
- Desafio: GDPR; confiança; viés por tipo de documento
- Excerto original: "We hosted LLMs and vector stores on our own servers to reduce GDPR risks ... Providing filenames and download links helped users validate AI outputs. In security use cases ... sources were intentionally hidden ... Unbalanced source data led to over-representation of some document types"

### 22. A15 — Metadados estruturais por unidade de evidência (documento, página, modalidade, título pai, tabela, parte)
- Localização: p.3 (Ingestão)
- Etapa: S3; S4
- Decisão/mudança: Esquema de metadados que permite reconstruir objetos multipartes
- Desafio: Evidência multimodal e tabelas fragmentadas
- Excerto original: "Each evidence unit is stored with metadata such as document identifier, page number, modality type, heading parent, table identifier, table part index, and document-local chunk index"

### 23. A17 — Deslocar o custo de estruturação para a ingestão offline
- Localização: p.7 (Latência)
- Etapa: S3; S5
- Decisão/mudança: Pré-computar o grafo; recuperação dinâmica sem top-k fixo
- Desafio: Métodos que varrem páginas na consulta são caros
- Excerto original: "Graph construction is performed once, offline during ingestion, not affecting inference-time latency. During inference, our agent-based retriever typically issues 2–5 LLM calls"

### 24. A18 — Enriquecer cada chunk com resumo do documento de origem (metadado sintético)
- Localização: p.5 (Pipeline)
- Etapa: S4
- Decisão/mudança: Chunking recursivo + prefixo de resumo; só recuperação densa
- Desafio: Contexto global perdido no chunking
- Excerto original: "We prepend the document-level summary to each chunk derived from that document ... The summary-augmented chunks are then embedded and indexed"

### 25. A19 — Forense de dados: rastrear até a fonte e o pipeline de coleta comprometidos
- Localização: p.2 (Introdução)
- Etapa: S1; S2
- Decisão/mudança: Priorizar rastreamento a defesas cada vez mais complexas
- Desafio: Defesas na inferência são contornadas por ataques adaptativos
- Excerto original: "By uncovering compromised data sources and vulnerabilities in the data collection pipeline, poison forensics enables proactive mitigation strategies"

### 26. A19 — Remoção de textos envenenados da base (descarte) com verificação da correção
- Localização: p.8 e p.10
- Etapa: S8; S7
- Decisão/mudança: Remover, reenviar a consulta e comparar; inserir textos benignos quando o erro é do modelo
- Desafio: Risco de remover texto benigno; erros que não vêm da base
- Excerto original: "A straightforward post-hoc defense strategy is to eliminate poisoned texts identified ... However ... PTR may mistakenly discard benign texts or fail to remove all poisoned ones ... some incorrect outputs ... may not be the result of poisoning"

### 27. A20 — Roteamento por tipo de pergunta entre dados estruturados (SQL) e não estruturados (vetorial)
- Localização: p.1 (Resumo)
- Etapa: S5
- Decisão/mudança: Rota SQL / híbrida + validador LLM + checagem de fatos
- Desafio: RAG vetorial falha em perguntas numéricas e agregadas
- Excerto original: "An adaptive router directs fact and aggregate-based queries to SQL, while conceptual or cross-paper synthesis questions trigger a hybrid mode"

### 28. A20 — Registrar feedback com rota, evidência e resposta aceita como dataset de melhoria
- Localização: Conclusão (p.6–7)
- Etapa: S6
- Decisão/mudança: Corpus de fine-tuning supervisionado crescente
- Desafio: Feedback ainda não integrado a um ciclo ativo (declarado)
- Excerto original: "These interactions, along with metadata such as the original question, route type (SQL, RAG, or hybrid), supporting evidence, and final accepted answer, are automatically stored in a structured CSV format"

### 29. A21 — Chunking semântico por limiar de similaridade em vez de divisão fixa por caracteres
- Localização: p.3–4 (Tabela III, Fig. 3)
- Etapa: S4
- Decisão/mudança: Chunks de tamanho variável (até 2.187 caracteres) conforme a densidade semântica
- Desafio: Divisão fixa separa unidades lógicas (fórmula e derivação)
- Excerto original: "SemanticChunker ... inserts a boundary wherever cosine similarity between consecutive sentence embeddings drops below the 70th-percentile threshold ... Questions 9 and 13 received scores of zero under fixed chunking because the 500-character limit severed a formula from its derivation"

### 30. A21 — Fronteira de privacidade por arquitetura: processar documentos localmente e enviar à nuvem só metadados de esquema
- Localização: p.1 e p.5
- Etapa: S3; S5
- Decisão/mudança: Especialização de modelos por tipo de dado
- Desafio: Residência de dados institucionais × qualidade de modelos em nuvem
- Excerto original: "The dual-model architecture enforces an auditable data-privacy boundary ... all document content is processed on local hardware, and only schema metadata reaches the cloud, making this boundary architectural rather than policy-based"

### 31. A22 — Controle de acesso antes da recuperação (policy-first) e refiltragem após a fusão
- Localização: p.1 e p.4 (Algoritmo 1)
- Etapa: S5
- Decisão/mudança: Filtro compilado de papel, inquilino, região e contexto; RBAC/ABAC; zero trust
- Desafio: Vazamento de conteúdo restrito para o prompt
- Excerto original: "If access control is applied too late, restricted text may leak into the model prompt ... access control is applied before any retrieval, reranking, or answer generation so that restricted text never reaches the model"

### 32. A22 — Registrar, por passagem, postagem léxica, vetor e metadados/ACL, com versão e ID para rollback
- Localização: p.3 (Ingestão)
- Etapa: S3; S7
- Decisão/mudança: Três artefatos derivados por passagem
- Desafio: Manter coerência entre índices léxico e vetorial e permissões
- Excerto original: "ID are stored to support traceability and rollback ... For each passage, the system writes: (i) a lexical posting for BM25 search, (ii) an embedding vector for dense search, and (iii) a metadata/ACL record"

### 33. A22 — Desempate por atualidade e manutenção da qualidade dos metadados de permissão
- Localização: p.3 e p.5
- Etapa: S5; S7
- Decisão/mudança: Freshness no ranking; red team e monitoramento contínuo
- Desafio: Política antiga semanticamente próxima mas inválida; ACLs desatualizadas causam bloqueios indevidos
- Excerto original: "The final ranking is produced by Reciprocal Rank Fusion (RRF) with deduplication and freshness-aware tie breaking ... policy and ACL data can be noisy in real portals due to outdated group membership or missing labels; this can cause false blocks"

### 34. A23 — Avaliar ferramentas de conversão pela acurácia final do RAG, não por métricas de fidelidade de parsing
- Localização: p.1 (Resumo) e p.21 (4.1)
- Etapa: S2; S4
- Decisão/mudança: Benchmark ponta a ponta com 21 configurações
- Desafio: Métricas de parsing não preveem desempenho no RAG
- Excerto original: "All of these configurations used the same LLM, the same embedding model, the same maximum chunk size, and the same retrieval parameters. The variation results solely from data preparation choices ... data preparation quality is the dominant factor in RAG system performance"

### 35. A23 — Divisão hierárquica com caminho da seção (breadcrumb) prefixado ao chunk
- Localização: p.18
- Etapa: S4
- Decisão/mudança: Docling + divisão hierárquica + descrição de imagens
- Desafio: Tabelas e estrutura perdidas no chunking básico
- Excerto original: "hierarchical recursive splitting, which maps the full document tree and prepends the section path to every chunk ... Docling without hierarchical metadata scored 84.7% ... with hierarchical splitting and breadcrumb metadata reached 91.2%"

### 36. A23 — Arquitetura em camadas Bronze/Silver/Gold para artefatos do pipeline RAG
- Localização: p.4
- Etapa: S2; S3
- Decisão/mudança: Separação de ingestão, transformação e indexação; troca por um parâmetro de configuração
- Desafio: Reprodutibilidade e troca de ferramentas
- Excerto original: "The Medallion Architecture, with Bronze (raw PDFs), Silver (intermediate processing artifacts), and Gold (cleaned Markdown with metadata, ready for indexing) layers, inspired the pipeline's data repository's layered design ... makes experiments reproducible"

### 37. A24 — Atualização contínua do banco vetorial sob leitura concorrente
- Localização: p.1 (Introdução)
- Etapa: S3; S7
- Decisão/mudança: Índice IVF de dois estágios com parâmetros de inserção separados
- Desafio: Índices de grafo têm construção cara e contenção em escrita
- Excerto original: "To improve future responses, RAG frequently updates the vector database with data representing new knowledge ... Graph indexes perform in-place updates, and require fine-grained locking ... This results in significant read-write contention"

### 38. A25 — Delegar a autorização ao IAM nativo de cada fonte, validando cada documento em tempo real
- Localização: p.1–3 (Introdução)
- Etapa: S5
- Decisão/mudança: Sem fusão de políticas; verificação por documento contra o provedor
- Desafio: Fontes com modelos de autorização heterogêneos (RBAC, ABAC, custom)
- Excerto original: "When a centralized vector database aggregates documents from multiple data providers, applying a unified access policy ... Centralized attempts to merge policies often result in permission escalation, ambiguous policy interpretation, and significant compliance overhead"

### 39. A25 — Identificador persistente por recurso ligando chunks à origem e ao IAM, para atualização e exclusão
- Localização: p.4–5 (Ingestão)
- Etapa: S2; S8
- Decisão/mudança: UUID global + ID local de origem
- Desafio: Recursos mudam (nome, local, permissão) ao longo do tempo
- Excerto original: "The Data Ingestion Manager assigns a globally unique resourceID to each resource, serving as a persistent identifier linking document chunks to their provider and IAM information, while also enabling efficient metadata updates and deletions"

### 40. A26 — Ontologia/grafo para desambiguar entidades e abreviações
- Localização: p.8
- Etapa: S4
- Decisão/mudança: Grafo de conhecimento com ontologia em vez de banco vetorial
- Desafio: Abreviações ambíguas e documentos quase idênticos
- Excerto original: "the same abbreviation can represent different concepts across documents ... participant I opted to use ontologies within a knowledge graph instead of a vector database ... certain types of data—such as addresses or product pages—are often highly similar"

### 41. A26 — Rodar benchmark de novo após mudanças nos dados ou componentes (teste de regressão)
- Localização: p.7
- Etapa: S7; S6
- Decisão/mudança: —
- Desafio: Prioridade moderada; ofuscada por 'aprendizado contínuo'
- Excerto original: "Continuous Operation encompasses the ability to maintain, monitor, and update the RAG system during deployment ... the importance of benchmarking the system regularly, especially after changes in data or system components"

### 42. A29 — Decidir quando e como indexar cada dataset conforme o uso esperado
- Localização: p.1 (Introdução)
- Etapa: S3
- Decisão/mudança: Índice adaptativo (cracking) que cresce com as consultas
- Desafio: Custo inicial de indexação não compensa para dados raramente consultados
- Excerto original: "Embedding data lakes, in principle, would require building millions of indexes across diverse datasets, modalities, workloads, and embedding models, which is neither feasible nor cost efficient ... data must be indexed, which raises two questions: when and how to index the data"

### 43. A30 — Metadados temporais e de proveniência para distinguir versões coexistentes de um dado
- Localização: p.3–4
- Etapa: S4; S7
- Decisão/mudança: Enriquecimento de metadados; critério de validade temporal na avaliação
- Desafio: Várias versões do mesmo dado no corpus geram respostas obsoletas
- Excerto original: "the '2020 geological reserves of the Moxi Gas Field' may differ from the '2023 recalculated reserves.' If a model cannot recognize temporal metadata, it is highly likely to reference outdated data ... Production values, reserve estimates, market prices, and policy documents may coexist in several versions, making temporal metadata and provenance important"

### 44. A30 — Ingestão automatizada com limpeza inteligente e vetorização dinâmica em ciclo fechado
- Localização: p.3–4 e p.11
- Etapa: S2
- Decisão/mudança: —
- Desafio: PDFs com layouts complexos, tabelas multipágina; semântica em imagens técnicas (sísmica, P&ID) que o OCR não captura
- Excerto original: "These documents have complex layouts that often include columns, multi-page tables, and metadata in headers and footers ... an automated, closed-loop business process involving automatic data ingestion, intelligent data cleansing, dynamic vectorization"

### 45. A31 — Filtrar documentos recuperados conforme as permissões do usuário antes da geração
- Localização: p.1 (Resumo/Introdução)
- Etapa: S5
- Decisão/mudança: Níveis de acesso por perfil (AL1/AL2)
- Desafio: LLMs não têm controle de acesso nativo; risco de vazamento de dados de pacientes
- Excerto original: "By combining RAG with access control, Generative AI can produce answers strictly based on documents permitted by user rights ... its architecture offers a potential foundation for integrating permission-aware content generation by dynamically filtering retrieved data based on user-specific permissions"

### 46. A32 — Armazenamento vetorial integrado ao banco operacional (multimodelo) em vez de banco vetorial isolado
- Localização: p.1 e p.4 (3.1)
- Etapa: S3
- Decisão/mudança: Arquitetura de armazenamento compartilhado (LindormDFS)
- Desafio: Trade-off desempenho × integração/consistência
- Excerto original: "specialized vector databases deliver low-latency in-memory search but struggle with scalability and integration with structured data, whereas general-purpose databases provide consistency and fault tolerance at the cost of query performance ... unifying structured and unstructured data management within a single scalable system"

### 47. A32 — Particionamento temporal de tabelas vetoriais com metadados de índice compartilhados
- Localização: p.9 (4.6.1)
- Etapa: S3; S7
- Decisão/mudança: Reuso de centróides e codebooks
- Desafio: Custo de treinar índices para cada nova partição
- Excerto original: "sharing metadata (including the centroids and the HNSW graph index over centroids) across multiple vector indexes ... especially valuable for time-partitioned or rolling tables (e.g., monthly tables). This design not only eliminates the costly K-Means and PQ training steps but also mitigates the cold-start problem"

### 48. A33 — Particionar índices de modo a refletir a proveniência (instituição, departamento) em recuperação federada
- Localização: p.4
- Etapa: S3
- Decisão/mudança: Árvore hierárquica de recuperadores
- Desafio: Prontuários distribuídos entre instituições e regulação (HIPAA) que restringe o compartilhamento
- Excerto original: "The partitioning of data among nodes is meant to reflect data provenance—the root node's children represent distinct medical centers ... This design allows the federation scheme to be different between organizations depending on their data storage practices"

### 49. A33 — Controle de acesso por políticas (PBAC) em cada recuperador, com sobre-busca para compensar documentos negados
- Localização: p.5
- Etapa: S5
- Decisão/mudança: Ponto de decisão de política por folha
- Desafio: Políticas dependem de atributos variáveis do usuário, não só do documento
- Excerto original: "we cannot use Qdrant's document attribute filtering to implement authorization filtering as our access policies depend on variable user attributes ... we fetch a surplus of fetch_k > k documents ... anticipating that the current user may not be authorized"

### 50. A34 — Delta-store para inserções/exclusões em tempo real e monitor de qualidade que dispara reindexação
- Localização: p.4
- Etapa: S7; S8
- Decisão/mudança: Armazenamento relacional com ACID; reindexação por gatilho
- Desafio: Manter consistência e recall com escrita contínua
- Excerto original: "MicroNN supports real-time updates using a delta-store, enabling concurrent reads and writes. The use of a relational data store also enables index rebuilds to be performed concurrently with transactionally consistent reads. An index monitor is used to track index quality upon updates, and triggers re-indexing when necessary"

### 51. A35 — Considerar o custo de log/replicação das atualizações do índice vetorial em bancos relacionais
- Localização: p.1 (Introdução)
- Etapa: S3; S7
- Decisão/mudança: Buffer de inserção + merge em lote por partição
- Desafio: Atualização fina do índice gera WAL alto e atraso de replicação
- Excerto original: "HNSW and IVFFlat perform fine-grained updates: one insert touches multiple graph nodes or list pages. The resulting WAL volume raises commit latency, increases replication lag, and caps insert throughput"

### 52. A35 — Desacoplar a visibilidade dos novos vetores da atualização da estrutura do índice
- Localização: p.3
- Etapa: S7
- Decisão/mudança: Merge a cada 1.000 inserções
- Desafio: Buffer grande aumenta o custo de busca; inserções concentradas sobrecarregam partições
- Excerto original: "The buffer decouples visibility (vectors are visible immediately) from durability of the index structure (indexes update at merge)"

### 53. A36 — Avaliar o banco vetorial sob cargas realistas (filtros, churn, restart) em vez de benchmarks estáticos
- Localização: p.1 (Introdução)
- Etapa: S5; S7
- Decisão/mudança: Oráculo de verdade com filtros (bitmap + FAISS flat adaptativo)
- Desafio: Benchmarks sem filtro e estáticos escondem degradações de produção
- Excerto original: "Queries are commonly constrained by structured metadata filters (e.g., tenant identifiers, document types, access control labels, or time ranges), executed concurrently with continuous data ingestion and deletion, and expected to recover gracefully from restarts"

### 54. A36 — Monitorar a cadência de compactação e dimensionar pelo pior caso transitório
- Localização: p.5
- Etapa: S7; S8
- Decisão/mudança: Provisionamento pelo pior caso
- Desafio: Manutenção em segundo plano compete com as consultas
- Excerto original: "Memory usage (RSS) oscillates rather than converges, with gradual growth during ingestion followed by abrupt drops when compaction reclaims space ... can precipitate OOM events ... These observations motivate provisioning based on worst-case transients and monitoring compaction cadence"

### 55. A37 — Avaliação por camada (recuperação separada de geração) e verificação fina de evidência
- Localização: Resumo (Resultados)
- Etapa: S6
- Decisão/mudança: —
- Desafio: Avaliação ponta a ponta esconde de onde vem a falha
- Excerto original: "Independent retrieval-layer evaluation was reported in 47/157 (29.9%) studies. Grounding and faithfulness evaluation was reported in 41/157 (26.1%) studies, and fine-grained evidence verification was reported in 22/157 (14%) studies"

### 56. A39 — Extração contínua de triplas com normalização, deduplicação e proveniência até a seção de origem
- Localização: p.1 (Resumo) e p.1–2 (2.1)
- Etapa: S2; S4
- Decisão/mudança: Índice vetorial unificado (tripla + texto de origem + metadados)
- Desafio: Jargão e referências cruzadas geram triplas ausentes ou ruidosas
- Excerto original: "Agents continuously extract, normalize, and deduplicate triplets from regulatory documents; each triplet is embedded and stored, together with linked source segments and metadata ... The provenance is captured by Λ: T→2^X, mapping each t_i to one or more source sections for auditability"

### 57. A39 — Esquema mínimo com canonicalização de entidades em vez de ontologia rígida
- Localização: p.2 (2.4)
- Etapa: S4
- Decisão/mudança: Canonicalização e ligação de entidades
- Desafio: Vocabulário fragmentado
- Excerto original: "The schema light choice accelerates ingestion while relying on canonicalization to temper emergent vocabularies"

### 58. A40 — Sequência de otimização: análise do corpus → chunking → índice → busca híbrida → calibração
- Localização: p.1 (Resumo/Introdução)
- Etapa: S4; S5
- Decisão/mudança: Processo de implantação repetível
- Desafio: Configurações padrão degradam com o crescimento do corpus
- Excerto original: "production deployments routinely leave three core design decisions at default configurations — fixed-size chunking, flat vector indices, and globally applied confidence thresholds — accepting retrieval quality penalties that accumulate with document volume and query diversity"

### 59. A40 — Chunking por estrutura (títulos, tabelas, itens numerados) com lógica por tipo de elemento
- Localização: p.3
- Etapa: S4
- Decisão/mudança: Chunking por estrutura em corpora técnicos e regulatórios
- Desafio: Chunk fixo corta obrigações; semântico falha em tabelas
- Excerto original: "Segment a numbered clause at token boundary 512 and the resulting chunk carries the beginning of a legal obligation without the condition under which it applies ... semantic chunking over-performs on narrative sections and under-performs on tabular and hierarchical content"

### 60. A40 — Escolher o índice pela frequência de atualização; pré-filtro por metadados como isolamento entre inquilinos
- Localização: p.4–5
- Etapa: S3; S5
- Decisão/mudança: HNSW para ingestão contínua; pré-filtro obrigatório
- Desafio: IVF exige retreino com adições; pós-filtro arrisca vazamento entre inquilinos
- Excerto original: "HNSW ... supports incremental updates without full retraining, making it the preferred architecture for enterprise corpora where document ingestion is continuous and index freshness is a correctness requirement ... a failure to filter before ANN computation ... risks surfacing passages from one tenant's documents in another tenant's query results"

### 61. A42 — Extração com preservação de estrutura (Markdown) + chunking por estrutura
- Localização: p.3
- Etapa: S2; S4
- Decisão/mudança: Extração com Azure Document Intelligence
- Desafio: —
- Excerto original: "performs structure-preserving extraction and outputs content in Markdown format, encoding headings, tables, and structural hierarchy ... particularly well-suited to structure-aware chunking, which yielded higher overall retrieval effectiveness while incurring significantly lower computational cost"

### 62. A43 — Trace por resposta com fonte, rota, latências, consulta reescrita, resultados de recuperação, prompts e guardrails
- Localização: p.10–11 (Apêndice, Fig. 3)
- Etapa: S6
- Decisão/mudança: Arquitetura de captura de respostas e feedback
- Desafio: Diagnosticar falhas por componente do pipeline
- Excerto original: "Category – the knowledge source from which information was retrieved; Expert Selected; Time Taken; Agent Thought; Rephrased Query; IR Results – intermediate retrieval; Prompts; Guardrail Metrics"

### 63. A43 — Tratar o viés e a escassez do feedback e remover PII antes de reutilizar os dados
- Localização: p.3
- Etapa: S6
- Decisão/mudança: Dados sintéticos (5 mil exemplos) para complementar
- Desafio: Feedback escasso, enviesado e com dados pessoais
- Excerto original: "users only provide feedback to a limited extent which results in unrepresentative data collection. Users tend to report negative feedback more frequently ... organizations need to remove all personally identifiable information (PII) from query–response pairs"

### 64. A44 — Grafo com relações tipadas (referência cruzada, hierarquia, similaridade) ligado aos chunks de origem, com deduplicação
- Localização: p.4
- Etapa: S4
- Decisão/mudança: Recuperação híbrida local+global no grafo
- Desafio: Chunks independentes fragmentam relações entre cláusulas
- Excerto original: "LightRAG prompts a language model to extract entities and typed relationships from each chunk ... stored together with metadata that links them back to the originating chunk(s). Repeated entities and relations ... are deduplicated"

### 65. A44 — Priorizar o modelo de embedding e calibrar o tamanho do chunk com a janela de contexto
- Localização: p.11
- Etapa: S4; S5
- Decisão/mudança: Chunks pequenos/médios + janela grande
- Desafio: Trade-off precisão semântica × capacidade de síntese
- Excerto original: "for compliance-oriented question answering, investing in higher-quality embedding models and retrieval infrastructure is more important than the standalone language model's size ... best overall result obtained at MAX_EMBED_TOKENS = 1024 and NUM_CTX = 8192"

### 66. A45 — Minimização e mascaramento na escrita, TTL de retenção e consentimento por item, filtro por finalidade na leitura
- Localização: p.3 (Plano de governança)
- Etapa: S2; S5; S8
- Decisão/mudança: Motor de políticas com regras GDPR / EU AI Act / NIST / ISO 42001 executáveis
- Desafio: Pipelines RAG raramente codificam limitação de finalidade, retenção ou linhagem verificável
- Excerto original: "Every read/write passes through the Data Memory Controller (DMC), which enforces minimization/redaction on ingress, attaches retention (TTL) and consent tags, and filters egress by declared purpose (allow/deny/sandbox)"

### 67. A45 — Armazenamento em camadas com política de retenção por camada e arquivo frio imutável para retenção legal
- Localização: p.3 (Camadas)
- Etapa: S3; S8
- Decisão/mudança: Promoção e expiração entre camadas
- Desafio: Diferentes tempos de vida e obrigações para dados de memória
- Excerto original: "Tier 1 (Working Set) stores task-scoped artifacts ... under strict TTL and purpose tags; Tier 2 (Semantic Store) provides policy-approved, redacted chunks indexed by ANN ... Tier 3 (Cold Archive) serves legal hold and reproducibility via immutable objects and W3C PROV bundles"

### 68. A47 — Escolher a granularidade do chunk pela completude da evidência recuperada
- Localização: p.1 (Resumo) e p.11
- Etapa: S4
- Decisão/mudança: Chunks de 256 tokens com busca híbrida
- Desafio: Unidades muito finas perdem evidência; muito grandes trazem distratores
- Excerto original: "Sentence-level retrieval under-recovers multi-hop evidence, especially for questions with three or more supporting facts, while paragraph-level and moderate token-level chunks recover substantially more complete evidence ... hybrid retrieval with 256-token chunks and no overlap achieves an F1 of 0.6816 with a supporting-fact recall of 0.9609"

### 69. A48 — Padrões de produção: sem sobreposição; chunking por sentença
- Localização: p.1 (Resumo) e p.2
- Etapa: S4
- Decisão/mudança: Estudo ponta a ponta para padronizar defaults
- Desafio: Chunking decidido por regra de bolso
- Excerto original: "(i) overlap provides no measurable benefit and increases indexing cost; (ii) sentence chunking is the most cost-effective method, matching semantic chunking up to ∼5k tokens"

### 70. A49 — Pós-processamento de chunks: dividir os grandes e fundir os minúsculos
- Localização: p.6 e p.17 (Tabela 7)
- Etapa: S4
- Decisão/mudança: Limites de 100–1.100 tokens
- Desafio: Fragmentos quase vazios (0–4 tokens) ocupam vagas do top-k
- Excerto original: "These small fragments carry little semantic content yet may intrude into the top-k candidate set, displacing informative chunks ... oversized re-split, applied only to chunks exceeding 1100 tokens, and tiny-chunk merge, applied only to chunks smaller than 100 tokens"

### 71. A51 — Estruturação hierárquica do documento + recuperação que funde filhos no pai (Auto-Merge)
- Localização: p.4
- Etapa: S4; S5
- Decisão/mudança: HC200 + Auto-Merge
- Desafio: Chunks semânticos têm granularidade irregular
- Excerto original: "HiChunk first splits a document D into a list of sentences ... output a set of hierarchical chunk points ... we apply a fixed-size chunking approach on the results of HiChunk ... and propose the Auto-Merge retrieval algorithm to balance issues of varying semantic granularity"

### 72. A52 — Chunking por delimitadores do domínio com injeção de metadados hierárquicos (Lei, Capítulo, Seção, título) no texto do chunk
- Localização: p.3 (Ingestão)
- Etapa: S4
- Decisão/mudança: Carimbo semântico determinístico
- Desafio: Chunking por janela separa provisos e exceções da seção que os governa
- Excerto original: "dividing text into 1200-character sections with 300-character overlaps while using a list of domain-specific delimiters which includes 'Notwithstanding anything contained' and 'Provided that' and 'Explanation' ... A deterministic 'Semantic Stamp' is then constructed and prepended to each chunk, explicitly embedding the governing section's identity"

### 73. A52 — Recuperação pai-filho e busca ampla seguida de reranking
- Localização: p.1 (Resumo) e p.3
- Etapa: S5
- Decisão/mudança: k=60 + cross-encoder (FlashRank)
- Desafio: Top-k padrão 'enterra' a seção correta
- Excerto original: "A novel parent-child retrieval architecture first selects small metadata-rich clauses for precision and then expands them to their parent sections in order to reconstruct full statutory context ... retrieve a broad candidate pool of the top 60 documents ... then fed into a cross-encoder reranking model"

### 74. A55 — Chunking estrutural guiado pela árvore sintática (split-then-merge)
- Localização: p.1 (Resumo/Introdução)
- Etapa: S4
- Decisão/mudança: max_chunk_size 2.000 caracteres
- Desafio: Chunking por linhas quebra funções e classes
- Excerto original: "Existing line-based chunking heuristics often break semantic structures, splitting functions or merging unrelated code ... recursively breaks large AST nodes into smaller chunks and merges sibling nodes while respecting size limits"

### 75. A55 — Preservar metadados estruturais (arquivo, classe, função) nos chunks
- Localização: p.1–2 (Vantagem 3)
- Etapa: S4
- Decisão/mudança: —
- Desafio: —
- Excerto original: "Metadata retention: AST-based chunks more faithfully capture metadata at the file, class, and function levels, enhancing context matching in hybrid code+natural language tasks"

### 76. A58 — Integrar o RAG ao lakehouse governado (tabelas Iceberg, catálogo, contratos de dados, evolução de esquema)
- Localização: p.1 (Resumo/Introdução)
- Etapa: S3
- Decisão/mudança: Embeddings no nível da partição Iceberg; metadados no Glue
- Desafio: RAG como silo sem governança: alucinação, baixa reprodutibilidade, custo com embeddings redundantes
- Excerto original: "existing RAG pipelines often operate as ungoverned silos detached from enterprise data contracts, lineage, or compliance controls ... integrates directly with Apache Iceberg tables stored on Amazon S3, governed through AWS Glue Catalog metadata and schema evolution"

### 77. A58 — Metadados de linhagem por chunk (tabela, partição, versão do esquema, política) propagados até a resposta
- Localização: p.3 e p.6
- Etapa: S4; S6
- Decisão/mudança: Reprodução por manifests de snapshot do Iceberg
- Desafio: Reproduzir e auditar respostas
- Excerto original: "Documents were split into 512-token segments with metadata (table ID, partition ID, schema version, and policy tag) preserved as Iceberg partition columns for lineage tracing ... Every generated response is accompanied by verifiable provenance, including snapshot ID, partition path, and policy tag"

### 78. A59 — Enriquecer o chunk com contexto do documento (contextual retrieval) × embedar o documento antes de dividir (late chunking)
- Localização: p.1 (Resumo) e p.4–6
- Etapa: S4
- Decisão/mudança: Escolha conforme o orçamento computacional
- Desafio: Chunks isolados perdem contexto global
- Excerto original: "contextual retrieval preserves semantic coherence more effectively but requires greater computational resources. In contrast, late chunking offers higher efficiency but tends to sacrifice relevance and completeness"

### 79. A60 — Metadados estruturados (empresa, ano, seção, tipo de formulário) como sinal de recuperação embutido, não só como filtro
- Localização: p.1 (Resumo/Introdução)
- Etapa: S4; S5
- Decisão/mudança: Prefixo de metadados ou embedding unificado
- Desafio: Documentos repetitivos com linguagem idêntica entre empresas e anos
- Excerto original: "Practitioners often flatten metadata into input text as a heuristic, but the impact and trade-offs of this practice remain poorly understood ... these fields are usually applied only for post-retrieval filtering"

## Adaptações cinzentas mapeadas sem excerto original nas entradas

- C05 — **Otimizador de consultas SQL** para escolha pré vs. pós-filtro em busca vetorial híbrida. Adapta estimativa de seletividade (`F_filters < F_IVF`) para decidir entre filtragem prévia ou varredura vetorial.. Excerto/localização: pendente.
- C30 — **Controle de acesso (RBAC/ABAC/IAM)** com verificação de escopos na fonte e filtragem dos chunks recuperados antes do prompt (não pré-recuperação nem sobre-busca `fetch_k > k`; corrigido após leitura de PT04). Motivação: vetores sincronizam periodicamente e permissões alteradas não são refletidas de imediato. Excerto/localização: PT04.txt L126 ("vector databases only sync periodically"), L130 ("verify permissions directly at the data source").
- C14 — **Linhagem W3C PROV** e **OpenTelemetry** para *traces* de recuperação (5 fases) e *Evidence Packs*. Adapta proveniência de workflows e tracing de microsserviços para registrar chunks, escores, filtros, versão de índice e prompts.. Excerto/localização: pendente.
- C20, C33 — **Chunking estrutural/hierárquico/AST** e **enriquecimento contextual** (SAC, *Semantic Stamp*, *breadcrumb*). Adapta pré-processamento textual para preservar hierarquia (tabelas, seções, AST) dentro da janela de embedding/contexto.. Excerto/localização: pendente.
- C10 — **Mascaramento de PII na ingestão** preservando tokens (`PERSON_1`) e **matriz de retenção de 10 artefatos**. Adapta redação de PII para não destruir coesão referencial no chunk e diferencia TTL entre vault, vetor, prompt e audit log.. Excerto/localização: pendente.

## Restrições de uso numérico nas fontes cinzentas

- **C09** — Incluída com restrição (sem uso de números ilustrativos/marketing). Retirar todos os números ($684→$120, 45%→78%): sem método/dataset, GPU a $0 e bug no código RRF. Excerto/localização individual: indisponível nos insumos.
- **C16** — Incluída com restrição (sem uso de números ilustrativos/marketing). Retirar números de marketing ($15K+, 847k vetores, 0,847→0,872); citar apenas o risco operacional e estimativa pública (~$10/1M docs). Excerto/localização individual: indisponível nos insumos.
- **C17** — Incluída com restrição (sem uso de números ilustrativos/marketing). Retirar números dos cenários da FDA (21 dias, 92→45, 4h): são hipotéticos; links de afiliado Bright Data. Excerto/localização individual: indisponível nos insumos.
- **C21** — Incluída com restrição (sem uso de números ilustrativos/marketing). Retirar comparação competitiva do Mixedbread Store (0,865) como prova de superioridade: baseline usou apenas BM25 lexical sem embeddings densos. Excerto/localização individual: indisponível nos insumos.

## Fontes próximas da nota de corte

Inclui fontes adequadas e excluídas com nota registrada de QA=4,0/4,5 ou QG=4,0. Para fontes cinzentas, não há excerto original nas entradas autorizadas.

### C01 — QG=4 — Incluída
- Observação: Autor promove a própria biblioteca (Ember); benchmark próprio
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C03 — QG=4 — Incluída
- Observação: Síntese com referências; sem uso próprio relatado
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C04 — QG=4 — Incluída
- Observação: Checklist de produção sem dados quantitativos
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C06 — QG=4.5 — Incluída
- Observação: Incluída (C06)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C09 — QG=4.5 — Incluída com restrição (sem uso de números ilustrativos/marketing)
- Observação: Números de projeto citados sem detalhar o método
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C10 — QG=4 — Incluída
- Observação: Incluída (C10)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C14 — QG=4.5 — Incluída
- Observação: Baseado em convenções OpenTelemetry GenAI
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C15 — QG=4 — Incluída
- Observação: Incluída (C15)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C16 — QG=4.5 — Incluída com restrição (sem uso de números ilustrativos/marketing)
- Observação: Fornecedor de versionamento vetorial
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C22 — QG=4.5 — Incluída
- Observação: Incluída (C22)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C25 — QG=4 — Incluída
- Observação: Incluída (C25)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C26 — QG=4.5 — Incluída
- Observação: Autor é criador da ferramenta (Graphiti)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C27 — QG=4 — Incluída
- Observação: Incluída (C27)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### C34 — QG=4.5 — Incluída
- Observação: Incluída (C34)
- Excerto/localização: indisponível nas entradas ou fonte excluída.

### A10 — QA=4.5 (1/1/0.5/1/0/1) — Adequada
- Observação: Não discute limitações; avaliação em pequena escala.
- p.3 (Pré-processamento): "RecursiveCharacterTextSplitter with a 1,000-character chunk size and 150-character overlap ... Chunks containing fewer than ten words were removed as noise, and duplicate entries were filtered using (rule_id, chunk_text) pairs prior to embedding"
- p.1 (Resumo): "integrates a structure-aware preprocessing pipeline ... The processed knowledge base contained 1,343 document objects, including structured text chunks and Markdown-converted tables"
- p.1 e Conclusão: "context recall of 0.66, context precision of 0.72, and faithfulness of 0.74 ... answer relevancy (0.45) ... stronger performance in the retrieval engine (0.694) compared with the generation component (0.594)"

### A27 — QA=4 (1/0.5/0.5/1/0.5/0.5) — Excluída
- Observação: Só pelo resumo.
- Resumo: "We suggest a mitigation technique of evaluating the RAG system's performance on a small subset of functions (which we call canary functions) from the codebase to determine the presence of poison"

### A31 — QA=4.5 (1/0.5/0.5/1/1/0.5) — Adequada
- Observação: Artigo curto (3 páginas); PoC; amostra pequena.
- p.1 (Resumo/Introdução): "By combining RAG with access control, Generative AI can produce answers strictly based on documents permitted by user rights ... its architecture offers a potential foundation for integrating permission-aware content generation by dynamically filtering retrieved data based on user-specific permissions"
- p.3 (Discussão): "When users attempt to access restricted information, the system suggests contacting a user with the necessary permissions ... limited by a simple numeric access control model and a small patient profile sample size"

### A38 — QA=4.5 (1/0.5/1/1/0.5/0.5) — Excluída (E5 — confirmada)
- Observação: Só pelo resumo.
- Resumo: "We propose a semantic-boundary-based multi-granularity chunking strategy with chunk-level permission annotation (ACL tagging)"

### A54 — QA=4.5 (1/0.5/1/1/0.5/0.5) — Excluída
- Observação: Só pelo resumo.
- Resumo: "The method breaks down sentence embeddings into latent topics, grouping thematically related sentences—including non-adjacent ones—while preserving contextual richness ... achieving up to 19.6×–32.6× speedup and enabling scalable offline indexing"

### A57 — QA=4 (1/0.5/0.5/1/0.5/0.5) — Excluída (QA < 4 após auditoria)
- Observação: Rebaixada na revisão humana (Eric): contradições internas na Tab. 1 e erro sobre SQuAD 1.0.
- p.3: "segmented dynamically based on token-level entropies, which serve as proxies for the density of information ... Each chunk has positional metadata that makes the location of that chunk easily found at a later time"
- p.4: "this cost is only incurred once during indexing and it does not have an effect on the query time retrieval latency ... the entropy calculation can be parallelized between documents, and can be precomputed offline"
