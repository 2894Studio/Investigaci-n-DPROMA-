"""Genera el informe para ingeniería: página web (web/entregables) y HTML de impresión para el PDF.

Uso: python3 -I construir.py <salida_pdf_html_dir>
El contenido vive en contenido.html y es el mismo para las dos presentaciones.
"""
import os, re, sys, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
WEB = os.path.join(REPO, 'web', 'entregables')
PDF_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'pdf-tmp')

TITULO = 'Qué corregir en las 50 pantallas'
CUERPO = open(os.path.join(AQUI, 'contenido.html'), encoding='utf-8').read()
FIN = open(os.path.join(WEB, 'finanzas.html'), encoding='utf-8').read()
BASE_CSS = FIN[FIN.index('<style>') + 7:FIN.index('</style>')]

# ------------------------------------------------------------------ web
WEB_CSS = r'''
:root{ --bad-text:#A3261C; --ok-text:#1D5A46; }
@media (prefers-color-scheme: dark){ :root{ --bad-text:#FF9C93; --ok-text:#8FD9B6; } }
:root[data-theme="dark"]{ --bad-text:#FF9C93; --ok-text:#8FD9B6; }
:root[data-theme="light"]{ --bad-text:#A3261C; --ok-text:#1D5A46; }

.sec .wrap-in{ }
.sec-head{ display:block; margin-bottom:1.5rem; }
.sec-head .num{ display:inline-flex; align-items:center; gap:.5em; font-size:.75rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--accent-text); }
.sec-head .num::before{ content:""; width:.5em; height:.5em; border-radius:999px; background:var(--accent); display:inline-block; }
.sec-head h2{ font-size:clamp(1.5rem,3vw,2rem); margin-top:.5rem; max-width:30ch; }
.lede{ max-width:68ch; color:var(--text-muted); font-size:1.0625rem; margin:0 0 2rem; }
.sec p{ max-width:74ch; color:var(--text-muted); }
.sec p strong, .sec p b{ color:var(--text); }
.sub{ font-size:1.125rem; margin:2.25rem 0 .75rem; }
.nota{ font-size:.875rem; }
code{ font-size:.8125rem; background:var(--surface-alt); padding:.1em .4em; border-radius:5px; overflow-wrap:anywhere; }
pre.cod{ background:var(--surface-alt); border:1px solid var(--border); border-radius:12px; padding:.9rem 1.1rem; font-size:.8125rem; overflow-x:auto; margin:.9rem 0 0; max-width:74ch; }
pre.cod, pre.cod code{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
pre.cod{ white-space:pre-wrap; overflow-wrap:anywhere; }

.stats{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.25rem; margin:0 0 .5rem; }
@media (max-width:900px){ .stats{ grid-template-columns:1fr; } }
.stat{ background:var(--surface); border:1px solid var(--border); border-radius:18px; padding:1.5rem; box-shadow:var(--shadow); }
.stat .n{ display:block; font-size:clamp(1.75rem,4vw,2.5rem); font-weight:700; line-height:1; letter-spacing:-.02em; color:var(--accent-text); }
.stat h3{ font-size:1rem; margin:.75rem 0 .4rem; }
.stat p{ font-size:.9375rem; margin:0; }

ol.plano, ul.plano{ margin:.5rem 0 0; padding-left:1.25rem; max-width:74ch; color:var(--text-muted); }
.plano li{ margin:.45rem 0; }
.plano li b{ color:var(--text); }

.table-scroll{ margin:1rem 0 1.25rem; }
.table-scroll table{ min-width:640px; table-layout:fixed; }
td.r, th.r{ text-align:right; } td.c, th.c{ text-align:center; }
td.ok{ color:var(--ok-text); font-weight:700; } td.no{ color:var(--bad-text); font-weight:700; }
td.sv{ color:var(--text-muted); font-style:italic; } td.na{ color:var(--text-muted); opacity:.6; }
.t-aviso td{ font-size:.875rem; }

ol.hallazgos{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1rem; counter-reset:h; }
li.h{ background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:1.3rem 1.5rem; box-shadow:var(--shadow); }
li.h h3{ font-size:1.0625rem; margin:.5rem 0 .55rem; max-width:60ch; }
li.h p{ margin:.5rem 0 0; font-size:.9375rem; }
.meta{ display:flex; gap:.6rem; align-items:center; flex-wrap:wrap; }
.ref{ font-size:.75rem; font-weight:700; letter-spacing:.06em; color:var(--text-muted); text-transform:uppercase; }
.ref code{ text-transform:none; letter-spacing:0; }
.pantallas{ font-size:.8125rem !important; }
.pantallas code{ margin-right:.15rem; }
.pill{ display:inline-block; font-size:.6875rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; padding:.2em .65em; border-radius:6px; }
.pill-crit,.pill-ok{ background:var(--accent-fill); color:var(--on-accent); }
.pill-leve{ background:transparent; border:1px solid var(--border); color:var(--text-muted); }
.pill-cond{ background:var(--warn-bg); border:1px solid var(--warn-border); color:var(--warn-text); }

.cards{ display:grid; grid-template-columns:repeat(2,1fr); gap:1.25rem; }
@media (max-width:760px){ .cards{ grid-template-columns:1fr; } }
.card{ background:var(--surface); border:1px solid var(--border); border-radius:18px; padding:1.4rem 1.5rem; box-shadow:var(--shadow); display:flex; flex-direction:column; gap:.4rem; }
.card.wide{ grid-column:1/-1; }
.card h3{ font-size:1.0625rem; margin-top:.4rem; }
.card p{ font-size:.9375rem; margin:0; }

figure{ margin:1.25rem 0; }
figure img{ display:block; width:100%; height:auto; border:1px solid var(--border); border-radius:14px; box-shadow:var(--shadow); }
figcaption{ margin-top:.6rem; font-size:.8125rem; color:var(--text-muted); }

.aviso{ margin-top:2rem; border:1px solid var(--warn-border); background:var(--warn-bg); color:var(--warn-text); border-radius:14px; padding:1.1rem 1.35rem; font-size:.9375rem; max-width:74ch; }
.aviso code{ background:rgba(0,0,0,.06); }
.descarga{ display:inline-flex; align-items:center; gap:.5rem; margin-top:1.5rem; padding:.6rem 1.1rem; border:1px solid var(--accent); border-radius:999px; font-weight:700; font-size:.9375rem; text-decoration:none; min-height:24px; }
.descarga:hover{ background:var(--accent-fill); color:var(--on-accent); }
'''

