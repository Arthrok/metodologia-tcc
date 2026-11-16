/* Página principal: tema, tabelas geradas, gráficos em HTML com tooltip e tabela da triagem. */
(() => {
'use strict';
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const TRI = window.TRIAGEM || [];
const fmt = (n) => Number(n).toLocaleString('pt-BR');

const ST = [
  ['S1', 'Fontes', '"data source*" OR "knowledge source*" OR "source selection" OR "source curation" OR "corpus curation"', 542, 46, 6, 0, 7, 3],
  ['S2', 'Ingestão', '"data ingestion" OR "document ingestion" OR "data extraction" OR "document parsing" OR OCR OR crawl*', 340, 18, 15, 13, 19, 7],
  ['S3', 'Armazenamento', '"vector database*" OR "vector store*" OR "vector index*" OR "document store*" OR "embedding store*"', 724, 13, 15, 11, 25, 4],
  ['S4', 'Preparação', 'chunk* OR "text segment*" OR "document split*" OR "text preprocessing" OR "document preprocessing" OR "text normalization" OR "embedding generation"', 712, 81, 15, 30, 36, 14],
  ['S5', 'Disponibilização', '"retrieval strateg*" OR "hybrid search" OR rerank* OR "metadata filter*" OR "context compression"', 768, 113, 15, 24, 34, 14],
  ['S6', 'Uso e feedback', '"RAG evaluation" OR "retrieval evaluation" OR observab* OR tracing OR "user feedback"', 290, 32, 15, 14, 25, 4],
  ['S7', 'Manutenção', 'freshness OR reindex* OR "document update*" OR "corpus update*" OR "incremental update*" OR version*', 291, 19, 15, 4, 24, 7],
  ['S8', 'Descarte', '"data deletion" OR "document deletion" OR deindex* OR erasure OR retention OR purge OR expiration', 99, 10, 10, 1, 9, 3],
];
const DIMS = [['Qualidade', 49, 31], ['Segurança', 18, 8], ['Governança', 23, 7], ['Rastreabilidade', 31, 10]];

/* tema */
$('#bTheme').addEventListener('click', () => {
  const root = document.documentElement;
  const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = dark ? 'light' : 'dark';
  try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* armazenamento indisponível */ }
});

/* strings e famílias */
$('#strings').innerHTML = ST.map(([id, n, t]) => `<tr><td><b>${id}</b> / G${id.slice(1)}</td><td>${n}</td><td><code class="q">(${esc(t)})</code></td></tr>`).join('');
$('#families').innerHTML = ST.map(([id, n, , sc, acl, dev, hn]) => `<tr><td>${id} · ${n}</td><td class="num">${fmt(sc)}</td><td class="num">${acl}</td><td class="num">${dev}</td><td class="num">${hn}</td></tr>`).join('');

/* funil */
const F = [['Publicações únicas das buscas diretas', 3250], ['Conjunto consolidado (com backward snowballing)', 4095], ['Pré-triados pelo modelo de linguagem', 2232], ['Avaliados por humanos', 80], ['Inclusões preliminares', 60], ['Com texto integral', 55], ['Adequadas em QA1–QA6', 52]];
$('#funnel').innerHTML = F.map(([l, n]) => `<div style="--w:${Math.max(1.5, n / 4095 * 100)}%"><span>${l}</span><b>${fmt(n)}</b></div>`).join('');

/* tooltip compartilhado */
const tip = $('#tip');
function showTip(ev, html) { tip.innerHTML = html; tip.hidden = false; moveTip(ev); }
function moveTip(ev) {
  const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
  let x = ev.clientX + pad, y = ev.clientY - h - pad;
  if (x + w > innerWidth - 8) x = ev.clientX - w - pad;
  if (y < 8) y = ev.clientY + pad;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
}
const hideTip = () => { tip.hidden = true; };
function bindTip(el, html) {
  el.addEventListener('pointerenter', (e) => showTip(e, html));
  el.addEventListener('pointermove', moveTip);
  el.addEventListener('pointerleave', hideTip);
  el.tabIndex = 0;
  el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); showTip({ clientX: r.left + r.width / 2, clientY: r.top }, html); });
  el.addEventListener('blur', hideTip);
}

/* rodadas */
const rounds = {};
TRI.forEach((r) => { (rounds[r.round] ||= { i: 0, e: 0, crit: {} }); const o = rounds[r.round]; if (r.decision === 'include') o.i++; else { o.e++; o.crit[r.criterion] = (o.crit[r.criterion] || 0) + 1; } });
const rk = Object.keys(rounds).sort();
const plot = $('#roundsPlot');
rk.forEach((k) => {
  const { i, e, crit } = rounds[k];
  const col = document.createElement('div');
  col.className = 'col';
  col.setAttribute('aria-label', `${k}: ${i} incluídas, ${e} excluídas`);
  col.innerHTML = `<div class="seg inc${e ? '' : ' top'}" style="height:${i * 10}%"></div>${e ? `<div class="seg exc top" style="height:calc(${e * 10}% - 2px)"></div>` : ''}<span class="v" style="bottom:calc(${i * 10}% - 22px)">${i}</span>`;
  plot.appendChild(col);
  const c = Object.entries(crit).map(([k2, v]) => `${v} por ${k2}`).join(', ');
  bindTip(col, `<b>${k}</b><br>${i} incluídas · ${e} excluídas${c ? ` (${c})` : ''}`);
});
$('#roundsX').innerHTML = rk.map((k) => `<span>${k}</span>`).join('');

