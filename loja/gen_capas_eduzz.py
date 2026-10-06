# Gera capas QUADRADAS (1000x1000) no estilo das apostilas, para o Eduzz. Saída: capas-eduzz/<slug>.jpg
import os, html
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "capas-eduzz"); os.makedirs(OUT, exist_ok=True)

PSS = ("PROGRAMA", "PSS SEED-PR", "2027", "PSS PARANÁ 2027")
# slug, (tag, org, ano), titulo, subtitulo, cor topo, cor base, texto escuro?
I = [
 ("matematica", PSS, "APOSTILA DE MATEMÁTICA", "Conteúdo específico — Matemática", "#173e65", "#0f2a47", 0),
 ("conhecimentos-basicos", PSS, "CONHECIMENTOS BÁSICOS", "Para todos os cargos · Língua Portuguesa, ECA, Direitos Humanos e Conhecimentos Didáticos", "#0e4995", "#0a3270", 0),
 ("pedagogo", PSS, "APOSTILA DE PEDAGOGO", "Conteúdo específico para o cargo de Pedagogo", "#3c175c", "#28103d", 0),
 ("educacao-especial", PSS, "APOSTILA DE EDUCAÇÃO ESPECIAL", "Educação inclusiva e atendimento educacional especializado", "#5c2e17", "#3d1f0f", 0),
 ("lingua-inglesa", PSS, "APOSTILA DE LÍNGUA INGLESA", "Versão normal e versão JUMBO (letra grande)", "#185a56", "#0f3d3a", 0),
 ("geografia", PSS, "APOSTILA DE GEOGRAFIA", "Conteúdo específico — Professor de Geografia", "#1a5c2e", "#103d1e", 0),
 ("historia", PSS, "APOSTILA DE HISTÓRIA", "Conteúdo específico — Professor de História", "#5b4317", "#3d2d0f", 0),
 ("artes", PSS, "APOSTILA DE ARTES", "Conteúdo específico — Professor de Artes", "#5b1748", "#3d0f31", 0),
 ("gestao-negocios", PSS, "ADMINISTRAÇÃO, GESTÃO E NEGÓCIOS", "Conteúdo do eixo Gestão e Negócios", "#3c098a", "#27065c", 0),
 ("lingua-portuguesa", PSS, "APOSTILA DE LÍNGUA PORTUGUESA", "Conteúdo específico — Professor de Língua Portuguesa", "#173e65", "#0f2a47", 0),
 ("educacao-fisica", PSS, "APOSTILA DE EDUCAÇÃO FÍSICA", "Conteúdo específico — Professor de Educação Física", "#18672e", "#104520", 0),
 ("quimica", PSS, "APOSTILA DE QUÍMICA", "Conteúdo específico — Professor de Química", "#ffad00", "#e69500", 1),
 ("simulado-matematica", PSS, "SIMULADOS DE MATEMÁTICA", "Simulados completos com gabarito comentado", "#292959", "#1b1b3d", 0),
 ("pedagogo-abaetetuba", ("CONCURSO PÚBLICO", "PREFEITURA DE ABAETETUBA-PA", "EDITAL 001/2026", "ABAETETUBA"), "PEDAGOGO E PROFESSOR", "Educação Infantil e Fundamental I · Banca: Instituto Vicente Nelson", "#234b89", "#152d59", 0),
 ("cisop-artesao", ("CONCURSO PÚBLICO · NÍVEL FUNDAMENTAL", "CISOP · CASCAVEL", "2026", ""), "APOSTILA DE ARTESÃO", "Consórcio Intermunicipal de Saúde do Oeste do Paraná · Banca: Fafipa · Prova: 18/10/2026", "#6b3e1d", "#3f2410", 0),
 ("cisop-agente-administrativo", ("CONCURSO PÚBLICO · NÍVEL MÉDIO", "CISOP · CASCAVEL", "2026", ""), "APOSTILA DE AGENTE ADMINISTRATIVO", "Consórcio Intermunicipal de Saúde do Oeste do Paraná · Banca: Fafipa · Prova: 18/10/2026", "#1c4c8c", "#163e72", 0),
 ("cisop-tecnico-enfermagem", ("CONCURSO PÚBLICO · NÍVEL TÉCNICO", "CISOP · CASCAVEL", "2026", ""), "APOSTILA DE TÉCNICO EM ENFERMAGEM", "Consórcio Intermunicipal de Saúde do Oeste do Paraná · Banca: Fafipa · Prova: 18/10/2026", "#0f6b7a", "#0a4c57", 0),
 ("cisop-monitor-biblioteca", ("TESTE SELETIVO · NÍVEL MÉDIO", "PREFEITURA DE CASCAVEL", "2026", ""), "APOSTILA DE MONITOR DE BIBLIOTECA", "Prefeitura Municipal de Cascavel/PR · Edital 354/2026 · Banca: Fafipa · Prova: 29/11/2026", "#4b3b86", "#352a63", 0),
 ("cisop-professor-ed-infantil", ("TESTE SELETIVO", "PREFEITURA DE CASCAVEL", "2026", ""), "APOSTILA DE PROFESSOR DE EDUCAÇÃO INFANTIL", "Prefeitura Municipal de Cascavel/PR · Edital 354/2026 · Banca: Fafipa · Prova: 29/11/2026", "#c1651a", "#8f4710", 0),
 ("cisop-professor-temporario", ("TESTE SELETIVO", "PREFEITURA DE CASCAVEL", "2026", ""), "APOSTILA DE PROFESSOR TEMPORÁRIO", "Prefeitura Municipal de Cascavel/PR · Edital 354/2026 · Banca: Fafipa · Prova: 29/11/2026", "#1e6f4f", "#14503a", 0),
]