def envolver_tablas(h):
    h = re.sub(r'<table class="t', '<div class="table-scroll"><table class="t', h)
    return h.replace('</table>', '</table></div>')

web_cuerpo = envolver_tablas(CUERPO)
PDF_NOMBRE = 'SIO-DPROMA-auditoria-pantallas-oct2026.pdf'
WEB_HTML = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITULO} — DPROMA × 2894 Studio</title>
<meta name="description" content="Lo que se midió en las 50 pantallas del paquete del 12 de octubre: qué corregir, en qué orden y qué se deja a criterio del equipo de ingeniería." />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&display=swap" rel="stylesheet">
<style>{BASE_CSS}{WEB_CSS}</style>
</head>
<body>

<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="wordmark" href="/">2894 <span>Studio × DPROMA</span></a>
    <nav aria-label="Secciones">
      <a href="/entregables">← Entregables</a>
      <a href="#transversales">Cinco sustituciones</a>
      <a href="#por-pantalla">Por pantalla</a>
      <a href="#aviso">Aviso del 28-sep</a>
      <a href="#redisenos">Propuestas</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Auditoría de pantallas · Octubre de 2026</span>
    <h1>Qué corregir en las 50 pantallas, y en qué orden.</h1>
    <p class="lede">Lo que se midió en el paquete del 12 de octubre: lo que hay que corregir sí o sí, lo que conviene corregir de paso y lo que se deja a criterio del equipo. Cada hallazgo lleva archivo, selector y línea para poder comprobarlo antes de tocar nada.</p>
    <p class="lede">Es la primera auditoría de estas pantallas. Describe lo que hay en los archivos recibidos y nada más.</p>
    <a class="descarga" href="/entregables/revisiones/{PDF_NOMBRE}">Descargar en PDF</a>
  </div>
</section>

<main class="wrap">
{web_cuerpo}
</main>

