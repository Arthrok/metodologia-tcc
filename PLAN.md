# Plano de Implementação — ACL Anthology + Scopus

## 1. Objetivo

Implementar a coleta automatizada das oito famílias de busca **S1–S8** nas bases:

* ACL Anthology
* Scopus

A implementação deve seguir a metodologia do TCC e produzir dados brutos rastreáveis e reprodutíveis para posterior:

```text
coleta
  ↓
consolidação
  ↓
deduplicação
  ↓
filtro temporal
  ↓
triagem com LLM/skill
  ↓
full text
  ↓
qualidade
  ↓
extração
```

Nesta implementação **não desenvolver ainda**:

* screening com LLM;
* avaliação QA1–QA6;
* download massivo de PDFs;
* classificação transferida/adaptada/nova;
* integração de literatura cinzenta;
* alterações nos coletores IEEE/ACM.

A metodologia define ACL Anthology e Scopus como duas das quatro bases acadêmicas e exige que cada execução registre base, data, string, campos pesquisados, filtros e quantidade de resultados.

---

# 2. Estado inicial do projeto

Já existem:

```text
.env
requirements.txt
```

O `requirements.txt` já contém:

```text
acl-anthology
```

No `.env` existe atualmente:

```env
SCORPUS_API_KEY=...
```

Corrigir preferencialmente para:

```env
SCOPUS_API_KEY=...
```

Durante a implementação pode ser aceito temporariamente:

```python
api_key = os.getenv("SCOPUS_API_KEY") or os.getenv("SCORPUS_API_KEY")
```

para evitar quebra enquanto o `.env` é corrigido.

Adicionar, se necessário:

```env
SCOPUS_INST_TOKEN=
```

O token institucional deve ser opcional.

---

# 3. Dependências

Manter a implementação simples.

```text
acl-anthology
requests
python-dotenv
pydantic
tenacity
PyYAML
```

Não adicionar nesta etapa:

```text
haystack
qdrant
langchain
pandas
openai
```

Essas dependências não são necessárias para a coleta.

---

# 4. Estrutura proposta

```text
project/
├── .env
├── .gitignore
├── requirements.txt
│
├── config/
│   └── search_queries.yaml
│
├── src/
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── acl.py
│   │   └── scopus.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── paper.py
│   │
│   ├── search/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── matcher.py
│   │
│   └── utils/
│       ├── io.py
│       └── text.py
│
├── scripts/
│   ├── collect_acl.py
│   └── collect_scopus.py
│
├── data/
│   ├── raw/
│   │   ├── acl/
│   │   └── scopus/
│   │
│   └── manifests/
│       ├── acl/
│       └── scopus/
│
└── tests/
    ├── test_matcher.py
    ├── test_acl_normalization.py
    └── test_scopus_normalization.py
```

Não reorganizar os coletores existentes do IEEE/ACM neste momento, a menos que seja necessário para compartilhar apenas o modelo de saída.

---

# 5. Fonte única das buscas S1–S8

Não duplicar as strings dentro dos coletores.

Criar:

```text
config/search_queries.yaml
```

A metodologia exige que a estrutura conceitual das buscas seja mantida e permite apenas adaptações sintáticas e dos campos pesquisados conforme cada base.

Em vez de armazenar apenas uma string booleana, estruturar os componentes.

Exemplo:

```yaml
domain:
  terms:
    - "retrieval augmented generation"
    - "retrieval-augmented generation"

families:

  S1:
    stage: sources
    label: Fontes
    terms:
      - "data source*"
      - "knowledge source*"
      - "source selection"
      - "source curation"
      - "corpus curation"

  S2:
    stage: ingestion
    label: Ingestão
    terms:
      - "data ingestion"
      - "document ingestion"
      - "data extraction"
      - "document parsing"
      - "OCR"
      - "crawl*"

  S3:
    stage: storage
    label: Armazenamento
    terms:
      - "vector database*"
      - "vector store*"
      - "vector index*"
      - "document store*"
      - "embedding store*"

  S4:
    stage: preparation
    label: Preparação
    terms:
      - "chunk*"
      - "text segment*"
      - "document split*"
      - "text preprocessing"
      - "document preprocessing"
      - "text normalization"
      - "embedding generation"

  S5:
    stage: serving
    label: Disponibilização
    terms:
      - "retrieval strateg*"
      - "hybrid search"
      - "rerank*"
      - "metadata filter*"
      - "context compression"

  S6:
    stage: usage_feedback
    label: Uso e feedback
    terms:
      - "RAG evaluation"
      - "retrieval evaluation"
      - "observab*"
      - "tracing"
      - "user feedback"

  S7:
    stage: maintenance
    label: Manutenção
    terms:
      - "freshness"
      - "reindex*"
      - "document update*"
      - "corpus update*"
      - "incremental update*"
      - "version*"

  S8:
    stage: disposal
    label: Descarte
    terms:
      - "data deletion"
      - "document deletion"
      - "deindex*"
      - "erasure"
      - "retention"
      - "purge"
      - "expiration"
```