def page(it):
    slug, (tag, org, ano, _), titulo, sub, c1, c2, dark = it
    L = max(len(w) for w in titulo.split())
    fg = "#1a2540" if dark else "#fff"
    ttl = "#1a2540" if dark else "#ffd84a"
    sz = 108 if len(titulo) <= 22 else 92 if len(titulo) <= 30 else 78
    sz = min(sz, int(850 / (L * 0.70)))
    return f"""<!doctype html><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800;900&family=Source+Sans+3:wght@400;600;700&display=swap" rel=stylesheet>
<style>*{{box-sizing:border-box;margin:0}}body{{width:1000px;height:1000px;overflow:hidden;font-family:'Source Sans 3',sans-serif;color:{fg};
background:linear-gradient(160deg,{c1},{c2});position:relative}}
.ring{{position:absolute;right:-170px;top:-170px;width:620px;height:620px;border-radius:50%;background:rgba(255,255,255,.10)}}
.ring2{{position:absolute;left:-120px;bottom:90px;width:360px;height:360px;border-radius:50%;background:rgba(255,255,255,.05)}}
.w{{position:absolute;inset:0;padding:64px 70px;display:flex;flex-direction:column}}
.tag{{font-size:25px;letter-spacing:.2em;font-weight:700;opacity:.85}}
.org{{font-size:44px;font-weight:700;letter-spacing:.04em;margin-top:8px}}
.ano{{font-size:30px;letter-spacing:.35em;color:{'#7a4a00' if dark else '#f0c75e'};font-weight:700;margin-top:6px}}
.div{{width:90px;height:4px;background:{'#7a4a00' if dark else '#f0c75e'};margin:24px 0}}
.bd{{display:inline-block;background:#c0392b;color:#fff;font-weight:700;font-size:25px;padding:9px 20px;border-radius:5px;align-self:flex-start}}
.t{{font-family:'Playfair Display',serif;font-weight:900;font-size:{sz}px;line-height:1.04;color:{ttl};margin-top:auto;text-wrap:balance}}
.s{{font-size:29px;line-height:1.3;margin-top:22px;opacity:.92;max-width:840px}}
.f{{margin-top:34px;font-size:21px;font-weight:600;opacity:.9}}
.bd2{{margin-top:10px;background:#c0392b;color:#fff;font-weight:600;font-size:19px;line-height:1.3;padding:9px 16px;border-radius:5px}}
</style><div class=ring></div><div class=ring2></div><div class=w>
<div class=tag>{html.escape(tag)}</div><div class=org>{html.escape(org)}</div><div class=ano>{html.escape(ano)}</div>
<div class=div></div><div class=bd>🚫 Proibido o compartilhamento · Cópia não autorizada</div>
<div class=t>{html.escape(titulo)}</div><div class=s>{html.escape(sub)}</div>
<div class=f>© RODRIGO GONÇALVES PEREIRA — TODOS OS DIREITOS RESERVADOS</div>
<div class=bd2>Proibido o compartilhamento deste arquivo. Cópia não autorizada. Violação sujeita a pena de detenção e multa (Lei 9.610/98 e Art. 184 do Código Penal).</div></div>"""

if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1000})
        for it in I:
            if only and it[0] not in only: continue
            pg.set_content(page(it), wait_until="networkidle"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, it[0] + ".jpg"), type="jpeg", quality=90)
            print(it[0])
        b.close()
