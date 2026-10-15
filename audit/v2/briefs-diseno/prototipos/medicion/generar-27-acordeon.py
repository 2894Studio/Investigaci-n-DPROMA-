#!/usr/bin/env python3
# Genera prototipos/27-acordeon-sucursales.html a partir de la maqueta del cliente (27_padron_clientes.html, sin tocarla).
import sys, re, pathlib
ORIG = pathlib.Path(sys.argv[1]); DEST = pathlib.Path(sys.argv[2])
s = ORIG.read_text(encoding='utf-8')

def sub(viejo, nuevo, n=1):
    global s
    c = s.count(viejo); assert c == n, f'se esperaban {n} coincidencias y hay {c}: {viejo[:80]!r}'
    s = s.replace(viejo, nuevo)

sub('<title>SIO-DPROMA — Padrón de clientes</title>', '<title>SIO-DPROMA — Padrón de clientes (prototipo: acordeón de sucursales)</title>') if '<title>SIO-DPROMA — Padrón de clientes</title>' in s else None

# ---------- CSS: sustituye el bloque .hijas / .suc-lista (líneas 658-672 de la maqueta) ----------
i0 = s.index('.hijas td{background:var(--surface-2);padding:0 var(--sp-4) var(--sp-4)}')
i1 = s.index('.suc-lista .der{margin-left:auto;display:flex;gap:var(--sp-2);align-items:center;flex-wrap:wrap}') + len('.suc-lista .der{margin-left:auto;display:flex;gap:var(--sp-2);align-items:center;flex-wrap:wrap}')
css = '''/* Fila hija de sucursales (§6.15). El panel declara su propio ancho de lectura: no hereda el del colspan.
   Sin tarjeta dentro de la tabla (§6.3): una banda --surface-2 con el riel de acento de la fila madre. */
.hijas > td{padding:0;overflow:visible;background:var(--surface-2);box-shadow:inset 3px 0 0 var(--accent)}
tbody tr:has(> td .suc-btn[aria-expanded="true"]) > th{box-shadow:inset 3px 0 0 var(--accent)}
.suc-lista{list-style:none;max-width:560px}
.suc-lista li{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:var(--sp-1) var(--sp-4);
  padding:var(--sp-2) var(--sp-4) var(--sp-2) calc(var(--sp-4) + 15px + var(--sp-3));
  border-bottom:1px solid var(--border);font-size:var(--fs-dense)}
.suc-lista li:last-child{border-bottom:0}
.suc-lista li:hover{background:var(--surface)}
.suc-lista .nom{display:flex;flex-direction:column;gap:2px;min-width:0}
.suc-lista .nom .l1{display:flex;align-items:center;gap:var(--sp-2);flex-wrap:wrap}
.suc-lista .nom b{font-weight:600}
.suc-lista .nom .dir{color:var(--text-2);font-size:var(--fs-meta)}
.suc-lista .acc{display:flex;align-items:center;justify-content:flex-end}'''
s = s[:i0] + css + s[i1:]
sub('.suc-btn{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--border);background:var(--surface);\n  color:var(--text);border-radius:var(--r-ctrl);padding:3px 9px 3px 7px;cursor:pointer;',
    '.suc-btn{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--border);background:var(--surface);min-height:28px;\n  color:var(--text);border-radius:var(--r-ctrl);padding:3px 9px 3px 7px;cursor:pointer;')

# ---------- CSS: modo tarjeta (<860 px) ----------
sub('''  .pad .hijas td{display:block;padding:0}
  .pad .hijas td::before{display:none}
  .pad .hijas .caja{border:0;border-radius:0}''',
'''  .pad .hijas td{display:block;padding:0}
  .pad .hijas td::before{display:none}
  .suc-lista{max-width:none}
  .suc-lista li{grid-template-columns:1fr;padding-left:var(--sp-4)}
  .suc-lista .acc{justify-content:flex-start}''')

