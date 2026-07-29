#!/usr/bin/env python3
"""Converte um subconjunto de Markdown em .docx sem dependencias externas.

Um .docx e um zip com XML (OOXML). Montamos as partes minimas validas:
[Content_Types].xml, _rels/.rels, word/styles.xml e word/document.xml.

Markdown suportado (suficiente para ATAs de reuniao):
    # Titulo            -> titulo principal
    ## Secao            -> titulo de secao
    ### Subsecao        -> titulo de subsecao
    - item              -> bullet
    | a | b |           -> tabela (primeira linha = cabecalho; linha --- ignorada)
    texto               -> paragrafo
    **negrito**         -> negrito inline
    (linha vazia)       -> separa blocos

Uso:
    python md_to_docx.py entrada.md -o saida.docx
"""

import argparse
import re
import sys
import zipfile
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/>
</w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
</w:styles>"""

# Tamanhos em meio-ponto: 32 = 16pt, 26 = 13pt, 24 = 12pt.
NIVEIS = {1: ("32", True), 2: ("26", True), 3: ("24", True)}


def runs(texto):
    """Converte **negrito** em runs OOXML; o resto vira run normal."""
    saida = []
    for i, parte in enumerate(re.split(r"\*\*(.+?)\*\*", texto)):
        if not parte:
            continue
        negrito = "<w:b/>" if i % 2 else ""
        saida.append(
            f'<w:r><w:rPr>{negrito}</w:rPr>'
            f'<w:t xml:space="preserve">{escape(parte)}</w:t></w:r>'
        )
    return "".join(saida)


def paragrafo(texto, tamanho=None, negrito=False, bullet=False, espaco_antes=0):
    corpo = runs(texto)
    if tamanho or negrito:
        marca = ("<w:b/>" if negrito else "") + (f'<w:sz w:val="{tamanho}"/>' if tamanho else "")
        corpo = corpo.replace("<w:rPr>", f"<w:rPr>{marca}")
    ind = '<w:ind w:left="360" w:hanging="180"/>' if bullet else ""
    esp = f'<w:spacing w:before="{espaco_antes}" w:after="120"/>'
    if bullet:
        corpo = '<w:r><w:t xml:space="preserve">•  </w:t></w:r>' + corpo
    return f"<w:p><w:pPr>{esp}{ind}</w:pPr>{corpo}</w:p>"


def tabela(linhas):
    """linhas: lista de listas de celulas; a primeira e o cabecalho."""
    bordas = "".join(
        f'<w:{lado} w:val="single" w:sz="4" w:color="999999"/>'
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>'
           f"<w:tblBorders>{bordas}</w:tblBorders></w:tblPr>"]
    for i, linha in enumerate(linhas):
        out.append("<w:tr>")
        for celula in linha:
            sombra = '<w:shd w:val="clear" w:fill="EFEFEF"/>' if i == 0 else ""
            conteudo = paragrafo(celula, negrito=(i == 0))
            out.append(f"<w:tc><w:tcPr>{sombra}</w:tcPr>{conteudo}</w:tc>")
        out.append("</w:tr>")
    out.append("</w:tbl>")
    # Paragrafo vazio depois da tabela: o Word exige separacao entre tabelas.
    out.append("<w:p/>")
    return "".join(out)


def celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def markdown_para_corpo(texto):
    blocos, linhas = [], texto.split("\n")
    i = 0
    while i < len(linhas):
        linha = linhas[i].rstrip()

        if not linha.strip():
            i += 1
            continue

        if linha.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                if not re.fullmatch(r"\|[\s:|-]+\|", linhas[i].strip()):
                    bloco.append(celulas(linhas[i]))
                i += 1
            blocos.append(tabela(bloco))
            continue

        if m := re.match(r"^(#{1,3})\s+(.*)$", linha):
            nivel = len(m.group(1))
            tamanho, negrito = NIVEIS[nivel]
            blocos.append(paragrafo(m.group(2), tamanho, negrito, espaco_antes=240))
        elif m := re.match(r"^[-*]\s+(.*)$", linha):
            blocos.append(paragrafo(m.group(1), bullet=True))
        else:
            blocos.append(paragrafo(linha))
        i += 1

    return "".join(blocos)


def escrever_docx(markdown, destino):
    corpo = markdown_para_corpo(markdown)
    documento = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f"<w:document {W}><w:body>{corpo}"
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>'
        "</w:sectPr></w:body></w:document>"
    )
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", documento)


def main():
    parser = argparse.ArgumentParser(description="Converte Markdown em .docx (stdlib).")
    parser.add_argument("markdown", help="arquivo .md de entrada")
    parser.add_argument("-o", "--output", required=True, help="arquivo .docx de saida")
    args = parser.parse_args()

    try:
        texto = open(args.markdown, encoding="utf-8").read()
    except FileNotFoundError:
        sys.exit(f"erro: arquivo nao encontrado: '{args.markdown}'")

    escrever_docx(texto, args.output)
    print(f"gerado: {args.output}")


if __name__ == "__main__":
    main()