<footer>
  <div class="wrap">
    <div class="footer-nav"><a href="/entregables">← Volver a Entregables</a></div>
    <div class="footer-meta"><span>2894 Studio × DPROMA · Octubre de 2026</span><a href="/entregables/revisiones/{PDF_NOMBRE}">Versión en PDF</a></div>
  </div>
</footer>

</body>
</html>
'''
open(os.path.join(WEB, 'auditoria-pantallas.html'), 'w', encoding='utf-8').write(WEB_HTML)

# ------------------------------------------------------------------ pdf
PDF_CSS = r'''
:root{ --az:#0A46FF; --tinta:#16181D; --gris:#5B6068; --gris2:#8A8F98; --linea:#DDE0E7; --fondo2:#F4F5F9; --ambar:#8A5300; --ambarbg:#FFF4E0; --ambarb:#B8862A; }
*{ box-sizing:border-box; }
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ margin:0; color:var(--tinta); font:10pt/1.55 "Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif; }
code{ font:8.4pt ui-monospace,Menlo,Consolas,"Liberation Mono",monospace; background:var(--fondo2); padding:0 3px; border-radius:3px; overflow-wrap:anywhere; }
a{ color:inherit; text-decoration:none; }

.cover{ height:252mm; display:flex; flex-direction:column; page-break-after:always; }
.cover .rule{ border-top:3pt solid var(--az); margin-top:2mm; }
.cover .eyebrow{ margin-top:5mm; font-size:8.5pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--gris); }
.cover .mid{ margin-top:auto; margin-bottom:auto; padding-top:20mm; }
.cover h1{ font-size:34pt; line-height:1.08; margin:0; max-width:120mm; letter-spacing:-.01em; }
.cover .sub{ margin-top:6mm; max-width:120mm; font-size:12pt; color:var(--gris); }
.cover .foot{ border-top:.75pt solid var(--linea); padding-top:4mm; display:flex; justify-content:space-between; font-size:8.5pt; color:var(--gris2); }

.sec{ page-break-before:always; }
.sec-head{ margin-bottom:5mm; }
.sec-head .num{ display:block; font-size:8pt; font-weight:700; letter-spacing:.2em; color:var(--az); margin-bottom:1.5mm; }
.sec-head h2{ font-size:21pt; line-height:1.15; margin:0; padding-bottom:3mm; border-bottom:2.2pt solid var(--tinta); letter-spacing:-.01em; }
.lede{ color:var(--gris); font-size:11pt; max-width:150mm; margin:0 0 6mm; }
.sec p{ margin:0 0 3mm; max-width:160mm; }
.sub{ font-size:12pt; margin:7mm 0 2.5mm; page-break-after:avoid; }
.nota{ color:var(--gris); font-size:9pt; }

.stats{ display:grid; grid-template-columns:repeat(3,1fr); gap:4mm; margin:0 0 3mm; }
.stat{ background:var(--fondo2); border:.75pt solid var(--linea); border-radius:8pt; padding:4.5mm; page-break-inside:avoid; }
.stat .n{ display:block; font-size:24pt; font-weight:700; color:var(--az); line-height:1.05; }
.stat h3{ font-size:10pt; margin:2mm 0 1.5mm; }
.stat p{ font-size:9pt; color:var(--gris); margin:0; }

ol.plano, ul.plano{ margin:0 0 3mm; padding-left:5mm; max-width:160mm; }
.plano li{ margin:1.4mm 0; }