Esses termos devem reproduzir as strings S1–S8 definidas no TCC.

A partir desta configuração devem ser geradas:

```text
query canônica
query Scopus
matcher ACL
```

Assim nenhuma base terá uma versão manual divergente da mesma família.

---

# 6. Modelo comum de artigo

Criar um modelo Pydantic.

Exemplo conceitual:

```python
class PaperRecord(BaseModel):
    source: str
    source_id: str

    title: str
    abstract: str | None

    doi: str | None

    authors: list[str]

    year: int | None
    publication_date: str | None

    venue: str | None

    url: str | None
    pdf_url: str | None

    search_families: list[str]

    retrieved_at: datetime
```

Também armazenar metadados da origem:

```python
class SearchProvenance(BaseModel):
    source: str
    family: str
    stage: str

    canonical_query: str
    executed_query: str

    searched_fields: list[str]

    retrieved_at: datetime
```

O objetivo é permitir posteriormente:

```text
mesmo artigo
  ├── encontrado em Scopus / S2
  ├── encontrado em Scopus / S4
  ├── encontrado em ACL / S2
  └── encontrado em ACL / S4
```

sem perder nenhuma ocorrência.

---

# 7. Não deduplicar entre famílias durante a coleta

Cada S1–S8 representa uma execução metodológica independente.

Portanto:

```text
S2 encontrou paper A
S4 encontrou paper A
```

é informação relevante.

Não transformar isso imediatamente em:

```text
paper A
```

e perder a proveniência.

Salvar primeiro a ocorrência.

Posteriormente será possível consolidar:

```json
{
  "paper_id": "...",
  "search_families": ["S2", "S4"]
}
```

---

# 8. Implementação do Scopus

## 8.1 Autenticação

Usar:

```http
X-ELS-APIKey
```

e opcionalmente:

```http
X-ELS-Insttoken
```

O Scopus Search API oficialmente exige a API Key e também suporta token institucional.

Implementar um `ScopusClient`.

Exemplo conceitual:

```python
class ScopusClient:

    def search(...):
        ...

    def get_abstract(...):
        ...
```

---

# 9. Geração da query Scopus

As S1–S8 devem ser executadas usando:

```text
TITLE-ABS-KEY(...)
```

Esse campo do Scopus pesquisa simultaneamente:

```text
title
abstract
keywords
```

Exemplo S2:

```text
TITLE-ABS-KEY(
    ("retrieval augmented generation"
     OR "retrieval-augmented generation")
    AND
    ("data ingestion"
     OR "document ingestion"
     OR "data extraction"
     OR "document parsing"
     OR OCR
     OR crawl*)
)
```

Criar função:

```python
build_scopus_query(family)
```

Nunca manter oito queries Scopus manualmente.

---

# 10. Não aplicar filtro temporal na coleta

Não adicionar:

```text
PUBYEAR > 2019
```

nem:

```text
date=2020-2026
```

durante esta coleta.

Isso é importante porque o TCC define:

```text
resultados brutos
→ consolidação
→ deduplicação
→ critério temporal
```

O E2 deve ser aplicado posteriormente, não na recuperação dos registros.

Portanto, o resultado bruto deve incluir também artigos anteriores a 2024.

---

# 11. Busca Scopus

Endpoint:

```text
GET https://api.elsevier.com/content/search/scopus
```

A API aceita consultas booleanas e paginação.

A primeira etapa deve usar:

```text
view=STANDARD
count=200
```

porque o `STANDARD` permite até 200 registros por chamada, enquanto `COMPLETE` tem limites menores. Atualmente a documentação da Elsevier informa máximo de 200 resultados por página para `STANDARD` e 25 para `COMPLETE`.

Objetivo desta etapa:

