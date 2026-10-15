#!/usr/bin/env python3
# Genera prototipos/24-tickets-zona-superior.html a partir de la maqueta del cliente (24_tickets.html, sin tocarla).
# Cada sustitución exige exactamente una coincidencia: si la maqueta cambia, el script falla en vez de adivinar.
import sys, pathlib
ORIG = pathlib.Path(sys.argv[1]); DEST = pathlib.Path(sys.argv[2]); MIN = len(sys.argv) > 3 and sys.argv[3] == 'min'
s = ORIG.read_text(encoding='utf-8')

def sub(viejo, nuevo, n=1):
    global s
    c = s.count(viejo)
    assert c == n, f'se esperaban {n} coincidencias y hay {c}: {viejo[:70]!r}'
    s = s.replace(viejo, nuevo)

# 0. título
sub('<title>SIO-DPROMA — Tickets TI</title>', '<title>SIO-DPROMA — Tickets TI (prototipo: zona superior)</title>')

# 1. Cabecera: el relleno inferior lo declara el contenedor (§3.1)
sub('.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0}',
    '.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;padding-bottom:var(--sp-3)}')

# 2. El margen de .banda era para una banda hija directa de .detalle; aquí vive dentro de otro contenedor.
sub('.detalle .banda{margin:var(--sp-4) var(--sp-6) 0}', '.detalle > .banda{margin:var(--sp-4) var(--sp-6) 0}')
sub('@media (max-width:1280px){.detalle .banda{margin-left:var(--sp-4);margin-right:var(--sp-4)}}',
    '@media (max-width:1280px){.detalle > .banda{margin-left:var(--sp-4);margin-right:var(--sp-4)}}')

if MIN:
    # Opción 1 (mínimo cambio): solo la cabecera y el selector del margen; el resto de la maqueta queda como está.
    sub('<title>SIO-DPROMA — Tickets TI (prototipo: zona superior)</title>', '<title>SIO-DPROMA — Tickets TI (opción 1: mínimo cambio)</title>')
    DEST.write_text(s, encoding='utf-8'); print('escrito (min)', DEST, len(s)); sys.exit(0)

# 3. Etiqueta de campo al suelo de 12 px (§2.1)
sub('.campo .et{font-size:10.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--text-3)}',
    '.campo .et{font-size:var(--fs-meta);font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--text-3)}')

# 4. .caja-plazo (bloque de ancho completo) → indicador de plazo con ancho declarado + toggletip (§6.20, §6.23)
ini = s.index('.caja-plazo{display:flex;gap:var(--sp-4)')
fin = s.index('.caja-plazo p b{font-weight:700}') + len('.caja-plazo p b{font-weight:700}')
css_nuevo = '''/* Indicador de plazo: declara su ancho (§6.20, §13.2 «fr acotado»); una sola caja ámbar en la zona alta. */
.resumen-ticket{display:grid;grid-template-columns:minmax(200px,240px) minmax(0,1fr);gap:var(--sp-4);align-items:stretch}
@media (max-width:560px){.resumen-ticket{grid-template-columns:1fr}}
.resumen-ticket .campos{display:flex;flex-wrap:wrap;gap:var(--sp-3) var(--sp-4);align-content:center}
.plazo-ind{position:relative;display:flex;flex-direction:column;justify-content:center;gap:var(--sp-1);
  padding:var(--sp-3) var(--sp-4);border-radius:var(--r-card);background:var(--warn-bg);color:var(--warn-ink)}
.plazo-ind.rojo{background:var(--err-bg);color:var(--err-ink)}
.plazo-ind.verde{background:var(--ok-bg);color:var(--ok-ink)}
.plazo-ind.gris{background:var(--surface-2);color:var(--text-2)}
.plazo-ind .et{font-size:var(--fs-meta);font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding-right:var(--sp-6)}
.plazo-ind .cifra{font-size:var(--fs-title);font-weight:800;line-height:1.15;font-variant-numeric:tabular-nums}
.plazo-ind .fecha{font-size:var(--fs-dense);font-weight:600;font-variant-numeric:tabular-nums}
html[data-plazo="no"] .plazo-ind.con-plazo,html:not([data-plazo="no"]) .plazo-ind.sin-plazo{display:none}
/* Toggletip (§6.23) */
.infob{width:24px;height:24px;padding:0;border:0;border-radius:50%;background:transparent;
  color:var(--text-3);display:grid;place-items:center;cursor:pointer;flex-shrink:0}
.infob:hover,.infob[aria-expanded="true"]{background:var(--surface-2);color:var(--text-2)}
[data-tacto="dedo"] .infob{width:46px;height:46px}
.infob svg{margin-top:0}
.plazo-ind .infob{position:absolute;top:var(--sp-1);right:var(--sp-1);color:inherit}
.plazo-ind .infob:hover,.plazo-ind .infob[aria-expanded="true"]{background:var(--surface);color:var(--text)}
.banda{position:relative}
.banda .infob{margin-left:auto;align-self:center}
.tip{position:absolute;right:0;top:calc(100% + 6px);z-index:30;width:220px;max-width:60vw;
  background:var(--text);color:var(--surface);font:500 var(--fs-meta)/1.5 var(--font-ui);
  border-radius:var(--r-ctrl);padding:var(--sp-2) var(--sp-3);box-shadow:var(--sh-float);text-align:left}'''