table.t{ width:100%; border-collapse:collapse; table-layout:fixed; margin:2mm 0 4mm; font-size:9pt; }
table.t th{ text-align:left; font-size:7.5pt; letter-spacing:.1em; text-transform:uppercase; color:var(--gris); padding:2mm 2.5mm 2mm 0; border-bottom:1.4pt solid var(--tinta); vertical-align:bottom; }
table.t td{ padding:2.2mm 2.5mm 2.2mm 0; border-bottom:.6pt solid var(--linea); vertical-align:top; }
table.t thead{ display:table-header-group; }
table.t tr{ page-break-inside:avoid; }
table.t{ page-break-inside:avoid; }
td.r, th.r{ text-align:right; padding-right:3mm !important; } td.c, th.c{ text-align:center; }
td.ok{ color:#1D5A46; font-weight:700; } td.no{ color:#A3261C; font-weight:700; } td.sv{ color:var(--gris); font-style:italic; } td.na{ color:var(--gris2); }
.t-aviso td{ font-size:8.4pt; } .t-aviso th{ font-size:6.8pt; letter-spacing:.06em; }

.pill{ display:inline-block; font-size:6.8pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase; padding:.7mm 2mm; border-radius:3pt; margin-right:1.5mm; vertical-align:middle; }
.pill-crit,.pill-ok{ background:var(--az); color:#fff; }
.pill-leve{ border:.75pt solid var(--linea); color:var(--gris); background:#fff; }
.pill-cond{ background:var(--ambarbg); border:.75pt solid var(--ambarb); color:var(--ambar); }

ol.hallazgos{ list-style:none; margin:0; padding:0; }
li.h{ border-left:2pt solid var(--az); padding:0 0 0 4mm; margin:0 0 3.6mm; page-break-inside:avoid; }
li.h .meta{ margin-bottom:1mm; }
.ref{ font-size:7.3pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--gris2); margin-right:2mm; vertical-align:middle; }
.ref code{ text-transform:none; letter-spacing:0; font-size:7.8pt; }
li.h h3{ font-size:11pt; margin:0 0 1.5mm; }
li.h p{ font-size:9pt; line-height:1.5; color:var(--gris); margin:0 0 1.5mm; }
li.h p b{ color:var(--tinta); }
.pantallas code{ margin-right:1mm; }
pre.cod{ background:var(--fondo2); border:.6pt solid var(--linea); border-radius:5pt; padding:2.5mm 3mm; font:7.4pt/1.4 ui-monospace,Menlo,Consolas,"Liberation Mono",monospace; white-space:pre-wrap; overflow-wrap:anywhere; margin:1.2mm 0 1.6mm; }

.cards{ display:grid; grid-template-columns:1fr 1fr; gap:4mm; }
.card{ border:.75pt solid var(--linea); border-radius:8pt; padding:4mm 4.5mm; page-break-inside:avoid; }
.card.wide{ grid-column:1/-1; }
.card h3{ font-size:10.5pt; margin:1.5mm 0 1.5mm; }
.card p{ font-size:9pt; color:var(--gris); margin:0; }

figure{ margin:3mm 0 4mm; page-break-inside:avoid; }
figure img{ display:block; width:100%; height:auto; border:.75pt solid var(--linea); border-radius:5pt; }
figcaption{ font-size:8.3pt; color:var(--gris2); margin-top:1.5mm; }

.aviso{ margin-top:6mm; border:.9pt solid var(--ambarb); background:var(--ambarbg); color:var(--ambar); border-radius:8pt; padding:4mm 4.5mm; font-size:9.2pt; page-break-inside:avoid; }
.aviso code{ background:rgba(0,0,0,.05); }
'''

pdf_cuerpo = CUERPO.replace('/entregables/img/auditoria/', 'img/').replace(' loading="lazy"', '')
PDF_HTML = f'''<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><title>{TITULO} · DPROMA × 2894 Studio</title><style>{PDF_CSS}</style></head>
<body>
<section class="cover">
  <div class="rule"></div>
  <div class="eyebrow">2894 Studio × DPROMA</div>
  <div class="mid">
    <h1>{TITULO}</h1>
    <p class="sub">Lo que se midió en el paquete del 12 de octubre, qué se le pide a ingeniería, qué conviene hacer de paso y qué se deja a su criterio.</p>
  </div>
  <div class="foot"><span>Informe para el equipo de ingeniería de DPROMA</span><span>Octubre de 2026</span></div>
</section>
{pdf_cuerpo}
</body></html>
'''
os.makedirs(os.path.join(PDF_DIR, 'img'), exist_ok=True)
for f in os.listdir(os.path.join(WEB, 'img', 'auditoria')):
    shutil.copy(os.path.join(WEB, 'img', 'auditoria', f), os.path.join(PDF_DIR, 'img', f))
open(os.path.join(PDF_DIR, 'informe.html'), 'w', encoding='utf-8').write(PDF_HTML)
print('web:', os.path.join(WEB, 'auditoria-pantallas.html'), len(WEB_HTML) // 1024, 'KB; pdf html:', PDF_DIR)
