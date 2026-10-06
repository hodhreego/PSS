# Gera loja/index.html a partir do catálogo abaixo (preços/links = produtos já publicados no Eduzz).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
pag = json.load(open(os.path.join(HERE, "img", "_paginas.json"), encoding="utf-8"))
CHK = "https://chk.eduzz.com/"
WA = "https://wa.me/5545999699444?text="

# slug, título curto, grupo, eduzz código checkout (None = em breve), preço, subtítulo, imagens(4 ou 2)
P = [
 ("matematica", "Matemática", "pss", "xsjteswd", 20, "Conteúdo específico do cargo de Professor de Matemática."),
 ("conhecimentos-basicos", "Conhecimentos Básicos", "pss", "yoeghnxb", 10, "Para todos os cargos do PSS: base comum cobrada na prova."),
 ("pedagogo", "Pedagogo", "pss", "w6tud6n2", 20, "Conteúdo específico do cargo de Pedagogo."),
 ("educacao-especial", "Educação Especial / Inclusiva", "pss", "466hxqqa", 20, "Educação inclusiva e atendimento educacional especializado."),
 ("lingua-inglesa", "Língua Inglesa", "pss", "rfeeo7ig", 20, "Versão normal e versão JUMBO (letra grande)."),
 ("geografia", "Geografia", "pss", "ktkzb34d", 20, "Conteúdo específico do cargo de Professor de Geografia."),
 ("historia", "História", "pss", "xi3bwjtm", 20, "Conteúdo específico do cargo de Professor de História."),
 ("artes", "Artes", "pss", "tgbaqcig", 20, "Conteúdo específico do cargo de Professor de Artes."),
 ("gestao-negocios", "Administração, Gestão e Negócios", "pss", "lbgwlvz3", 20, "Conteúdo do eixo Gestão e Negócios."),
 ("lingua-portuguesa", "Língua Portuguesa", "pss", "ndhizctf", 20, "Conteúdo específico do cargo de Professor de Língua Portuguesa."),
 ("educacao-fisica", "Educação Física", "pss", "zsa3iutj", 20, "Conteúdo específico do cargo de Professor de Educação Física."),
 ("quimica", "Química", "pss", "jg3vxafi", 20, "Conteúdo específico do cargo de Professor de Química."),
 ("informacao-comunicacao", "Informação e Comunicação", "pss", None, 20, "Eixo Informação e Comunicação."),
 ("simulado-matematica", "Simulado de Matemática", "simulado", "linutiqk", 10, "Questões para treinar com o estilo da prova."),
 ("pedagogo-abaetetuba", "Pedagogo · Abaetetuba-PA", "outros", "x3khho43", 20, "Apostila completa para a Prefeitura de Abaetetuba-PA 2026."),
 ("cisop-artesao", "Artesão", "cisop", None, 20, "CISOP Cascavel 2026 · banca Fundação Fafipa."),
 ("cisop-agente-administrativo", "Agente Administrativo", "cisop", None, 20, "CISOP Cascavel 2026."),
 ("cisop-tecnico-enfermagem", "Técnico em Enfermagem", "cisop", None, 20, "CISOP Cascavel 2026."),
 ("cisop-monitor-biblioteca", "Monitor de Biblioteca", "cisop", None, 20, "CISOP Cascavel 2026."),
 ("cisop-professor-ed-infantil", "Professor de Educação Infantil", "cisop", None, 20, "CISOP Cascavel 2026."),
 ("cisop-professor-temporario", "Professor Temporário", "cisop", None, 20, "CISOP Cascavel 2026."),
]
GRUPOS = {"pss": "PSS SEED-PR 2027", "cisop": "CISOP Cascavel 2026", "simulado": "Simulados", "outros": "Outros concursos"}
items = []
for slug, nome, g, code, preco, sub in P:
    imgs = [f"img/{slug}-{k}.jpg" for k in range(1, 5) if os.path.exists(os.path.join(HERE, "img", f"{slug}-{k}.jpg"))]
    items.append({"slug": slug, "nome": nome, "grupo": g, "grupoNome": GRUPOS[g], "link": (CHK + code) if code else None,
                  "preco": preco, "sub": sub, "imgs": imgs, "paginas": pag.get(slug, {}).get("paginas")})

