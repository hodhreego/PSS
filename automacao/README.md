# Co-work automático: OpenCode + extensão do Chrome

Duas formas de fazer sozinho o que hoje é feito à mão (cadastrar produto na Eduzz,
no catálogo do WhatsApp, na Meta…). As duas usam **os mesmos dados**:
`automacao/produtos.json`, gerado a partir do catálogo da loja (`loja/build_loja.py`).

```
loja/build_loja.py ──► python automacao/catalogo.py ──► automacao/produtos.json ──► OpenCode (receitas)
                                                    ├─► automacao/feed-meta.csv  ──► Meta / WhatsApp (planilha)
                                                    └─► extensao-chrome/produtos.json ──► extensão "Postador"
```

Sempre que mudar algum produto em `loja/build_loja.py`, rode:

```
python automacao/catalogo.py --capas
```

---

## Caminho 1 — OpenCode faz tudo sozinho (com sua confirmação)

### Instalar (uma vez)

No PowerShell, dentro da pasta do projeto:

```
npm i -g opencode-ai
pip install playwright
python -m playwright install chromium
```

### Fazer login nos sites (uma vez por site)

```
python automacao/navegador.py login whatsapp   # leia o QR code e feche a janela
python automacao/navegador.py login eduzz      # entre com sua senha e feche a janela
```

O login fica guardado em `automacao/.perfil/` (essa pasta **não** vai para o GitHub).

### Usar

Abra o OpenCode na pasta do projeto (`opencode`) e aperte **Tab** até aparecer o agente
**cowork**. Comandos prontos:

| Digite | O que acontece |
|---|---|
| `/postar-whatsapp matematica` | ensaio no catálogo do WhatsApp → mostra prints → pergunta se pode salvar |
| `/postar-eduzz quimica --pdf "C:/Apostilas/quimica.pdf"` | ensaio na Eduzz → prints → pergunta se pode salvar |
| `/feed-meta` | gera a planilha para subir todos os produtos de uma vez na Meta |
| `/nova-ferramenta atualizar o preço de um produto na Eduzz` | o OpenCode **cria uma ferramenta nova** sozinho |

Ou só peça em português: *"coloca todas as apostilas do CISOP no catálogo do WhatsApp"*.

### Primeira vez de cada receita: calibrar

As receitas vêm com seletores "prováveis" (`VERIFICADO = False`). Na primeira vez o
OpenCode abre o site pelo MCP **navegador**, olha a tela, ajusta os seletores, roda
um ensaio e te mostra os prints. Quando estiver certo, ele marca `VERIFICADO = True`.
Enquanto não estiver calibrada, a receita **se recusa** a salvar.

As regras que o OpenCode segue estão em `AGENTS.md` (raiz) e `automacao/PROTOCOLO.md`.
O protocolo é o "manual" que ensina ele a **criar as próprias ferramentas**.

### Usar o SEU Chrome em vez de um navegador separado (opcional)

1. Feche o Chrome e abra assim (Chrome exige uma pasta de perfil separada):
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\chrome-cowork
   ```
2. Em `opencode.json`, troque `"enabled": false` para `true` no servidor `chrome-real`.

---

## Caminho 2 — Extensão do Chrome "Postador" (você no controle)

Para quando você mesmo quer cadastrar, mas sem digitar nada.

### Instalar

1. `python automacao/catalogo.py --capas`
2. Chrome → `chrome://extensions` → ligue **Modo do desenvolvedor**
3. **Carregar sem compactação** → escolha a pasta `extensao-chrome`
4. Fixe o ícone da extensão na barra.

### Usar

1. Abra o WhatsApp Web, a Eduzz ou o Gerenciador de Comércio da Meta e abra o formulário
   de **novo item/produto**.
2. Clique no ícone do Postador → abre o painel lateral.
3. Escolha o produto → **Preencher nesta aba**.
4. Ele preenche nome, preço, descrição, link e foto, e **destaca em vermelho** o botão
   final. Confira e clique você.

Cada campo também tem um botão **copiar**, para colar à mão se precisar.

### Se um campo não for preenchido

Abra **Calibrar campos deste site**, escolha o campo, clique em **Calibrar** e depois
clique no campo na página. Pronto: fica gravado. O botão **Copiar calibragem** gera um
texto para colar no OpenCode, que atualiza as receitas com os mesmos seletores.

---

## WhatsApp: o jeito oficial para muitos produtos de uma vez

1. `python automacao/catalogo.py` gera `automacao/feed-meta.csv`.
2. business.facebook.com → **Gerenciador de Comércio** → seu catálogo → **Fontes de dados**
   → **Planilha de dados** → envie o CSV.
3. No WhatsApp Business: **Ferramentas comerciais → Catálogo** → conectar ao catálogo da Meta
   (ou, no Gerenciador do WhatsApp, vincule o catálogo ao número).

As fotos da planilha precisam estar publicadas na internet: o CSV usa
`https://hodhreego.github.io/Loja/img/<produto>-1.jpg`, então publique a loja antes.

## Cuidados

- Nada é publicado sem você dizer "pode publicar". Todo ensaio deixa prints em `automacao/registros/`.
- Senhas e códigos de verificação: só você digita, na janela do navegador.
- Não use automação para disparar mensagens em massa no WhatsApp; isso pode bloquear o número.
