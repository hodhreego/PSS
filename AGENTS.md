# PSS — Loja de Matemática (Prof. Rodrigo)

Responda sempre em **português do Brasil**. O dono do projeto não é programador:
explique o que vai fazer em frases curtas e peça confirmação antes de qualquer ação
que publique, venda, envie mensagem ou gaste dinheiro.

## O que é este repositório

- `index.html`, `apostilas.html`, `provas-anteriores-pss-seed-pr.html` — páginas do PSS SEED-PR.
- `loja/` — a loja publicada em https://hodhreego.github.io/Loja/
  - `loja/build_loja.py` — **catálogo oficial** (lista `P`: slug, nome, grupo, código do checkout Eduzz, preço, subtítulo). Gera `loja/index.html`.
  - `loja/gen_capas_eduzz.py` — gera as capas quadradas 1000×1000 em `loja/capas-eduzz/`.
  - `loja/render_thumbs.py`, `loja/img/` — páginas de amostra (capa, índice, miolo).
  - `loja/anuncios/` — imagens e textos de anúncio para redes sociais.
- `automacao/` — **ferramentas de co-work** (automação de navegador). Leia `automacao/PROTOCOLO.md`.
- `extensao-chrome/` — extensão "Postador" que preenche formulários no Chrome do próprio usuário.

## Fluxo de um produto novo (ordem certa)

1. Adicionar a linha em `P` de `loja/build_loja.py` (código `None` enquanto não houver checkout) e em `I` de `loja/gen_capas_eduzz.py`.
2. `python loja/gen_capas_eduzz.py <slug>` → capa quadrada.
3. `python automacao/catalogo.py` → atualiza `automacao/produtos.json` e o feed da Meta.
4. Cadastrar na **Eduzz** (comando `/postar-eduzz <slug>`), pegar o código do checkout e colocar em `P`.
5. `python loja/build_loja.py` e `python automacao/catalogo.py` de novo.
6. Cadastrar no **catálogo do WhatsApp** (comando `/postar-whatsapp <slug>`).
7. Commit com mensagem curta em português, no estilo do histórico (`git log --oneline`).

## Regras de ouro da automação

- **Nunca** clique em Salvar/Publicar/Enviar/Pagar sem o usuário dizer "pode publicar" naquela conversa.
- Toda receita roda primeiro em **ensaio** (sem `--confirmar`), mostre os prints de `automacao/registros/` e só então peça autorização.
- Senhas, tokens e códigos de verificação: **nunca** escreva em arquivo, commit ou log. O login é feito pelo próprio usuário na janela do navegador.
- Não use o mesmo perfil de navegador em dois lugares ao mesmo tempo (o MCP usa `automacao/.perfil/mcp`; as receitas usam `automacao/.perfil/<site>`).
- Os dados dos produtos vêm **só** de `automacao/produtos.json`. Não invente preço, nome ou link.
- Se um seletor falhar, não "chute" cliques: pare, tire um snapshot com o MCP `navegador` e recalibre (PROTOCOLO, etapa 2).

## Ambiente

- Windows (há `desktop.ini` nas pastas). Use `python` (não `python3`) e caminhos com `/`.
- Dependências: `pip install playwright` e `python -m playwright install chromium`; Node.js para os MCPs (`npx`).
