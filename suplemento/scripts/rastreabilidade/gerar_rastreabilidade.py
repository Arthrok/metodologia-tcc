"""Gera o registro de rastreabilidade entre as 244 evidências e as tabelas QP1–QP3.

Saídas em consolidado/rastreabilidade/ e a tabela tcc/secoes/tab_qp3.tex.
Uso: python3 scripts/rastreabilidade/gerar_rastreabilidade.py

A codificação evidência→tema (TEMAS) e evidência→linha da QP2 (QP2) foi
consolidada com apoio de modelo de linguagem a partir das fichas de extração;
cada atribuição pode ser conferida pelo ID da evidência em evidencias_244.csv.
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

from evidencias import BASE, CINZ, carregar

OUT = BASE / "consolidado/rastreabilidade"
TAB_QP1 = BASE / "tcc/secoes/tab_qp1.tex"
TAB_QP3 = BASE / "tcc/secoes/tab_qp3.tex"

# Rótulos de tipo de evidência por fonte. Acadêmicas sem rótulo na matriz: EE.
ROT_ACAD = {"A04": "EP", "A32": "EP", "A43": "EP", "A45": "PC"}
ROT_CINZ = {"C01": "EL", "C02": "EL", "C03": "GP", "C04": "GP", "C05": "EP", "C06": "GP",
            "C07": "EL", "C08": "EL", "C10": "GP", "C11": "EP", "C12": "EL", "C13": "EL",
            "C14": "GP", "C15": "GP", "C16": "MI", "C17": "MI", "C18": "EP", "C19": "EP",
            "C20": "EL", "C22": "GP", "C23": "EL", "C24": "EL", "C25": "GP", "C26": "GP",
            "C28": "EP", "C29": "GP", "C30": "GP", "C31": "GP", "C32": "GP", "C33": "EL",
            "C34": "GP", "C35": "EP", "C36": "EL", "C37": "GP"}  # C09, C21, C27: sem rótulo


def rotulo(fonte):
    if fonte.startswith("A"):
        return ROT_ACAD.get(fonte, "EE")
    return ROT_CINZ.get(fonte, "sem rótulo")


# Temas da Tabela QP3: (nome, definição operacional, evidências, temas da planilha de 34)
TEMAS = [
    ("Medallion para documentos RAG",
     "Camadas Bronze/Silver/Gold aplicadas a artefatos documentais do pipeline RAG",
     "A23-e03", ["(tema novo, desdobrado da QP2)"]),
    ("Índices federados por domínio",
     "Índices e documentos mantidos por domínio ou instituição, com roteamento federado",
     "A02-e01 A02-e02 A33-e01", ["(tema novo, desdobrado da QP2)"]),
    ("Pré/pós-filtro na busca vetorial",
     "Decisão sobre onde e como aplicar filtros de atributos na busca vetorial (pré/pós-filtro, pushdown, varredura iterativa, seletividade)",
     "A12-e03 A32-e04 A34-e03 A36-e02 A40-e03 A58-e02 C05-e02", ["(tema novo, desdobrado da QP2)"]),
    ("Autorização antes da geração",
     "Controle de acesso aplicado na recuperação ou antes do prompt (ACL, RBAC/ABAC/PBAC, IAM da fonte, finalidade)",
     "A22-e01 A22-e04 A25-e01 A25-e04 A31-e01 A31-e02 A33-e02 A40-e03 A45-e01 A58-e02 C05-e01 C06-e02 C30-e01 C35-e03",
     ["Controle de acesso na recuperação (ACL/políticas)"]),
    ("Linhagem e traces por resposta",
     "Registro de proveniência ou trace que liga fonte, trecho, rota e resposta",
     "A02-e04 A04-e04 A22-e03 A43-e01 A43-e02 A45-e03 A58-e03 C14-e01",
     ["Rastreamento por requisição e observabilidade da recuperação",
      "Integridade do índice e da linhagem (Merkle, assinaturas)"]),
    ("Chunking estrutural e contexto",
     "Preservação de estrutura, tabelas e hierarquia ou inclusão de contexto e metadados do documento no chunk",
     "A06-e01 A09-e02 A10-e02 A12-e01 A12-e02 A15-e01 A15-e02 A18-e02 A23-e02 A40-e02 A42-e02 "
     "A44-e01 A51-e02 A52-e01 A52-e03 A55-e01 A55-e03 A59-e01 A60-e01 A60-e03 "
     "C02-e03 C20-e01 C29-e02 C33-e01 C35-e02",
     ["Preservar tabelas e estrutura na extração e no chunking",
      "Enriquecer o chunk com contexto e metadados do documento"]),
    ("Retenção por artefato e mascaramento de PII",
     "Minimização, redação ou mascaramento de dados pessoais e prazos de retenção por artefato ou camada",
     "A02-e04 A04-e04 A43-e03 A45-e01 A45-e02 C10-e01 C10-e03 C14-e02",
     ["Redação/mascaramento de PII e minimização",
      "Retenção por tipo de artefato (logs, prompts, camadas)"]),
    ("Índices ANN, WAL e latência filtrada",
     "Mecanismos internos de construção, atualização, compactação e manutenção de índices ANN",
     "A24-e01 A24-e03 A29-e01 A29-e02 A29-e03 A32-e02 A32-e03 A34-e01 A34-e02 A35-e01 A35-e02 "
     "A36-e01 A36-e03 A36-e04",
     ["Manutenção estrutural do índice ANN (reconstrução, split/merge)",
      "Atualização incremental e consistência durante a atualização (parte acadêmica)"]),
    ("Métricas intrínsecas de chunk",
     "Medidas da qualidade do fragmento independentes da resposta final",
     "A30-e02 A49-e01 A53-e01", ["Métricas intrínsecas de qualidade do chunk"]),
    ("Orçamento formal de contexto",
     "Seleção ou dimensionamento do contexto sob orçamento explícito de tokens",
     "A15-e04 A42-e01 A47-e02 A48-e02", ["Seleção do contexto sob orçamento de tokens"]),
    ("Defasagem de estado entre índices, fontes e permissões",
     "Divergência entre o estado do índice e o da fonte ou das permissões, e sua ressincronização",
     "A16-e01 A16-e02 A16-e04 A22-e04 A25-e03 C28-e01 C30-e01",
     ["Sincronização entre índices/armazenamentos e defasagem"]),
    ("Exclusão em índices e derivados",
     "Remoção de documentos ou dados de índices e derivados (tombstone, purge, compactação, eliminação criptográfica, verificação)",
     "A19-e03 A24-e02 A25-e02 A32-e02 A34-e02 A35-e03 A58-e02 C01-e01 C01-e02 C10-e02 C12-e02",
     ["Exclusão em índices vetoriais (tombstone, compactação, purge)",
      "Exclusão verificável e direito ao esquecimento"]),
    ("Ingestão idempotente e retomável",
     "Ingestão ou reprocessamento controlado por hash de conteúdo, checkpoints e filas de falha",
     "C06-e01 C12-e01", ["Ingestão idempotente e retomável (hash, checkpoint)"]),
    ("Migração de embedding e troca de versão",
     "Troca de modelo de embedding, índice ou configuração com validação, versão e rollback",
     "A08-e04 A22-e02 A40-e04 A43-e04 C11-e01 C16-e01 C16-e02",
     ["Migração do modelo de embedding (re-embedding)",
      "Versionamento do corpus/índice e rollback"]),
]

# Linhas da Tabela QP2 e evidências que as sustentam.
QP2 = [
    ("Medallion documental", "A23-e03"),
    ("Lakehouse versionado", "A58-e01 A58-e02 A58-e04"),
    ("Propriedade por domínio", "A02-e01 A33-e01"),
    ("Partição e integração vetorial", "A32-e01 A32-e03 A35-e01 A35-e02 C05-e01 C28-e01"),
    ("Metadado mutável separado", "A25-e02 A25-e03 A60-e02"),
    ("Índice progressivo", "A29-e01 A29-e02"),
    ("Otimização de filtros", "A32-e04 A34-e03 C05-e02"),
    ("Autorização antes da geração", "A22-e01 A25-e01 A33-e02 C30-e01"),
    ("Contexto sob orçamento", "A15-e04 A42-e01"),
    ("Curadoria por incerteza", "A03-e03"),
    ("Qualidade intrínseca do fragmento", "A49-e01 A49-e02 A53-e01"),
    ("Traces e feedback", "A43-e01 A43-e02 A43-e03 A45-e03 C14-e01"),
]


def ids_celula(cell):
    out = []
    for a, b in re.findall(r"([AC]\d{2})(?:--([AC]?\d{2}))?", cell):
        if b:
            out += [f"{a[0]}{n:02d}" for n in range(int(a[1:]), int(b.lstrip('AC')) + 1)]
        else:
            out.append(a)
    return out


def escrever(nome, campos, linhas):
    with (OUT / nome).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(campos)
        w.writerows(linhas)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ev, dec = carregar()
    por_id = {e["evid"]: e for e in ev}
    por_fonte = defaultdict(list)
    for e in ev:
        por_fonte[e["fonte"]].append(e)

    # 1. Evidências
    campos = ["evid", "fonte", "literatura", "etapas", "dimensao", "pratica", "classificacao",
              "decisao", "desafio", "metrica", "localizacao", "excerto"]
    escrever("evidencias_244.csv", campos + ["tipo_evidencia_fonte"],
             [[e[c] for c in campos] + [rotulo(e["fonte"])] for e in ev])

    # 2. QP3: codificação, frequências e Tabela 19
    cod, freq = [], []
    tema_por_ev = defaultdict(list)
    for n, (nome, defin, evids, _) in enumerate(TEMAS, 1):
        lista = evids.split()
        for x in lista:
            assert x in por_id, (nome, x)
            tema_por_ev[x].append(f"T{n:02d}")
            cod.append([f"T{n:02d}", nome, x, por_id[x]["fonte"], por_id[x]["literatura"],
                        por_id[x]["etapas"], por_id[x]["pratica"]])
        fontes = sorted({por_id[x]["fonte"] for x in lista})
        ac = [f for f in fontes if f.startswith("A")]
        ci = [f for f in fontes if f.startswith("C")]
        pres = "Ambas" if ac and ci else "Acadêmica" if ac else "Cinzenta"
        freq.append(dict(n=n, nome=nome, defin=defin, pres=pres, ac=ac, ci=ci,
                         tipos_ac=Counter(rotulo(f) for f in ac), tipos_ci=Counter(rotulo(f) for f in ci),
                         n_ev=len(lista)))
    escrever("qp3_codificacao_evidencia_tema.csv",
             ["tema_id", "tema", "evid", "fonte", "literatura", "etapas", "pratica"], cod)

    def tipos(c):
        return "/".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))

    escrever("qp3_tabela19_frequencias.csv",
             ["tema_id", "tema", "definicao_operacional", "presenca", "n_fontes_acad", "n_fontes_cinz",
              "n_evidencias", "fontes_acad", "fontes_cinz", "tipos_acad", "tipos_cinz"],
             [[f"T{t['n']:02d}", t["nome"], t["defin"], t["pres"], len(t["ac"]), len(t["ci"]), t["n_ev"],
               ", ".join(t["ac"]), ", ".join(t["ci"]), tipos(t["tipos_ac"]), tipos(t["tipos_ci"])]
              for t in freq])

    # 3. Correspondência com os 34 temas da planilha (frequência recalculada no corpus final)
    final = {e["fonte"] for e in ev}
    wb = openpyxl.load_workbook(CINZ, read_only=True)
    mapa = defaultdict(list)
    for n, (nome, _, _, origem) in enumerate(TEMAS, 1):
        for o in origem:
            mapa[o].append(f"T{n:02d} {nome}")
    linhas34 = []
    for r in list(wb["QP3"].iter_rows(min_row=2, values_only=True)):
        if not r[0]:
            continue
        ac = [i.strip() for i in str(r[4] or "").split(",") if i.strip() and i.strip() != "None"]
        ci = [i.strip() for i in str(r[6] or "").split(",") if i.strip() and i.strip() != "None"]
        fora = [i for i in ac + ci if i not in final]
        ac2 = [i for i in ac if i in final]
        ci2 = [i for i in ci if i in final]
        alvo = [m for k, v in mapa.items() if k == r[0] or k.startswith(r[0]) or r[0].startswith(k.split(" (")[0])
                for m in v]
        linhas34.append([r[0], r[1], r[3], r[5], len(ac2), len(ci2), ", ".join(ac2), ", ".join(ci2),
                         ", ".join(fora) or "—",
                         "; ".join(alvo) or "Não apresentado na Tabela 19 (tratado no texto da QP1/QP2 ou só no suplemento)"])
    assert len(linhas34) == 34
    escrever("qp3_correspondencia_34_temas.csv",
             ["tema_planilha", "etapa", "n_acad_planilha", "n_cinz_planilha", "n_acad_corpus_final",
              "n_cinz_corpus_final", "acad_corpus_final", "cinz_corpus_final", "ids_fora_do_corpus_final",
              "linha_tabela19"], linhas34)

    # 4. QP1: vínculo célula→evidências pela etapa da linha
    qp1, sem = [], []
    for line in TAB_QP1.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(S\d) & (.*?) & (.*?) & (.*?) & ", line)
        if not m:
            continue
        st = m.group(1)
        for f in ids_celula(m.group(4)):
            evs = [e["evid"] for e in por_fonte[f] if st in e["etapas"].split("/")]
            if not evs:
                sem.append(f"{st}-{f}")
            qp1.append([st, f, rotulo(f), " ".join(evs) or "SEM EVIDÊNCIA NA ETAPA"])
    assert not sem, f"Células da QP1 sem evidência na etapa: {sem}"
    escrever("qp1_vinculo_celula_evidencias.csv", ["etapa", "fonte", "tipo_evidencia_fonte", "evidencias"], qp1)

    # 5. QP2
    qp2 = []
    for linha, evids in QP2:
        for x in evids.split():
            assert x in por_id, x
            e = por_id[x]
            qp2.append([linha, x, e["fonte"], e["etapas"], e["classificacao"] or "—", e["pratica"], e["localizacao"]])
    escrever("qp2_vinculo_linha_evidencias.csv",
             ["linha_tabela18", "evid", "fonte", "etapas", "classificacao_extracao", "pratica", "localizacao"], qp2)

    # 6. Evidência → tabelas (visão invertida)
    em_qp1 = defaultdict(list)
    for st, f, _, evs in qp1:
        for x in evs.split():
            em_qp1[x].append(st)
    em_qp2 = defaultdict(list)
    for linha, x, *_ in qp2:
        em_qp2[x].append(linha)
    escrever("evidencia_para_tabelas.csv", ["evid", "fonte", "etapas", "qp1_linhas", "qp2_linhas", "qp3_temas"],
             [[e["evid"], e["fonte"], e["etapas"], " ".join(em_qp1[e["evid"]]) or "—",
               "; ".join(em_qp2[e["evid"]]) or "—", " ".join(tema_por_ev[e["evid"]]) or "—"] for e in ev])

    # 7. Tabela 19 (LaTeX)
    def tex_tipos(t):
        partes = []
        if t["ac"]:
            partes.append("acad. " + ", ".join(f"{k} {v}" for k, v in sorted(t["tipos_ac"].items())))
        if t["ci"]:
            partes.append("cinz. " + ", ".join(f"{k} {v}" for k, v in sorted(t["tipos_ci"].items())))
        return "; ".join(partes)

    linhas = [rf"{t['nome']} & {t['pres']} & {len(t['ac'])}/{len(t['ci'])} & "
              rf"{', '.join(t['ac'])}{'; ' if t['ac'] and t['ci'] else ''}{', '.join(t['ci'])} & {tex_tipos(t)} \\"
              for t in freq]
    TAB_QP3.write_text("\n".join([
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{QP3: presença temática e natureza do suporte. A frequência conta as fontes com ao menos uma evidência codificada no tema e não mede eficácia; uma evidência pode integrar mais de um tema. Os rótulos contam fontes: EP = produção, EE = experimento acadêmico, EL = experimento cinzento, GP = guia/proposta, PC = proposta conceitual acadêmica, MI = material ilustrativo de uso restrito. A codificação e a correspondência com os 34 temas da planilha de extração constam do material suplementar.}",
        r"\label{tab:qp3-sintese}",
        r"\scriptsize",
        r"\begin{tabularx}{\textwidth}{p{3.2cm} p{1.25cm}p{1.25cm}X p{3.1cm}}",
        r"\toprule",
        r"Tema & Presença & Fontes acad./cinz. & IDs das fontes & Tipo de suporte (fontes) \\",
        r"\midrule",
        *linhas,
        r"\bottomrule",
        r"\end{tabularx}",
        r"\end{table*}",
        ""]), encoding="utf-8")

    # 8. Auditoria humana (seção 3.3.7): itens nominais e base documental de cada afirmação
    aval = {r["Código"]: r for r in dec if r["Código"]}
    itens = []
    for r in dec:
        p = r["Pontuação"].replace(",", ".")
        if r["Código"] and (re.search(r"QA=4(?:\.0|\.5)?\b", p) or re.search(r"QG=4(?:\.0|\.5)?\b", p)):
            itens.append(["Caso próximo ao corte", r["Código"], r["Bloco"], r["Pontuação"], r["Avaliador"],
                          r["Decisão final"], r["Observação"]])
    for linha, evids in QP2:
        for f in sorted({x.split("-")[0] for x in evids.split()}):
            itens.append(["Adaptação da QP2 (Tabela 18): " + linha, f, aval[f]["Bloco"], aval[f]["Pontuação"],
                          aval[f]["Avaliador"], aval[f]["Decisão final"], evids])
    n_corte = sum(i[0] == "Caso próximo ao corte" for i in itens)
    assert n_corte == 20, n_corte
    escrever("auditoria_humana_itens.csv",
             ["item", "fonte", "bloco", "pontuacao", "avaliador_atribuido", "decisao_final", "observacao_ou_evidencias"],
             itens)
    div = Counter((r["Avaliador"], r["Bloco"]) for r in dec)
    escrever("auditoria_humana_registro.csv", ["afirmacao_secao_3_3_7", "base_documental", "o_que_o_registro_comprova", "o_que_nao_comprova"], [
        [f"Divisão nominal: Eric {sum(v for (a, _), v in div.items() if a == 'Eric')} registros, "
         f"Arthur {sum(v for (a, _), v in div.items() if a == 'Arthur')}",
         "consolidado/AUDITORIA_DECISOES_CORPUS.csv, coluna Avaliador",
         "; ".join(f"{a}/{b}: {v}" for (a, b), v in sorted(div.items())),
         "Data e conteúdo de cada conferência"],
        ["Conferência dos 20 casos próximos dos cortes QA=4,0/4,5 e QG=4,0/4,5",
         "auditoria_humana_itens.csv (item = Caso próximo ao corte)",
         "Lista nominal dos 20 casos, avaliador atribuído e decisão final",
         "O que foi confirmado ou alterado em cada nota"],
        ["Conferência dirigida das adaptações da QP2",
         "auditoria_humana_itens.csv (itens da Tabela 18); qp2_vinculo_linha_evidencias.csv; consolidado/CONFERENCIA_QP2_E_CORTE.md",
         "Fontes e excertos de cada adaptação apresentada, com avaliador atribuído",
         "Resultado individual da conferência de cada adaptação"],
        ["Rebaixamento de A57 para QA < 4,0",
         "consolidado/AUDITORIA_DECISOES_CORPUS.csv (A57: Decisão final e Observação)",
         aval["A57"]["Decisão final"] + " — " + aval["A57"]["Observação"], "—"],
        ["Restrição de uso numérico de C09, C16, C17 e C21",
         "consolidado/AUDITORIA_DECISOES_CORPUS.csv (Decisão final)",
         "; ".join(f"{c}: {aval[c]['Decisão final']}" for c in ("C09", "C16", "C17", "C21")), "—"],
    ])

    # Resumo
    print("evidências:", len(ev), "| temas:", len(TEMAS), "| codificações:", len(cod),
          "| evidências em algum tema:", len({c[2] for c in cod}))
    for t in freq:
        print(f"T{t['n']:02d} {t['nome'][:45]:45} {t['pres']:9} {len(t['ac'])}/{len(t['ci'])}  {tex_tipos(t)}")
    print("QP1 células:", len(qp1), "| QP2 vínculos:", len(qp2))


if __name__ == "__main__":
    main()
