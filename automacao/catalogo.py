# Fonte única dos produtos para as automações (OpenCode, scripts e extensão do Chrome).
# Lê o catálogo de loja/build_loja.py (sem executá-lo) e gera:
#   automacao/produtos.json          -> usado pelas receitas e pelas ferramentas do OpenCode
#   automacao/feed-meta.csv          -> planilha para o Gerenciador de Comércio da Meta (catálogo do WhatsApp)
#   extensao-chrome/produtos.json    -> cópia para a extensão do Chrome
#   extensao-chrome/capas/<slug>.jpg -> cópia das capas quadradas (só com --capas)
#
# Uso:  python automacao/catalogo.py            (gera tudo)
#       python automacao/catalogo.py --capas    (também copia as capas para a extensão)
import ast, csv, json, os, shutil, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOJA_DIR = os.path.join(RAIZ, "loja")
LOJA_URL = "https://hodhreego.github.io/Loja/"
IMG_URL = LOJA_URL + "img/"          # imagens públicas usadas no feed da Meta
CHK = "https://chk.eduzz.com/"
WHATSAPP = "(45) 99969-9444"


def ler_literais(caminho, nomes):
    """Pega variáveis literais (listas, dicts, sets) de um .py sem executar o arquivo."""
    arvore = ast.parse(open(caminho, encoding="utf-8").read())
    achados = {}
    for no in arvore.body:
        if isinstance(no, ast.Assign) and len(no.targets) == 1 and isinstance(no.targets[0], ast.Name):
            nome = no.targets[0].id
            if nome in nomes:
                achados[nome] = ast.literal_eval(no.value)
    faltam = set(nomes) - set(achados)
    if faltam:
        sys.exit(f"Não achei {faltam} em {caminho}. O formato do catálogo mudou?")
    return achados


def descricao_longa(nome, sub, paginas):
    linhas = [nome, sub]
    if paginas:
        linhas.append(f"{paginas} páginas em PDF.")
    linhas += [
        "Material digital em PDF: leia no celular, tablet ou computador.",
        "Entrega imediata após o pagamento.",
        f"Veja capa, índice e páginas internas antes de comprar: {LOJA_URL}",
        f"Dúvidas no WhatsApp: {WHATSAPP}",
    ]
    return "\n".join(linhas)


def montar():
    lit = ler_literais(os.path.join(LOJA_DIR, "build_loja.py"), {"P", "GRUPOS", "SEM_SIMULADO"})
    paginas = json.load(open(os.path.join(LOJA_DIR, "img", "_paginas.json"), encoding="utf-8"))
    produtos = []
    for slug, curto, grupo, codigo, preco, sub in lit["P"]:
        nome = curto if slug in lit["SEM_SIMULADO"] else "Apostila + Simulados: " + curto
        capa = f"loja/capas-eduzz/{slug}.jpg"
        imgs = [f"loja/img/{slug}-{k}.jpg" for k in range(1, 5)
                if os.path.exists(os.path.join(LOJA_DIR, "img", f"{slug}-{k}.jpg"))]
        pag = paginas.get(slug, {}).get("paginas")
        produtos.append({
            "slug": slug,
            "nome": nome,
            "nome_curto": curto,
            "grupo": grupo,
            "grupo_nome": lit["GRUPOS"][grupo],
            "titulo_catalogo": f"{nome} · {lit['GRUPOS'][grupo]}"[:100],
            "preco": preco,
            "preco_texto": f"R$ {preco:.2f}".replace(".", ","),
            "resumo": sub,
            "descricao": descricao_longa(nome, sub, pag),
            "status": "publicado" if codigo else "em_breve",
            "eduzz_codigo": codigo,
            "checkout": (CHK + codigo) if codigo else None,
            "link_loja": LOJA_URL,
            "capa": capa if os.path.exists(os.path.join(RAIZ, capa)) else None,
            "imagens": imgs,
            "imagem_publica": (IMG_URL + f"{slug}-1.jpg") if imgs else None,
            "paginas": pag,
        })
    return produtos


def salvar_feed_meta(produtos, caminho):
    """CSV no formato de feed de dados da Meta (Gerenciador de Comércio -> catálogo -> fontes de dados)."""
    cols = ["id", "title", "description", "availability", "condition", "price", "link", "image_link", "brand"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in produtos:
            if p["status"] != "publicado" or not p["imagem_publica"]:
                continue
            w.writerow({
                "id": p["slug"],
                "title": p["titulo_catalogo"][:150],
                "description": p["descricao"][:5000],
                "availability": "in stock",
                "condition": "new",
                "price": f"{p['preco']:.2f} BRL",
                "link": p["checkout"],
                "image_link": p["imagem_publica"],
                "brand": "Loja de Matemática",
            })


if __name__ == "__main__":
    produtos = montar()
    txt = json.dumps(produtos, ensure_ascii=False, indent=1)
    open(os.path.join(RAIZ, "automacao", "produtos.json"), "w", encoding="utf-8").write(txt + "\n")
    ext = os.path.join(RAIZ, "extensao-chrome")
    if os.path.isdir(ext):
        open(os.path.join(ext, "produtos.json"), "w", encoding="utf-8").write(txt + "\n")
        if "--capas" in sys.argv:
            os.makedirs(os.path.join(ext, "capas"), exist_ok=True)
            for p in produtos:
                if p["capa"]:
                    shutil.copy(os.path.join(RAIZ, p["capa"]), os.path.join(ext, "capas", p["slug"] + ".jpg"))
    salvar_feed_meta(produtos, os.path.join(RAIZ, "automacao", "feed-meta.csv"))
    pub = sum(p["status"] == "publicado" for p in produtos)
    print(f"ok: {len(produtos)} produtos ({pub} publicados) -> automacao/produtos.json, automacao/feed-meta.csv")
