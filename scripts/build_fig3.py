"""Generate Figure 3 (PRISMA selection flow) in the exact visual style of Figure 2."""
from pathlib import Path
import html

W = 1280
H = 820

# Colors matching Figure 2 (figura3_ciclo_selecao.pdf)
STROKE = "#1f2937"
TEXT_MAIN = "#111827"
TEXT_MUTED = "#4b5563"
FILL_WHITE = "#ffffff"
FILL_HUMAN = "#e5e7eb"
FILL_DASH = "#f9fafb"


def box(x, y, w, h, title, lines, tag=None, human=False, thick=False, dashed=False, center_title=True):
    fill = FILL_HUMAN if human else (FILL_DASH if dashed else FILL_WHITE)
    sw = "2.1" if thick else "1.25"
    da = ' stroke-dasharray="5,4"' if dashed else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" ry="5" fill="{fill}" stroke="{STROKE}" stroke-width="{sw}"{da}/>']
    if tag:
        out.append(f'<text x="{x+9}" y="{y+15}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="10" font-weight="600" fill="{TEXT_MUTED}">{html.escape(tag)}</text>')
    # Vertical centering of title + lines
    total_lines = 1 + len(lines)
    line_h = 16
    block_h = total_lines * line_h
    start_y = y + (h - block_h) / 2 + 13 + (4 if tag else 0)
    cx = x + w / 2 if center_title else x + 12
    anchor = 'middle' if center_title else 'start'
    out.append(f'<text x="{cx}" y="{start_y:.1f}" text-anchor="{anchor}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="13.5" font-weight="700" fill="{TEXT_MAIN}">{html.escape(title)}</text>')
    for i, ln in enumerate(lines, 1):
        out.append(f'<text x="{cx}" y="{start_y + i * line_h:.1f}" text-anchor="{anchor}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="11.5" fill="{TEXT_MUTED if not thick else TEXT_MAIN}">{html.escape(ln)}</text>')
    return "\n".join(out)


def arrow(x1, y1, x2, y2, dashed=False):
    da = ' stroke-dasharray="5,4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{STROKE}" stroke-width="1.25"{da} marker-end="url(#arr)"/>'


