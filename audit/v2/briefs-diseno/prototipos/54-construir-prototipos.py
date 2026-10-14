#!/usr/bin/env python3
# Prototipos del panel «Con qué filtros» (54) a partir de COPIAS de la maqueta del cliente.
import re, pathlib
import os
MAQUETAS = pathlib.Path(os.environ.get('MAQUETAS', '/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/v2zip/Actualizacion-12-10-26'))
SRC = (MAQUETAS / '54_bitacora_descargas.html').read_text(encoding='utf-8')
OUT = pathlib.Path('/home/user/Investigaci-n-DPROMA-/audit/v2/briefs-diseno/prototipos')

def sub1(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a))
    return s.replace(a, b)

CSS = """
/* ===== Cambio mínimo del panel «Con qué filtros» (todo con tokens del :root) ===== */
.filtros{list-style:none;margin:0;padding:0}
.sens{display:inline-flex;align-items:center;gap:5px;margin:var(--sp-2) 0 0;font-size:var(--fs-meta);line-height:1.4;
  background:var(--surface);border:1px solid var(--border-fuerte);border-radius:var(--r-ctrl);padding:2px 8px;color:var(--text)}
.sens .ico{color:var(--text-2)}
.sens b{font-weight:700}
"""

def celda(m):
    cuerpo = m.group(1)
    chips = re.findall(r'<span class="f-chip(?: pers)?">.*?</span></span>|<span class="f-chip">.*?</span>', cuerpo)
    # separar filtros y marca
    pers = re.search(r'<span class="f-chip pers">incluye <b>(.*?)</b></span>', cuerpo)
    normales = re.findall(r'<span class="f-chip">(.*?)</span>(?=<span class="f-chip|$)', cuerpo)
    lis = ''.join(f'<li class="f-chip">{c}</li>' for c in normales)
    lis = lis.replace('plaza <b>2 de 5</b>', 'plaza <b>Querétaro y Celaya</b>')
    marca = ''
    if pers:
        marca = ('<p class="sens"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-shield"/></svg>'
                 f'<span>Dato personal: <b>{pers.group(1)}</b></span></p>')
    return f'<td data-et="Con qué filtros"><ul class="filtros" aria-label="Filtros aplicados">{lis}</ul>{marca}</td>'

def hacer():
    s = SRC
    s = sub1(s, '<title>SIO-DPROMA — Descargas de reportes</title>', '<title>Prototipo bitácora — panel con qué filtros</title>') if '<title>SIO-DPROMA — Descargas de reportes</title>' in s else s
    n0 = s.count('<td data-et="Con qué filtros">')
    s = re.sub(r'<td data-et="Con qué filtros"><span class="filtros">(.*?)</span></td>', celda, s, flags=re.S)
    assert s.count('<ul class="filtros"') == n0 == 5, (n0, s.count('<ul class="filtros"'))
    # el contador de dato personal deja de ser semáforo: es un conteo, no un juicio
    s = sub1(s, 'class="schip c-warn" type="button" aria-pressed="false" data-f="warn"',
             'class="schip c-neutro" type="button" aria-pressed="false" data-f="warn"')
    # la nota ya no explica un color: queda solo la restricción que importa; el icono de escudo se reserva para dato personal
    s = re.sub(r'<p class="nota"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg><span>.*?</span></p>',
               '<p class="nota"><svg class="ico" aria-hidden="true"><use href="#i-book"/></svg><span><b>Un renglón de la bitácora no se edita ni se borra.</b></span></p>', s, flags=re.S)
    s = sub1(s, '</style>\n</head>', CSS + '</style>\n</head>')
    return s

