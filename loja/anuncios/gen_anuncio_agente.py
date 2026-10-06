# Imagem de anúncio 4:5 (1080x1350) — Agente Administrativo CISOP Cascavel
import os
from playwright.sync_api import sync_playwright
H = """<!doctype html><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800;900&family=Source+Sans+3:wght@400;600;700;800&display=swap" rel=stylesheet>
<style>*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;font-family:'Source Sans 3',sans-serif;color:#fff;background:linear-gradient(165deg,#1c4c8c,#0f2a52);position:relative;overflow:hidden}
.ring{position:absolute;right:-200px;top:-200px;width:700px;height:700px;border-radius:50%;background:rgba(255,255,255,.08)}
.w{position:absolute;inset:0;padding:70px 76px;display:flex;flex-direction:column}
.top{background:#c0392b;font-weight:800;font-size:36px;padding:16px 26px;border-radius:10px;align-self:flex-start;letter-spacing:.02em}
.tag{margin-top:46px;font-size:28px;letter-spacing:.22em;font-weight:700;opacity:.85}
h1{font-family:'Playfair Display',serif;font-weight:900;font-size:96px;line-height:1.02;color:#ffd84a;margin-top:14px}
.sub{font-size:36px;font-weight:600;margin-top:20px;opacity:.95}
ul{list-style:none;margin-top:40px;margin-bottom:40px;display:flex;flex-direction:column;gap:18px}
li{background:rgba(255,255,255,.12);border-radius:14px;padding:20px 26px;font-size:36px;font-weight:700;display:flex;justify-content:space-between}
li span{color:#ffd84a}
.price{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between}
.p{white-space:nowrap;font-family:'Playfair Display',serif;font-weight:900;font-size:120px;color:#ffd84a;line-height:1}
.p small{display:block;font-family:'Source Sans 3';font-size:30px;font-weight:700;color:#fff;margin-bottom:8px}
.cta{background:#25d366;color:#0b2a14;font-weight:800;font-size:40px;padding:26px 34px;border-radius:16px;text-align:center;line-height:1.15}
.f{margin-top:26px;font-size:24px;opacity:.8}
</style><div class=ring></div><div class=w>
<div class=top>FALTAM 12 DIAS PARA A PROVA · 18/10</div>
<div class=tag>CISOP · CASCAVEL 2026 · NÍVEL MÉDIO</div>
<h1>AGENTE<br>ADMINISTRATIVO</h1>
<div class=sub>Apostila completa, direto ao que o edital cobra</div>
<ul><li>Apostila <span>130 páginas</span></li><li>Versão JUMBO (letra grande) <span>206 páginas</span></li><li>Simulados <span>36 páginas</span></li></ul>
<div class=price><div class=p><small>Pasta completa em PDF</small>R$ 20</div><div class=cta>Entrega imediata<br>Link no primeiro comentário</div></div>
<div class=f>Prof. Rodrigo Gonçalves Pereira · Loja de Matemática</div></div>"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(H,wait_until="networkidle");pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"anuncio-agente-administrativo.jpg"),type="jpeg",quality=92);b.close()
