# Receita: cadastrar 1 produto digital (PDF) na EDUZZ.
#
#   python automacao/receitas/eduzz_produto.py quimica --pdf "C:/Apostilas/quimica.pdf"
#   python automacao/receitas/eduzz_produto.py quimica --pdf ... --confirmar
#
# Antes: python automacao/navegador.py login eduzz
#
# ATENÇÃO: a Eduzz muda o painel com frequência. Os SELETORES abaixo são o ponto de
# partida e PRECISAM ser calibrados (veja automacao/PROTOCOLO.md). A URL de criação
# também pode mudar: confirme com o Playwright MCP e ajuste URL_NOVO_PRODUTO.
#
# Depois de publicado: copie o código do checkout (chk.eduzz.com/XXXX) para a linha do
# produto em loja/build_loja.py, rode build_loja.py e automacao/catalogo.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navegador import abrir, achar, args_padrao, caminho, exigir_calibrado, produto, Registro, SITES

VERIFICADO = False
URL_NOVO_PRODUTO = SITES["eduzz"]  # calibrar: página que abre o formulário de novo produto

SELETORES = {
    "novo_produto": [{"role": "button", "name": "re:(Novo|Criar|Cadastrar) produto"},
                     {"role": "link", "name": "re:(Novo|Criar|Cadastrar) produto"}],
    "tipo_digital": [{"text": "re:(E-?book|Arquivo|Produto digital|PDF)"}],
    "nome":         [{"label": "re:Nome do produto"}, {"placeholder": "re:Nome do produto"}],
    "descricao":    [{"label": "re:Descrição"}, {"placeholder": "re:Descrição"}],
    "preco":        [{"label": "re:(Preço|Valor)"}, {"placeholder": "re:(Preço|Valor)"}],
    "capa":         [{"css": "input[type=file][accept*='image']"}],
    "arquivo":      [{"css": "input[type=file][accept*='pdf']"}, {"css": "input[type=file]:not([accept*='image'])"}],
    "salvar":       [{"role": "button", "name": "re:^(Salvar|Publicar|Criar produto|Concluir)"}],
}


def main():
    a = args_padrao("Cadastra um produto digital na Eduzz",
                    [("--pdf", {"help": "caminho do PDF que o comprador vai receber"})])
    exigir_calibrado(VERIFICADO, a.confirmar, "eduzz_produto")
    p = produto(a.slug)
    if p["status"] == "publicado" and a.confirmar:
        sys.exit(f"{a.slug} já tem checkout na Eduzz ({p['checkout']}). Não vou duplicar.")
    from playwright.sync_api import sync_playwright
    reg = Registro("eduzz", a.slug)
    with sync_playwright() as pw:
        ctx, pg = abrir("eduzz", pw, a.headless)
        pg.goto(URL_NOVO_PRODUTO)
        pg.wait_for_load_state("networkidle")
        reg.passo(pg, "painel")
        if "login" in pg.url:
            sys.exit("Não está logado. Rode: python automacao/navegador.py login eduzz")

        achar(pg, SELETORES["novo_produto"], timeout=20000).click()
        pg.wait_for_timeout(1000)
        try:
            achar(pg, SELETORES["tipo_digital"], timeout=3000).click()
        except RuntimeError:
            pass
        reg.passo(pg, "formulario")

        achar(pg, SELETORES["nome"]).fill(p["nome"])
        achar(pg, SELETORES["descricao"]).fill(p["descricao"])
        achar(pg, SELETORES["preco"]).fill(f"{p['preco']:.2f}".replace(".", ","))
        if p["capa"]:
            achar(pg, SELETORES["capa"]).set_input_files(caminho(p["capa"]))
        if a.pdf:
            achar(pg, SELETORES["arquivo"]).set_input_files(a.pdf)
        else:
            print("(sem --pdf: o arquivo de entrega terá de ser enviado à mão)")
        reg.passo(pg, "preenchido")

        botao = achar(pg, SELETORES["salvar"])
        if a.confirmar:
            botao.click()
            pg.wait_for_timeout(4000)
            reg.passo(pg, "salvo")
            print("OK: produto salvo. Pegue o código do checkout e atualize loja/build_loja.py.")
        else:
            botao.highlight()
            reg.passo(pg, "ensaio-parado-antes-de-salvar")
            print("ENSAIO: nada foi salvo. Confira os prints em", reg.pasta)
        ctx.close()


if __name__ == "__main__":
    main()