# ---------- Marcado: filas madre + filas hijas ----------
SUC = {
 'gav': [('Centro · Querétaro','Av. Constituyentes Pte. 1204, 76000 Querétaro, Qro.',None),
         ('Juriquilla · Querétaro','Blvd. Villas del Mesón 220, 76230 Querétaro, Qro.',None),
         ('Satélite · Naucalpan','Circuito Novelistas 88, 53100 Naucalpan, Méx.',None),
         ('Celaya · Guanajuato','Av. Tecnológico 88, 38010 Celaya, Gto.',None)],
 'cvb': [('Irapuato · Guanajuato','Blvd. Díaz Ordaz 1450, 36660 Irapuato, Gto.','bloq'),
         ('León · Guanajuato','Av. López Mateos 3020, 37530 León, Gto.','bloq')],
 'aca': [('Matriz · Poza Rica','Carr. Poza Rica–Tuxpan km 4, 93230 Poza Rica, Ver.',None)],
 'rda': [('Matriz · San Luis Potosí','Av. Salvador Nava 780, 78290 San Luis Potosí, S.L.P.','bloq'),
         ('Soledad · San Luis Potosí','Carr. a Matehuala 155, 78430 Soledad, S.L.P.','bloq'),
         ('Aguascalientes','Av. Aguascalientes Sur 601, 20328 Aguascalientes, Ags.','baja')],
 'dpa': [('Matriz · Toluca','Paseo Tollocan 1201, 50140 Toluca, Méx.',None)],
}
PILL = {
 'bloq': '<span class="pill p-warn"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-clock"/></svg>Bloqueada: faltan documentos</span>',
 'baja': '<span class="pill p-pause"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-pause"/></svg>De baja</span>',
}
def hijas(clave, nombre, abierta):
    lis = []
    for n, d, est in SUC[clave]:
        pill = PILL.get(est, '')
        lis.append(f'<li><span class="nom"><span class="l1"><b translate="no">{n}</b>{pill}</span><span class="dir" translate="no">{d}</span></span>'
                   f'<span class="acc"><button class="btn mini" type="button" aria-label="Ver órdenes de {n}">Ver órdenes</button></span></li>')
    ocul = '' if abierta else ' hidden'
    return (f'<tr class="hijas" id="suc-{clave}"{ocul}><td colspan="7" data-et="Sucursales"><ul class="suc-lista" aria-label="Sucursales de {nombre}">'
            + ''.join(lis) + '</ul></td></tr>')

tb0 = s.index('<tbody>') + len('<tbody>'); tb1 = s.index('</tbody>')
filas = re.findall(r'<tr[^>]*>.*?</tr>', s[tb0:tb1], flags=re.S)
assert len(filas) == 7, len(filas)
nuevo = []
for f in filas:
    if 'class="hijas"' in f:        # la fila hija de la maqueta se reconstruye con todas las demás
        continue
    m = re.search(r'class="suc-btn"[^>]*aria-controls="suc-(\w+)"', f)
    if m:
        clave = m.group(1)
        nombre = re.search(r'<b translate="no">([^<]+)</b>', f).group(1)
        n = len(SUC[clave]); sing = 'sucursal' if n == 1 else 'sucursales'
        abierta = (clave == 'gav')
        f = re.sub(r'<button class="suc-btn"[^>]*>',
                   f'<button class="suc-btn" type="button" aria-expanded="{"true" if abierta else "false"}" aria-controls="suc-{clave}" aria-label="{n} {sing} de {nombre}">', f)
        nuevo.append(f); nuevo.append(hijas(clave, nombre, abierta))
    else:
        nuevo.append(f)
s = s[:tb0] + ''.join(nuevo) + s[tb1:]

# ---------- JS: abre/cierra, Escape devuelve el foco al botón (§6.15) ----------
js = '''
(function(){
  document.querySelectorAll('.suc-btn[aria-controls]').forEach(function(bt){
    var hija=document.getElementById(bt.getAttribute('aria-controls'));
    if(!hija)return;
    bt.addEventListener('click',function(){
      var abierto=bt.getAttribute('aria-expanded')==='true';
      bt.setAttribute('aria-expanded',String(!abierto));
      hija.hidden=abierto;
    });
    function cierra(e){
      if(e.key!=='Escape'||bt.getAttribute('aria-expanded')!=='true')return;
      e.stopPropagation();
      bt.setAttribute('aria-expanded','false');hija.hidden=true;bt.focus();
    }
    bt.addEventListener('keydown',cierra);
    hija.addEventListener('keydown',cierra);
  });
})();
</script>
</body>'''
sub('</script>\n</body>', js)
DEST.write_text(s, encoding='utf-8'); print('escrito', DEST, len(s))
