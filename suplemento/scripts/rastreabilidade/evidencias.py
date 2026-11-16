"""Carrega as 244 evidências válidas do corpus final com identificadores estáveis.

Acadêmicas: extracao/lote_*.json, filtradas pelas fontes "Adequada" de
consolidado/AUDITORIA_DECISOES_CORPUS.csv (179). Cinzentas: aba "Extração" de
cinzenta/Literatura_cinzenta_r009.xlsx, filtrada pelas fontes incluídas (65).
ID da evidência: <fonte>-e<NN>, na ordem em que o excerto aparece na ficha.
"""
import csv, glob, json, re
from pathlib import Path
import openpyxl

BASE = Path(__file__).resolve().parents[2]
DECISOES = BASE / "consolidado/AUDITORIA_DECISOES_CORPUS.csv"
CINZ = BASE / "cinzenta/Literatura_cinzenta_r009.xlsx"
ETAPA_RE = re.compile(r"S[1-8]")


def decisoes():
    return list(csv.DictReader(DECISOES.open(encoding="utf-8-sig", newline="")))


def carregar():
    dec = decisoes()
    pid2cod = {r["ID"]: r["Código"] for r in dec if r["Bloco"] == "Acadêmica"}
    acad = {r["Código"] for r in dec if r["Bloco"] == "Acadêmica" and r["Decisão final"] == "Adequada"}
    cinz = {r["Código"]: r for r in dec if r["Bloco"] == "Cinzenta" and r["Decisão final"].startswith("Incluída")}
    out = []
    for f in sorted(glob.glob(str(BASE / "extracao/lote_*.json"))):
        for art in json.loads(Path(f).read_text(encoding="utf-8")):
            cod = pid2cod[art["id"]]
            if cod not in acad:
                continue
            for n, e in enumerate(art.get("evidencias", []), 1):
                out.append(dict(evid=f"{cod}-e{n:02d}", fonte=cod, literatura="Acadêmica",
                                etapas="/".join(sorted(set(ETAPA_RE.findall(e.get("etapa", ""))))),
                                dimensao=e.get("dimensao", ""), pratica=e.get("pratica", ""),
                                classificacao=e.get("classificacao", ""), decisao=e.get("decisao", ""),
                                desafio=e.get("desafio", ""), metrica=e.get("metrica", ""),
                                localizacao=e.get("pagina", ""), excerto=e.get("evidencia", "")))
    wb = openpyxl.load_workbook(CINZ, read_only=True)
    id2c = {r[1]: r[0] for r in wb["Avaliação QG"].iter_rows(min_row=2, values_only=True) if r[0]}
    cont = {}
    for r in wb["Extração"].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        cod = id2c.get(r[0], r[0])
        if cod not in cinz:
            continue
        cont[cod] = cont.get(cod, 0) + 1
        out.append(dict(evid=f"{cod}-e{cont[cod]:02d}", fonte=cod, literatura="Cinzenta",
                        etapas="/".join(sorted(set(ETAPA_RE.findall(str(r[5] or ""))))),
                        dimensao=r[6] or "", pratica=r[7] or "", classificacao="",
                        decisao=r[10] or "", desafio=r[9] or "", metrica=r[12] or "",
                        localizacao=r[3] or "", excerto=r[4] or ""))
    acad_n = sum(e["literatura"] == "Acadêmica" for e in out)
    assert (acad_n, len(out) - acad_n) == (179, 65), (acad_n, len(out) - acad_n)
    return out, dec


if __name__ == "__main__":
    ev, _ = carregar()
    for e in ev:
        print(e["evid"], e["etapas"], "|", e["pratica"], "|", e["decisao"][:110])