```text
descobrir todos os Scopus IDs
+
metadados básicos
+
quantidade bruta
```

---

# 12. Paginação Scopus

Implementar inicialmente paginação normal:

```text
start=0
count=200

start=200
count=200

start=400
...
```

Continuar até atingir `totalResults`.

A API suporta `start` e `count` oficialmente.

Entretanto, adicionar proteção para:

```python
if total_results > 5000:
```

usar **cursor pagination**, porque a Elsevier impõe limite de 5.000 resultados quando paginação por cursor não é utilizada.

Não truncar silenciosamente.

Se cursor pagination não puder ser utilizado pela autenticação disponível:

```text
ERRO EXPLÍCITO
```

registrando que aquela execução não coletou o universo completo.

---

# 13. Scopus: busca e enriquecimento devem ser separados

Não usar uma chamada pesada para cada registro logo durante a busca.

Fazer:

```text
Scopus Search
     ↓
IDs encontrados
     ↓
salvar resultado bruto
     ↓
IDs únicos
     ↓
Abstract Retrieval
```

Isso evita buscar o mesmo abstract várias vezes quando um artigo aparece em S2, S4 e S5.

---

# 14. Scopus Abstract Retrieval

Depois de executar as oito buscas, reunir os Scopus IDs únicos.

Para cada artigo:

```text
GET /content/abstract/scopus_id/{id}
```

Usar preferencialmente:

```text
view=META_ABS
```

O `META_ABS` inclui, entre outros campos:

```text
title
authors
DOI
publication date
abstract
```

e especificamente contém `dc:description`, correspondente ao texto do abstract.

Não utilizar `FULL` sem necessidade.

O objetivo é obter informação suficiente para futura triagem por:

```text
title
abstract
metadata
```

---

# 15. Cache de abstracts do Scopus

Nunca chamar `Abstract Retrieval` duas vezes para o mesmo `Scopus ID`.

Criar:

```text
data/raw/scopus/metadata/
```

por exemplo:

```text
2-s2.0-85123456789.json
```

ou utilizar um índice local.

Fluxo:

```text
if metadata existe:
    reutilizar
else:
    consultar API
```

Isso economiza quota e permite retomar uma coleta interrompida.

---

# 16. Rate limit e retries

Implementar tratamento para:

```text
429
500
502
503
504
```

Usar `tenacity`.

Exemplo conceitual:

```text
retry exponencial
1s
2s
4s
8s
...
```

O Scopus atualmente retorna HTTP 429 ao exceder o limite e fornece informações de quota/rate limit nos headers.

Registrar:

```text
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
```

quando disponíveis.

Nunca fazer requests em paralelo agressivamente.

---

# 17. Raw payload Scopus

Para reprodutibilidade, preservar os dados retornados pela API.

Estrutura:

```text
data/raw/scopus/
├── S1/
│   ├── page_0001.json
│   ├── page_0002.json
│   └── records.jsonl
├── S2/
│   └── ...
│
└── metadata/
    ├── SCOPUS_ID_1.json
    └── SCOPUS_ID_2.json
```

Os arquivos `page_*.json` são a resposta bruta.

`records.jsonl` é a representação normalizada.

---

# 18. Implementação ACL Anthology

O ACL não deve ser tratado como uma API REST de busca equivalente ao Scopus.

O projeto oficial fornece um pacote Python para acessar programaticamente papers, autores, volumes e demais metadados. Esse é o método recomendado pelo próprio ACL Anthology.

Criar:

```python
class ACLCollector:
    ...
```

A responsabilidade dele será:

```text
carregar Anthology
→ percorrer papers
→ aplicar matcher S1–S8
→ normalizar resultados
```

---

# 19. Snapshot do ACL

A coleta deve ser reprodutível.

Registrar:

```text
data/hora da coleta
versão do acl-anthology
commit/snapshot do repositório, quando disponível
```

O ACL Anthology mantém os metadados oficiais dos papers, autores e venues no seu repositório GitHub.

Ideal:

```json
{
  "acl_package_version": "...",
  "acl_repository_commit": "...",
  "retrieved_at": "..."
}
```

Se o pacote não expuser diretamente o commit, registrar pelo menos:

```text
package version
collection timestamp
```

---

# 20. Campos pesquisados no ACL

Para ACL, realizar a busca local sobre:

```text
title + abstract
```

Registrar no manifest:

