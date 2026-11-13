#!/usr/bin/env python3
"""Gera um QR code por aluno a partir de um CSV (colunas: nome,url).

Uso:  python3 gerar_qr_alunos.py alunos.csv [pasta_saida]
Requer: pip install segno pillow
Cada PNG leva o nome do aluno embaixo. Também gera folha.html para imprimir.
"""
import csv, io, re, sys, unicodedata
from html import escape
from pathlib import Path
import segno
from PIL import Image, ImageDraw, ImageFont

def slug(txt):
    t = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower() or "aluno"

def fonte(tam):
    for f in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            pass
    return ImageFont.load_default()

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    csv_path = Path(sys.argv[1])
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else csv_path.parent / "saida"
    saida.mkdir(parents=True, exist_ok=True)
    usados, itens = set(), []
    with open(csv_path, newline="", encoding="utf-8-sig") as fh:
        for n, lin in enumerate(csv.DictReader(fh), start=2):
            nome, url = (lin.get("nome") or "").strip(), (lin.get("url") or "").strip()
            if not nome or not url:
                print(f"linha {n}: ignorada (nome/url vazio)"); continue
            base = slug(nome); arq = base; i = 2
            while arq in usados:
                arq = f"{base}-{i}"; i += 1
            usados.add(arq)
            buf = io.BytesIO()
            segno.make(url, error="m").save(buf, kind="png", scale=10, border=3)
            qr = Image.open(buf).convert("RGB")
            f = fonte(34)
            img = Image.new("RGB", (qr.width, qr.height + 70), "white")
            img.paste(qr, (0, 0))
            d = ImageDraw.Draw(img)
            w = d.textlength(nome, font=f)
            d.text(((img.width - w) / 2, qr.height + 12), nome, fill="black", font=f)
            img.save(saida / f"{arq}.png")
            itens.append((nome, f"{arq}.png"))
    cards = "".join(f'<figure><img src="{a}"><figcaption>{escape(n)}</figcaption></figure>' for n, a in itens)
    (saida / "folha.html").write_text(
        "<!doctype html><meta charset=utf-8><title>QR alunos</title>"
        "<style>body{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:12px}"
        "figure{margin:0;width:6cm;text-align:center;break-inside:avoid}img{width:100%}</style>" + cards,
        encoding="utf-8")
    print(f"{len(itens)} QR(s) gerados em {saida}")

if __name__ == "__main__":
    main()