HTML = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Loja de Matemática — Apostilas e Simulados</title>
<meta name="description" content="Apostilas e simulados para PSS SEED-PR 2027, CISOP Cascavel 2026 e outros concursos. Veja as páginas antes de comprar.">
<meta property="og:title" content="Loja de Matemática — Apostilas e Simulados">
<meta property="og:description" content="Apostilas e simulados para PSS SEED-PR 2027, CISOP Cascavel 2026 e mais.">
<meta property="og:image" content="https://hodhreego.github.io/PSS/loja/img/matematica-1.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--navy:#1B3A6B;--navy-deep:#0F2547;--gold:#C9A227;--gold-light:#E9D48E;--bg:#EEF3FB;--ink:#1B2733;--mut:#5b6b80;--card:#fff;--ok:#1f7a4d;--line:#d9e2f1}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Source Sans 3',system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
header.hero{background:linear-gradient(135deg,var(--navy-deep),var(--navy) 60%,#27508f);color:#fff;padding:46px 0 64px;position:relative;overflow:hidden}
header.hero:after{content:"";position:absolute;right:-90px;top:-90px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(201,162,39,.35),transparent 70%)}
.eyebrow{letter-spacing:.22em;font-size:12px;color:var(--gold-light);font-weight:600;text-transform:uppercase}
h1{font-family:'Playfair Display',serif;font-size:clamp(30px,5vw,50px);line-height:1.1;margin:10px 0 12px}
h1 em{color:var(--gold-light);font-style:normal}
.hero p{max-width:620px;color:#d6e1f5;font-size:18px}
.perks{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.perk{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);padding:7px 14px;border-radius:99px;font-size:14px;font-weight:600}
.tools{margin-top:-30px;position:relative;z-index:2}
.bar{background:#fff;border-radius:16px;box-shadow:0 10px 30px rgba(15,37,71,.15);padding:14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:8px;flex:1}
.chip{border:1.5px solid var(--line);background:#fff;color:var(--navy);font:600 14px 'Source Sans 3';padding:8px 14px;border-radius:99px;cursor:pointer;transition:.15s}
.chip:hover{border-color:var(--navy)}
.chip.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chip small{opacity:.7;font-weight:600;margin-left:4px}
#q{border:1.5px solid var(--line);border-radius:99px;padding:9px 16px;font:500 15px 'Source Sans 3';min-width:220px;outline:none}
#q:focus{border-color:var(--navy)}
section.grupo{margin-top:34px}
section.grupo h2{font-family:'Playfair Display',serif;color:var(--navy);font-size:26px;display:flex;align-items:center;gap:12px}
section.grupo h2:after{content:"";flex:1;height:2px;background:linear-gradient(90deg,var(--gold),transparent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:20px;margin-top:16px}
.card{background:var(--card);border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(15,37,71,.09);display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(15,37,71,.18)}
.cover{position:relative;aspect-ratio:3/4;background:#dfe7f5;cursor:pointer;overflow:hidden}
.cover img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .35s}
.card:hover .cover img{transform:scale(1.04)}
.badge{position:absolute;top:10px;left:10px;font-size:12px;font-weight:700;padding:4px 10px;border-radius:99px;background:var(--ok);color:#fff}
.badge.soon{background:var(--gold);color:#3b2f00}
.peek{position:absolute;bottom:10px;right:10px;background:rgba(15,37,71,.85);color:#fff;font-size:12px;font-weight:600;padding:5px 11px;border-radius:99px}
.info{padding:14px 15px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.info small{color:var(--mut);font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.info h3{font-size:18px;line-height:1.2;color:var(--navy-deep)}
.info p{font-size:14px;color:var(--mut);flex:1}
.row{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:8px}
.price{font-family:'Playfair Display',serif;font-weight:700;font-size:24px;color:var(--navy)}
.price span{font-size:14px;margin-right:2px}
.btn{display:inline-block;text-decoration:none;font:700 14px 'Source Sans 3';padding:10px 16px;border-radius:10px;border:0;cursor:pointer;transition:.15s}
.btn.buy{background:var(--gold);color:#2b2200}.btn.buy:hover{background:#b48f1c}
.btn.wa{background:#1f9d57;color:#fff}.btn.wa:hover{background:#188047}
.btn.ghost{background:#fff;color:var(--navy);border:1.5px solid var(--line)}
.empty{display:none;text-align:center;padding:50px 0;color:var(--mut)}
footer{margin-top:60px;background:var(--navy-deep);color:#c5d3ee;padding:34px 0;font-size:14px}
footer b{color:#fff}.warn{margin-top:12px;background:#a1262a;color:#fff;border-radius:10px;padding:10px 14px;font-weight:600}
/* modal */
.modal{position:fixed;inset:0;background:rgba(10,20,40,.82);display:none;align-items:center;justify-content:center;z-index:50;padding:14px}
.modal.open{display:flex}
.box{background:#fff;border-radius:18px;max-width:880px;width:100%;max-height:94vh;overflow:auto;display:grid;grid-template-columns:1.1fr 1fr}
.stage{background:#e6ecf7;padding:14px;display:flex;flex-direction:column;gap:10px;align-items:center}
.stage img.big{width:100%;max-height:68vh;object-fit:contain;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.2);background:#fff}
.thumbs{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.thumbs img{width:56px;height:76px;object-fit:cover;object-position:top;border-radius:5px;border:2px solid transparent;cursor:pointer;opacity:.7}
.thumbs img.on{border-color:var(--gold);opacity:1}
.side{padding:24px;display:flex;flex-direction:column;gap:10px}
.side h3{font-family:'Playfair Display',serif;font-size:26px;color:var(--navy-deep);line-height:1.15}
.side .row{margin-top:auto}
.x{position:absolute;top:14px;right:18px;color:#fff;font-size:34px;cursor:pointer;background:none;border:0}
.lab{font-size:12px;color:var(--mut);text-align:center}

/* whatsapp */
.fab{position:fixed;right:16px;bottom:16px;z-index:40;background:#1f9d57;color:#fff;border:0;border-radius:99px;padding:13px 20px;font:700 15px 'Source Sans 3';box-shadow:0 8px 22px rgba(0,0,0,.28);cursor:pointer;display:flex;gap:8px;align-items:center}
.fab:hover{background:#188047}
.wpanel{position:fixed;right:16px;bottom:74px;z-index:45;width:min(360px,calc(100vw - 32px));background:#fff;border-radius:18px;box-shadow:0 18px 44px rgba(10,20,40,.35);display:none;overflow:hidden}
.wpanel.open{display:block}
.wpanel header{background:#1f9d57;color:#fff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.wpanel header b{font-size:16px}.wpanel header button{background:none;border:0;color:#fff;font-size:26px;cursor:pointer;line-height:1}
.wbody{padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;max-height:72vh;overflow:auto}
.wbody label.t{font-size:12px;font-weight:700;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.opt{display:flex;gap:8px;align-items:flex-start;border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14px;cursor:pointer}
.opt:has(input:checked){border-color:#1f9d57;background:#eaf7f0}
.opt input{margin-top:3px;accent-color:#1f9d57}
.wbody select,.wbody textarea{width:100%;border:1.5px solid var(--line);border-radius:10px;padding:9px 10px;font:500 14px 'Source Sans 3';outline:none}
.wbody textarea{min-height:92px;resize:vertical}
.wbody .btn.wa{text-align:center;padding:12px}
.wbody small{color:var(--mut);font-size:12px}
@media(max-width:720px){.box{grid-template-columns:1fr}.stage img.big{max-height:52vh}.grid{grid-template-columns:repeat(2,1fr);gap:12px}.info h3{font-size:15px}.price{font-size:20px}.row{flex-direction:column;align-items:stretch;gap:6px}.row .btn{text-align:center}.info{padding:12px}#q{width:100%}.fab{padding:11px 16px}}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">Prof. Rodrigo Gonçalves Pereira</div>
  <h1>Loja de <em>Matemática</em><br>Apostilas &amp; Simulados</h1>
  <p>Material de estudo organizado, direto ao ponto e atualizado com os editais. Confira capa, índice e páginas internas antes de comprar.</p>
  <div class="perks"><span class="perk">📄 Entrega digital em PDF</span><span class="perk">🔎 Veja as páginas antes</span><span class="perk">🔠 Versão JUMBO (letra grande)</span><span class="perk">⚡ Pagamento seguro pela Eduzz</span></div>
</div></header>

<div class="wrap tools"><div class="bar">
  <div class="chips" id="chips"></div>
  <input id="q" type="search" placeholder="Buscar apostila…">
</div></div>

<main class="wrap" id="main"></main>
<div class="wrap empty" id="empty">Nenhum material encontrado.</div>

<footer><div class="wrap">
  <p><b>Loja de Matemática</b> — Prof. Rodrigo Gonçalves Pereira. Dúvidas ou pedidos de novos materiais: <a style="color:var(--gold-light)" href="#" onclick="wtoggle(true);return false">WhatsApp (+55 45 99969-9444)</a>.</p>
  <p class="warn">Proibido o compartilhamento. Cópia não autorizada. Violação sujeita à pena de detenção e multa (Lei 9.610/98 e Art. 184 do Código Penal).</p>
</div></footer>


<button class="fab" id="fab" onclick="wtoggle()">💬 Falar no WhatsApp</button>
<div class="wpanel" id="wp" role="dialog" aria-label="Falar no WhatsApp"><header><b>Fale com o Prof. Rodrigo</b><button onclick="wtoggle()" aria-label="Fechar">×</button></header>
 <div class="wbody">
  <label class="t">Sobre o que você quer falar?</label>
  <div id="wopts"></div>
  <label class="t" for="wprod">Material (opcional)</label>
  <select id="wprod"></select>
  <label class="t" for="wmsg">Sua mensagem (você pode editar)</label>
  <textarea id="wmsg"></textarea>
  <a class="btn wa" id="wgo" target="_blank" rel="noopener" href="#">Abrir WhatsApp</a>
  <small>Você será levado ao WhatsApp com a mensagem pronta; só precisa tocar em enviar.</small>
 </div></div>
<div class="modal" id="modal" onclick="if(event.target===this)fecha()"><button class="x" onclick="fecha()" aria-label="Fechar">×</button>
  <div class="box"><div class="stage"><img class="big" id="big" alt=""><div class="thumbs" id="th"></div><div class="lab" id="lab"></div></div>
  <div class="side" id="side"></div></div></div>

<script>
const ITENS=__DATA__;
const WA="__WA__";
const GR=[["pss","PSS SEED-PR 2027"],["cisop","CISOP Cascavel 2026"],["simulado","Simulados"],["outros","Outros concursos"]];
let filtro="todos",busca="";
const $=s=>document.querySelector(s);
const brl=n=>n.toFixed(2).replace(".",",");
function card(it){
  const soon=!it.link;
  const act=soon?`<button class="btn wa" onclick="wabre('${it.slug}')">Avisar-me</button>`
                 :`<a class="btn buy" target="_blank" rel="noopener" href="${it.link}">Comprar</a>`;
  return `<article class="card" data-s="${it.slug}"><div class="cover" onclick="abre('${it.slug}')"><img loading="lazy" src="${it.imgs[0]}" alt="Capa da apostila ${it.nome}"><span class="badge ${soon?'soon':''}">${soon?'Em breve':'Disponível'}</span><span class="peek">👁 ver páginas</span></div>
  <div class="info"><small>${it.grupoNome}</small><h3>${it.nome}</h3><p>${it.sub}${it.paginas?` · ${it.paginas} págs.`:''}</p>
  <div class="row"><div class="price"><span>R$</span>${brl(it.preco)}</div>${act}</div></div></article>`;
}
function render(){
  const q=busca.toLowerCase();let total=0;
  $("#main").innerHTML=GR.map(([g,nome])=>{
    if(filtro!=="todos"&&filtro!==g)return "";
    const l=ITENS.filter(i=>i.grupo===g&&(i.nome+" "+i.grupoNome).toLowerCase().includes(q));
    total+=l.length;if(!l.length)return "";
    return `<section class="grupo"><h2>${nome}</h2><div class="grid">${l.map(card).join("")}</div></section>`;}).join("");
  $("#empty").style.display=total?"none":"block";
}
function chips(){
  const c=g=>ITENS.filter(i=>g==="todos"||i.grupo===g).length;
  $("#chips").innerHTML=[["todos","Todos"],...GR].map(([k,n])=>`<button class="chip ${filtro===k?'on':''}" onclick="filtro='${k}';chips();render()">${n}<small>${c(k)}</small></button>`).join("");
}
const NOMES=["Capa","Índice","Página interna","Página interna"];
let cur=null;
function abre(s){cur=ITENS.find(i=>i.slug===s);
  $("#th").innerHTML=cur.imgs.map((u,k)=>`<img src="${u}" onclick="foto(${k})" alt="">`).join("");
  const soon=!cur.link;
  $("#side").innerHTML=`<small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.06em">${cur.grupoNome}</small><h3>${cur.nome}</h3><p>${cur.sub}</p>
   <p style="font-size:14px;color:var(--mut)">${cur.paginas?cur.paginas+' páginas · ':''}PDF digital${cur.slug.startsWith('cisop')||cur.grupo==='pss'?' · inclui versão JUMBO (letra grande) quando disponível':''}</p>
   <div class="row"><div class="price"><span>R$</span>${brl(cur.preco)}</div>${soon?`<button class="btn wa" onclick="fecha();wabre('${cur.slug}')">Falar no WhatsApp</button>`:`<a class="btn buy" target="_blank" rel="noopener" href="${cur.link}">Comprar agora</a>`}</div>`;
  foto(0);$("#modal").classList.add("open");document.body.style.overflow="hidden";}
function foto(k){$("#big").src=cur.imgs[k];$("#lab").textContent=(cur.imgs.length>2?NOMES[k]:(k?"Índice":"Capa"))+" · "+(k+1)+"/"+cur.imgs.length;
  [...$("#th").children].forEach((e,i)=>e.classList.toggle("on",i===k));}
function fecha(){$("#modal").classList.remove("open");document.body.style.overflow=""}
document.addEventListener("keydown",e=>{if(e.key==="Escape")fecha();
  if($("#modal").classList.contains("open")&&cur){const on=[...$("#th").children].findIndex(x=>x.classList.contains("on"));
    if(e.key==="ArrowRight")foto(Math.min(on+1,cur.imgs.length-1));if(e.key==="ArrowLeft")foto(Math.max(on-1,0));}});
$("#q").addEventListener("input",e=>{busca=e.target.value;render()});
chips();render();
const WNUM="5545999699444";
const WOPT=[
 ["Tenho uma dúvida sobre um material","Olá, Prof. Rodrigo! Tenho uma dúvida sobre o material{P}."],
 ["Quero ajuda para escolher o material certo para o meu cargo","Olá, Prof. Rodrigo! Quero ajuda para escolher o material certo para o meu cargo. Meu cargo/concurso é: "],
 ["Já paguei e não recebi o PDF","Olá, Prof. Rodrigo! Já fiz o pagamento{P}, mas ainda não recebi o PDF. O e-mail da compra é: "],
 ["Quero a versão JUMBO (letra grande)","Olá, Prof. Rodrigo! Gostaria da versão JUMBO (letra grande){P}. Pode me orientar?"],
 ["Pedir um material de outra disciplina ou concurso","Olá, Prof. Rodrigo! Gostaria de pedir um material de outra disciplina/concurso: "],
 ["Quero ser avisado de novos materiais","Olá, Prof. Rodrigo! Quero ser avisado(a) quando sair material novo do concurso: "],
 ["Mentoria (plano de aula, ação ou atendimento)","Olá, Prof. Rodrigo! Tenho interesse na mentoria para a Prova Prática do PSS. Pode me passar mais informações?"],
 ["Outro assunto","Olá, Prof. Rodrigo! "]];
function wprod(){const v=$("#wprod").value;return v?" "+v:""}
function wbuild(){const i=+(document.querySelector('input[name=wo]:checked')||{value:0}).value;$("#wmsg").value=WOPT[i][1].replace("{P}",wprod()?" ("+wprod().trim()+")":"");wlink()}
function wlink(){$("#wgo").href="https://wa.me/"+WNUM+"?text="+encodeURIComponent($("#wmsg").value)}
function winit(){
  $("#wopts").innerHTML=WOPT.map((o,i)=>`<label class="opt"><input type="radio" name="wo" value="${i}" ${i?'':'checked'} onchange="wbuild()"><span>${o[0]}</span></label>`).join("");
  $("#wprod").innerHTML='<option value="">— nenhum / não sei —</option>'+ITENS.map(i=>`<option value="Apostila ${i.nome} · ${i.grupoNome}">${i.nome} · ${i.grupoNome}</option>`).join("");
  $("#wprod").onchange=wbuild;$("#wmsg").oninput=wlink;wbuild();}
function wtoggle(force){const p=$("#wp");const on=force===undefined?!p.classList.contains("open"):force;p.classList.toggle("open",on);}
function wabre(slug){const it=ITENS.find(i=>i.slug===slug);if(it)$("#wprod").value="Apostila "+it.nome+" · "+it.grupoNome;wbuild();wtoggle(true);}
winit();
</script>
</body>
</html>'''
out = HTML.replace("__DATA__", json.dumps(items, ensure_ascii=False)).replace("__WA__", WA)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("ok", len(items), "itens")
