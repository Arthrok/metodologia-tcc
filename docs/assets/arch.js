/* Mapa da arquitetura da revisão em níveis. Cada vista é uma grade de cards; as setas são
   calculadas a partir da posição real dos cards e refeitas quando a grade muda de tamanho.
   Nó: id, k (det|ia|hum|obj), c/r (grid-column/grid-row), t, s, n, chips, go (vista), d (painel).
   Seta: a→b, s/t (lado: l|r|t|b), fa/fb (fração ao longo do lado), ty (flow|fb|appr|data),
   l (rótulo), mid (fração do cotovelo), off (afastamento em U), lp (posição do rótulo), lo [dx,dy]. */
(() => {
'use strict';

const GH = 'https://github.com/Arthrok/metodologia-tcc/';
const TRI = window.TRIAGEM || [];
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ROLE = { det: 'Script', ia: 'IA · sugere', hum: 'Humano · decide' };

/* ---------- blocos de conteúdo do painel ---------- */
const kv = (rows) => `<div class="kv">${rows.map(([k, v]) => `<div>${k}</div><div>${v}</div>`).join('')}</div>`;
const files = (list) => `<div class="files">${list.map(([p, d]) => {
  const url = GH + (p.endsWith('/') ? 'tree/main/' + p.slice(0, -1) : 'blob/main/' + p);
  return `<a href="${url}" target="_blank" rel="noopener"><code>${esc(p)}</code><span class="small">${d}</span></a>`;
}).join('')}</div>`;
const cmd = (s) => `<pre><code>${esc(s)}</code></pre>`;
const goBtn = (view, label) => `<button class="btn solid go-btn" type="button" data-go="${view}">${label} →</button>`;
const doiLink = (r) => r.doi ? `https://doi.org/${r.doi}` : r.url;
const paperList = (rows) => rows.length ? `<div class="papers">${rows.map((r) =>
  `<div><b>${esc(r.title)}</b><span class="muted">${esc((r.authors || []).join(', '))} · ${esc(r.year)}</span>${doiLink(r) ? ` · <a href="${esc(doiLink(r))}" target="_blank" rel="noopener">${r.doi ? 'DOI' : 'registro'}</a>` : ''}</div>`).join('')}</div>` : '<p class="muted">Nenhuma.</p>';

/* ---------- ciclo de vida (Tabela do referencial + contagens do artigo) ---------- */
const STAGES = {
  S1: { name: 'Fontes', q: 'De onde o conteúdo vem, quem responde por ele e sob quais restrições pode ser usado?', sig: 'Autoridade, atualidade, cobertura, duplicidade e permissão documental.', terms: '"data source*" OR "knowledge source*" OR "source selection" OR "source curation" OR "corpus curation"', sc: 542, acl: 46, ieee: 343, acm: 13, tri: 10, exA: 7, exG: 3, dev: [6, 6], hn: [494, 0] },
  S2: { name: 'Ingestão', q: 'Como a equipe registra, extrai e valida a entrada de novos dados?', sig: 'Versão do documento, parsing, OCR, metadados de origem e tratamento de falhas.', terms: '"data ingestion" OR "document ingestion" OR "data extraction" OR "document parsing" OR OCR OR crawl*', sc: 340, acl: 18, ieee: 173, acm: 27, tri: 17, exA: 19, exG: 7, dev: [81, 15], hn: ['1.361', 13] },
  S3: { name: 'Armazenamento', q: 'Onde dados e derivados permanecem disponíveis?', sig: 'Ligação entre documento, texto extraído, chunk, embedding, índice e cache.', terms: '"vector database*" OR "vector store*" OR "vector index*" OR "document store*" OR "embedding store*"', sc: 724, acl: 13, ieee: 452, acm: 33, tri: 27, exA: 25, exG: 4, dev: [289, 15], hn: [546, 11] },
  S4: { name: 'Preparação', q: 'Como os dados se tornam adequados ao consumo?', sig: 'Preservação de estrutura, chunking, enriquecimento por metadados e vetorização.', terms: 'chunk* OR "text segment*" OR "document split*" OR "text preprocessing" OR "document preprocessing" OR "text normalization" OR "embedding generation"', sc: 712, acl: 81, ieee: 470, acm: 51, tri: 27, exA: 36, exG: 14, dev: [438, 15], hn: [451, 30] },
  S5: { name: 'Disponibilização', q: 'Como o consumidor recebe o dado?', sig: 'Filtros, recuperação, reranqueamento e montagem de contexto em tempo de consulta.', terms: '"retrieval strateg*" OR "hybrid search" OR rerank* OR "metadata filter*" OR "context compression"', sc: 768, acl: 113, ieee: 443, acm: 63, tri: 18, exA: 34, exG: 14, dev: [264, 15], hn: [210, 24] },
  S6: { name: 'Uso e feedback', q: 'Que sinais revelam utilidade ou falha?', sig: 'Trechos irrelevantes, respostas sem evidência, traces e retorno de usuários.', terms: '"RAG evaluation" OR "retrieval evaluation" OR observab* OR tracing OR "user feedback"', sc: 290, acl: 32, ieee: 235, acm: 57, tri: 13, exA: 25, exG: 4, dev: [175, 15], hn: [408, 14] },
  S7: { name: 'Manutenção', q: 'Como a equipe preserva coerência e utilidade ao longo do tempo?', sig: 'Reindexação, atualização de vetores, revisão de permissões e análise de impacto.', terms: 'freshness OR reindex* OR "document update*" OR "corpus update*" OR "incremental update*" OR version*', sc: 291, acl: 19, ieee: 188, acm: 33, tri: 4, exA: 24, exG: 7, dev: [160, 15], hn: [239, 4] },
  S8: { name: 'Descarte', q: 'Como a equipe remove ou restringe dados e seus derivados?', sig: 'Remoção coordenada de documentos, chunks, vetores, índices e caches.', terms: '"data deletion" OR "document deletion" OR deindex* OR erasure OR retention OR purge OR expiration', sc: 99, acl: 10, ieee: 75, acm: 128, tri: 3, exA: 9, exG: 3, dev: [10, 10], hn: [160, 1] },
};
const DIMS = [['Qualidade', 'qualidade', 24, 49, 31], ['Segurança', 'segurança', 16, 18, 8], ['Governança', 'governança', 11, 23, 7], ['Rastreabilidade', 'rastreabilidade', 11, 31, 10]];
const RAG_BLOCK = '("retrieval augmented generation" OR "retrieval-augmented generation")';

function stageSection(id) {
  const s = STAGES[id];
  const inc = TRI.filter((r) => r.decision === 'include' && r.stages.includes(id));
  return `<h3>${id} · ${s.name}</h3>
    <p><b>Pergunta de engenharia.</b> ${s.q}</p>
    <p><b>Sinal relevante em RAG.</b> ${s.sig}</p>
    ${kv([
      ['Scopus: ocorrências da família', s.sc], ['ACL Anthology: ocorrências', s.acl],
      ['IEEE Xplore (exploratória)', s.ieee], ['ACM DL, só Abstract (exploratória)', s.acm],
      ['DEV Community: aderentes / candidatos', `${s.dev[0]} / ${s.dev[1]}`], ['Hacker News: ocorrências / candidatos', `${s.hn[0]} / ${s.hn[1]}`],
      ['Inclusões preliminares na triagem', s.tri], ['Fontes acadêmicas com evidência', s.exA], ['Fontes cinzentas com evidência', s.exG],
    ])}
    <h3>String ${id} (e G${id.slice(1)} com o bloco de tipologia)</h3>
    ${cmd(`${RAG_BLOCK}\nAND (${s.terms})`)}
    <h3>Fontes incluídas na triagem com ${id} (${inc.length})</h3>
    <p class="small muted">Associação feita na pré-triagem, por título e resumo; é conferida na leitura integral.</p>
    ${paperList(inc)}`;
}
const stageDrawer = (step, artifact, ids, extra = '') => ({
  kind: ids.join(' · '), title: step,
  html: `<p>Produz: <b>${artifact}</b>.</p>${extra}${ids.map(stageSection).join('')}`,
});

/* ---------- vistas ---------- */
const VIEWS = {};

VIEWS.geral = {
  tab: 'Visão geral', title: 'Desenho do estudo',
  sub: 'Revisão multivocal em cinco fases. As literaturas acadêmica e cinzenta seguem caminhos próprios de busca e seleção e se encontram na ficha de extração. Clique nos blocos com ↘ para abrir cada caminho.',
  cols: 'repeat(5,minmax(0,1fr))', minw: 1080, rg: 72,
  phases: [['1', 'Planejamento'], ['2', 'Busca'], ['3', 'Seleção'], ['4', 'Extração'], ['5', 'Síntese']],
  zones: [{ c: '2/4', r: '1', l: 'Literatura acadêmica' }, { c: '2/4', r: '2', l: 'Literatura cinzenta' }],
  nodes: [
    { id: 'plan', k: 'obj', c: '1', r: '1/3', tall: true, t: 'Questões de pesquisa e PICOC', s: 'QP1–QP3 · critérios de elegibilidade I1–I3 e E1–E5 · recorte a partir de 2024',
      d: { kind: 'Planejamento', title: 'Questões de pesquisa e PICOC', html: `
        <p>A unidade de análise é uma prática ou um desafio de engenharia de dados associado ao ciclo de vida de sistemas RAG.</p>
        <h3>Questões de pesquisa</h3>
        <ul><li><b>QP1.</b> Quais práticas de engenharia de dados são relatadas em sistemas RAG e como se distribuem ao longo do ciclo de vida dos dados?</li>
        <li><b>QP2.</b> Quais adaptações e desafios são relatados na aplicação dessas práticas em sistemas RAG?</li>
        <li><b>QP3.</b> Quais práticas, adaptações e desafios de engenharia de dados em sistemas RAG são relatados na literatura acadêmica, na literatura cinzenta ou em ambas?</li></ul>
        <h3>PICOC</h3>
        <ul><li><b>População:</b> sistemas RAG.</li>
        <li><b>Interesse:</b> práticas de engenharia de dados aplicadas à construção, operação, manutenção e governança de sistemas RAG.</li>
        <li><b>Comparação:</b> distribuição dos achados entre literatura acadêmica e cinzenta; quando documentado, contraste com outros contextos de engenharia de dados.</li>
        <li><b>Resultados:</b> práticas e sua distribuição no ciclo de vida, variações, adaptações documentadas e desafios associados.</li>
        <li><b>Contexto:</b> desenvolvimento e operação de sistemas RAG em contextos acadêmicos e industriais.</li></ul>
        ${files([['config/review_protocol.yaml', 'Protocolo operacional (QPs, PICOC, critérios, parâmetros das rodadas)'], ['data/review/protocols/', 'Versões registradas do protocolo']])}` } },
    { id: 'abusca', k: 'det', c: '2', r: '1', t: 'Duas bases', s: 'Scopus e ACL Anthology · strings S1–S8 · sem filtro temporal', n: '3.250<small>publicações únicas</small>', go: 'academica' },
    { id: 'asel', k: 'hum', c: '3', r: '1', t: 'Triagem e qualidade', s: 'pré-triagem por IA, rodadas de dez com decisão humana, QA1–QA6', n: '52<small>fontes adequadas</small>', go: 'academica' },
    { id: 'gbusca', k: 'det', c: '2', r: '2', t: 'Três frentes', s: 'DEV Community, Hacker News e portais institucionais · strings G1–G8', n: '210<small>candidatos únicos</small>', go: 'cinzenta' },
    { id: 'gsel', k: 'hum', c: '3', r: '2', t: 'Triagem e qualidade', s: 'decisão humana (I1–I3, E1–E5) e avaliação QG1–QG6', n: '37<small>fontes incluídas</small>', go: 'cinzenta' },
    { id: 'extr', k: 'obj', c: '4', r: '1/3', tall: true, t: 'Ficha por fonte', s: 'práticas e etapas · adaptações · desafios · excertos de apoio', n: '246<small>evidências</small>', go: 'extracao' },
    { id: 'sint', k: 'obj', c: '5', r: '1/3', tall: true, t: 'Respostas', s: 'QP1: práticas no ciclo de vida · QP2: adaptações e desafios · QP3: acadêmica e cinzenta',
      d: { kind: 'Síntese', title: 'Síntese e organização dos resultados', html: `
        <p>As informações extraídas são organizadas por etapa do ciclo de vida e articuladas às três questões.</p>
        <ul><li><b>QP1:</b> síntese das práticas mapeadas, de suas finalidades, contextos e distribuição ao longo do ciclo de vida.</li>
        <li><b>QP2:</b> adaptações documentadas, requisitos que as motivaram e desafios técnicos e operacionais associados.</li>
        <li><b>QP3:</b> comparação descritiva da distribuição entre literatura acadêmica e cinzenta: cada achado é situado como acadêmico, cinzento ou de ambas.</li></ul>
        <p>A ausência de menção em um grupo não é interpretada como inexistência do achado fora do corpus. A síntese distingue a frequência de menção da força, do tipo e do contexto das evidências.</p>` } },
    { id: 'ciclo', k: 'obj', c: '1/6', r: '3', strip: true, go: 'rag',
      html: `<span class="t">Lente de análise: ciclo de vida dos dados em RAG</span>${Object.entries(STAGES).map(([k, v]) => `<span class="chip">${k} ${v.name}</span>`).join('')}${DIMS.map((d) => `<span class="chip dim">${d[0]}</span>`).join('')}` },
  ],
  edges: [
    { a: 'plan', b: 'abusca', s: 'r', t: 'l' }, { a: 'plan', b: 'gbusca', s: 'r', t: 'l' },
    { a: 'abusca', b: 'asel', s: 'r', t: 'l' }, { a: 'gbusca', b: 'gsel', s: 'r', t: 'l' },
    { a: 'asel', b: 'abusca', s: 'b', t: 'b', ty: 'fb', off: 24, l: 'snowballing', lo: [0, 12] },
    { a: 'asel', b: 'extr', s: 'r', t: 'l', fb: .35 }, { a: 'gsel', b: 'extr', s: 'r', t: 'l', fb: .65 },
    { a: 'extr', b: 'sint', s: 'r', t: 'l' },
  ],
};

VIEWS.rag = {
  tab: 'Pipeline RAG', title: 'O objeto: a cadeia de dados de um sistema RAG',
  sub: 'Fluxo offline de construção da base recuperável e fluxo online de consulta (Figura 1 do artigo), com cada passo associado às etapas S1–S8 que organizam as famílias de busca. Clique em um passo para ver a pergunta de engenharia, as contagens da busca e as fontes incluídas naquela etapa.',
  cols: 'repeat(6,minmax(0,1fr))', minw: 1180, padr: 140, rg: 74,
  zones: [{ c: '1/7', r: '1', l: 'Fluxo offline: construção da base recuperável' }, { c: '1/7', r: '2', l: 'Fluxo online: uso em tempo de consulta' }, { c: '1/7', r: '3', l: 'Operação ao longo do tempo' }],
  nodes: [
    { id: 'fontes', k: 'obj', c: '1', r: '1', t: 'Fontes', s: 'documentos', chips: ['S1'], d: stageDrawer('Fontes', 'documentos', ['S1']) },
    { id: 'ingest', k: 'obj', c: '2', r: '1', t: 'Ingestão', s: 'arquivos registrados', chips: ['S2'], d: stageDrawer('Ingestão', 'arquivos registrados', ['S2']) },
    { id: 'parse', k: 'obj', c: '3', r: '1', t: 'Parsing e limpeza', s: 'texto e estrutura', chips: ['S2', 'S4'], d: stageDrawer('Parsing e limpeza', 'texto e estrutura', ['S2', 'S4'], '<p>O <i>parsing</i> aparece no sinal da ingestão (extração, OCR) e a preservação de estrutura, no da preparação.</p>') },
    { id: 'chunk', k: 'obj', c: '4', r: '1', t: 'Chunking e metadados', s: 'chunks e metadados', chips: ['S4'], d: stageDrawer('Chunking e metadados', 'chunks e metadados', ['S4']) },
    { id: 'emb', k: 'obj', c: '5', r: '1', t: 'Embeddings', s: 'vetores', chips: ['S4'], d: stageDrawer('Embeddings', 'vetores', ['S4']) },
    { id: 'index', k: 'obj', c: '6', r: '1', t: 'Índice', s: 'índice consultável', chips: ['S3'], d: stageDrawer('Índice', 'índice consultável', ['S3']) },
    { id: 'perg', k: 'obj', c: '1', r: '2', t: 'Pergunta', s: 'consulta', d: { kind: 'Fluxo online', title: 'Pergunta', html: '<p>Entrada do fluxo online. A pergunta do usuário é o ponto de partida da recuperação; daí em diante, as etapas de disponibilização (S5) decidem quais evidências chegam ao modelo.</p>' } },
    { id: 'auth', k: 'obj', c: '2', r: '2', t: 'Autorização e filtros', s: 'escopo permitido', chips: ['S5'], d: stageDrawer('Autorização e filtros', 'escopo permitido', ['S5']) },
    { id: 'retr', k: 'obj', c: '3', r: '2', t: 'Recuperação', s: 'candidatos', chips: ['S5'], d: stageDrawer('Recuperação', 'candidatos', ['S5']) },
    { id: 'rerank', k: 'obj', c: '4', r: '2', t: 'Reranking', s: 'evidências ordenadas', chips: ['S5'], d: stageDrawer('Reranking', 'evidências ordenadas', ['S5']) },
    { id: 'ctx', k: 'obj', c: '5', r: '2', t: 'Montagem do contexto', s: 'contexto', chips: ['S5'], d: stageDrawer('Montagem do contexto', 'contexto', ['S5']) },
    { id: 'gen', k: 'obj', c: '6', r: '2', t: 'Geração da resposta', s: 'resposta', d: { kind: 'Fluxo online', title: 'Geração da resposta', html: '<p>O modelo de linguagem gera a resposta condicionada ao contexto montado. Uma resposta inadequada pode resultar de fonte incompleta, <i>parsing</i> que perdeu estrutura, <i>chunking</i> que separou contexto, metadados insuficientes, índice desatualizado ou filtro de acesso incorreto, mesmo com a chamada ao modelo correta.</p>' } },
    { id: 'descarte', k: 'obj', c: '1/3', r: '3', t: 'Descarte', s: 'remoção coordenada de documentos, chunks, vetores, índices e caches', chips: ['S8'], d: stageDrawer('Descarte', 'remoção ou restrição de dados e derivados', ['S8']) },
    { id: 'manut', k: 'obj', c: '3/5', r: '3', t: 'Manutenção', s: 'reindexação, atualização de vetores, revisão de permissões', chips: ['S7'], d: stageDrawer('Manutenção', 'base coerente ao longo do tempo', ['S7']) },
    { id: 'uso', k: 'obj', c: '5/7', r: '3', t: 'Uso e feedback', s: 'traces, avaliação, retorno de usuários', chips: ['S6'], d: stageDrawer('Uso e feedback', 'sinais de utilidade ou falha', ['S6']) },
    { id: 'dims', k: 'obj', c: '1/7', r: '4', strip: true,
      html: `<span class="t">Dimensões transversais</span>${DIMS.map((d) => `<span class="chip dim">${d[0]}</span>`).join('')}<span class="s">não são famílias de busca; são registradas na extração e associadas às etapas</span>`,
      d: { kind: 'Transversais', title: 'Dimensões transversais', html: `
        <p>Qualidade, segurança, governança e rastreabilidade podem estar ligadas a uma ou mais etapas, por isso não formam famílias de busca próprias. São identificadas nas fontes recuperadas e registradas na extração.</p>
        <table><thead><tr><th>Dimensão</th><th class="num">Triagem</th><th class="num">Acad.</th><th class="num">Cinz.</th></tr></thead>
        <tbody>${DIMS.map((d) => `<tr><td>${d[0]}</td><td class="num">${d[2]}</td><td class="num">${d[3]}</td><td class="num">${d[4]}</td></tr>`).join('')}</tbody></table>
        <p class="caption">Triagem: inclusões preliminares associadas na pré-triagem. Acad./Cinz.: fontes com evidência extraída do texto integral.</p>` } },
  ],
  edges: [
    { a: 'fontes', b: 'ingest', s: 'r', t: 'l' }, { a: 'ingest', b: 'parse', s: 'r', t: 'l' }, { a: 'parse', b: 'chunk', s: 'r', t: 'l' },
    { a: 'chunk', b: 'emb', s: 'r', t: 'l' }, { a: 'emb', b: 'index', s: 'r', t: 'l' },
    { a: 'perg', b: 'auth', s: 'r', t: 'l' }, { a: 'auth', b: 'retr', s: 'r', t: 'l' }, { a: 'retr', b: 'rerank', s: 'r', t: 'l' },
    { a: 'rerank', b: 'ctx', s: 'r', t: 'l' }, { a: 'ctx', b: 'gen', s: 'r', t: 'l' },
    { a: 'index', b: 'retr', s: 'b', t: 't', ty: 'data', l: 'consulta ao índice', mid: .5 },
    { a: 'gen', b: 'uso', s: 'b', t: 't', fb: .75, fa: .5, l: 'traces' },
    { a: 'uso', b: 'index', s: 'r', t: 'r', ty: 'fb', off: 34, l: 'revisão offline', lo: [0, 0] },
    { a: 'uso', b: 'manut', s: 'l', t: 'r', ty: 'fb', l: 'falhas' },
  ],
};

VIEWS.academica = {
  tab: 'Seleção acadêmica', title: 'Ciclo de busca e seleção das fontes acadêmicas',
  sub: 'Scripts fazem o que é determinístico, o modelo de linguagem só sugere e prioriza, e os pesquisadores tomam todas as decisões. Lista curta, ranqueamento e decisão se repetem a cada rodada de dez candidatos (Figura 3 do artigo).',
  cols: 'repeat(6,minmax(0,1fr))', minw: 1180, rg: 64,
  zones: [{ c: '4/7', r: '1', l: 'Repetido a cada rodada' }],
  nodes: [
    { id: 'buscas', k: 'det', c: '1', r: '1', t: 'Buscas S1–S8', s: 'Scopus (TITLE-ABS-KEY) e ACL Anthology', n: '3.142 + 299<small>únicos</small>',
      d: { kind: 'Script', title: 'Buscas S1–S8', html: `
        <p>Cada família combina o bloco RAG com um bloco de termos da etapa: <code>BLOCO-RAG AND BLOCO-ETAPA</code>. Na Scopus, as famílias foram consultadas em <code>TITLE-ABS-KEY</code> e os registros enriquecidos pela <i>Abstract Retrieval API</i>. Na ACL Anthology, a busca usou o snapshot do commit <code>e4d087a11bc0</code>, sobre título e resumo normalizados. Coletas em 23/09/2026, sem filtro temporal.</p>
        <table><thead><tr><th>Família</th><th class="num">Scopus</th><th class="num">ACL</th></tr></thead><tbody>
        ${Object.entries(STAGES).map(([k, v]) => `<tr><td>${k} · ${v.name}</td><td class="num">${v.sc}</td><td class="num">${v.acl}</td></tr>`).join('')}
        </tbody><tfoot><tr><td>Ocorrências</td><td class="num">3.766</td><td class="num">332</td></tr><tr><td>Registros únicos</td><td class="num">3.142</td><td class="num">299</td></tr></tfoot></table>
        <p class="caption">Um registro pode ser recuperado por mais de uma família. IEEE Xplore e ACM Digital Library tiveram só consultas exploratórias, sem coleta consolidada.</p>
        <h3>Comandos</h3>${cmd('python scripts/collect_scopus.py   # busca + enriquecimento dos resumos\npython scripts/collect_acl.py      # clona/atualiza a Anthology e busca\npython scripts/report.py           # resumo por família')}
        <h3>Arquivos</h3>${files([['config/search_queries.yaml', 'Fonte única das strings S1–S8'], ['scripts/collect_scopus.py', 'Coletor Scopus (retry, paginação, retomada, cache)'], ['scripts/collect_acl.py', 'Coletor ACL Anthology'], ['src/search/', 'Geração das queries e matcher local'], ['data/manifests/scopus/', 'Manifestos das coletas Scopus'], ['data/manifests/acl/', 'Manifesto da coleta ACL (commit do snapshot)']])}` } },
    { id: 'consol', k: 'det', c: '2', r: '1', t: 'Consolidação', s: 'deduplicação (E1) · recorte temporal só marcado', n: '4.095<small>no conjunto</small>',
      d: { kind: 'Script', title: 'Consolidação e deduplicação', html: `
        <p>Os registros das duas bases e do <i>snowballing</i> formam um único conjunto, deduplicado pelo DOI e, na ausência dele, pelo título normalizado. O identificador de cada registro (<code>P-xxxxxxxxxxxx</code>) é um hash dessa chave, então refazer as coletas reproduz os mesmos identificadores.</p>
        ${kv([['Registros únicos na Scopus', '3.142'], ['Registros únicos na ACL Anthology', '299'], ['Da Scopus já presentes na ACL (E1)', '191'], ['Publicações únicas das buscas diretas', '3.250'], ['Acrescentados pelo backward snowballing', '845'], ['Conjunto consolidado', '4.095'], ['Anteriores a 2024 (marcados, não excluídos)', '486'], ['… dos quais vindos só do snowballing', '472'], ['Sem resumo', '9']])}
        <p class="small muted" style="margin-top:10px">A única exclusão automática é a de duplicatas (E1). Registros anteriores ao recorte recebem <code>temporal_status: pre_cutoff</code>; quem decide E2 ou a exceção fundacional são os pesquisadores.</p>
        <h3>Comando</h3>${cmd('python scripts/review_loop.py sync')}
        <h3>Arquivos</h3>${files([['src/review/corpus.py', 'Consolidação do pool'], ['data/review/syncs/', 'Registro de cada sincronização']])}` } },
    { id: 'pretri', k: 'ia', c: '3', r: '1', t: 'Pré-triagem', s: 'sugestão, prioridade, etapas e excerto literal', n: '2.232<small>pré-triados</small>',
      d: { kind: 'IA · sugere', title: 'Pré-triagem por modelo de linguagem', html: `
        <p>Em lotes de 50, a partir de título, resumo e metadados. Para cada registro, o modelo registra uma sugestão (incluir, excluir ou ambíguo), uma prioridade, as etapas do ciclo de vida e as dimensões transversais e, quando apresenta evidência, um excerto literal do resumo. <b>Um lote com qualquer excerto não literal é rejeitado inteiro na importação.</b></p>
        ${kv([['Pré-triados (de 4.095)', '2.232'], ['… no recorte / anteriores a 2024', '1.954 / 278'], ['Sugestão: incluir', '827'], ['Sugestão: excluir', '781'], ['Sugestão: ambíguo', '624'], ['Não pré-triados (permanecem não revisados)', '1.863']])}
        <h3>Modelos</h3>
        <p>Mesma instrução, <code>mlr-screening-v2</code>: <code>claude-opus-5-5</code> em 1.647 registros e <code>codex-gpt-5</code> em 585.</p>
        <h3>Comandos</h3>${cmd('python scripts/review_loop.py pretriage-batches\n# skill mlr-screening escreve batch_NNNN.output.jsonl\npython scripts/review_loop.py import-pretriage')}
        <h3>Arquivos</h3>${files([['.claude/skills/mlr-screening/SKILL.md', 'Instrução da pré-triagem'], ['data/review/pretriage/pretriage.jsonl', 'Sugestões com modelo, versão do prompt e excerto citado']])}` } },
    { id: 'lista', k: 'det', c: '4', r: '1', t: 'Lista curta', s: 'trinta não revisados mais próximos das fontes validadas', n: '30<small>por rodada</small>',
      d: { kind: 'Script', title: 'Lista curta da rodada', html: `
        <p>Parte dos registros pré-triados e ainda não revisados, ordenados pela sugestão e pela prioridade da pré-triagem e, em seguida, pela maior similaridade lexical (TF-IDF sobre título e resumo) com as fontes já incluídas. Os 30 primeiros formam a lista curta.</p>
        <p><b>Registros não apresentados não são excluídos.</b> Quem não entra entre os dez de uma rodada continua não revisado e pode aparecer depois.</p>
        <h3>Comando</h3>${cmd('python scripts/review_loop.py round-new')}
        <h3>Arquivos</h3>${files([['src/review/ranking.py', 'Ordenação e similaridade TF-IDF'], ['src/review/workspace.py', 'Estado das rodadas']])}` } },
    { id: 'rank', k: 'ia', c: '5', r: '1', t: 'Ranqueamento', s: 'dez candidatos justificados', n: '10<small>de 30</small>',
      d: { kind: 'IA · sugere', title: 'Ranqueamento dos dez candidatos', html: `
        <p>O modelo reordena a lista curta e indica exatamente dez candidatos de maior aderência, cada um com justificativa e com as fontes validadas relacionadas. A importação recusa qualquer ranqueamento que não tenha exatamente 10 candidatos da lista curta.</p>
        <p>Modelo: <code>codex-gpt-5</code>, instrução <code>mlr-ranking-v1</code>, nas oito rodadas.</p>
        <h3>Comando</h3>${cmd('# skill mlr-ranking escreve rounds/rNNN/ranking.input.json\npython scripts/review_loop.py round-rank rNNN data/review/rounds/rNNN/ranking.input.json')}
        <h3>Arquivos</h3>${files([['.claude/skills/mlr-ranking/SKILL.md', 'Instrução do ranqueamento'], ['data/review/rounds/', 'Os dez escolhidos em cada rodada (ranking.json)']])}` } },
    { id: 'decisao', k: 'hum', c: '6', r: '1', t: 'Decisão', s: 'incluir ou excluir, com critério e justificativa', n: '80<small>decisões</small>', d: null },
    { id: 'valid', k: 'obj', c: '6', r: '2', t: 'Fontes validadas', s: 'inclusões preliminares', n: '60', d: null },
    { id: 'snow', k: 'det', c: '3/5', r: '3', t: 'Snowballing backward e forward', s: 'referências (Scopus) e citações (OpenAlex) das validadas', n: '845<small>novos pelo backward</small>',
      d: { kind: 'Script', title: 'Snowballing', html: `
        <h3>Backward, na Scopus</h3>
        <p>Executado entre as rodadas pela visão <code>REF</code> da <i>Abstract Retrieval API</i>, sem reaplicar as strings S1–S8 e sem filtro temporal. Os candidatos voltam ao mesmo fluxo de pré-triagem e seleção, sem inclusão automática.</p>
        ${kv([['Execuções efetivas', '8'], ['Referências candidatas recuperadas', '905'], ['Registros novos após consolidação', '845'], ['Coincidentes com as buscas diretas', '58'], ['Inéditos nas duas últimas execuções', '32'], ['… todos com sugestão de exclusão (29 anteriores a 2024)', '32']])}
        <h3>Forward, no OpenAlex</h3>
        <p>Executado em 14/11/2026, após o encerramento da descoberta geral, a partir das 52 fontes acadêmicas adequadas na avaliação de qualidade (duas não estavam indexadas).</p>
        ${kv([['Trabalhos ≥ 2024 que citam alguma semente', '426'], ['Já no corpus', '26'], ['Candidatos novos', '400'], ['Sem RAG no título nem no resumo (sugestão I2)', '158'], ['Pré-triagem por título: incluir / ambíguo / excluir (E3)', '71 / 24 / 147']])}
        <p class="small muted" style="margin-top:10px">Os candidatos do forward seguem o mesmo fluxo de decisão humana e avaliação de qualidade; a incorporação depende dessa decisão.</p>
        <h3>Comando (backward)</h3>${cmd('python scripts/review_loop.py snowball --direction backward \\\n    --seed-source validated   # padrão: só fontes incluídas por humanos')}
        <h3>Arquivos</h3>${files([['src/review/snowball.py', 'Snowballing via Scopus'], ['data/manifests/snowball/', 'Sementes e resultados de cada execução']])}` } },
    { id: 'refine', k: 'ia', c: '3/5', r: '4', t: 'Análise e refinamento das strings', s: 'propõe incluir, remover ou trocar termos', n: 'v1<small>usada nas 8 rodadas</small>',
      d: { kind: 'IA · sugere', title: 'Análise e refinamento das strings', html: `
        <p>O modelo analisa padrões, lacunas e o desempenho dos termos entre os registros revisados e pode propor uma nova versão das strings. A proposta só passa a valer depois que os pesquisadores a aprovam e registram, com revisor e justificativa.</p>
        <p>Após a rodada r003, a proposta <b>q2</b> incluía <code>"hybrid retrieval"</code> na família S5. <b>Não foi aprovada</b>, e as oito rodadas usaram a versão 1, cuja impressão digital SHA-256 começa por <code>4fa085f6c7d5</code>.</p>
        <h3>Comandos</h3>${cmd('python scripts/review_loop.py analyze     # + skill mlr-analysis\npython scripts/review_loop.py refine      # + skill mlr-refinement\n# só com aprovação:\npython scripts/review_loop.py register-queries --reviewer NOME --justification "..."')}
        <h3>Arquivos</h3>${files([['data/review/refinement/proposal_q2.md', 'Proposta q2 (não aprovada)'], ['data/review/analysis/', 'Notas de análise e cobertura por rodada'], ['data/review/queries/q1.yaml', 'Snapshot da versão 1 das strings'], ['.claude/skills/mlr-refinement/SKILL.md', 'Instrução do refinamento']])}` } },
    { id: 'parada', k: 'hum', c: '6', r: '3/5', t: 'Critérios de parada', s: 'estabilidade das strings · entrada de novos estudos · saturação temática · cobertura S1–S8', n: '3 de 4<small>após r008</small>', d: null },
  ],
  edges: [
    { a: 'buscas', b: 'consol', s: 'r', t: 'l' }, { a: 'consol', b: 'pretri', s: 'r', t: 'l' }, { a: 'pretri', b: 'lista', s: 'r', t: 'l' },
    { a: 'lista', b: 'rank', s: 'r', t: 'l' }, { a: 'rank', b: 'decisao', s: 'r', t: 'l' },
    { a: 'decisao', b: 'valid', s: 'b', t: 't', l: 'incluídas', lside: 'l' },
    { a: 'valid', b: 'rank', s: 'l', t: 'b', fa: .3, ty: 'fb' },
    { a: 'valid', b: 'lista', s: 'l', t: 'b', fa: .3, ty: 'fb', l: 'orientam lista curta e ranqueamento', lp: .62 },
    { a: 'valid', b: 'snow', s: 'l', t: 'r', fa: .62, ty: 'fb', mid: .55, l: 'sementes' },
    { a: 'snow', b: 'consol', s: 'l', t: 'b', ty: 'fb', l: 'novos candidatos' },
    { a: 'valid', b: 'refine', s: 'l', t: 'r', fa: .88, ty: 'fb', mid: .3, l: 'padrões e lacunas' },
    { a: 'refine', b: 'buscas', s: 'l', t: 'b', ty: 'appr', l: 'nova versão, só com aprovação' },
    { a: 'valid', b: 'parada', s: 'b', t: 't', l: 'após cada rodada', lside: 'l' },
  ],
};

/* Painéis que dependem dos dados da triagem */
(() => {
  const rounds = {};
  TRI.forEach((r) => { (rounds[r.round] ||= { i: 0, e: 0 })[r.decision === 'include' ? 'i' : 'e']++; });
  const rows = Object.entries(rounds).sort().map(([k, v]) => `<tr><td>${k}</td><td class="num">${v.i}</td><td class="num">${v.e}</td></tr>`).join('');
  const N = (id) => VIEWS.academica.nodes.find((n) => n.id === id);
  N('decisao').d = { kind: 'Humano · decide', title: 'Decisão humana', html: `
    <p>Os pesquisadores decidem os dez candidatos: <code>include</code>, <code>exclude</code> ou <code>full_text</code>, com critério E1–E5 quando houver exclusão e justificativa sempre. <b>Uma rodada só fecha com 10 decisões humanas.</b></p>
    <p>Oito rodadas entre 25 e 27/09/2026. Todos os 80 candidatos tinham sugestão de inclusão com prioridade alta na pré-triagem; os pesquisadores divergiram em 20 casos (25%), que resultaram em exclusão.</p>
    <table><thead><tr><th>Rodada</th><th class="num">Incluídas</th><th class="num">Excluídas</th></tr></thead><tbody>${rows}</tbody>
    <tfoot><tr><td>Total</td><td class="num">60</td><td class="num">20 (19 E3, 1 E4)</td></tr></tfoot></table>
    <p style="margin-top:12px"><a href="./#triagem">Ver as 80 decisões, com título e justificativas →</a></p>
    <h3>Comandos</h3>${cmd('# preencher rounds/rNNN/review.csv: decision, criterion, justification, reviewer\npython scripts/review_loop.py round-review rNNN data/review/rounds/rNNN/review.csv\npython scripts/review_loop.py round-close rNNN')}
    <h3>Arquivos</h3>${files([['data/review/decisions.jsonl', 'As 80 decisões, com critério e justificativa'], ['data/review/workspace.json', 'Rodadas, versões das strings e mudanças de protocolo']])}` };
  const inc = TRI.filter((r) => r.decision === 'include');
  const by = (f) => inc.filter(f).length;
  N('valid').d = { kind: 'Conjunto', title: 'Fontes validadas', html: `
    <p>As inclusões preliminares formam o conjunto de referências validadas, que orienta a lista curta e o ranqueamento das rodadas seguintes, serve de semente ao <i>snowballing</i> e alimenta a análise e o refinamento das strings.</p>
    ${kv([['Inclusões preliminares', inc.length], ['Com proveniência Scopus', by((r) => r.sources.includes('scopus'))], ['Com proveniência ACL Anthology', by((r) => r.sources.includes('acl'))], ['Recuperadas pelas buscas diretas', by((r) => r.origins.includes('search'))], ['Também pelo snowballing', by((r) => r.origins.includes('snowball'))], ['Anteriores a 2024 incluídas', 0]])}
    <p class="caption">As contagens de proveniência não são mutuamente exclusivas.</p>
    <h3>Por etapa (associação da pré-triagem)</h3>
    <table><thead><tr><th>Etapa</th><th class="num">Fontes</th></tr></thead><tbody>${Object.entries(STAGES).map(([k, v]) => `<tr><td>${k} · ${v.name}</td><td class="num">${v.tri}</td></tr>`).join('')}</tbody></table>
    <h3>Depois da triagem</h3>
    <p>O texto integral foi obtido para 55 das 60 (cinco excluídas por E5), e 52 foram consideradas adequadas em QA1–QA6.</p>
    ${goBtn('extracao', 'Ver texto integral, qualidade e extração')}` };
  N('parada').d = { kind: 'Humano · decide', title: 'Critérios de parada', html: `
    <p>Quatro indicadores do protocolo são calculados após cada rodada. Eles apoiam a decisão, mas não encerram o loop sozinhos.</p>
    <div class="ind">
      <div><span class="ok">✓</span><span><b>Estabilidade das consultas</b>: pelo menos três rodadas sem nova versão das strings. As oito usaram a versão 1.</span></div>
      <div><span class="no">✗</span><span><b>Baixa entrada de estudos</b>: no máximo uma inclusão nas três últimas rodadas. As três últimas somaram 18.</span></div>
      <div><span class="ok">✓</span><span><b>Saturação temática</b>: nenhuma etapa ou dimensão nova entre as inclusões das três últimas rodadas.</span></div>
      <div><span class="ok">✓</span><span><b>Cobertura</b>: ao menos três fontes incluídas em cada etapa S1–S8 (a menor, S8, tem 3).</span></div>
    </div>
    <p style="margin-top:12px">A descoberta acadêmica geral foi encerrada por decisão humana em <b>27/09/2026</b>, com base em estabilidade, saturação temática e cobertura. O registro não demonstra saturação bibliográfica estrita.</p>
    <h3>Comando</h3>${cmd('python scripts/review_loop.py status')}` };
})();

VIEWS.cinzenta = {
  tab: 'Literatura cinzenta', title: 'Recuperação e seleção da literatura cinzenta', rg: 28,
  sub: 'Três frentes de descoberta com consultas derivadas de G1–G8, consolidação pela URL, pré-triagem por título e descrição, leitura integral e avaliação QG1–QG6. Executada em 13/11/2026; a natureza editorial de cada publicação é verificada na seleção, não pelo mecanismo que a encontrou.',
  cols: 'repeat(6,minmax(0,1fr))', minw: 1180,
  nodes: [
    { id: 'dev', k: 'det', c: '1', r: '1', t: 'DEV Community', s: 'API pública · etiqueta rag · G1–G8 aplicadas localmente', n: '104<small>candidatos</small>',
      d: { kind: 'Frente 1', title: 'DEV Community', html: `
        <p>A API pública não oferece busca textual. A recuperação usou a listagem das publicações com a etiqueta <code>rag</code>, em ordem cronológica e pelo filtro de mais populares dos últimos 1.100 dias: <b>6.059 publicações</b>. As expressões G1–G8 foram aplicadas localmente a título, descrição e etiquetas das publicações a partir de 2024.</p>
        <p>Encerramento por esforço delimitado: os 15 primeiros registros de cada família, ordenados por reações. A popularidade só ordenou a leitura; não entrou na avaliação de qualidade.</p>
        <table><thead><tr><th>Família</th><th class="num">Aderentes</th><th class="num">Candidatos</th></tr></thead><tbody>
        ${Object.entries(STAGES).map(([k, v]) => `<tr><td>G${k.slice(1)} · ${v.name}</td><td class="num">${v.dev[0]}</td><td class="num">${v.dev[1]}</td></tr>`).join('')}</tbody>
        <tfoot><tr><td>Candidatos únicos</td><td></td><td class="num">104</td></tr></tfoot></table>` } },
    { id: 'hn', k: 'det', c: '1', r: '2', t: 'Hacker News (Algolia)', s: '92 consultas termo a termo · stories desde 01/01/2024', n: '94<small>candidatos</small>',
      d: { kind: 'Frente 2', title: 'Hacker News, via Algolia', html: `
        <p>O Hacker News é o mecanismo de descoberta; o documento original no domínio externo é a fonte candidata. A API não interpreta <code>OR</code> nem curingas, então cada termo do bloco de etapa foi combinado ao bloco de domínio (<code>retrieval augmented generation</code> ou <code>RAG</code>) em <b>92 consultas</b> restritas a <i>stories</i> a partir de 01/01/2024. Mantiveram-se as publicações com endereço externo cujo título ou URL tivesse um termo do domínio e um da família.</p>
        <p>Encerramento: os 50 primeiros resultados de cada consulta, na ordem de relevância do mecanismo (1.897 resultados lidos).</p>
        <table><thead><tr><th>Família</th><th class="num">Ocorrências</th><th class="num">Candidatos</th></tr></thead><tbody>
        ${Object.entries(STAGES).map(([k, v]) => `<tr><td>G${k.slice(1)} · ${v.name}</td><td class="num">${v.hn[0]}</td><td class="num">${v.hn[1]}</td></tr>`).join('')}</tbody>
        <tfoot><tr><td>Candidatos únicos</td><td></td><td class="num">94</td></tr></tfoot></table>` } },
    { id: 'portais', k: 'hum', c: '1', r: '3', t: 'Portais institucionais', s: 'busca manual sistemática nos domínios de produtores', n: '12<small>candidatos</small>',
      d: { kind: 'Frente 3', title: 'Portais institucionais', html: `
        <p>Consultas direcionadas aos domínios dos produtores definidos no protocolo, com termos das famílias G1–G8. Os portais foram escolhidos por pertinência temática, disponibilidade pública, responsabilidade editorial identificável, especificidade técnica e possibilidade de recuperação sistemática.</p>
        <ul><li>Microsoft (Azure Architecture Center)</li><li>AWS (Prescriptive Guidance, Security Blog, documentação do Amazon Bedrock)</li><li>Google Cloud Architecture Center</li><li>Databricks, NVIDIA, IBM, Uber, Elastic e Pinecone</li></ul>
        <p>No LinkedIn, a busca encontrou apenas um artigo científico, que não foi considerado literatura cinzenta.</p>` } },
    { id: 'gconsol', k: 'det', c: '2', r: '1/4', tall: true, t: 'Consolidação pela URL', s: 'proveniência preservada quando a mesma publicação vem de mais de um mecanismo', n: '210<small>candidatos únicos</small>',
      d: { kind: 'Script', title: 'Consolidação', html: `<p>Os registros das três frentes são consolidados e deduplicados pela URL. A proveniência registra o mecanismo, a família, a consulta, os parâmetros, a data, o título, a URL, a autoria e, quando aplicável, a posição do resultado.</p>${kv([['Candidatos únicos das APIs', '198'], ['Candidatos dos portais', '12'], ['Total', '210']])}` } },
    { id: 'gpre', k: 'ia', c: '3', r: '1/4', tall: true, t: 'Pré-triagem', s: 'por título e descrição, com sugestões do modelo', n: '149<small>excluídos (E3 ou E4)</small>',
      d: { kind: 'IA · sugere', title: 'Pré-triagem da literatura cinzenta', html: `<p>Sem rodadas de dez: os 210 candidatos passaram por pré-triagem por título e descrição, com sugestões de <code>claude-opus-5-5</code>. Foram excluídos 149, em sua maioria anúncios de ferramentas, tutoriais introdutórios e listas promocionais; 61 seguiram para a leitura integral.</p>` } },
    { id: 'gler', k: 'hum', c: '4', r: '1/4', tall: true, t: 'Leitura integral', s: 'texto arquivado com a data de acesso · elegibilidade I1–I3, E1–E5', n: '61<small>lidas</small>',
      d: { kind: 'Humano · decide', title: 'Leitura integral e elegibilidade', html: `<p>O texto de cada fonte lida foi arquivado com a data de acesso. Duas páginas inacessíveis no endereço original foram lidas a partir de cópias do Internet Archive.</p>
        <p>Para I1, vale a data de publicação ou, em documentação continuamente atualizada, a data explícita da última atualização. Sem data confirmável, a elegibilidade temporal fica indeterminada e a fonte não entra.</p>` } },
    { id: 'gqg', k: 'ia', c: '5', r: '1/4', tall: true, t: 'Qualidade QG1–QG6', s: 'mínimo 4,0 e QG6 > 0 · notas com apoio do modelo, conferidas pelos pesquisadores', n: '24<small>excluídas após a leitura</small>',
      d: { kind: 'Qualidade', title: 'Avaliação QG1–QG6', html: `
        <p>Escala 0 / 0,5 / 1 por critério, máximo 6,0. A fonte precisa de pelo menos 4,0 e nota acima de zero em QG6. Quando a fonte promove um produto da própria organização ou do autor, isso é registrado como possível viés comercial.</p>
        <ul><li><b>QG1 Autoridade</b>: autoria ou responsável identificável</li><li><b>QG2 Especificidade técnica</b></li><li><b>QG3 Evidência de uso</b>: implementação, caso industrial, dados operacionais</li><li><b>QG4 Atualidade</b></li><li><b>QG5 Transparência</b>: contexto, restrições, configurações</li><li><b>QG6 Verificabilidade</b></li></ul>
        <h3>Exclusões após a leitura</h3>
        ${kv([['Pontuação inferior a 4,0', '9'], ['E4 após a leitura', '6'], ['E5', '3'], ['Elegibilidade temporal indeterminada (I1)', '3'], ['Autoria não identificável (QG1 = 0)', '2'], ['QG6 = 0', '1'], ['Total', '24']])}` } },
    { id: 'gincl', k: 'obj', c: '6', r: '1/4', tall: true, t: 'Fontes cinzentas incluídas', s: 'blogs técnicos, relatos industriais, documentação e arquiteturas de referência, relatórios técnicos', n: '37',
      d: { kind: 'Conjunto', title: 'Fontes cinzentas incluídas', html: `${kv([['Descobertas pela DEV Community', '14'], ['Descobertas pelo Hacker News', '14'], ['Dos portais institucionais', '9'], ['Com 5,0 pontos ou mais', '23'], ['Com 4,0 ou 4,5', '14']])}${goBtn('extracao', 'Ver a extração')}` } },
  ],
  edges: [
    { a: 'dev', b: 'gconsol', s: 'r', t: 'l', fb: .2 }, { a: 'hn', b: 'gconsol', s: 'r', t: 'l' }, { a: 'portais', b: 'gconsol', s: 'r', t: 'l', fb: .8 },
    { a: 'gconsol', b: 'gpre', s: 'r', t: 'l', l: '210' }, { a: 'gpre', b: 'gler', s: 'r', t: 'l', l: '61' }, { a: 'gler', b: 'gqg', s: 'r', t: 'l' }, { a: 'gqg', b: 'gincl', s: 'r', t: 'l', l: '37' },
  ],
};

VIEWS.extracao = {
  tab: 'Qualidade e extração', title: 'Do conjunto selecionado à ficha de extração',
  sub: 'Três decisões em sequência: elegibilidade, qualidade metodológica da fonte aceita e, só depois, caracterização das práticas. Notas e extração foram feitas com apoio do modelo de linguagem e passam pela conferência dos pesquisadores.',
  cols: 'repeat(5,minmax(0,1fr))', minw: 1080, rg: 74,
  zones: [{ c: '1/4', r: '1', l: 'Literatura acadêmica' }, { c: '1/4', r: '2', l: 'Literatura cinzenta' }],
  nodes: [
    { id: 'x60', k: 'hum', c: '1', r: '1', t: 'Inclusões preliminares', s: 'oito rodadas de decisão humana', n: '60', go: 'academica' },
    { id: 'xfull', k: 'det', c: '2', r: '1', t: 'Texto integral', s: 'Portal de Periódicos da CAPES (acesso UnB) e repositórios abertos', n: '55<small>obtidos · 5 por E5</small>',
      d: { kind: 'Elegibilidade', title: 'Texto integral', html: '<p>O texto integral das 60 inclusões preliminares foi buscado pelo acesso institucional da Universidade de Brasília ao Portal de Periódicos da CAPES e por repositórios de acesso aberto. Foi obtido para 55; as cinco restantes foram excluídas por E5.</p>' } },
    { id: 'xqa', k: 'ia', c: '3', r: '1', t: 'Qualidade QA1–QA6', s: 'mínimo 4,0 · zero em QA2 e QA3 ao mesmo tempo desclassifica', n: '52<small>adequadas</small>',
      d: { kind: 'Qualidade', title: 'Avaliação QA1–QA6', html: `
        <p>Escala 0 / 0,5 / 1 por critério, máximo 6,0, mínimo 4,0. QA2 e QA3 são centrais. Métricas bibliométricas não entram na qualidade metodológica.</p>
        <ul><li><b>QA1</b> Clareza do objetivo</li><li><b>QA2</b> Transparência metodológica</li><li><b>QA3</b> Fundamentação das evidências</li><li><b>QA4</b> Especificidade da contribuição</li><li><b>QA5</b> Limitações e contexto</li><li><b>QA6</b> Rastreabilidade técnica</li></ul>
        ${kv([['Avaliadas (texto integral)', '55'], ['Adequadas', '52'], ['… com 5,5 ou 6,0', '41'], ['Zero em QA2 e QA3', '1'], ['Somaram 3,0', '2']])}` } },
    { id: 'x37', k: 'hum', c: '1/4', r: '2', t: 'Fontes cinzentas incluídas', s: 'já avaliadas em QG1–QG6 na seleção', n: '37', go: 'cinzenta' },
    { id: 'xficha', k: 'ia', c: '4', r: '1/3', tall: true, t: 'Ficha de extração', s: 'prática · finalidade · contexto · etapas e dimensões · artefatos · variações · adaptações · desafios · excertos', n: '181 + 65<small>evidências</small>', d: null },
    { id: 'xsint', k: 'obj', c: '5', r: '1/3', tall: true, t: 'Síntese', s: 'QP1 práticas no ciclo de vida · QP2 adaptações e desafios · QP3 acadêmica, cinzenta ou ambas', d: null },
  ],
  edges: [
    { a: 'x60', b: 'xfull', s: 'r', t: 'l' }, { a: 'xfull', b: 'xqa', s: 'r', t: 'l' },
    { a: 'xqa', b: 'xficha', s: 'r', t: 'l', fb: .3 }, { a: 'x37', b: 'xficha', s: 'r', t: 'l', fb: .75 },
    { a: 'xficha', b: 'xsint', s: 'r', t: 'l' },
  ],
};
VIEWS.extracao.nodes.find((n) => n.id === 'xsint').d = VIEWS.geral.nodes.find((n) => n.id === 'sint').d;
VIEWS.extracao.nodes.find((n) => n.id === 'xficha').d = { kind: 'Extração', title: 'Ficha de extração', html: `
  <p>Para cada fonte, a ficha registra tipo de literatura, prática, finalidade, contexto de RAG, etapas e dimensões, artefatos envolvidos, variações de implementação, adaptações relatadas e suas bases de comparação, desafios e efeitos, e os excertos que sustentam cada achado, com página ou seção.</p>
  <p>Uma <b>adaptação</b> só é registrada quando a fonte descreve uma mudança identificável em relação a um princípio ou contexto anterior, ou oferece base para uma comparação explícita. A ausência desses elementos não é lida como ausência de adaptação.</p>
  ${kv([['Fontes acadêmicas extraídas', '52'], ['Fontes cinzentas extraídas', '37'], ['Evidências acadêmicas', '181'], ['Evidências cinzentas', '65']])}
  <h3>Fontes com evidência por etapa e dimensão</h3>
  <table><thead><tr><th>Etapa ou dimensão</th><th class="num">Acad.</th><th class="num">Cinz.</th></tr></thead><tbody>
  ${Object.entries(STAGES).map(([k, v]) => `<tr><td>${k} · ${v.name}</td><td class="num">${v.exA}</td><td class="num">${v.exG}</td></tr>`).join('')}
  ${DIMS.map((d) => `<tr><td>${d[0]}</td><td class="num">${d[3]}</td><td class="num">${d[4]}</td></tr>`).join('')}</tbody></table>
  <p class="caption">A diferença em relação à triagem vem de a extração considerar o texto integral, e não só título e resumo.</p>` };

VIEWS.repo = {
  tab: 'Implementação', title: 'Como o repositório implementa o loop',
  sub: 'Strings e protocolo versionados em config/, coletores determinísticos, um CLI para todos os passos do loop e uma trilha de auditoria em data/review/. As skills são instruções em Markdown que o agente segue em cada passo de IA.',
  cols: 'repeat(5,minmax(0,1fr))', minw: 1080,
  nodes: [
    { id: 'cfg', k: 'hum', c: '1', r: '1', t: 'config/', s: 'search_queries.yaml (S1–S8, versão N) · review_protocol.yaml',
      d: { kind: 'Configuração', title: 'config/', html: `<p>Fonte única das strings e do protocolo. Cada versão das strings tem impressão digital SHA-256; uma nova versão só vale depois de <code>register-queries</code>, com revisor e justificativa. Mudanças no protocolo passam por <code>protocol-update</code>.</p>${files([['config/search_queries.yaml', 'Strings S1–S8 (versão atual)'], ['config/review_protocol.yaml', 'QPs, PICOC, I1–I3, E1–E5, recorte temporal, parâmetros das rodadas e de parada']])}` } },
    { id: 'col', k: 'det', c: '2', r: '1', t: 'Coletores', s: 'scripts/collect_scopus.py · scripts/collect_acl.py · src/search · src/collectors',
      d: { kind: 'Script', title: 'Coletores', html: `<p>Executam S1–S8 em cada base, com retry, paginação, retomada e cache. Nenhuma coleta aplica filtro temporal. As chaves ficam só no <code>.env</code>; os manifestos registram se houve proxy, mas nunca as chaves.</p>${files([['scripts/collect_scopus.py', 'Scopus + enriquecimento de resumos'], ['scripts/collect_acl.py', 'ACL Anthology sobre snapshot local'], ['src/collectors/', 'Clientes e normalização'], ['src/search/', 'Geração das queries e matcher local (frases, curinga *)'], ['src/models/paper.py', 'PaperRecord e proveniência']])}` } },
    { id: 'raw', k: 'obj', c: '3', r: '1', t: 'data/raw/ + manifestos', s: 'registros por base e versão das strings (fora do git) · manifestos versionados',
      d: { kind: 'Dados', title: 'Dados brutos e manifestos', html: `<p>Os termos da API da Elsevier não permitem redistribuir resumos e metadados completos da Scopus, então <code>data/raw/</code> fica fora do git e é regenerado pelos coletores. Os manifestos de cada coleta ficam versionados: strings executadas e impressão digital, campos pesquisados, contagens por família, paginação, uso de API e, na ACL, o commit do snapshot.</p>${files([['data/manifests/', 'Manifestos de coletas e de snowballing']])}` } },
    { id: 'loop', k: 'det', c: '4', r: '1/3', tall: true, t: 'scripts/review_loop.py', s: 'init · sync · pretriage-batches · import-pretriage · round-new · round-rank · round-review · round-close · snowball · analyze · refine · register-queries · status',
      d: { kind: 'Script', title: 'CLI do loop de revisão', html: `<p>Todos os passos são subcomandos de <code>review_loop.py</code>. O código impõe as regras do protocolo: exatamente 10 candidatos ranqueados, rodada fechada só com 10 decisões humanas justificadas, excertos literais, nenhuma exclusão automática por data.</p>
        ${cmd('python scripts/review_loop.py status')}
        ${files([['scripts/review_loop.py', 'CLI'], ['src/review/workspace.py', 'Workspace, rodadas, versões'], ['src/review/corpus.py', 'Pool consolidado'], ['src/review/ranking.py', 'Lista curta TF-IDF'], ['src/review/snowball.py', 'Snowballing'], ['src/review/analysis.py', 'Cobertura e pacotes de análise'], ['tests/', '97 testes, nenhum acessa a rede']])}` } },
    { id: 'audit', k: 'obj', c: '5', r: '1/3', tall: true, t: 'data/review/', s: 'trilha de auditoria versionada, sem resumos',
      d: { kind: 'Trilha de auditoria', title: 'data/review/', html: files([['data/review/workspace.json', 'Rodadas, versões das strings, mudanças de protocolo, sincronizações'], ['data/review/decisions.jsonl', 'As 80 decisões humanas, com critério e justificativa'], ['data/review/pretriage/pretriage.jsonl', 'Sugestões da IA com modelo, versão do prompt e excerto citado'], ['data/review/rounds/', 'Os 10 candidatos escolhidos pela IA em cada rodada'], ['data/review/analysis/', 'Notas de análise e cobertura por rodada'], ['data/review/refinement/', 'Proposta q2 das strings'], ['data/review/protocols/', 'Versões do protocolo'], ['data/review/queries/', 'Versões das strings']]) } },
    { id: 'skills', k: 'ia', c: '2/4', r: '2', t: '.claude/skills/', s: 'mlr-screening · mlr-ranking · mlr-analysis · mlr-refinement (o .codex/skills aponta para os mesmos arquivos)',
      d: { kind: 'IA · sugere', title: 'Skills', html: `<p>Instruções em Markdown que o agente (Claude Code ou Codex) segue em cada passo de IA. O agente lê um pacote gerado pelo CLI e escreve uma saída que o CLI valida antes de importar.</p>
        <table><thead><tr><th>Skill</th><th>Entrada → saída</th></tr></thead><tbody>
        <tr><td><code>mlr-screening</code></td><td>lotes de pré-triagem → sugestão, prioridade, etapas, dimensões, excerto literal</td></tr>
        <tr><td><code>mlr-ranking</code></td><td>lista curta + validadas → exatamente 10 candidatos justificados</td></tr>
        <tr><td><code>mlr-analysis</code></td><td>pacote de análise → padrões, lacunas e cobertura QP1–QP3</td></tr>
        <tr><td><code>mlr-refinement</code></td><td>pacote de refinamento → proposta de termos, aprovada pelos pesquisadores</td></tr></tbody></table>
        ${files([['.claude/skills/', 'As quatro skills']])}` } },
    { id: 'people', k: 'hum', c: '5', r: '3', t: 'Pesquisadores', s: 'review.csv de cada rodada · aprovação de strings e protocolo · decisão de parada',
      d: { kind: 'Humano · decide', title: 'Pesquisadores', html: '<p>Preenchem <code>rounds/rNNN/review.csv</code> (decisão, critério, exceção fundacional, justificativa, revisor), aprovam novas versões das strings e do protocolo e decidem quando encerrar a descoberta. <code>audit-new</code> e <code>audit-import</code> sorteiam e importam a conferência amostral da pré-triagem.</p>' } },
  ],
  edges: [
    { a: 'cfg', b: 'col', s: 'r', t: 'l', l: 'strings' }, { a: 'col', b: 'raw', s: 'r', t: 'l' },
    { a: 'raw', b: 'loop', s: 'r', t: 'l', fb: .2 }, { a: 'loop', b: 'audit', s: 'r', t: 'l', fa: .3, fb: .3 },
    { a: 'skills', b: 'loop', s: 'r', t: 'b', ty: 'fb', fb: .3, l: 'saídas validadas' },
    { a: 'people', b: 'loop', s: 'l', t: 'b', fb: .7, l: 'decisões' },
    { a: 'cfg', b: 'skills', s: 'b', t: 'l', ty: 'fb', l: 'protocolo' },
  ],
};

const ORDER = ['geral', 'rag', 'academica', 'cinzenta', 'extracao', 'repo'];

/* ---------- glossário e regras ---------- */
const GLOSS = [
  ['RAG', 'Retrieval-Augmented Generation: sistemas que recuperam informação externa e usam o conteúdo recuperado para compor ou fundamentar a geração.'],
  ['MLR', 'Multivocal Literature Review: revisão que reúne literatura acadêmica e literatura cinzenta (Garousi et al., 2019).'],
  ['Literatura cinzenta', 'Publicações técnicas fora de veículos revisados por pares: documentação, blogs de engenharia, relatórios técnicos, arquiteturas de referência, estudos de caso.'],
  ['PICOC', 'População, Interesse, Comparação, Resultados (Outcomes) e Contexto: matriz que delimita a revisão.'],
  ['Famílias S1–S8 / G1–G8', 'Uma família de busca por etapa do ciclo de vida. S para a busca acadêmica (BLOCO-RAG AND BLOCO-ETAPA); G para a cinzenta, com o BLOCO-TIPOLOGIA acrescentado.'],
  ['BLOCO-TIPOLOGIA', '"technical guide" OR "technical documentation" OR "engineering blog" OR "white paper" OR "technical report" OR "reference architecture" OR "case study" OR "best practices". Orienta a busca; não define a natureza da fonte.'],
  ['Dimensões transversais', 'Qualidade, segurança, governança e rastreabilidade. Não são famílias de busca; são registradas na extração.'],
  ['Conjunto consolidado (pool)', 'Todos os registros das buscas e do snowballing, deduplicados pelo DOI ou pelo título normalizado.'],
  ['Pré-triagem', 'Sugestão do modelo (incluir, excluir, ambíguo) com prioridade, etapas, dimensões e excerto literal. Ordena candidatos; não decide.'],
  ['Lista curta', 'Os 30 registros não revisados mais bem posicionados por sugestão, prioridade e similaridade TF-IDF com as fontes validadas.'],
  ['Rodada', 'Dez candidatos escolhidos pelo modelo a partir da lista curta e decididos pelos pesquisadores.'],
  ['Fontes validadas', 'Inclusões preliminares feitas por humanos; orientam as rodadas seguintes e servem de sementes ao snowballing.'],
  ['Snowballing', 'Backward: seguir as referências das fontes validadas. Forward: seguir os trabalhos que as citam.'],
  ['I1–I3 / E1–E5', 'Critérios de inclusão (recorte temporal, aderência ao escopo, contribuição analisável) e de exclusão (duplicata, fora do recorte, fora do escopo, conteúdo insuficiente, texto indisponível ou fonte derivada).'],
  ['Exceção fundacional', 'Fonte anterior a 2024 incluída por contribuição direta à origem, definição ou consolidação de conceitos centrais de RAG, com justificativa. Nenhuma foi usada.'],
  ['QA1–QA6 / QG1–QG6', 'Critérios de qualidade metodológica para fontes acadêmicas e cinzentas, em escala 0 / 0,5 / 1, mínimo 4,0.'],
  ['Excerto literal', 'Trecho citado pelo modelo que precisa aparecer exatamente no resumo; um lote com excerto não literal é rejeitado inteiro.'],
  ['Impressão digital', 'Hash SHA-256 de cada versão das strings, registrado nos manifestos e no workspace.'],
  ['Manifesto', 'Registro JSON de cada coleta ou execução de snowballing: parâmetros, contagens, sementes, commit do snapshot.'],
  ['Skill', 'Instrução em Markdown que o agente de IA segue em um passo específico do loop.'],
];
const RULES = [
  ['Registros não apresentados não são excluídos.', 'Quem não entrou entre os dez de uma rodada continua não revisado e pode aparecer depois.'],
  ['O modelo não decide.', 'O ranqueamento precisa ter exatamente 10 candidatos da lista curta. Uma rodada só fecha com 10 decisões humanas, cada uma com justificativa e, quando houver exclusão, com o critério E1–E5.'],
  ['Evidência literal.', 'Na pré-triagem, todo excerto citado pelo modelo precisa aparecer literalmente no resumo. Um lote com qualquer excerto não literal é rejeitado inteiro na importação.'],
  ['Sem exclusão automática por data.', 'A única exclusão automática é a de duplicatas (E1). Registros anteriores ao recorte são só marcados; quem decide E2 ou a exceção fundacional são os pesquisadores.'],
  ['Strings versionadas.', 'Cada versão tem impressão digital SHA-256 e dados brutos próprios. Uma nova versão só vale depois de register-queries, com revisor e justificativa.'],
  ['Parada é decisão humana.', 'Os quatro indicadores (estabilidade, baixa entrada, saturação temática, cobertura) apoiam a decisão, mas não encerram o loop sozinhos.'],
];

/* ---------- renderização ---------- */
const map = $('#map'), drawer = $('#drawer'), scrim = $('#scrim');
let current = 'geral', selected = null;

function nodeHTML(n) {
  if (n.strip) return n.html + (n.go ? '<span class="go" aria-hidden="true">↘</span>' : '');
  return `${ROLE[n.k] ? `<span class="role">${ROLE[n.k]}</span>` : ''}${n.go ? '<span class="go" aria-hidden="true">↘</span>' : ''}
    <span class="t">${n.t}</span>${n.s ? `<span class="s">${n.s}</span>` : ''}${n.n ? `<span class="n">${n.n}</span>` : ''}
    ${n.chips ? `<span class="chips">${n.chips.map((c) => `<span class="chip">${c}</span>`).join('')}</span>` : ''}`;
}

function render(viewId, nodeId) {
  const v = VIEWS[viewId] || VIEWS.geral;
  current = VIEWS[viewId] ? viewId : 'geral';
  map.style.gridTemplateColumns = v.cols;
  map.style.setProperty('--minw', v.minw + 'px');
  map.style.setProperty('--rg', (v.rg || 58) + 'px');
  map.style.paddingRight = (v.padr || 18) + 'px';
  map.style.paddingTop = ((v.zones && !v.phases) ? 46 : 18) + 'px';
  let html = '';
  const off = v.phases ? 1 : 0; // a faixa de fases ocupa a linha 1
  const shift = (r) => off ? String(r).split('/').map((x) => +x + off).join('/') : r;
  if (v.phases) v.phases.forEach(([num, l], i) => { html += `<div class="phase" style="grid-column:${i + 1};grid-row:1"><b>${num}</b>${l}</div>`; });
  (v.zones || []).forEach((z) => { html += `<div class="zone" style="grid-column:${z.c};grid-row:${shift(z.r)}"><span class="zl">${z.l}</span></div>`; });
  v.nodes.forEach((n) => {
    const cls = ['node', n.k, n.tall ? 'tall' : '', n.strip ? 'strip' : ''].join(' ');
    html += `<button type="button" class="${cls}" data-id="${n.id}" style="grid-column:${n.c};grid-row:${shift(n.r)}" aria-pressed="false"${n.go ? ` aria-label="${(n.t || 'Ciclo de vida')}: abrir vista"` : ''}>${nodeHTML(n)}</button>`;
  });
  map.innerHTML = html + '<svg class="edges" aria-hidden="true"></svg>';
  $('#vTitle').textContent = v.title;
  $('#vSub').textContent = v.sub;
  document.title = `${v.tab} · Arquitetura da revisão`;
  renderTabs(); renderCrumbs(); renderLegend();
  requestAnimationFrame(drawEdges);
  closeDrawer(true);
  if (nodeId) { const n = v.nodes.find((x) => x.id === nodeId); if (n && n.d) openNode(n, true); }
}

function renderTabs() {
  $('#views').innerHTML = ORDER.map((id) => `<button type="button" role="tab" data-view="${id}" aria-selected="${id === current}">${VIEWS[id].tab}</button>`).join('');
}
function renderCrumbs() {
  const c = $('#crumbs');
  c.innerHTML = current === 'geral' ? '<span aria-current="page">Visão geral</span>'
    : `<button type="button" data-view="geral">Visão geral</button><i>›</i><span aria-current="page">${VIEWS[current].tab}</span>`;
}
function renderLegend() {
  const line = (cls, dash) => `<svg viewBox="0 0 42 10"><path d="M2 5H32" stroke="var(--${cls})" stroke-width="1.8" ${dash ? `stroke-dasharray="${dash}"` : ''}/><path d="M32 1 40 5 32 9z" fill="var(--${cls})"/></svg>`;
  $('#legend').innerHTML = `
    <span>${line('text')}fluxo</span><span>${line('muted', '6 5')}realimentação</span><span>${line('ia', '10 4 2 4')}depende de aprovação</span><span>${line('accent')}consulta a dados</span>
    <span><i class="sw" style="background:var(--det)"></i>script (determinístico)</span>
    <span><i class="sw" style="background:var(--ia)"></i>IA: sugere, não decide</span>
    <span><i class="sw" style="background:var(--hum)"></i>decisão humana</span>
    <span><i class="sw" style="background:var(--accent)"></i>artefato ou conjunto</span>`;
}

/* ---------- setas ---------- */
const sidePt = (r, side, f = .5) => side === 'r' ? { x: r.right, y: r.top + r.height * f } : side === 'l' ? { x: r.left, y: r.top + r.height * f }
  : side === 't' ? { x: r.left + r.width * f, y: r.top } : { x: r.left + r.width * f, y: r.bottom };
const horiz = (s) => s === 'l' || s === 'r';

function route(e, A, B) {
  const p1 = sidePt(A, e.s, e.fa ?? .5), p2 = sidePt(B, e.t, e.fb ?? .5);
  const pts = [p1];
  if (horiz(e.s) && horiz(e.t)) {
    if (e.s === e.t) { const x = e.s === 'r' ? Math.max(p1.x, p2.x) + (e.off || 24) : Math.min(p1.x, p2.x) - (e.off || 24); pts.push({ x, y: p1.y }, { x, y: p2.y }); }
    else if (Math.abs(p1.y - p2.y) > 1) { const x = p1.x + (p2.x - p1.x) * (e.mid ?? .5); pts.push({ x, y: p1.y }, { x, y: p2.y }); }
  } else if (!horiz(e.s) && !horiz(e.t)) {
    if (e.s === e.t) { const y = e.s === 'b' ? Math.max(p1.y, p2.y) + (e.off || 24) : Math.min(p1.y, p2.y) - (e.off || 24); pts.push({ x: p1.x, y }, { x: p2.x, y }); }
    else if (Math.abs(p1.x - p2.x) > 1) { const y = p1.y + (p2.y - p1.y) * (e.mid ?? .5); pts.push({ x: p1.x, y }, { x: p2.x, y }); }
  } else if (horiz(e.s)) pts.push({ x: p2.x, y: p1.y });
  else pts.push({ x: p1.x, y: p2.y });
  pts.push(p2);
  return pts;
}
function pathD(pts, rad = 9) {
  let d = `M${pts[0].x},${pts[0].y}`;
  for (let i = 1; i < pts.length - 1; i++) {
    const a = pts[i - 1], b = pts[i], c = pts[i + 1];
    const l1 = Math.hypot(b.x - a.x, b.y - a.y), l2 = Math.hypot(c.x - b.x, c.y - b.y);
    const r = Math.min(rad, l1 / 2, l2 / 2);
    if (!r) { d += ` L${b.x},${b.y}`; continue; }
    d += ` L${b.x - (b.x - a.x) / l1 * r},${b.y - (b.y - a.y) / l1 * r} Q${b.x},${b.y} ${b.x + (c.x - b.x) / l2 * r},${b.y + (c.y - b.y) / l2 * r}`;
  }
  const z = pts[pts.length - 1];
  return d + ` L${z.x},${z.y}`;
}

function drawEdges() {
  const v = VIEWS[current];
  const svg = map.querySelector('svg.edges');
  if (!svg) return;
  map.querySelectorAll('.elabel').forEach((x) => x.remove());
  const M = map.getBoundingClientRect();
  svg.setAttribute('width', map.scrollWidth); svg.setAttribute('height', map.scrollHeight);
  const rect = (id) => { const el = map.querySelector(`[data-id="${id}"]`); if (!el) return null; const r = el.getBoundingClientRect();
    return { left: r.left - M.left, right: r.right - M.left, top: r.top - M.top, bottom: r.bottom - M.top, width: r.width, height: r.height }; };
  const mk = (id) => `<marker id="m-${id}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z"/></marker>`;
  let out = `<defs>${['flow', 'fb', 'appr', 'data'].map(mk).join('')}</defs>`;
  (v.edges || []).forEach((e) => {
    const A = rect(e.a), B = rect(e.b);
    if (!A || !B) return;
    const pts = route(e, A, B), ty = e.ty || 'flow';
    out += `<path class="${ty}" d="${pathD(pts)}" marker-end="url(#m-${ty})"/>`;
    if (e.l) {
      const segs = pts.slice(0, -1).map((p, i) => ({ a: p, b: pts[i + 1], L: Math.hypot(pts[i + 1].x - p.x, pts[i + 1].y - p.y), h: Math.abs(pts[i + 1].y - p.y) < 1 }));
      const hs = segs.filter((g) => g.h && g.L >= 44);
      const pool = hs.length ? hs : segs;
      const seg = pool.reduce((m, g) => (g.L > m.L ? g : m), pool[0]);
      const a = seg.a, b = seg.b, f = e.lp ?? .5;
      const lab = document.createElement('span');
      lab.className = 'elabel'; lab.textContent = e.l;
      let x = a.x + (b.x - a.x) * f, y = a.y + (b.y - a.y) * f;
      if (!seg.h) lab.style.transform = e.lside === 'l' ? 'translate(calc(-100% - 8px),-50%)' : 'translate(8px,-50%)';
      else y -= 12;
      if (e.lo) { x += e.lo[0]; y += e.lo[1]; }
      lab.style.left = x + 'px'; lab.style.top = y + 'px';
      map.appendChild(lab);
    }
  });
  svg.innerHTML = out;
}

/* ---------- painel ---------- */
function openPanel(kind, title, html, cls = '') {
  $('#dKind').textContent = kind;
  $('#dKind').className = 'tag ' + cls;
  $('#dBody').innerHTML = (title ? `<h2>${title}</h2>` : '') + html;
  $('#dBody').scrollTop = 0;
  drawer.hidden = false; scrim.hidden = false;
}
function openNode(n, silent) {
  selected = n.id;
  map.querySelectorAll('.node').forEach((el) => el.setAttribute('aria-pressed', el.dataset.id === n.id));
  openPanel(n.d.kind, n.d.title, n.d.html, { ia: 'ia', hum: 'hum', det: 'det' }[n.k] || 'inc');
  if (!silent) history.replaceState(null, '', `#${current}/${n.id}`);
  $('#dClose').focus({ preventScroll: true });
}
function closeDrawer(silent) {
  drawer.hidden = true; scrim.hidden = true; selected = null;
  map.querySelectorAll('.node[aria-pressed="true"]').forEach((el) => el.setAttribute('aria-pressed', 'false'));
  if (!silent) history.replaceState(null, '', `#${current}`);
}
function go(viewId) { history.pushState(null, '', `#${viewId}`); render(viewId); window.scrollTo({ top: 0, behavior: 'smooth' }); }

/* ---------- eventos ---------- */
map.addEventListener('click', (ev) => {
  const el = ev.target.closest('.node'); if (!el) return;
  const n = VIEWS[current].nodes.find((x) => x.id === el.dataset.id);
  if (n.go && !n.d) return go(n.go);
  if (n.d) openNode(n);
});
document.addEventListener('click', (ev) => {
  const t = ev.target.closest('[data-view],[data-go]');
  if (t) { ev.preventDefault(); go(t.dataset.view || t.dataset.go); }
});
$('#dClose').addEventListener('click', () => closeDrawer());
scrim.addEventListener('click', () => closeDrawer());
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !drawer.hidden) closeDrawer(); });
$('#bGloss').addEventListener('click', () => openPanel('Glossário', 'Glossário', `<dl class="gl">${GLOSS.map(([t, d]) => `<dt>${t}</dt><dd>${esc(d)}</dd>`).join('')}</dl>`));
$('#bRules').addEventListener('click', () => openPanel('Regras', 'Regras que o código impõe', `<p>O repositório transforma o protocolo em verificações executáveis. Estas são as que mais afetam a interpretação dos resultados:</p><div class="ind">${RULES.map(([t, d]) => `<div><span class="ok">●</span><span><b>${t}</b> ${d}</span></div>`).join('')}</div>`));
$('#bTheme').addEventListener('click', () => {
  const root = document.documentElement;
  const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = dark ? 'light' : 'dark';
  try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* armazenamento indisponível */ }
});
new ResizeObserver(() => requestAnimationFrame(drawEdges)).observe(map);
if (document.fonts) document.fonts.ready.then(() => requestAnimationFrame(drawEdges));
const fromHash = () => { const [v, n] = location.hash.slice(1).split('/'); render(v || 'geral', n); };
window.addEventListener('popstate', fromHash);
fromHash();
})();
