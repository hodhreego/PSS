// Ferramentas do OpenCode para consultar o catálogo de produtos.
// Viram: catalogo_listar e catalogo_produto.
import { tool } from "@opencode-ai/plugin"
import { join } from "node:path"

const RAIZ = join(import.meta.dir, "..", "..")
const ARQ = join(RAIZ, "automacao", "produtos.json")

async function produtos(): Promise<any[]> {
  const f = Bun.file(ARQ)
  if (!(await f.exists())) throw new Error("automacao/produtos.json não existe. Rode: python automacao/catalogo.py")
  return f.json()
}

export const listar = tool({
  description: "Lista os produtos da loja (slug, nome, grupo, preço, status publicado/em_breve). Fonte: automacao/produtos.json",
  args: {
    grupo: tool.schema.string().optional().describe("filtra por grupo: pss, cisop, prefeitura, outros"),
  },
  async execute(args) {
    const lista = (await produtos()).filter((p) => !args.grupo || p.grupo === args.grupo)
    return lista.map((p) => `${p.slug} | ${p.nome} | ${p.grupo_nome} | ${p.preco_texto} | ${p.status}`).join("\n")
  },
})

export const produto = tool({
  description: "Mostra todos os dados de um produto (nome, descrição, preço, checkout Eduzz, capa, imagens) pelo slug",
  args: { slug: tool.schema.string().describe("slug do produto, ex.: matematica") },
  async execute(args) {
    const p = (await produtos()).find((x) => x.slug === args.slug)
    if (!p) return `Produto '${args.slug}' não encontrado. Use catalogo_listar.`
    return JSON.stringify(p, null, 1)
  },
})