# ------------------------------------------------------------------ página de la regla (3 contextos + antes)
def regla():
    lines = SRC.split('\n')
    tokens = '\n'.join(lines[7:191])   # <style> + :root claro + oscuro (idéntico al de la maqueta)
    assert tokens.lstrip().startswith('<style>') or ':root' in tokens[:40]
    html = f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prototipo marca de sensibilidad</title>
{tokens if tokens.lstrip().startswith('<style>') else '<style>' + tokens}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:400 var(--fs-dense)/1.5 var(--font-ui);padding:var(--sp-6) var(--sp-4)}}
.ico{{width:18px;height:18px;stroke:currentColor;stroke-width:1.6;fill:none;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}}
.ico-xs{{width:11px;height:11px}}
h1{{font-size:var(--fs-title);margin:0 0 var(--sp-4)}}
h2{{font-size:var(--fs-base);margin:var(--sp-6) 0 var(--sp-2)}}
.caja{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-card);padding:var(--sp-4);max-width:720px}}
.tema{{margin-bottom:var(--sp-4)}}
.tema button{{border:1px solid var(--border-2);background:var(--surface);color:var(--text);border-radius:var(--r-ctrl);padding:var(--sp-2) var(--sp-3);font:600 var(--fs-meta) var(--font-ui);min-height:32px}}
/* regla: marca de sensibilidad */
.sens{{display:inline-flex;align-items:center;gap:5px;font-size:var(--fs-meta);line-height:1.4;background:var(--surface);
  border:1px solid var(--border-fuerte);border-radius:var(--r-ctrl);padding:2px 8px;color:var(--text)}}
.sens .ico{{color:var(--text-2)}}
.sens b{{font-weight:700}}
/* antes (cliente): solo para comparar */
.f-chip{{display:inline-flex;align-items:center;gap:5px;font-size:var(--fs-meta);line-height:1.4;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--r-ctrl);padding:2px 8px;color:var(--text-2)}}
.f-chip b{{color:var(--text);font-weight:700}}
.f-chip.pers{{border-color:var(--warn);background:var(--warn-bg);color:var(--warn-ink)}}
.f-chip.pers b{{color:var(--warn-ink)}}
.schip{{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--border-2);background:var(--surface);border-radius:var(--r-pill);padding:5px 12px;font-size:var(--fs-dense);color:var(--text-2);border-style:dashed}}
.schip b{{color:var(--text)}}
dl{{display:grid;grid-template-columns:140px 1fr;gap:var(--sp-2) var(--sp-3);margin:0}}
dt{{color:var(--text-2)}} dd{{margin:0;display:flex;gap:var(--sp-2);align-items:center;flex-wrap:wrap}}
.fila{{display:flex;gap:var(--sp-2);flex-wrap:wrap;align-items:center}}
small.et{{display:block;color:var(--text-3);font-size:var(--fs-meta);margin-bottom:var(--sp-1)}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></symbol></defs></svg>
<h1>Marca de sensibilidad de un dato</h1>
<p class="tema"><button type="button" id="t">Cambiar tema</button></p>
<div class="caja">
<h2 style="margin-top:0">1 · En una celda de tabla</h2>
<small class="et">Antes: ámbar de semáforo</small>
<div class="fila"><span class="f-chip">marca <b>todas</b></span><span class="f-chip pers">incluye <b>razón social y RFC</b></span></div>
<small class="et" style="margin-top:var(--sp-3)">Después: marca de sensibilidad</small>
<div class="fila"><span class="f-chip">marca <b>todas</b></span></div>
<div class="fila" style="margin-top:var(--sp-2)"><span class="sens" id="s1"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-shield"/></svg><span>Dato personal: <b>razón social y RFC</b></span></span></div>
<h2>2 · En un contador</h2>
<div class="fila"><span class="schip"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-shield"/></svg><b>41</b> con dato personal</span></div>
<h2>3 · En una ficha</h2>
<dl><dt>Razón social</dt><dd>Refaccionaria del Altiplano</dd>
<dt>RFC</dt><dd>RAL010101AB1 <span class="sens" id="s3"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-shield"/></svg><span>Dato personal</span></span></dd></dl>
</div>
<script>
(function(){{var r=document.documentElement,b=document.getElementById('t');
b.addEventListener('click',function(){{var o=matchMedia('(prefers-color-scheme: dark)').matches;var t=r.getAttribute('data-theme');var oscuro=t?t==='dark':o;r.setAttribute('data-theme',oscuro?'light':'dark');}});}})();
</script>
</body>
</html>
"""
    return html

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / '54-panel-con-que-filtros.html').write_text(hacer(), encoding='utf-8')
    (OUT / '54-marca-sensibilidad.html').write_text(regla(), encoding='utf-8')
    print('ok')
