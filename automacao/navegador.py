# Motor comum das receitas de automação (Playwright + Python).
#
# - Usa um PERFIL PERSISTENTE (automacao/.perfil/<site>): você faz login uma vez
#   (QR code do WhatsApp, senha da Eduzz) e as próximas execuções já entram logadas.
# - Toda receita roda em modo ENSAIO por padrão: preenche tudo, tira print e PARA
#   antes do botão final. Só salva/publica de verdade com --confirmar.
# - Cada passo gera um print em automacao/registros/<data>/ para conferência.
#
# Login (rode no SEU terminal, não pelo agente, porque espera você fechar a janela):
#   python automacao/navegador.py login whatsapp
#   python automacao/navegador.py login eduzz
import datetime, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERFIS = os.path.join(RAIZ, "automacao", ".perfil")
REGISTROS = os.path.join(RAIZ, "automacao", "registros")
SITES = {
    "whatsapp": "https://web.whatsapp.com/",
    "eduzz": "https://orbita.eduzz.com/",
    "meta": "https://business.facebook.com/commerce/",
}


def produtos():
    return json.load(open(os.path.join(RAIZ, "automacao", "produtos.json"), encoding="utf-8"))


def produto(slug):
    for p in produtos():
        if p["slug"] == slug:
            return p
    sys.exit(f"Produto '{slug}' não existe em automacao/produtos.json. Rode: python automacao/catalogo.py")


def caminho(rel):
    return os.path.join(RAIZ, rel) if rel else None


def abrir(site, playwright, headless=False):
    """Abre o Chromium com o perfil do site. Retorna (contexto, página)."""
    os.makedirs(os.path.join(PERFIS, site), exist_ok=True)
    ctx = playwright.chromium.launch_persistent_context(
        os.path.join(PERFIS, site), headless=headless, viewport={"width": 1366, "height": 860},
        locale="pt-BR", slow_mo=120)
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    return ctx, pg


class Registro:
    """Prints numerados de cada passo, para o humano (e o agente) conferirem."""

    def __init__(self, receita, slug):
        hora = datetime.datetime.now().strftime("%Y-%m-%d/%H%M%S")
        self.pasta = os.path.join(REGISTROS, hora + f"-{receita}-{slug}")
        os.makedirs(self.pasta, exist_ok=True)
        self.n = 0

    def passo(self, pg, nome):
        self.n += 1
        arq = os.path.join(self.pasta, f"{self.n:02d}-{nome}.png")
        pg.screenshot(path=arq)
        print(f"[passo {self.n}] {nome} -> {os.path.relpath(arq, RAIZ)}")


def achar(pg, spec, timeout=8000):
    """Localiza um elemento a partir de uma lista de alternativas (a primeira que aparecer vence).

    Cada alternativa é um dict com UMA chave de estratégia:
      {"role": "button", "name": "Adicionar item"}   -> get_by_role (name aceita regex "re:...")
      {"label": "Nome do item"}                       -> get_by_label
      {"placeholder": "Preço"}                        -> get_by_placeholder
      {"text": "Catálogo"}                            -> get_by_text
      {"css": "input[type=file]"}                     -> seletor CSS
    """
    def nome(v):
        return re.compile(v[3:], re.I) if isinstance(v, str) and v.startswith("re:") else v

    erros = []
    for alt in spec:
        try:
            if "role" in alt:
                loc = pg.get_by_role(alt["role"], name=nome(alt.get("name")))
            elif "label" in alt:
                loc = pg.get_by_label(nome(alt["label"]))
            elif "placeholder" in alt:
                loc = pg.get_by_placeholder(nome(alt["placeholder"]))
            elif "text" in alt:
                loc = pg.get_by_text(nome(alt["text"]))
            else:
                loc = pg.locator(alt["css"])
            loc = loc.first
            loc.wait_for(state="attached", timeout=timeout // max(len(spec), 1))
            return loc
        except Exception as e:  # tenta a próxima alternativa
            erros.append(f"{alt}: {type(e).__name__}")
    raise RuntimeError("Elemento não encontrado. Tentativas:\n  " + "\n  ".join(erros) +
                       "\n=> Recalibre o seletor (veja automacao/PROTOCOLO.md, etapa 2).")


def args_padrao(descricao, extras=()):
    """extras: lista de (flag, kwargs) para argumentos próprios da receita."""
    import argparse
    ap = argparse.ArgumentParser(description=descricao)
    ap.add_argument("slug", help="slug do produto (veja automacao/produtos.json)")
    ap.add_argument("--confirmar", action="store_true",
                    help="clica no botão final (salvar/publicar). Sem isso é só ENSAIO.")
    ap.add_argument("--headless", action="store_true", help="sem janela (só depois de calibrado)")
    for flag, kw in extras:
        ap.add_argument(flag, **kw)
    return ap.parse_args()


def exigir_calibrado(verificado, confirmar, receita):
    if confirmar and not verificado:
        sys.exit(f"{receita}: os seletores ainda NÃO foram calibrados (VERIFICADO = False). "
                 "Rode em ensaio, confira os prints, ajuste SELETORES e marque VERIFICADO = True.")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "login" and sys.argv[2] in SITES:
        from playwright.sync_api import sync_playwright
        site = sys.argv[2]
        with sync_playwright() as p:
            ctx, pg = abrir(site, p)
            pg.goto(SITES[site])
            print(f"Faça o login em {site} na janela aberta. Quando terminar, FECHE a janela.")
            pg.wait_for_event("close", timeout=0)
            ctx.close()
        print("Perfil salvo em", os.path.relpath(os.path.join(PERFIS, site), RAIZ))
    else:
        print("uso: python automacao/navegador.py login {" + "|".join(SITES) + "}")