/* etapas: barras horizontais agrupadas */
const max = Math.max(...ST.map((s) => s[7]), ...DIMS.map((d) => d[1]));
const bar = (cls, v, total, label) => `<div class="b ${cls}" style="width:calc(${v / max} * (100% - 34px))" data-tip="${label}: ${v} de ${total} fontes"><span>${v}</span></div>`;
const rowsBars = [...ST.map((s) => [`<small>${s[0]}</small>${s[1]}`, s[1], s[7], s[8]]), null, ...DIMS.map((d) => [d[0], d[0], d[1], d[2]])];
$('#stageBars').innerHTML = rowsBars.map((r) => r ? `<div class="lbl">${r[0]}</div><div class="pair">${bar('a', r[2], 52, `${r[1]} · acadêmicas`)}${bar('g', r[3], 37, `${r[1]} · cinzentas`)}</div>` : '<div class="sep"></div>').join('');
document.querySelectorAll('#stageBars .b').forEach((b) => bindTip(b, esc(b.dataset.tip)));
$('#stageTable').innerHTML = `<table><thead><tr><th>Etapa ou dimensão</th><th class="num">Acadêmicas (52)</th><th class="num">Cinzentas (37)</th></tr></thead><tbody>${ST.map((s) => `<tr><td>${s[0]} · ${s[1]}</td><td class="num">${s[7]}</td><td class="num">${s[8]}</td></tr>`).join('')}${DIMS.map((d) => `<tr><td>${d[0]}</td><td class="num">${d[1]}</td><td class="num">${d[2]}</td></tr>`).join('')}</tbody></table>`;
$('#bStageTable').addEventListener('click', (e) => {
  const t = $('#stageTable'); t.hidden = !t.hidden;
  e.currentTarget.setAttribute('aria-expanded', String(!t.hidden));
  e.currentTarget.textContent = t.hidden ? 'Ver como tabela' : 'Ocultar tabela';
});

/* triagem */
const fr = $('#fr'), fs = $('#fs');
rk.forEach((k) => fr.insertAdjacentHTML('beforeend', `<option value="${k}">${k}</option>`));
ST.forEach((s) => fs.insertAdjacentHTML('beforeend', `<option value="${s[0]}">${s[0]} · ${s[1]}</option>`));
const body = $('#triBody');
const link = (r) => r.doi ? `https://doi.org/${r.doi}` : r.url;
function renderTri() {
  const q = $('#fq').value.trim().toLowerCase(), d = $('#fd').value, rr = fr.value, s = fs.value;
  const rows = TRI.filter((r) => (!rr || r.round === rr) && (!d || r.decision === d) && (!s || r.stages.includes(s)) &&
    (!q || [r.title, r.venue, (r.authors || []).join(' '), r.justification, r.ai_justification, r.id, r.doi].join(' ').toLowerCase().includes(q)));
  $('#fcount').textContent = `${rows.length} de ${TRI.length}`;
  body.innerHTML = rows.map((r) => `
    <tr class="row" data-id="${r.id}" tabindex="0" aria-expanded="false">
      <td><span class="tag">${r.round}</span><div class="meta">#${r.rank ?? '–'}</div></td>
      <td><div class="t">${esc(r.title)}</div><div class="meta">${esc((r.authors || []).join(', '))} · ${esc(r.year)} · ${esc(r.venue)}</div></td>
      <td class="hide-sm"><div class="chips">${r.stages.map((x) => `<span class="tag">${x}</span>`).join('')}</div></td>
      <td>${r.decision === 'include' ? '<span class="tag inc">incluída</span>' : `<span class="tag exc">excluída · ${esc(r.criterion)}</span>`}</td>
    </tr>
    <tr class="det" data-for="${r.id}" hidden><td colspan="4"><dl>
      <dt>Justificativa humana</dt><dd>${esc(r.justification)}</dd>
      <dt>Ranqueamento (IA)</dt><dd>${esc(r.ai_justification || '—')}</dd>
      <dt>Dimensões</dt><dd>${r.dimensions.length ? esc(r.dimensions.join(', ')) : '—'}</dd>
      <dt>Origem</dt><dd>${esc(r.sources.join(', '))} · ${esc(r.origins.map((o) => o === 'search' ? 'busca direta' : o).join(', '))}${r.families.length ? ` · famílias ${esc(r.families.join(', '))}` : ''}</dd>
      <dt>Identificador</dt><dd><code>${r.id}</code>${link(r) ? ` · <a href="${esc(link(r))}" target="_blank" rel="noopener">${r.doi ? 'doi:' + esc(r.doi) : 'registro'}</a>` : ''}</dd>
    </dl></td></tr>`).join('');
}
function toggle(tr) {
  const det = body.querySelector(`tr.det[data-for="${tr.dataset.id}"]`);
  det.hidden = !det.hidden; tr.setAttribute('aria-expanded', String(!det.hidden));
}
body.addEventListener('click', (e) => { if (e.target.closest('a')) return; const tr = e.target.closest('tr.row'); if (tr) toggle(tr); });
body.addEventListener('keydown', (e) => { const tr = e.target.closest('tr.row'); if (tr && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); toggle(tr); } });
['fq', 'fd', 'fr', 'fs'].forEach((id) => $('#' + id).addEventListener('input', renderTri));
renderTri();

/* seção ativa na navegação */
const links = [...document.querySelectorAll('.nav a')];
const io = new IntersectionObserver((ents) => ents.forEach((en) => {
  if (en.isIntersecting) links.forEach((a) => a.toggleAttribute('aria-current', a.getAttribute('href') === '#' + en.target.id));
}), { rootMargin: '-40% 0px -55% 0px' });
links.forEach((a) => { const s = document.querySelector(a.getAttribute('href')); if (s) io.observe(s); });
})();