```json
{
  "searched_fields": [
    "title",
    "abstract"
  ]
}
```

Não fingir que a execução ACL foi `TITLE-ABS-KEY`, pois essa é uma adaptação específica do Scopus.

O TCC permite explicitamente adaptações de campo entre bases desde que elas sejam registradas.

---

# 21. Matcher ACL

Não implementar um parser booleano completo.

As buscas possuem a estrutura:

```text
(RAG_TERM_1 OR RAG_TERM_2)
AND
(TERM_1 OR TERM_2 OR TERM_3...)
```

Então implementar diretamente:

```python
matches_domain(text)
and
matches_family(text, family)
```

Exemplo:

```python
if matches_any(text, rag_terms) and matches_any(text, family_terms):
    return True
```

---

# 22. Normalização textual ACL

Antes do matching:

```text
Unicode normalize
↓
lowercase
↓
normalizar espaços
↓
manter pontuação necessária
```

Evitar stemming ou lematização.

Queremos reproduzir as strings de busca, não implementar uma busca semântica.

---

# 23. Tratamento das aspas

Termos como:

```text
"vector database"
"data ingestion"
"retrieval augmented generation"
```

devem funcionar como frases.

Ou seja:

```text
"data ingestion"
```

não deve significar simplesmente:

```text
data AND ingestion em qualquer posição
```

Deve procurar a sequência textual correspondente, tolerando apenas normalizações triviais de espaços.

---

# 24. Tratamento de wildcard `*`

Implementar prefix matching.

Exemplo:

```text
chunk*
```

deve reconhecer:

```text
chunk
chunks
chunking
chunked
```

`observab*`:

```text
observable
observability
observability-related
```

`version*`:

```text
version
versions
versioning
```

Converter internamente para regex com limite de palavra adequado.

Exemplo conceitual:

```python
r"\bchunk\w*"
```

Tomar cuidado com termos compostos:

```text
"vector database*"
```

deve reconhecer:

```text
vector database
vector databases
```

---

# 25. Matching das oito famílias no ACL

Não percorrer todo o ACL oito vezes.

Fazer apenas uma passagem:

```python
for paper in anthology:
    text = normalize(
        title + " " + abstract
    )

    if not matches_rag(text):
        continue

    for family in families:
        if matches_family(text, family):
            registrar ocorrência
```

Isso reduz drasticamente processamento.

Um artigo pode pertencer a várias famílias.

Exemplo:

```json
{
  "source_id": "2025.acl-long.123",
  "families": [
    "S2",
    "S4",
    "S5"
  ]
}
```

---

# 26. ACL sem abstract

Alguns registros podem não possuir abstract.

Não descartar automaticamente.

Nesse caso:

```text
searched text = title
```

e registrar:

```json
{
  "abstract_available": false
}
```

A ausência de abstract é uma característica do registro, não um critério automático de exclusão.

---

# 27. ACL PDF

O ACL Anthology hospeda os PDFs dos papers em seus servidores.

Nesta etapa apenas gerar/salvar:

```text
paper_url
pdf_url
```

Não baixar os PDFs.

Exemplo:

```json
{
  "url": "https://aclanthology.org/2025.acl-long.123/",
  "pdf_url": "https://aclanthology.org/2025.acl-long.123.pdf"
}
```

PDF será usado apenas na etapa posterior de análise full-text.

---

# 28. Raw ACL

Estrutura:

```text
data/raw/acl/
├── S1.jsonl
├── S2.jsonl
├── S3.jsonl
├── S4.jsonl
├── S5.jsonl
├── S6.jsonl
├── S7.jsonl
└── S8.jsonl
```

Além disso:

```text
data/raw/acl/all_records.jsonl
```

Pode armazenar cada paper apenas uma vez com:

```json
{
  "search_families": [
    "S2",
    "S4"
  ]
}
```

Os arquivos S1–S8 devem ser derivados desta informação, sem perder a associação.

---

# 29. Manifest de execução

Cada execução deve gerar um manifest independente.

Exemplo:

```text
data/manifests/scopus/
2026-09-23T200000.json

data/manifests/acl/
2026-09-23T201500.json
```

Scopus:

```json
{
  "source": "scopus",
  "executed_at": "...",
  "search_fields": [
    "title",
    "abstract",
    "keywords"
  ],
  "adapter": "TITLE-ABS-KEY",
  "families": {
    "S1": {
      "canonical_query": "...",
      "executed_query": "TITLE-ABS-KEY(...)",
      "total_results_reported": 0,
      "total_results_collected": 0
    }
  }
}
```

