import { SITES, valores, siteDaUrl } from "./seletores.js";
import { preencherNaPagina, capturarNaPagina } from "./pagina.js";

const $ = (s) => document.querySelector(s);
let PRODUTOS = [];
let atual = null;
const ROTULOS = { nome: "nome", preco: "preço", descricao: "descrição", link: "link", codigo: "código" };

async function abaAtual() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function calibrados() {
  const { calibrados = {} } = await chrome.storage.local.get("calibrados");
  return calibrados;
}

// Mapa final do site: seletor calibrado (se houver) na frente das alternativas padrão.
async function mapaDoSite(site) {
  const cal = (await calibrados())[site] || {};
  const mapa = {};
  for (const [campo, alts] of Object.entries(SITES[site].campos)) {
    mapa[campo] = cal[campo] ? [{ css: cal[campo] }, ...alts] : alts;
  }
  return mapa;
}

async function siteAtual() {
  const tab = await abaAtual();
  return { tab, site: tab ? siteDaUrl(tab.url) : null };
}

async function atualizarSite() {
  const { site } = await siteAtual();
  const el = $("#site");
  el.textContent = site ? SITES[site].nome : "site não suportado";
  el.classList.toggle("on", !!site);
  $("#campoCal").innerHTML = site
    ? Object.keys(SITES[site].campos).map((c) => `<option>${c}</option>`).join("")
    : "";
  await mostrarCalibrados();
}

function renderLista() {
  const q = $("#busca").value.toLowerCase();
  const lista = PRODUTOS.filter((p) => !q || (p.nome + " " + p.grupo_nome + " " + p.slug).toLowerCase().includes(q));
  $("#lista").innerHTML = lista
    .map((p) => `<option value="${p.slug}">${p.status === "em_breve" ? "⏳ " : ""}${p.nome_curto} · ${p.grupo_nome}</option>`)
    .join("");
}

async function imagemDoProduto(p) {
  for (const url of [chrome.runtime.getURL(`capas/${p.slug}.jpg`), p.imagem_publica]) {
    if (!url) continue;
    try {
      const r = await fetch(url);
      if (!r.ok) continue;
      const blob = await r.blob();
      const dataUrl = await new Promise((ok, erro) => {
        const fr = new FileReader();
        fr.onload = () => ok(fr.result);
        fr.onerror = erro;
        fr.readAsDataURL(blob);
      });
      return { dataUrl, nome: `${p.slug}.jpg` };
    } catch { /* tenta a próxima fonte */ }
  }
  return null;
}

function campo(rotulo, valor) {
  const d = document.createElement("div");
  d.className = "campo";
  d.innerHTML = `<small><span></span><button>copiar</button></small><div></div>`;
  d.querySelector("span").textContent = rotulo;
  d.querySelector("div").textContent = valor;
  d.querySelector("button").addEventListener("click", async (e) => {
    await navigator.clipboard.writeText(valor);
    e.target.textContent = "copiado ✓";
    setTimeout(() => (e.target.textContent = "copiar"), 1200);
  });
  return d;
}

async function selecionar(slug) {
  atual = PRODUTOS.find((p) => p.slug === slug);
  if (!atual) return;
  $("#det").hidden = false;
  $("#nome").textContent = atual.nome;
  $("#meta").textContent = `${atual.grupo_nome} · ${atual.preco_texto} · ${atual.status === "publicado" ? "publicado na Eduzz" : "em breve (sem checkout)"}`;
  $("#capa").src = chrome.runtime.getURL(`capas/${atual.slug}.jpg`);
  $("#capa").onerror = () => { $("#capa").onerror = null; $("#capa").src = atual.imagem_publica || ""; };
  const { site } = await siteAtual();
  const v = valores(atual, site || "whatsapp");
  const box = $("#campos");
  box.replaceChildren(...Object.entries(v).map(([k, val]) => campo(ROTULOS[k] || k, val)));
  $("#log").replaceChildren();
}

function log(linhas) {
  $("#log").replaceChildren(...linhas.map((t) => Object.assign(document.createElement("li"), { textContent: t })));
}

async function preencher() {
  if (!atual) return;
  const { tab, site } = await siteAtual();
  if (!site) return log(["Abra o WhatsApp Web, a Eduzz ou o Gerenciador de Comércio nesta aba."]);
  log(["preenchendo…"]);
  try {
    const mapa = await mapaDoSite(site);
    const vals = valores(atual, site);
    for (const k of Object.keys(vals)) if (!mapa[k]) delete vals[k]; // só campos que o site tem
    const imagem = mapa.imagem ? await imagemDoProduto(atual) : null;
    const [res] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: preencherNaPagina,
      args: [mapa, vals, imagem],
    });
    log(res.result || ["sem resposta da página"]);
  } catch (e) {
    log(["erro: " + e.message]);
  }
}

async function calibrar() {
  const { tab, site } = await siteAtual();
  const nomeCampo = $("#campoCal").value;
  if (!site || !nomeCampo) return;
  try {
    const [res] = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: capturarNaPagina });
    if (!res.result) return;
    const cal = await calibrados();
    cal[site] = { ...(cal[site] || {}), [nomeCampo]: res.result };
    await chrome.storage.local.set({ calibrados: cal });
    await mostrarCalibrados();
  } catch (e) {
    log(["erro ao calibrar: " + e.message]);
  }
}

async function mostrarCalibrados() {
  const { site } = await siteAtual();
  const cal = site ? (await calibrados())[site] || {} : {};
  const itens = Object.entries(cal).map(([c, css]) => {
    const li = document.createElement("li");
    li.innerHTML = `<span><b></b>: <code></code></span><button>apagar</button>`;
    li.querySelector("b").textContent = c;
    li.querySelector("code").textContent = css;
    li.querySelector("button").addEventListener("click", async () => {
      const todos = await calibrados();
      delete todos[site][c];
      await chrome.storage.local.set({ calibrados: todos });
      await mostrarCalibrados();
    });
    return li;
  });
  $("#calibrados").replaceChildren(...itens);
}

async function exportar() {
  const cal = await calibrados();
  await navigator.clipboard.writeText(JSON.stringify(cal, null, 2));
  $("#exportar").textContent = "copiado ✓ (cole no OpenCode)";
}

async function iniciar() {
  try {
    PRODUTOS = await (await fetch(chrome.runtime.getURL("produtos.json"))).json();
  } catch {
    log(["produtos.json não encontrado. Rode: python automacao/catalogo.py"]);
  }
  renderLista();
  $("#busca").addEventListener("input", renderLista);
  $("#lista").addEventListener("change", (e) => selecionar(e.target.value));
  $("#preencher").addEventListener("click", preencher);
  $("#calibrar").addEventListener("click", calibrar);
  $("#exportar").addEventListener("click", exportar);
  chrome.tabs.onActivated.addListener(atualizarSite);
  chrome.tabs.onUpdated.addListener((_id, info) => { if (info.url || info.status === "complete") atualizarSite(); });
  await atualizarSite();
}

iniciar();
