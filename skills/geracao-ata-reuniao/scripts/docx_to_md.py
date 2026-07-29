#!/usr/bin/env python3
"""Extrai Markdown estruturado de um .docx, sem dependencias externas.

Serve para reconstruir o `- ATA.md` a partir de uma `- ATA.docx` legada, de modo
que os dois fiquem equivalentes. E o inverso de md_to_docx.py.

Heuristica de titulos: o Word nao usa estilos de heading nestas ATAs, so
tamanho de fonte + negrito. Tamanhos absolutos nao sao comparaveis entre
arquivos (uma ATA usa 30 para o titulo, outra usa 48), entao os tamanhos de
paragrafos em negrito sao ranqueados dentro de cada documento e o ranking vira
o nivel de titulo.

Uso:
    python docx_to_md.py "arquivo.docx" [-o saida.md]
"""

import argparse
import re
import sys
import zipfile
from xml.etree import ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MARCADORES = ("•", "", "-", "–", "*")


def texto_de(no):
    partes = []
    for x in no.iter():
        if x.tag == f"{W}t":
            partes.append(x.text or "")
        elif x.tag == f"{W}tab":
            partes.append(" ")
        elif x.tag == f"{W}br":
            # Um paragrafo pode conter varias linhas (ex.: lista inteira de
            # participantes num unico <w:p> separada por <w:br/>).
            partes.append("\n")
    return "".join(partes).strip()


def runs_markdown(p):
    """Reconstroi o paragrafo marcando **negrito** apenas nos runs em negrito."""
    saida = []
    for r in p.findall(f"{W}r"):
        t = "".join(x.text or "" for x in r.iter(f"{W}t"))
        if not t:
            continue
        if r.find(f"{W}rPr/{W}b") is not None and t.strip():
            # O espaco tem de ficar fora do **: "**Data: **" nao renderiza.
            inicio = t[: len(t) - len(t.lstrip())]
            fim = t[len(t.rstrip()) :]
            saida.append(f"{inicio}**{t.strip()}**{fim}")
        else:
            saida.append(t)
    # Junta ***a******b*** adjacentes que o Word quebra em varios runs.
    return re.sub(r"\*\*(\s*)\*\*", r"\1", "".join(saida)).strip()


def tamanho(p):
    sz = p.find(f".//{W}sz")
    return int(sz.get(f"{W}val")) if sz is not None else 0


def em_negrito(p):
    runs = p.findall(f"{W}r")
    if not runs:
        return False
    return all(r.find(f"{W}rPr/{W}b") is not None for r in runs if texto_de(r))


def tabela_markdown(tbl):
    linhas = []
    for tr in tbl.findall(f"{W}tr"):
        celulas = [texto_de(tc).replace("\n", " ") or " " for tc in tr.findall(f"{W}tc")]
        linhas.append(celulas)
    if not linhas:
        return []
    largura = max(len(l) for l in linhas)
    linhas = [l + [" "] * (largura - len(l)) for l in linhas]
    saida = ["| " + " | ".join(linhas[0]) + " |",
             "|" + "---|" * largura]
    for l in linhas[1:]:
        saida.append("| " + " | ".join(l) + " |")
    return saida


def converter(caminho):
    with zipfile.ZipFile(caminho) as z:
        root = ElementTree.fromstring(z.read("word/document.xml"))

    corpo = root.find(f"{W}body")

    # 1a passada: ranking dos tamanhos usados em paragrafos de titulo.
    tamanhos = sorted({tamanho(p) for p in corpo.iter(f"{W}p")
                       if em_negrito(p) and tamanho(p) and texto_de(p)}, reverse=True)
    nivel_de = {t: min(i + 1, 3) for i, t in enumerate(tamanhos)}

    linhas, titulo_visto, pendente_subtitulo = [], False, False

    for filho in corpo:
        if filho.tag == f"{W}tbl":
            linhas.extend(tabela_markdown(filho))
            linhas.append("")
            continue
        if filho.tag != f"{W}p":
            continue

        txt = texto_de(filho)
        if not txt:
            continue

        lista = filho.find(f".//{W}numPr") is not None
        partes = [p.strip() for p in txt.split("\n") if p.strip()]
        marcador = partes[0][:1] in MARCADORES and len(partes[0]) > 2

        if lista or marcador:
            for parte in partes:
                if parte[:1] in MARCADORES:
                    parte = parte[1:].strip()
                linhas.extend([f"- {parte}", ""])
            pendente_subtitulo = False
            continue

        if len(partes) > 1:
            for parte in partes:
                linhas.extend([parte, ""])
            pendente_subtitulo = False
            continue

        if em_negrito(filho) and tamanho(filho) in nivel_de:
            nivel = nivel_de[tamanho(filho)]
            if not titulo_visto:
                linhas.extend([f"# {txt}", ""])
                titulo_visto, pendente_subtitulo = True, True
                continue
            if pendente_subtitulo:
                # Paragrafo logo apos o titulo e o subtitulo da ata, nao secao.
                linhas.extend([txt, ""])
                pendente_subtitulo = False
                continue
            linhas.extend([f"{'#' * max(nivel, 2)} {txt}", ""])
            continue

        pendente_subtitulo = False
        linhas.extend([runs_markdown(filho) or txt, ""])

    return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Extrai Markdown de um .docx.")
    parser.add_argument("docx")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    try:
        md = converter(args.docx)
    except FileNotFoundError:
        sys.exit(f"erro: arquivo nao encontrado: '{args.docx}'")

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as h:
            h.write(md)
        print(f"gerado: {args.output}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
