#!/usr/bin/env python3
"""Converte .docx em texto puro sem dependencias externas.

Um .docx e um zip contendo word/document.xml. Extraimos o texto de cada
paragrafo (<w:p>), preservando quebras de linha, e ignoramos toda a formatacao.

Uso:
    python docx_to_text.py "<caminho.docx>" [-o saida.txt]
    python docx_to_text.py "<caminho.docx>" --meta

Sem -o, escreve em stdout (UTF-8). Com --meta, imprime os metadados do pacote
(data de criacao) em vez do texto: e a fonte mais confiavel da data da reuniao,
porque o cabecalho em texto depende do fuso do gravador.

Nota: o .docx de transcricao do Teams NAO contem lista de presenca — so quem
falou. Quem participou em silencio precisa vir de outra fonte.
"""

import argparse
import re
import sys
import zipfile
from xml.etree import ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragraph_text(paragraph):
    """Concatena os runs de texto de um <w:p>, tratando tabs e quebras."""
    parts = []
    for node in paragraph.iter():
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag == f"{W}tab":
            parts.append("\t")
        elif node.tag == f"{W}br":
            parts.append("\n")
    return "".join(parts)


def docx_to_text(path):
    with zipfile.ZipFile(path) as archive:
        with archive.open("word/document.xml") as document:
            tree = ElementTree.parse(document)

    lines = [paragraph_text(p) for p in tree.getroot().iter(f"{W}p")]
    text = "\n".join(lines)
    # Colapsa sequencias de 3+ linhas vazias em 2 e remove espacos a direita.
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def docx_metadata(path):
    """Extrai data de criacao/modificacao de docProps/core.xml."""
    with zipfile.ZipFile(path) as archive:
        if "docProps/core.xml" not in archive.namelist():
            return {}
        raw = archive.read("docProps/core.xml").decode("utf-8", "replace")

    fields = ("created", "modified")
    return {
        f: m.group(1)
        for f in fields
        if (m := re.search(rf"<dcterms:{f}[^>]*>([^<]+)<", raw))
    }


def main():
    parser = argparse.ArgumentParser(description="Converte .docx em texto puro.")
    parser.add_argument("docx", help="caminho do arquivo .docx")
    parser.add_argument("-o", "--output", help="arquivo de saida (default: stdout)")
    parser.add_argument(
        "--meta",
        action="store_true",
        help="imprime metadados (data de criacao) em vez do texto",
    )
    args = parser.parse_args()

    if args.meta:
        for key, value in docx_metadata(args.docx).items():
            print(f"{key}: {value}")
        return

    try:
        text = docx_to_text(args.docx)
    except (zipfile.BadZipFile, KeyError):
        sys.exit(f"erro: '{args.docx}' nao e um .docx valido")
    except FileNotFoundError:
        sys.exit(f"erro: arquivo nao encontrado: '{args.docx}'")

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
