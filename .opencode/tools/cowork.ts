// Ferramenta do OpenCode que roda as receitas de automação com segurança.
// Vira: cowork_rodar. Sempre ensaio, a não ser que confirmar=true.
import { tool } from "@opencode-ai/plugin"
import { join } from "node:path"
import { readdirSync } from "node:fs"

const RAIZ = join(import.meta.dir, "..", "..")
const PY = process.platform === "win32" ? "python" : "python3"

// Ao criar uma receita nova (PROTOCOLO, etapa 5), adicione o nome do arquivo aqui.
const RECEITAS = ["whatsapp_catalogo", "eduzz_produto"] as const

function ultimosPrints(): string {
  try {
    const base = join(RAIZ, "automacao", "registros")
    const dia = readdirSync(base).sort().at(-1)!
    const exec = readdirSync(join(base, dia)).sort().at(-1)!
    const pasta = join(base, dia, exec)
    return readdirSync(pasta).sort().map((f) => join("automacao", "registros", dia, exec, f)).join("\n")
  } catch {
    return "(nenhum print encontrado)"
  }
}

export const rodar = tool({
  description:
    "Roda uma receita de automação de navegador para um produto. confirmar=false (padrão) = ENSAIO: preenche e para antes do botão final, tirando prints. " +
    "Só use confirmar=true depois que o usuário viu o ensaio e autorizou explicitamente nesta conversa.",
  args: {
    receita: tool.schema.enum(RECEITAS).describe("qual receita rodar"),
    slug: tool.schema.string().describe("slug do produto (veja catalogo_listar)"),
    confirmar: tool.schema.boolean().default(false).describe("true = clica no botão final de verdade"),
    extra: tool.schema.string().optional().describe('argumentos extras da receita, ex.: --pdf "C:/Apostilas/x.pdf"'),
  },
  async execute(args) {
    const script = join(RAIZ, "automacao", "receitas", `${args.receita}.py`)
    const extra = (args.extra?.match(/"[^"]*"|\S+/g) ?? []).map((s) => s.replace(/^"|"$/g, ""))
    const flags = args.confirmar ? ["--confirmar"] : []
    const r = await Bun.$`${PY} ${script} ${args.slug} ${flags} ${extra}`.cwd(RAIZ).nothrow().quiet()
    const saida = (r.stdout.toString() + "\n" + r.stderr.toString()).trim()
    return [
      `modo: ${args.confirmar ? "PUBLICAÇÃO" : "ENSAIO"} | código de saída: ${r.exitCode}`,
      saida.slice(-6000),
      "prints:",
      ultimosPrints(),
    ].join("\n")
  },
})
