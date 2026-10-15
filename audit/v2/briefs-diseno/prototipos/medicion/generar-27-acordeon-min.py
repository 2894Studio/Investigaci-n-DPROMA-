#!/usr/bin/env python3
# Opción 1 (mínimo cambio) del acordeón: conserva el dibujo del cliente (tarjeta, encabezado, pills) y solo
# (a) da id real y `hidden` a las cinco filas hijas, (b) añade el manejador (el del original de Studio, padron-clientes.html:1503),
# (c) arregla el nombre accesible, (d) acota el ancho de la tarjeta a 560 px para que pill y botón no se vayan al borde del colspan.
import sys, re, pathlib
ORIG = pathlib.Path(sys.argv[1]); DEST = pathlib.Path(sys.argv[2])
s = ORIG.read_text(encoding='utf-8')
def sub(viejo, nuevo, n=1):
    global s
    c = s.count(viejo); assert c == n, f'{c} coincidencias: {viejo[:70]!r}'
    s = s.replace(viejo, nuevo)
sub('<title>SIO-DPROMA — Padrón de clientes</title>', '<title>SIO-DPROMA — Padrón de clientes (opción 1: mínimo cambio)</title>')
sub('</style>\n</head>', '.hijas .caja{max-width:560px}\n</style>\n</head>')
OK = '<span class="pill p-ok"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-check"/></svg>Puede recibir órdenes</span>'
BL = '<span class="pill p-warn"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-clock"/></svg>Bloqueada: faltan documentos</span>'
SUC = {  # los estados son los de la entrega de Studio del 8-sep (web/entregables/propuestas/padron-clientes.html:952-1012)
 'cvb': [('Irapuato · Guanajuato','Blvd. Díaz Ordaz 1450, 36660 Irapuato, Gto.',OK),('León · Guanajuato','Av. López Mateos 3020, 37530 León, Gto.',OK)],
 'aca': [('Matriz · Poza Rica','Carr. Poza Rica–Tuxpan km 4, 93230 Poza Rica, Ver.',OK)],
 'rda': [('Matriz · San Luis Potosí','Av. Salvador Nava 780, 78290 San Luis Potosí, S.L.P.',BL),('Soledad · San Luis Potosí','Carr. a Matehuala 155, 78430 Soledad, S.L.P.',BL),('Aguascalientes','Av. Aguascalientes Sur 601, 20328 Aguascalientes, Ags.',BL)],
 'dpa': [('Matriz · Toluca','Paseo Tollocan 1201, 50140 Toluca, Méx.',BL)],
}
def hija(clave):
    lis = ''.join(f'<li><span class="nom"><b translate="no">{n}</b><span>{d}</span></span><span class="der">{p}<button class="btn mini" type="button">Ver órdenes</button></span></li>' for n, d, p in SUC[clave])
    return (f'<tr class="hijas" id="suc-{clave}" hidden><td colspan="7" data-et="Razón social / RFC"><div class="caja">'
            f'<div class="enc"><svg class="ico ico-sm" aria-hidden="true"><use href="#i-pin"/></svg>Sucursales de esta razón social</div><ul class="suc-lista">{lis}</ul></div></td></tr>')
tb0 = s.index('<tbody>') + 7; tb1 = s.index('</tbody>')
filas = re.findall(r'<tr[^>]*>.*?</tr>', s[tb0:tb1], flags=re.S)
nuevo = []
for f in filas:
    m = re.search(r'class="suc-btn"[^>]*aria-controls="suc-(\w+)"', f)
    if m and 'class="hijas"' not in f:
        clave = m.group(1)
        nombre = re.search(r'<b translate="no">([^<]+)</b>', f).group(1)
        n = {'gav': 4, 'cvb': 2, 'aca': 1, 'rda': 3, 'dpa': 1}[clave]
        f = re.sub(r'aria-label="Ver las? \d+ sucursal(es)? de ', f'aria-label="Ver {"la sucursal" if n == 1 else "las " + str(n) + " sucursales"} de ', f)
        nuevo.append(f)
        if clave != 'gav': nuevo.append(hija(clave))
    else:
        nuevo.append(f)
s = s[:tb0] + ''.join(nuevo) + s[tb1:]
# el original de Studio (padron-clientes.html:1503-1522): clic alterna; Escape cierra y devuelve el foco
js = '''
(function(){
  document.querySelectorAll('.suc-btn[aria-controls]').forEach(function(bt){
    var hija=document.getElementById(bt.getAttribute('aria-controls'));
    if(!hija)return;
    bt.addEventListener('click',function(){var a=bt.getAttribute('aria-expanded')==='true';bt.setAttribute('aria-expanded',String(!a));hija.hidden=a;});
    function cierra(e){if(e.key!=='Escape'||bt.getAttribute('aria-expanded')!=='true')return;e.stopPropagation();bt.setAttribute('aria-expanded','false');hija.hidden=true;bt.focus();}
    bt.addEventListener('keydown',cierra);hija.addEventListener('keydown',cierra);
  });
})();
</script>
</body>'''
sub('</script>\n</body>', js)
DEST.write_text(s, encoding='utf-8'); print('escrito', DEST, len(s))
