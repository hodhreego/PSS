# Protocolo: como o OpenCode cria e usa as próprias ferramentas de co-work

Uma "ferramenta de co-work" aqui é uma **tarefa repetitiva feita num site** (cadastrar
produto, atualizar preço, postar anúncio, responder pedido…) transformada em algo que
roda com um comando. Ela sempre tem 3 peças:

| Peça | Onde fica | Para que serve |
|---|---|---|
| **Receita** (script Playwright) | `automacao/receitas/<site>_<tarefa>.py` | faz a tarefa no navegador, com ensaio e prints |
| **Comando** | `.opencode/commands/<tarefa>.md` | o usuário digita `/<tarefa> <slug>` no OpenCode |
| **Ferramenta** (opcional) | `.opencode/tools/*.ts` | dá ao agente um botão seguro (ex.: `cowork_rodar`) em vez de bash livre |

Use `automacao/receitas/whatsapp_catalogo.py` como **modelo** de toda receita nova.

## Etapa 1 — Entender a tarefa
- Pergunte ao usuário: qual site, qual objetivo, quais dados entram, qual é o "botão final".
- Os dados de produto vêm de `automacao/produtos.json` (gerado por `automacao/catalogo.py`). Se faltar um campo, adicione-o em `catalogo.py`, não no script.

## Etapa 2 — Explorar e calibrar com o MCP `navegador` (Playwright MCP)
1. `browser_navigate` até o site. Se pedir login, peça ao usuário para logar **na janela aberta** e espere ele avisar.
2. Siga o caminho até o formulário usando `browser_snapshot` a cada tela (o snapshot mostra a árvore de acessibilidade: papéis, nomes, rótulos).
3. Para cada campo/botão anote o seletor **mais estável**, nesta preferência:
   1. `{"role": ..., "name": ...}` (papel + texto visível)
   2. `{"label": ...}` ou `{"placeholder": ...}`
   3. `{"css": ...}` só com atributos estáveis (`name`, `aria-label`, `data-testid`, `type`, `accept`). **Nunca** classes geradas (`.x1n2onr6`, `.css-1abc`).
4. Use `re:` para aceitar variações de texto: `"re:Adicionar (novo )?item"`.
5. Dê mais de uma alternativa por elemento (a lista é tentada em ordem).
6. **Não clique no botão final durante a exploração.**

## Etapa 3 — Escrever/ajustar a receita
- Copie o modelo, preencha `SELETORES`, mantenha `VERIFICADO = False`.
- Use só as funções de `automacao/navegador.py`: `abrir`, `achar`, `Registro.passo`, `args_padrao`, `exigir_calibrado`, `produto`.
- Um `reg.passo(pg, "nome")` depois de cada tela.
- O clique final fica dentro de `if a.confirmar:`; no ensaio use `botao.highlight()`.

## Etapa 4 — Ensaiar
- O usuário roda (ou autoriza rodar): `python automacao/receitas/<arquivo>.py <slug>`.
- Abra os prints de `automacao/registros/<data>/` e confira campo a campo com o usuário.
- Deu certo? Marque `VERIFICADO = True`. Falhou? Volte à Etapa 2 só no seletor que quebrou.

## Etapa 5 — Registrar
- Crie `.opencode/commands/<tarefa>.md` (copie `postar-whatsapp.md`).
- Adicione a receita na lista `RECEITAS` de `.opencode/tools/cowork.ts`.
- Atualize a tabela "Ferramentas prontas" abaixo e faça commit.

## Etapa 6 — Manutenção
Sites mudam. Quando uma receita quebrar: rode em ensaio, veja em qual passo parou
(o erro lista as alternativas tentadas), recalibre só aquele seletor, ensaie de novo.

## Quando NÃO automatizar pela tela
Prefira sempre o caminho oficial quando existir — é mais estável e não arrisca a conta:
- **WhatsApp (muitos itens):** catálogo da Meta via planilha `automacao/feed-meta.csv` (Gerenciador de Comércio → Catálogo → Fontes de dados → Planilha) e depois conectar o catálogo à conta do WhatsApp Business.
- **Eduzz:** verifique se a API oficial da Eduzz cobre a operação (consulta de vendas, por exemplo) antes de automatizar pela tela.
- Automatizar o WhatsApp Web em volume pode violar os termos do WhatsApp. Use receitas para tarefas pontuais, em ritmo humano, nunca para disparo em massa de mensagens.

## Ferramentas prontas

| Comando | Receita | Calibrada? |
|---|---|---|
| `/postar-whatsapp <slug>` | `receitas/whatsapp_catalogo.py` | não |
| `/postar-eduzz <slug> [--pdf caminho]` | `receitas/eduzz_produto.py` | não |
| `/feed-meta` | `catalogo.py` (gera `feed-meta.csv`) | sim |
| `/nova-ferramenta <descrição>` | cria uma nova seguindo este protocolo | — |
