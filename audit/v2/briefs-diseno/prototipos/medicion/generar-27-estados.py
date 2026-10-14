#!/usr/bin/env python3
# Genera prototipos/27-etiquetas-de-estado.html a partir de la maqueta del cliente (27_padron_clientes.html, sin tocarla).
import sys, re, pathlib
ORIG = pathlib.Path(sys.argv[1]); DEST = pathlib.Path(sys.argv[2])
s = ORIG.read_text(encoding='utf-8')
def sub(viejo, nuevo, n=1):
    global s
    c = s.count(viejo); assert c == n, f'se esperaban {n} coincidencias y hay {c}: {viejo[:80]!r}'
    s = s.replace(viejo, nuevo)

sub('<title>SIO-DPROMA — Padrón de clientes</title>', '<title>SIO-DPROMA — Padrón de clientes (prototipo: etiquetas de estado)</title>')

# 1. Celdas de «Documentos fiscales»: una etiqueta por estado y, si hace falta, una línea con lo que falta (§6.11 reglas 7 y 8; §6.12 regla 9)
ICO = lambda n: f'<svg class="ico ico-xs" aria-hidden="true"><use href="#i-{n}"/></svg>'
ok   = f'<span class="exp"><span class="pill p-ok">{ICO("check")}Completos</span></span>'
pend1= f'<span class="exp"><span class="pill p-warn">{ICO("clock")}Pendientes</span><span class="falta">Falta <b>constancia</b></span></span>'
pend2= f'<span class="exp"><span class="pill p-warn">{ICO("clock")}Pendientes</span><span class="falta">Faltan <b>constancia</b> e <b>identificación</b></span></span>'
sinc = f'<span class="exp"><span class="pill p-neutro">{ICO("alert")}Sin calcular</span><span class="falta">No se pudo comprobar</span></span>'
orden = [ok, pend1, ok, ok, pend2, sinc]     # GAV, CVB, ACA (Por vencer → Completos, D7), Laura, RDA, DPA
it = iter(orden)
s, n = re.subn(r'<td data-et="Documentos fiscales">.*?</td>', lambda m: f'<td data-et="Documentos fiscales">{next(it)}</td>', s, flags=re.S)
assert n == 6, n

# 2. Cabecera de la columna con toggletip (§6.23, §8 nivel 2)
tip = ('<span class="thx">Documentos fiscales<button class="infob" type="button" aria-expanded="false" aria-controls="tip-docs" aria-describedby="tip-docs" '
       'aria-label="Más información sobre documentos fiscales">' + ICO('info') + '</button>'
       '<span class="tip" id="tip-docs" role="tooltip" hidden>Opcionales para dar de alta, obligatorios para programar o facturar. «Sin calcular» significa que no se pudo comprobar, no que falten.</span></span>')
sub('<th scope="col">Documentos fiscales</th>', f'<th scope="col">{tip}</th>')

# 3. Chips: «sin los dos documentos» → «con documentos pendientes»; «por vencer» fuera (D7)
c1 = re.search(r'<button class="schip c-err"[^>]*data-f="sin-documentos">.*?</button>', s, flags=re.S).group(0)
sub(c1, f'<button class="schip c-warn" type="button" aria-pressed="false" data-f="documentos-pendientes">{ICO("clock")}<b class="tnum">42</b> con documentos pendientes</button>')
c2 = re.search(r'<button class="schip c-warn"[^>]*data-f="documento-por-vencer">.*?</button>', s, flags=re.S).group(0)
sub(c2, '')

# 4. Las dos notas que explicaban estados salen de la pantalla (su contenido vive en el toggletip de la cabecera)
n1 = re.search(r'<p class="nota"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg><span><b>Los dos documentos son opcionales.*?</p>\n', s, flags=re.S).group(0)
sub(n1, '')
n2 = re.search(r'<p class="nota"><svg class="ico" aria-hidden="true"><use href="#i-alert"/></svg><span><b>«Sin calcular» no es «faltan»:.*?</p>\n', s, flags=re.S).group(0)
sub(n2, '')

# 5. Símbolo, CSS y JS del toggletip
sub('<symbol id="i-receipt"', '<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></symbol><symbol id="i-receipt"')
css = '''/* Toggletip (§6.23) en la cabecera de «Documentos fiscales» */
.infob{width:24px;height:24px;padding:0;border:0;border-radius:50%;background:transparent;
  color:var(--text-3);display:grid;place-items:center;cursor:pointer;flex-shrink:0}
.infob:hover,.infob[aria-expanded="true"]{background:var(--surface-2);color:var(--text-2)}
[data-tacto="dedo"] .infob{width:46px;height:46px}
.thx{display:inline-flex;align-items:center;gap:var(--sp-1);white-space:normal}
.thx .infob{margin:-4px 0}
.tip{position:absolute;right:0;top:calc(100% + 6px);z-index:30;width:220px;max-width:60vw;
  background:var(--text);color:var(--surface);font:500 var(--fs-meta)/1.5 var(--font-ui);
  border-radius:var(--r-ctrl);padding:var(--sp-2) var(--sp-3);box-shadow:var(--sh-float);text-align:left;
  white-space:normal;text-transform:none;letter-spacing:normal}
</style>'''
sub('</style>\n</head>', css + '\n</head>')
js = '''
(function(){
  function cierra(b,foco){var t=document.getElementById(b.getAttribute('aria-controls'));b.setAttribute('aria-expanded','false');if(t)t.hidden=true;if(foco)b.focus();}
  function abiertos(){return document.querySelectorAll('.infob[aria-expanded="true"]');}
  document.querySelectorAll('.infob').forEach(function(b){
    b.addEventListener('click',function(e){
      e.stopPropagation();
      var ya=b.getAttribute('aria-expanded')==='true';
      abiertos().forEach(function(o){cierra(o,false);});
      if(!ya){b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false;}
    });
    b.addEventListener('keydown',function(e){if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){e.stopPropagation();cierra(b,true);}});
  });
  document.addEventListener('click',function(){abiertos().forEach(function(o){cierra(o,false);});});
  document.addEventListener('focusin',function(e){abiertos().forEach(function(o){if(e.target!==o)cierra(o,false);});});
})();
</script>
</body>'''
sub('</script>\n</body>', js)
DEST.write_text(s, encoding='utf-8'); print('escrito', DEST, len(s))
