// Funções injetadas na aba do site com chrome.scripting.executeScript({ func, args }).
// Precisam ser autocontidas (não podem usar nada de fora do próprio corpo).

// Preenche os campos e destaca o botão final. NUNCA clica em salvar.
export function preencherNaPagina(mapa, valores, imagem) {
  const norm = (s) => (s || "").replace(/\s+/g, " ").trim();
  const casa = (txt, re) => new RegExp(re, "i").test(norm(txt));
  const visivel = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  const campos = () => [...document.querySelectorAll("input, textarea, [contenteditable=true], [role=textbox]")];

  function porRotulo(re) {
    for (const el of campos()) {
      if (!visivel(el) && el.type !== "file") continue;
      const lbl = el.labels && el.labels[0] ? el.labels[0].innerText : "";
      const ref = el.getAttribute("aria-labelledby");
      const refTxt = ref ? ref.split(" ").map((id) => document.getElementById(id)?.innerText || "").join(" ") : "";
      for (const t of [lbl, refTxt, el.getAttribute("aria-label"), el.getAttribute("placeholder"), el.getAttribute("title")]) {
        if (t && casa(t, re)) return el;
      }
    }
    return null;
  }
  function porBotao(re) {
    return [...document.querySelectorAll("button, [role=button], input[type=submit]")]
      .find((b) => visivel(b) && (casa(b.innerText || b.value, re) || casa(b.getAttribute("aria-label"), re))) || null;
  }
  function achar(alts) {
    for (const a of alts || []) {
      try {
        const el = a.css ? document.querySelector(a.css) : a.rotulo ? porRotulo(a.rotulo) : a.botao ? porBotao(a.botao) : null;
        if (el) return el;
      } catch { /* seletor inválido: tenta o próximo */ }
    }
    return null;
  }
  function escrever(el, texto) {
    el.focus();
    if (el.isContentEditable || el.getAttribute("role") === "textbox") {
      document.execCommand("selectAll", false);
      document.execCommand("insertText", false, texto);
    } else {
      const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      Object.getOwnPropertyDescriptor(proto, "value").set.call(el, texto); // funciona com React
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }
    el.style.outline = "3px solid #1f9d57";
  }

  const rel = [];
  for (const [campo, valor] of Object.entries(valores)) {
    const el = achar(mapa[campo]);
    if (!el) { rel.push(`✗ ${campo}: não encontrado (calibre)`); continue; }
    escrever(el, valor);
    rel.push(`✓ ${campo}`);
  }
  if (imagem && mapa.imagem) {
    const el = achar(mapa.imagem);
    if (!el || el.type !== "file") rel.push("✗ imagem: campo de arquivo não encontrado (clique em 'adicionar foto' e tente de novo)");
    else {
      const [cab, b64] = imagem.dataUrl.split(",");
      const bin = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
      const dt = new DataTransfer();
      dt.items.add(new File([bin], imagem.nome, { type: cab.match(/:(.*?);/)[1] }));
      el.files = dt.files;
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
      rel.push("✓ imagem");
    }
  }
  const salvar = achar(mapa.salvar);
  if (salvar) {
    salvar.style.outline = "4px solid #c0392b";
    salvar.style.outlineOffset = "3px";
    salvar.scrollIntoView({ block: "center" });
    rel.push("→ confira tudo e clique você mesmo no botão destacado em vermelho");
  } else rel.push("? botão final não identificado");
  return rel;
}

// Modo calibrar: o usuário clica num elemento e devolvemos um seletor CSS estável.
export function capturarNaPagina() {
  return new Promise((resolve) => {
    const aleatorio = (s) => /\d{3,}|[a-z]\d[a-z]\d|^[a-z0-9]{6,}$|_/i.test(s);
    const esc = (s) => CSS.escape(s);
    function seletor(el) {
      if (el.id && !aleatorio(el.id)) return `#${esc(el.id)}`;
      for (const at of ["data-testid", "name", "aria-label", "placeholder", "title"]) {
        const v = el.getAttribute(at);
        if (v) {
          const s = `${el.tagName.toLowerCase()}[${at}="${v.replace(/"/g, '\\"')}"]`;
          if (document.querySelectorAll(s).length === 1) return s;
        }
      }
      if (el.type === "file") return `input[type=file]${el.accept ? `[accept="${el.accept}"]` : ""}`;
      const partes = [];
      for (let n = el; n && n.nodeType === 1 && n !== document.body; n = n.parentElement) {
        let p = n.tagName.toLowerCase();
        const irmaos = [...(n.parentElement?.children || [])].filter((x) => x.tagName === n.tagName);
        if (irmaos.length > 1) p += `:nth-of-type(${irmaos.indexOf(n) + 1})`;
        partes.unshift(p);
        if (document.querySelectorAll(partes.join(" > ")).length === 1) break;
      }
      return partes.join(" > ");
    }
    const aviso = Object.assign(document.createElement("div"), {
      textContent: "Postador: clique no campo que quer calibrar (Esc cancela)",
    });
    aviso.style.cssText = "position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:2147483647;background:#1B3A6B;color:#fff;padding:10px 16px;border-radius:10px;font:600 14px system-ui";
    document.body.append(aviso);
    let ultimo;
    const sobre = (e) => { if (ultimo) ultimo.style.outline = ""; ultimo = e.target; ultimo.style.outline = "3px dashed #C9A227"; };
    const fim = (valor) => {
      document.removeEventListener("mouseover", sobre, true);
      document.removeEventListener("click", clique, true);
      document.removeEventListener("keydown", tecla, true);
      if (ultimo) ultimo.style.outline = "";
      aviso.remove();
      resolve(valor);
    };
    const clique = (e) => {
      e.preventDefault(); e.stopPropagation();
      let el = e.target;
      // clicou no rótulo/caixa em volta? tenta achar o campo de dentro
      const dentro = el.querySelector?.("input, textarea, [contenteditable=true]");
      if (!/^(INPUT|TEXTAREA|BUTTON)$/.test(el.tagName) && !el.isContentEditable && dentro) el = dentro;
      fim(seletor(el));
    };
    const tecla = (e) => { if (e.key === "Escape") fim(null); };
    document.addEventListener("mouseover", sobre, true);
    document.addEventListener("click", clique, true);
    document.addEventListener("keydown", tecla, true);
  });
}
