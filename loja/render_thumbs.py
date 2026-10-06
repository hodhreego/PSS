# Renderiza 4 páginas (capa, índice, 2 interiores) de cada apostila para a loja.
import fitz, os, sys, json
B = r"I:\Meu Drive\##Aulas @hodhreego\#$old1\PSS VENDAS"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
P = {
 "matematica":        ("Av80 Apostila Matemática PSS Av80", "Apostila PSS Matemática — SEED-PR 2027.pdf"),
 "conhecimentos-basicos": ("Av81 Apostila Conhecimentos Básicos PSS Av81", "Apostila PSS Conhecimentos Básicos — SEED-PR 2027.pdf"),
 "pedagogo":          ("Av82 Apostila Pedagogo Av82", "Apostila PSS Pedagogo — SEED-PR 2027.pdf"),
 "educacao-especial": ("Av83 Apostila Educação Especial - Inclusiva Av83", "Apostila PSS Educação Especial — SEED-PR 2027.pdf"),
 "geografia":         ("Av85 Apostila de Geografia Av85", "Apostila PSS Geografia — SEED-PR 2027.pdf"),
 "artes":             ("Av86 Apostila de Artes Av86", "Apostila PSS Artes — SEED-PR 2027.pdf"),
 "lingua-inglesa":    ("Av87 Apostila de L. Inglesa Inglês PSS Av87", "Apostila PSS Língua Inglesa — SEED-PR 2027.pdf"),
 "educacao-fisica":   ("Av88 Apostila de Ed. Física PSS Av88", "Apostila PSS Educação Física — SEED-PR 2027.pdf"),
 "lingua-portuguesa": ("Av88 Apostila de Língua Portuguesa", "Apostila PSS Língua Portuguesa 2.0 — SEED-PR 2027.pdf"),
 "gestao-negocios":   ("Av89 Apostila de Gestão e Negócios — Administração", "Apostila PSS Gestão e Negócios (Administração) — SEED-PR 2027.pdf"),
 "informacao-comunicacao": ("Av90 Apostila de Infomação e Comunicação", "Apostila PSS INFORMAÇÃO E COMUNICAÇÃO — SEED-PR 2027.pdf"),
 "quimica":           ("Av91 Apostila de Química Av91", "Apostila PSS Química — SEED-PR 2027.pdf"),
 "pedagogo-abaetetuba": ("Abaetetuba/Pedagogo Av90", "Apostila Completa Pedagogo — Concurso Prefeitura de Abaetetuba-PA 2026.pdf"),
 "simulado-matematica": ("Av80 Apostila Matemática PSS Av80", "Simulados PSS Matemática — SEED-PR 2027 Av79.pdf"),
 "cisop-artesao":     ("Av102 Apostila Artesao Av102", "Apostila Artesao CISOP 2026.pdf"),
 "cisop-agente-administrativo": ("Av103 Apostila Agente Administrativo Av103", "Apostila Agente Administrativo CISOP 2026.pdf"),
 "cisop-tecnico-enfermagem": ("Av104 Apostila Tecnico em Enfermagem Av104", "Apostila Tecnico em Enfermagem CISOP 2026.pdf"),
 "cisop-monitor-biblioteca": ("Av105 Apostila Monitor de Biblioteca Av105", "Apostila Monitor de Biblioteca Cascavel 2026.pdf"),
 "cisop-professor-ed-infantil": ("Av106 Apostila Professor Ed Infantil Av106", "Apostila Professor Ed Infantil Cascavel 2026.pdf"),
 "cisop-professor-temporario": ("Av107 Apostila Professor Temporario Av107", "Apostila Professor Temporario Cascavel 2026.pdf"),
}
def pick(doc):
    n = len(doc); idx = 1
    for i in range(1, min(10, n)):
        t = doc[i].get_text().upper()
        if "SUMÁRIO" in t or "ÍNDICE" in t or "SUMARIO" in t:
            idx = i; break
    def rich(i):  # evita páginas quase em branco
        return len(doc[i].get_text().strip()) > 400
    def near(p):
        for d in range(0, 12):
            for j in (p+d, p-d):
                if idx+2 < j < n-2 and rich(j): return j
        return p
    return [0, idx, near(int(n*.33)), near(int(n*.66))], n
res = {}
only = sys.argv[1:]
for slug, (folder, fn) in P.items():
    if only and slug not in only: continue
    path = os.path.join(B, folder, fn)
    if not os.path.exists(path): print("FALTA", slug, path); continue
    doc = fitz.open(path); pages, n = pick(doc)
    for k, pg in enumerate(pages, 1):
        pix = doc[pg].get_pixmap(matrix=fitz.Matrix(560/doc[pg].rect.width, 560/doc[pg].rect.width))
        pix.save(os.path.join(OUT, f"{slug}-{k}.jpg"), jpg_quality=82)
    res[slug] = {"paginas": n, "usadas": [p+1 for p in pages]}
    print(slug, res[slug])
json.dump(res, open(os.path.join(OUT, "_paginas.json"), "w"), indent=1)