ACL:

```json
{
  "source": "acl",
  "executed_at": "...",
  "search_fields": [
    "title",
    "abstract"
  ],
  "search_mode": "local_metadata_matching",
  "acl_package_version": "...",
  "families": {
    "S1": {
      "canonical_query": "...",
      "total_results": 0
    }
  }
}
```

---

# 30. Não aplicar E1–E5 nesta fase

Não excluir artigos porque:

```text
ano < 2024
RAG parece incidental
não parece engenharia de dados
não parece relevante
```

A coleta deve produzir os **resultados brutos**.

Especialmente E2:

```text
publicação anterior a 2024
```

será aplicado depois.

Isso está de acordo com a metodologia, que separa execução da busca, consolidação, critério temporal e triagem.

---

# 31. Não usar LLM nesta implementação

Nenhum resultado deve ser eliminado via GPT nesta etapa.

Não utilizar:

```text
OpenAI
prompt
embedding
similaridade
skill
```

para decidir os resultados da busca.

A futura skill receberá posteriormente:

```text
title
abstract
metadata
```

e aplicará:

```text
I1
I2
I3
E3
E4
E5
```

Mas isso será outro módulo.

---

# 32. Preparar compatibilidade com a futura skill

O registro normalizado deve conter pelo menos:

```json
{
  "id": "...",
  "source": "...",
  "title": "...",
  "abstract": "...",
  "authors": [],
  "year": 2025,
  "doi": "...",
  "venue": "...",
  "search_families": [],
  "url": "...",
  "pdf_url": "..."
}
```

Assim, no futuro:

```text
PaperRecord
    ↓
mlr-screening skill
```

sem alterar os coletores.

---

# 33. CLI dos coletores

Criar:

```bash
python scripts/collect_scopus.py
```

para executar:

```text
S1
S2
S3
S4
S5
S6
S7
S8
```

Também permitir:

```bash
python scripts/collect_scopus.py --family S4
```

e:

```bash
python scripts/collect_acl.py
```

ou:

```bash
python scripts/collect_acl.py --family S4
```

Adicionar:

```bash
--force
```

para ignorar cache.

E:

```bash
--output-dir
```

quando necessário.

---

# 34. Resume de coleta

Uma coleta interrompida não pode obrigar o usuário a começar novamente.

Scopus:

```text
S1 page 1 ✓
S1 page 2 ✓
S1 page 3 ✗
```

na próxima execução:

```text
retomar S1 page 3
```

Abstract Retrieval:

```text
ID já existe
→ não chamar API novamente
```

ACL:

```text
coleta local
→ pode sobrescrever normalmente
```

por não depender de quota externa.

---

# 35. Logs

Utilizar `logging`.

Exemplo:

```text
[SCOPUS] Starting S1
[SCOPUS] Query: TITLE-ABS-KEY(...)
[SCOPUS] Total reported: 742
[SCOPUS] Page 1/4: 200
[SCOPUS] Page 2/4: 200
...
[SCOPUS] S1 completed: 742

[ACL] Loading Anthology
[ACL] Papers scanned: 131152
[ACL] RAG candidates: 342
[ACL] S1: 43
[ACL] S2: 75
...
```

Não mostrar a API Key.

---

# 36. Relatório final da execução

Ao fim, imprimir:

```text
=================================
ACADEMIC COLLECTION
=================================

SCOPUS

S1 Fontes              000
S2 Ingestão            000
S3 Armazenamento       000
S4 Preparação          000
S5 Disponibilização    000
S6 Uso e feedback      000
S7 Manutenção          000
S8 Descarte            000

Total de ocorrências: 000
Papers únicos: 000


ACL ANTHOLOGY

S1 Fontes              000
S2 Ingestão            000
S3 Armazenamento       000
S4 Preparação          000
S5 Disponibilização    000
S6 Uso e feedback      000
S7 Manutenção          000
S8 Descarte            000

Total de ocorrências: 000
Papers únicos: 000
=================================
```

Esses números deverão posteriormente poder alimentar as tabelas metodológicas.

---

# 37. Testes obrigatórios do matcher ACL

Criar testes unitários.

### RAG

