# Receita: adicionar 1 produto ao CATÁLOGO do WhatsApp Business pelo WhatsApp Web.
#
#   python automacao/receitas/whatsapp_catalogo.py matematica              (ensaio: preenche e para)
#   python automacao/receitas/whatsapp_catalogo.py matematica --confirmar  (salva o item)
#
# Antes: python automacao/navegador.py login whatsapp   (ler o QR code uma vez)
#
# ATENÇÃO: os SELETORES abaixo são o ponto de partida (textos que o WhatsApp costuma
# usar em português). Eles PRECISAM ser calibrados na sua tela antes do primeiro
# --confirmar. O agente faz isso com o Playwright MCP (veja automacao/PROTOCOLO.md).
#
# Alternativa oficial e mais estável para cadastrar MUITOS itens de uma vez:
# automacao/feed-meta.csv no Gerenciador de Comércio da Meta (ver automacao/README.md).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navegador import abrir, achar, args_padrao, caminho, exigir_calibrado, produto, Registro, SITES

VERIFICADO = False  # mude para True depois de calibrar e ver um ensaio dar certo

SELETORES = {
    # caminho até o formulário
    "menu":            [{"role": "button", "name": "re:^(Menu|Mais opções)$"}, {"css": "[data-icon='menu']"}],
    "ferramentas":     [{"role": "button", "name": "re:Ferramentas (comerciais|para empresas)"},
                        {"text": "re:Ferramentas (comerciais|para empresas)"}],
    "catalogo":        [{"role": "button", "name": "re:^Catálogo"}, {"text": "re:^Catálogo$"}],
    "novo_item":       [{"role": "button", "name": "re:Adicionar (novo )?(item|produto)"},
                        {"text": "re:Adicionar (novo )?(item|produto)"}],
    # campos
    "imagem":          [{"css": "input[type=file][accept*='image']"}, {"css": "input[type=file]"}],
    "nome":            [{"label": "re:Nome do (item|produto)"}, {"placeholder": "re:Nome do (item|produto)"}],
    "preco":           [{"label": "re:Preço"}, {"placeholder": "re:Preço"}],
    "descricao":       [{"label": "re:Descrição"}, {"placeholder": "re:Descrição"}],
    "link":            [{"label": "re:Link"}, {"placeholder": "re:Link"}],
    "codigo":          [{"label": "re:Código do (item|produto)"}, {"placeholder": "re:Código"}],
    # botão final (só clicado com --confirmar)
    "salvar":          [{"role": "button", "name": "re:^(Adicionar ao catálogo|Salvar|Adicionar)$"}],
}


def main():
    a = args_padrao("Adiciona um produto ao catálogo do WhatsApp Business")
    exigir_calibrado(VERIFICADO, a.confirmar, "whatsapp_catalogo")
    p = produto(a.slug)
    if p["status"] != "publicado":
        sys.exit(f"{a.slug} está 'em breve' (sem checkout na Eduzz). Publique na Eduzz primeiro.")
    from playwright.sync_api import sync_playwright
    reg = Registro("whatsapp", a.slug)
    with sync_playwright() as pw:
        ctx, pg = abrir("whatsapp", pw, a.headless)
        pg.goto(SITES["whatsapp"])
        achar(pg, SELETORES["menu"], timeout=60000)  # espera o WhatsApp carregar (login salvo)
        reg.passo(pg, "whatsapp-aberto")
        for etapa in ("menu", "ferramentas", "catalogo", "novo_item"):
            achar(pg, SELETORES[etapa]).click()
            pg.wait_for_timeout(800)
            reg.passo(pg, etapa)

        imagens = [caminho(p["capa"])] + [caminho(i) for i in p["imagens"][:3]]
        achar(pg, SELETORES["imagem"]).set_input_files([i for i in imagens if i and os.path.exists(i)])
        achar(pg, SELETORES["nome"]).fill(p["titulo_catalogo"])
        achar(pg, SELETORES["preco"]).fill(f"{p['preco']:.2f}".replace(".", ","))
        achar(pg, SELETORES["descricao"]).fill(p["descricao"])
        achar(pg, SELETORES["link"]).fill(p["checkout"])
        try:
            achar(pg, SELETORES["codigo"], timeout=2000).fill(p["slug"])
        except RuntimeError:
            print("(campo 'código do item' não encontrado — seguindo sem ele)")
        reg.passo(pg, "formulario-preenchido")

        botao = achar(pg, SELETORES["salvar"])
        if a.confirmar:
            botao.click()
            pg.wait_for_timeout(3000)
            reg.passo(pg, "salvo")
            print(f"OK: '{p['titulo_catalogo']}' adicionado ao catálogo.")
        else:
            botao.highlight()
            reg.passo(pg, "ensaio-parado-antes-de-salvar")
            print("ENSAIO: nada foi salvo. Confira os prints em", reg.pasta)
        ctx.close()


if __name__ == "__main__":
    main()
