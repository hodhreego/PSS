---
description: Adiciona um produto ao catálogo do WhatsApp Business (ensaio primeiro)
agent: cowork
---
Adicionar ao catálogo do WhatsApp Business o produto: $ARGUMENTS

1. Confira o produto com `catalogo_produto` (se não passei o slug, liste com `catalogo_listar` e pergunte qual).
2. Rode `cowork_rodar` com receita `whatsapp_catalogo`, o slug e `confirmar: false`.
3. Mostre os prints e o que foi preenchido. Pergunte se pode salvar.
4. Só com o meu "sim", rode de novo com `confirmar: true`.
