---
description: Cadastra um produto digital (PDF) na Eduzz (ensaio primeiro)
agent: cowork
---
Cadastrar na Eduzz o produto: $ARGUMENTS

1. Confira o produto com `catalogo_produto`. Se ele já tiver `checkout`, avise que já está na Eduzz e pare.
2. Pergunte o caminho do PDF de entrega, se eu não tiver passado (`--pdf`).
3. Rode `cowork_rodar` com receita `eduzz_produto`, o slug, `extra: "--pdf <caminho>"` e `confirmar: false`.
4. Mostre os prints e pergunte se pode salvar. Só com o meu "sim", rode com `confirmar: true`.
5. Depois de salvo, me ajude a pegar o código do checkout (chk.eduzz.com/XXXX), coloque em `P` de `loja/build_loja.py`, rode `python loja/build_loja.py` e `python automacao/catalogo.py`.