def build_svg():
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="{STROKE}"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>
''']

    # Section column headers
    parts.append(f'<text x="175" y="34" text-anchor="middle" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="{TEXT_MAIN}">Literatura acadêmica</text>')
    parts.append(f'<text x="820" y="34" text-anchor="middle" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="{TEXT_MAIN}">Literatura cinzenta</text>')

    # Subtle vertical divider between the two streams
    parts.append(f'<line x1="635" y1="22" x2="635" y2="740" stroke="#e5e7eb" stroke-width="1.2" stroke-dasharray="4,4"/>')

    # --- LEFT COLUMN: ACADEMIC ---
    ax, aw = 30, 290
    sx, sw = 365, 240
    ys = [52, 134, 216, 298, 384, 470, 552, 634]
    h = 62

    parts.append(box(ax, ys[0], aw, h, "Buscas diretas", ["Scopus (3.142) e ACL Anthology (299)"]))
    parts.append(box(sx, ys[0]+5, sw, 52, "Duplicatas entre bases (E1)", ["191 registros removidos"], dashed=True))
    parts.append(arrow(ax+aw, ys[0]+h/2, sx, ys[0]+h/2, dashed=True))

    parts.append(box(ax, ys[1], aw, h, "Publicações únicas: 3.250", ["Backward snowballing: +845 novos"]))
    parts.append(arrow(ax+aw/2, ys[0]+h, ax+aw/2, ys[1]))

    parts.append(box(ax, ys[2], aw, 56, "Conjunto consolidado: 4.095", []))
    parts.append(box(sx, ys[2]+3, sw, 50, "Não pré-triados: 1.863", ["sem decisão de exclusão"], dashed=True))
    parts.append(arrow(ax+aw/2, ys[1]+h, ax+aw/2, ys[2]))
    parts.append(arrow(ax+aw, ys[2]+28, sx, ys[2]+28, dashed=True))

    parts.append(box(ax, ys[3], aw, h, "Pré-triados pelo modelo: 2.232", ["827 incluir · 781 excluir · 624 ambíguo"], tag="IA"))
    parts.append(box(sx, ys[3]+5, sw, 52, "Não priorizados: 2.152", ["não apresentados nas 8 rodadas"], dashed=True))
    parts.append(arrow(ax+aw/2, ys[2]+56, ax+aw/2, ys[3]))
    parts.append(arrow(ax+aw, ys[3]+h/2, sx, ys[3]+h/2, dashed=True))

    parts.append(box(ax, ys[4], aw, h, "Avaliados pelos pesquisadores: 80", ["8 rodadas de 10 candidatos (Arthur)"], tag="HUMANO", human=True))
    parts.append(box(sx, ys[4]+5, sw, 52, "Excluídos na triagem: 20", ["E3: 19 · E4: 1"], dashed=True))
    parts.append(arrow(ax+aw/2, ys[3]+h, ax+aw/2, ys[4]))
    parts.append(arrow(ax+aw, ys[4]+h/2, sx, ys[4]+h/2, dashed=True))

    parts.append(box(ax, ys[5], aw, 56, "Inclusões na triagem: 60", ["busca do texto integral"]))
    parts.append(box(sx, ys[5]+3, sw, 50, "Excluídas por E5: 5", ["texto integral indisponível"], dashed=True))
    parts.append(arrow(ax+aw/2, ys[4]+h, ax+aw/2, ys[5]))
    parts.append(arrow(ax+aw, ys[5]+28, sx, ys[5]+28, dashed=True))

    parts.append(box(ax, ys[6], aw, h, "Avaliadas na qualidade: 55", ["critérios QA1–QA6 (mín. 4,0)"], tag="IA + HUMANO"))
    parts.append(box(sx, ys[6]+5, sw, 52, "Desconsideradas na QA: 4", ["A01, A28, A50 e A57 (rebaixada)"], dashed=True))
    parts.append(arrow(ax+aw/2, ys[5]+56, ax+aw/2, ys[6]))
    parts.append(arrow(ax+aw, ys[6]+h/2, sx, ys[6]+h/2, dashed=True))

    parts.append(box(ax, ys[7], aw, 60, "Corpus acadêmico adequado: 51", ["179 evidências · 261 associações S1–S8"], thick=True))
    parts.append(arrow(ax+aw/2, ys[6]+h, ax+aw/2, ys[7]))

    # Forward snowballing note box (bottom-right of academic side)
    parts.append(box(sx, ys[7]-2, sw, 64, "Forward snowballing (OpenAlex)", ["400 novos (95 priorizados)", "encerrados por escopo"], dashed=True))
    parts.append(arrow(ax+aw, ys[7]+30, sx, ys[7]+30, dashed=True))

    # --- RIGHT COLUMN: GREY ---
    gx, gw = 665, 310
    gy_side_x, gy_side_w = 1015, 235

    parts.append(box(gx, 52, gw, 78, "Buscas em 3 frentes", ["DEV Community: 6.059 publicações", "Hacker News: 92 consultas", "Portais: 12 candidatas (9 incluídas)"]))

    parts.append(box(gx, 186, gw, 84, "Candidatos únicos: 210", ["198 APIs: pré-triagem IA + revisão de Eric", "12 portais seguem direto ao texto integral"], tag="IA + HUMANO", human=True))
    parts.append(box(gy_side_x, 196, gy_side_w, 64, "Excluídos na pré-triagem: 149", ["E3 ou E4 (título/descrição)"], dashed=True))
    parts.append(arrow(gx+gw/2, 130, gx+gw/2, 186))
    parts.append(arrow(gx+gw, 228, gy_side_x, 228, dashed=True))

    parts.append(box(gx, 340, gw, 84, "Candidatas ao texto integral: 61", ["decisões finais de Eric e notas QG1–QG6", "(2 cópias via Wayback Machine)"], tag="IA + HUMANO", human=True))
    parts.append(box(gy_side_x, 336, gy_side_w, 92, "Excluídas na avaliação: 24", ["QG < 4: 9 · E4: 6 · E5: 3", "I1: 3 · QG1=0: 2 · QG6=0: 1"], dashed=True))
    parts.append(arrow(gx+gw/2, 270, gx+gw/2, 340))
    parts.append(arrow(gx+gw, 382, gy_side_x, 382, dashed=True))

    parts.append(box(gx, 502, gw, 68, "Corpus cinzento incluído: 37", ["14 DEV · 14 HN · 9 portais · 65 evidências"], thick=True))
    parts.append(arrow(gx+gw/2, 424, gx+gw/2, 502))

    # Final combined corpus summary box (joined from 51 academic + 37 grey)
    parts.append(box(gx, 632, gw, 64, "Corpus final da revisão: 88 fontes", ["51 acadêmicas + 37 cinzentas · 244 evidências"], human=False, thick=True))
    parts.append(arrow(gx+gw/2, 570, gx+gw/2, 632))
    # Route dashed/solid connector from bottom of academic 51 into final 88 box
    parts.append(f'<path d="M {ax+aw/2} {ys[7]+60} L {ax+aw/2} 722 L {gx+gw/2 - 55} 722 L {gx+gw/2 - 55} 696" fill="none" stroke="{STROKE}" stroke-width="1.25" marker-end="url(#arr)"/>')

    # Bottom Legend matching Figure 2
    ly = 775
    parts.append(f'<line x1="30" y1="{ly}" x2="72" y2="{ly}" stroke="{STROKE}" stroke-width="1.25" marker-end="url(#arr)"/>')
    parts.append(f'<text x="80" y="{ly+4}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="12" font-style="italic" fill="{TEXT_MUTED}">fluxo principal</text>')

    parts.append(f'<line x1="185" y1="{ly}" x2="227" y2="{ly}" stroke="{STROKE}" stroke-width="1.25" stroke-dasharray="5,4" marker-end="url(#arr)"/>')
    parts.append(f'<text x="235" y="{ly+4}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="12" font-style="italic" fill="{TEXT_MUTED}">exclusão / não avançou</text>')

    parts.append(f'<rect x="395" y="{ly-9}" width="24" height="16" rx="3" fill="{FILL_HUMAN}" stroke="{STROKE}" stroke-width="1.25"/>')
    parts.append(f'<text x="427" y="{ly+4}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="12" font-style="italic" fill="{TEXT_MUTED}">decisão humana</text>')

    parts.append(f'<rect x="545" y="{ly-9}" width="24" height="16" rx="3" fill="{FILL_WHITE}" stroke="{STROKE}" stroke-width="2.1"/>')
    parts.append(f'<text x="577" y="{ly+4}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="12" font-style="italic" fill="{TEXT_MUTED}">corpus final</text>')

    parts.append(f'<text x="675" y="{ly+4}" font-family="Liberation Sans, Helvetica, Arial, sans-serif" font-size="12" font-style="italic" fill="{TEXT_MUTED}">IA: apoio por modelo de linguagem, sem decisão de elegibilidade</text>')

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / "figura_prisma_selecao.svg"
    svg_path.write_text(build_svg(), encoding="utf-8")
    print("Wrote", svg_path)