```text
"Retrieval-Augmented Generation"
→ match

"retrieval augmented generation"
→ match

"retrieval generation"
→ não match
```

### Wildcard

```text
chunk
→ chunk* match

chunking
→ chunk* match

chunked
→ chunk* match
```

### Phrase

```text
"vector database"
→ "vector database*" match

"vector databases"
→ match
```

### AND entre blocos

```text
"This paper proposes document ingestion..."

sem RAG
→ NÃO retornar S2
```

```text
"Retrieval augmented generation using document ingestion..."

→ S2
```

---

# 38. Testes Scopus

Mockar HTTP.

Testar:

```text
200
401
403
429
500
paginação
resultado vazio
total > 5000
abstract ausente
DOI ausente
```

Validar também:

```text
S1 → query gerada corretamente
...
S8 → query gerada corretamente
```

---

# 39. Critérios de aceite — Scopus

A implementação do Scopus estará pronta quando:

* conseguir autenticar com `SCOPUS_API_KEY`;
* executar separadamente S1–S8;
* gerar `TITLE-ABS-KEY(...)` corretamente;
* não aplicar filtro temporal;
* coletar todas as páginas;
* detectar situações >5.000 resultados;
* manter resposta bruta;
* registrar total reportado e total coletado;
* coletar metadata/abstract dos IDs únicos;
* reutilizar cache;
* gerar JSONL normalizado;
* gerar manifest;
* conseguir retomar execução;
* não expor a API Key em logs.

---

# 40. Critérios de aceite — ACL

A implementação ACL estará pronta quando:

* carregar os metadados oficiais via `acl-anthology`;
* percorrer o corpus apenas uma vez;
* pesquisar title + abstract;
* reconhecer os dois termos RAG;
* implementar corretamente phrases;
* implementar corretamente `*`;
* classificar um paper em múltiplas famílias;
* preservar papers sem abstract;
* gerar URLs para página e PDF;
* não baixar PDFs;
* gerar S1–S8;
* registrar versão/snapshot da fonte;
* gerar JSONL normalizado;
* gerar manifest.

---

# 41. Ordem recomendada de implementação

### Etapa 1 — Configuração

Implementar:

```text
search_queries.yaml
loader da configuração
modelo PaperRecord
modelo SearchProvenance
```

### Etapa 2 — Matcher compartilhado

Implementar:

```text
normalização textual
phrase matching
wildcard
matches_domain()
matches_family()
```

Escrever testes antes de seguir.

### Etapa 3 — ACL

Implementar ACL primeiro porque:

```text
não possui quota de API
não possui autenticação
permite validar S1–S8 rapidamente
```

Resultado esperado:

```text
data/raw/acl/
+
manifest ACL
```

### Etapa 4 — Scopus Search

Implementar:

```text
autenticação
query builder
search
paginação
retry
rate limit
raw pages
```

Resultado esperado:

```text
IDs Scopus das S1–S8
```

### Etapa 5 — Scopus enrichment

Implementar:

```text
IDs únicos
→ Abstract Retrieval
→ META_ABS
→ cache
```

Resultado:

```text
title
abstract
authors
DOI
metadata
```

### Etapa 6 — Normalização

Garantir que ACL e Scopus entreguem o mesmo modelo:

```text
PaperRecord
```

### Etapa 7 — Manifests

Gerar:

```text
queries
datas
campos
resultados
versões
quantidades
```

### Etapa 8 — Relatório final

Exibir S1–S8 por base e total de artigos únicos.

---

# 42. Resultado esperado desta implementação

Ao final deste trabalho devem existir:

```text
ACL
├── resultados S1–S8
├── metadata normalizada
├── links de PDF
├── manifest
└── snapshot/versionamento da coleta

Scopus
├── resultados S1–S8
├── respostas brutas
├── metadata/abstract
├── cache
├── manifest
└── informações de quota
```

Produzindo:

```text
             S1..S8
                │
       ┌────────┴────────┐
       │                 │
      ACL             Scopus
       │                 │
       └────────┬────────┘
                │
        PaperRecord comum
                │
                ▼
          etapa futura
                │
     consolidação/deduplicação
                │
          filtro E2
                │
        mlr-screening skill
```

A implementação termina no `PaperRecord comum`.

**Não implementar a skill de screening nesta entrega.**

A skill deve ser uma próxima etapa independente, porque a metodologia separa coleta, consolidação/recorte e triagem.