s = s[:ini] + css_nuevo + s[fin:]

# 5. Marcado: sprite con i-info, banda neutra bajo las acciones, indicador + campos en una fila
sub('<symbol id="i-receipt"', '<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></symbol><symbol id="i-receipt"')

banda_nueva = '''<div class="banda b-info"><svg class="ico" aria-hidden="true"><use href="#i-info"/></svg><p>Marcarlo resuelto no lo cierra: el cierre lo confirma quien lo reportó.</p><button class="infob" type="button" aria-expanded="false" aria-controls="tip-cierre" aria-describedby="tip-cierre" aria-label="Más información sobre el cierre automático"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-info"/></svg></button><span class="tip" id="tip-cierre" role="tooltip" hidden>Si quien lo reportó no responde, el ticket se cierra solo a los 5 días hábiles.</span></div>
'''
# la banda va al final de .dh, justo bajo los botones que explica
sub('<button class="btn" type="button"><svg class="ico ico-sm" aria-hidden="true"><use href="#i-clock"/></svg>Poner en espera del usuario</button></div>\n</div>',
    '<button class="btn" type="button"><svg class="ico ico-sm" aria-hidden="true"><use href="#i-clock"/></svg>Poner en espera del usuario</button></div>\n' + banda_nueva + '</div>')

i0 = s.index('<div class="caja-plazo">')
i1 = s.index('<div class="campos">')
j1 = s.index('</div>\n\n<p class="descrip">')   # cierre de .campos
campos_viejo = s[i1:j1 + len('</div>')]
campos_nuevo = '''<div class="campos">
<div class="campo"><span class="et">Reporta</span><span class="vl">Mesa de Control · Querétaro</span></div>
<div class="campo"><span class="et">Atiende</span><span class="vl">Alex Rai</span></div>
<div class="campo"><span class="et">Abierto</span><span class="vl tnum">21 ago 2026 · 08:12</span></div>
</div>'''
ind = '''<div class="resumen-ticket">
<div class="plazo-ind ambar con-plazo" role="group" aria-labelledby="pz-et"><span class="et" id="pz-et">Plazo</span><b class="cifra">Vence hoy</b><span class="fecha">24 ago 2026</span><button class="infob" type="button" aria-expanded="false" aria-controls="tip-plazo" aria-describedby="tip-plazo" aria-label="Más información sobre el plazo"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-info"/></svg></button><span class="tip" id="tip-plazo" role="tooltip" hidden>Se fijó al abrir el ticket y no cambia. El sábado y el domingo no cuentan.</span></div>
<div class="plazo-ind gris sin-plazo" role="group" aria-labelledby="pz-et2"><span class="et" id="pz-et2">Lleva abierto</span><b class="cifra">3 días</b><span class="fecha">desde el 21 ago 2026, 08:12</span></div>
''' + campos_nuevo + '\n</div>'
s = s[:i0] + ind + s[j1 + len('</div>'):]

# 6. JS del toggletip (§6.23, reglas 3 y 5) y selector de modo en el andamio
js_tip = '''
(function(){
  function cierra(b,foco){var t=document.getElementById(b.getAttribute('aria-controls'));b.setAttribute('aria-expanded','false');if(t)t.hidden=true;if(foco)b.focus();}
  function abiertos(){return document.querySelectorAll('.infob[aria-expanded="true"]');}
  document.querySelectorAll('.infob').forEach(function(b){
    b.addEventListener('click',function(e){
      e.stopPropagation();
      var yaAbierto=b.getAttribute('aria-expanded')==='true';
      abiertos().forEach(function(o){cierra(o,false);});
      if(!yaAbierto){b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false;}
    });
    b.addEventListener('keydown',function(e){if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){e.stopPropagation();cierra(b,true);}});
  });
  document.addEventListener('click',function(){abiertos().forEach(function(o){cierra(o,false);});});
  document.addEventListener('focusin',function(e){abiertos().forEach(function(o){if(e.target!==o)cierra(o,false);});});
  document.querySelectorAll('.demo [data-plazo]').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.demo [data-plazo]').forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
      if(b.dataset.plazo==='no')document.documentElement.setAttribute('data-plazo','no');else document.documentElement.removeAttribute('data-plazo');
    });
  });
})();
</script>
</body>'''
sub('</script>\n</body>', js_tip)
sub('<button type="button" data-set="error" aria-pressed="false">Error</button>\n</div>',
    '<button type="button" data-set="error" aria-pressed="false">Error</button>\n<span class="div"></span><span class="et-g">PLAZO</span>\n<button type="button" data-plazo="si" aria-pressed="true">Con plazo</button>\n<button type="button" data-plazo="no" aria-pressed="false">Solo antigüedad</button>\n</div>')

DEST.write_text(s, encoding='utf-8')
print('escrito', DEST, len(s), 'bytes')
