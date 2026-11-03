// Mapa de campos por site. Cada campo tem alternativas tentadas em ordem:
//   {css}            seletor CSS (só atributos estáveis)
//   {rotulo}         texto (regex) do <label>, aria-label ou placeholder do campo
//   {botao}          texto (regex) de um botão
// Estes são PONTOS DE PARTIDA. Use "Calibrar" no painel para gravar o seletor real
// da sua tela: o seletor calibrado é salvo no navegador e passa a ter prioridade.
export const SITES = {
  whatsapp: {
    nome: "Catálogo do WhatsApp Business",
    hosts: ["web.whatsapp.com"],
    campos: {
      imagem: [{ css: "input[type=file][accept*='image']" }, { css: "input[type=file]" }],
      nome: [{ rotulo: "nome do (item|produto)" }],
      preco: [{ rotulo: "preço" }],
      descricao: [{ rotulo: "descrição" }],
      link: [{ rotulo: "link" }],
      codigo: [{ rotulo: "código" }],
      salvar: [{ botao: "^(adicionar ao catálogo|salvar|adicionar)$" }],
    },
  },
  eduzz: {
    nome: "Eduzz (novo produto)",
    hosts: ["eduzz.com"],
    campos: {
      nome: [{ rotulo: "nome do produto" }, { rotulo: "^nome" }],
      descricao: [{ rotulo: "descrição" }],
      preco: [{ rotulo: "(preço|valor)" }],
      imagem: [{ css: "input[type=file][accept*='image']" }],
      salvar: [{ botao: "^(salvar|publicar|criar produto|concluir)" }],
    },
  },
  meta: {
    nome: "Catálogo da Meta (Gerenciador de Comércio)",
    hosts: ["business.facebook.com"],
    campos: {
      imagem: [{ css: "input[type=file][accept*='image']" }, { css: "input[type=file]" }],
      nome: [{ rotulo: "^(título|nome)" }],
      descricao: [{ rotulo: "descrição" }],
      link: [{ rotulo: "(link do site|site|url)" }],
      preco: [{ rotulo: "^preço" }],
      codigo: [{ rotulo: "(id do conteúdo|sku|código)" }],
      salvar: [{ botao: "^(adicionar item|salvar|concluir)" }],
    },
  },
};

// Que valor de cada campo vem do produto (automacao/produtos.json).
export function valores(p, site) {
  return {
    nome: site === "eduzz" ? p.nome : p.titulo_catalogo,
    preco: p.preco.toFixed(2).replace(".", ","),
    descricao: p.descricao,
    link: p.checkout || p.link_loja,
    codigo: p.slug,
  };
}

export function siteDaUrl(url) {
  try {
    const host = new URL(url).hostname;
    return Object.keys(SITES).find((k) => SITES[k].hosts.some((h) => host === h || host.endsWith("." + h))) || null;
  } catch {
    return null;
  }
}
