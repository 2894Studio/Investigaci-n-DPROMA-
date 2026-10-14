#!/usr/bin/env python3
# Genera los prototipos de la agenda (34) a partir de COPIAS de la maqueta del cliente.
# No toca la maqueta original. Salida: briefs-diseno/prototipos/
import re, sys, pathlib
import os
MAQUETAS = pathlib.Path(os.environ.get('MAQUETAS', '/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/v2zip/Actualizacion-12-10-26'))
SRC = (MAQUETAS / '34_instaladores.html').read_text(encoding='utf-8')
OUT = pathlib.Path('/home/user/Investigaci-n-DPROMA-/audit/v2/briefs-diseno/prototipos')

def sub1(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a))
    return s.replace(a, b)

def cabecera(s, etiqueta, descr):
    s = sub1(s, '<title>SIO-DPROMA — Instaladores y agenda</title>',
             f'<title>Prototipo agenda — {etiqueta}</title>')
    return s

# ---------------------------------------------------------------- piezas comunes
LIBRE_VIEJO = '<span class="libre">—</span>'
LIBRE_NUEVO = '<span class="libre">—<span class="sr">sin visitas</span></span>'
CARGA_VIEJO = '<span style="font-size:10.5px;color:var(--text-3)">órdenes abiertas</span>'
CARGA_NUEVO = '<span class="et-carga">órdenes abiertas</span>'

def semana_sin_asignar(s):
    """Saca la visita «Sin instalador» de la fila de M. Ríos y la pone en una fila propia «Sin asignar»."""
    tile = '<a class="vt sin" href="#"><b>10:00</b><span>Sin instalador</span></a>'
    assert s.count(tile) == 1
    # en la fila de Mauricio el miércoles queda hueco
    s = sub1(s, '<td data-et="Miérc. 26"><div class="cel">' + tile + '</div></td>',
             '<td data-et="Miérc. 26"><div class="cel">' + LIBRE_NUEVO + '</div></td>')
    filas = []
    dias = ['Lunes 24', 'Martes 25', 'Miérc. 26', 'Jueves 27', 'Viernes 28', 'Sábado 29', 'Domingo 30']
    tds = ''
    for d in dias:
        cls = ' class="dom-col"' if d.startswith('Domingo') else ''
        cont = ('<div class="cel">' + tile + '</div>') if d == 'Miérc. 26' else ''
        tds += f'<td{cls} data-et="{d}">{cont}</td>'
    fila = ('<tr class="sin-asignar"><th scope="row" data-et="Instalador y carga"><span class="dos"><b>Sin asignar</b>'
            '<small>1 visita sin instalador</small></span></th>' + tds + '</tr>')
    return sub1(s, '<tbody><tr>\n<th scope="row" data-et="Instalador y carga"><span class="dos"><b>Jonathan',
                '<tbody>' + fila + '<tr>\n<th scope="row" data-et="Instalador y carga"><span class="dos"><b>Jonathan')

def a11y_libres(s):
    s = s.replace(LIBRE_VIEJO, LIBRE_NUEVO)
    s = s.replace(CARGA_VIEJO, CARGA_NUEVO)
    return s

# vista de día: celdas de continuación (sin fusionar filas) y columna «Sin asignar»
def dia_continuacion(s):
    horas = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00']
    personas = ['J. Olvera', 'R. Beltrán', 'M. Ríos', 'S. Elizalde']
    # (persona, hora de inicio, horas, cliente, sucursal, sin)
    citas = [('J. Olvera', '08:00', 4, 'Vértice del Bajío', 'Centro · Querétaro', False),
             ('R. Beltrán', '09:00', 5, 'Refaccionaria del Altiplano', 'Matriz · Celaya', False),
             ('Sin asignar', '10:00', 3, 'Sin instalador asignado', 'Cerro Azul · San Juan del Río', True)]
    cols = personas[:2] + ['Sin asignar'] + [personas[3]]
    # M. Ríos queda sin citas ese día; «Sin asignar» ocupa su sitio al final para no cambiar el orden de las personas
    cols = ['J. Olvera', 'R. Beltrán', 'M. Ríos', 'S. Elizalde', 'Sin asignar']
    thead = '<thead><tr><th scope="col">Hora</th>' + ''.join(f'<th scope="col">{c}</th>' for c in cols) + '</tr></thead>'
    cuerpo = ''
    for i, h in enumerate(horas):
        fila = f'<tr>\n<th scope="row" data-et="Hora">{h}</th>\n'
        for c in cols:
            contenido = ''
            for (p, ini, dur, cli, suc, sin) in citas:
                if p != c:
                    continue
                i0 = horas.index(ini)
                hasta = f'{int(ini[:2]) + dur:02d}:00'
                if i == i0:
                    cls = 'bloque-cita sin' if sin else 'bloque-cita'
                    contenido = (f'<span class="{cls}"><b>{cli}</b><span>{suc}</span>'
                                 f'<span class="dur">{ini} – {hasta} · {dur} h</span></span>')
                elif i0 < i < i0 + dur:
                    cls = 'ocupa sin' if sin else 'ocupa'
                    contenido = f'<span class="{cls}"><span class="sr">Sigue ocupado hasta las {hasta}: {cli}</span></span>'
            fila += f'<td data-et="{c}"><div class="cont-col">{contenido}</div></td>'
        cuerpo += fila + '\n</tr>'
    tabla = ('<table><caption>Agenda del lunes 24 de agosto, hora por hora y por instalador</caption>' + thead
             + '<tbody>' + cuerpo + '</tbody></table>')
    ini = s.index('<div class="dia-caja"><table>')
    fin = s.index('</table></div>', ini) + len('</table></div>')
    return s[:ini] + '<div class="dia-caja">' + tabla + '</div>' + s[fin:]

CSS_PISO = """
/* piso de 12 px (§2.1): lo que el PDF del cliente ya declara */
.agenda thead th{font-size:var(--fs-meta)}
.agenda .dos small{font-size:var(--fs-meta)}
.agenda .et-carga{font-size:var(--fs-meta);color:var(--text-3)}
.vt{font-size:var(--fs-meta)}
.libre{font-size:var(--fs-meta)}
.agenda tr.sin-asignar th{padding-top:var(--sp-3);padding-bottom:var(--sp-3);vertical-align:middle}
.dia-caja thead th{font-size:var(--fs-meta)}
.dia-caja tbody th{font-size:var(--fs-meta)}
.bloque-cita{font-size:var(--fs-meta)}
.bloque-cita .dur{font-size:var(--fs-meta)}
"""
CSS_ANCHO = """
.agenda thead th:first-child{width:176px}
.agenda table{min-width:960px}
.vt span{white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere}
.agenda .dos b{white-space:normal}
.dia-caja table{min-width:820px}
"""
CSS_SCROLL = """
/* la cabecera sticky de §6.11 no se pega con overflow-x:auto: la agenda se desplaza dentro de su caja */
.agenda{overflow:auto;max-height:min(70vh,640px)}
"""
CSS_CONT = """
.ocupa{display:block;min-height:19px;border-radius:var(--r-ctrl);background:var(--surface-2);border-left:3px solid var(--serie-1)}
.ocupa.sin{background:var(--err-bg);border-left-color:var(--err)}
"""
CSS_A_MIN = CSS_PISO + CSS_ANCHO + CSS_SCROLL + CSS_CONT

# ---------------------------------------------------------------- A′
def hacer_aprime():
    s = SRC
    s = cabecera(s, 'A′ (agenda del cliente + cambio mínimo)', '')
    s = sub1(s, '--text-3: #66717F;', '--text-3: #5C6675;')   # claro; el oscuro (#8B96A6) no se toca
    s = a11y_libres(s)
    s = semana_sin_asignar(s)
    s = dia_continuacion(s)
    s = sub1(s, '</style>\n</head>', CSS_A_MIN + '</style>\n</head>')
    return s

# ---------------------------------------------------------------- C
CSS_C = """
/* ===== C — propuesta previa de agenda (v1, «§6.24», no vigente en 2.15.0) ===== */
.vt b{font-size:var(--fs-dense)}
.rango{display:flex;align-items:center;gap:var(--sp-2);margin-left:auto}
.rango .iconbtn{width:36px;height:36px}
.agenda th[data-laborable="no"],.agenda td[data-laborable="no"]{background:var(--pause-bg)}
"""
def hacer_c():
    s = SRC
    s = cabecera(s, 'C (propuesta previa de agenda)', '')
    s = a11y_libres(s)
    s = semana_sin_asignar(s)
    s = sub1(s, '</style>\n</head>', CSS_PISO + '</style>\n</head>')
    # el calendario laborable es un dato, no una clase del componente
    s = s.replace('class="dom-col"', 'data-laborable="no"')
    s = s.replace('<th scope="col" data-laborable="no">', '<th scope="col" data-laborable="no">')
    s = s.replace('.agenda th.dom-col,.agenda td.dom-col{background:var(--pause-bg)}', '')
    # no se ofrece un rango sin vista detrás: se retira «Quincena»
    s = sub1(s, '<button type="button" aria-pressed="false">Quincena</button>', '')
    # control de rango con etiqueta concreta y navegación anterior/siguiente
    s = sub1(s, '<span class="n tnum">24 – 30 ago 2026</span></header>\n<div class="agenda">',
             '<span class="n tnum rango-et">24 – 30 ago 2026</span>'
             '<span class="rango"><button class="iconbtn" type="button" aria-label="Semana anterior"><span aria-hidden="true">‹</span></button>'
             '<button class="iconbtn" type="button" aria-label="Semana siguiente"><span aria-hidden="true">›</span></button></span></header>\n<div class="agenda">')
    # región viva + foco al cambiar de vista; vista de día por omisión por debajo de 860 px
    s = sub1(s, '<div class="v-semana">', '<p class="sr" id="vivo" role="status" aria-live="polite"></p>\n<div class="v-semana">')
    js = """
<script>
(function(){
var ag=document.getElementById('ag'),vivo=document.getElementById('vivo');
function poner(v,anunciar){
  ag.setAttribute('data-vista',v);
  document.querySelectorAll('.seg [data-vista]').forEach(function(o){o.setAttribute('aria-pressed',String(o.dataset.vista===v));});
  if(anunciar){
    var h=ag.querySelector('.v-'+v+' h2'); if(h){h.setAttribute('tabindex','-1');h.focus();}
    vivo.textContent=v==='dia'?'Vista de día: lunes 24 de agosto':'Vista de semana: 24 al 30 de agosto';
  }
}
document.querySelectorAll('.seg [data-vista]').forEach(function(b){b.addEventListener('click',function(){poner(b.dataset.vista,true);});});
if(window.matchMedia('(max-width:860px)').matches)poner('dia',false);
})();
</script>
"""
    s = sub1(s, '</body>', js + '</body>')
    s = sub1(s, '</style>\n</head>', CSS_C + '</style>\n</head>')
    return s

# ---------------------------------------------------------------- B (§13.9)
CSS_B = """
/* ===== B — §13.9 aplicado a la vista de día: alto del bloque = duración × escala ===== */
.dia-b{--esc:.9px;--eje:64px;overflow-x:auto}
.dia-b .malla{min-width:760px;display:grid;grid-template-columns:var(--eje) repeat(var(--cols,4),minmax(0,1fr))}
.dia-b .cab{position:sticky;top:0;z-index:3;background:var(--surface);border-bottom:1px solid var(--border);
  padding:var(--sp-2) var(--sp-3);font-size:var(--fs-meta);font-weight:700;letter-spacing:.04em;color:var(--text-2);text-transform:uppercase}
.dia-b .eje{position:relative;height:calc(480 * var(--esc))}
.dia-b .eje span{position:absolute;right:var(--sp-3);transform:translateY(-50%);font-size:var(--fs-meta);font-weight:700;color:var(--text-3);font-variant-numeric:tabular-nums}
.dia-b .eje span:first-child{transform:none}
.dia-b .col{position:relative;height:calc(480 * var(--esc));margin:0;padding:0;list-style:none;border-left:1px solid var(--border);
  background:repeating-linear-gradient(to bottom,transparent 0,transparent calc(60 * var(--esc) - 1px),var(--border) calc(60 * var(--esc) - 1px),var(--border) calc(60 * var(--esc)))}
.dia-b .col > li{position:absolute;left:var(--sp-1);right:var(--sp-1);top:calc(var(--ini) * var(--esc));height:calc(var(--dur) * var(--esc))}
.dia-b .ev{display:flex;flex-direction:column;gap:2px;height:100%;overflow:hidden;box-sizing:border-box;
  padding:4px var(--sp-2);border-radius:var(--r-ctrl);background:var(--surface-2);border-left:3px solid var(--serie-1);
  color:inherit;text-decoration:none;font-size:var(--fs-meta);line-height:1.4}
.dia-b .ev.sin{background:var(--err-bg);border-left-color:var(--err);color:var(--err-ink)}
.dia-b .ev > *{flex-shrink:0}               /* §13.9, parte 1: nada se encoge por debajo de su line-height */
.dia-b .ev .cli{font-size:var(--fs-dense);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dia-b .ev .suc{color:var(--text-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dia-b .ev .dur{color:var(--text-3);font-variant-numeric:tabular-nums}
.dia-b .ev.sin .suc,.dia-b .ev.sin .dur{color:var(--err-ink)}
.dia-b[data-sinplan] .ev > *{flex-shrink:1}  /* control: el comportamiento por omisión de flex, sin plan de contenido */
"""
def bloque_b(ini_min, dur, cli, suc, sin=False, estres=False):
    h0 = 7 * 60
    ini = ini_min - h0
    hi = f'{ini_min // 60:02d}:{ini_min % 60:02d}'
    fin_min = ini_min + dur
    hf = f'{fin_min // 60:02d}:{fin_min % 60:02d}'
    durtxt = f'{dur // 60} h' if dur % 60 == 0 else (f'{dur} min')
    cls = 'ev sin' if sin else 'ev'
    est = ' data-estres="1"' if estres else ''
    return (f'<li style="--ini:{ini};--dur:{dur}"{est}><a class="{cls}" href="#" data-dur="{dur}" '
            f'aria-label="{cli}, {suc}, de {hi} a {hf} ({durtxt})">'
            f'<span class="cli" data-prio="3">{cli}</span><span class="suc" data-prio="2">{suc}</span>'
            f'<span class="dur" data-prio="1">{hi} – {hf} · {durtxt}</span></a></li>')

def hacer_b():
    s = SRC
    s = cabecera(s, 'B (§13.9 aplicado a la vista de día)', '')
    personas = ['J. Olvera', 'R. Beltrán', 'M. Ríos', 'S. Elizalde']
    reales = {0: [(8*60, 240, 'Vértice del Bajío', 'Centro · Querétaro', False)],
              1: [(9*60, 300, 'Refaccionaria del Altiplano', 'Matriz · Celaya', False)],
              2: [(10*60, 180, 'Sin instalador asignado', 'Cerro Azul · San Juan del Río', True)],
              3: []}
    # banco de pruebas (NO es dato del cliente): duraciones cortas para forzar el plan de contenido
    estres = {0: [(12*60, 45, 'Visita corta A', 'Sucursal de prueba', False), (13*60, 90, 'Visita B', 'Sucursal de prueba', False)],
              1: [(7*60, 60, 'Visita corta C', 'Sucursal de prueba', False), (8*60, 30, 'Visita D', 'Sucursal de prueba', False)],
              2: [(7*60, 90, 'Visita E', 'Sucursal de prueba', False), (13*60, 60, 'Visita F', 'Sucursal de prueba', False)],
              3: [(8*60, 30, 'Visita G', 'Sucursal de prueba', False), (10*60, 45, 'Visita H', 'Sucursal de prueba', False),
                  (11*60, 60, 'Visita I', 'Sucursal de prueba', False), (12*60, 120, 'Visita J', 'Sucursal de prueba', False)]}
    cab = '<div class="cab">Hora</div>' + ''.join(f'<h3 class="cab" id="pb{i}">{p}</h3>' for i, p in enumerate(personas))
    eje = '<div class="eje" aria-hidden="true">' + ''.join(
        f'<span style="top:calc({i*60} * var(--esc))">{7+i:02d}:00</span>' for i in range(8)) + '</div>'
    cols = ''
    for i, p in enumerate(personas):
        lis = ''.join(bloque_b(*b) for b in reales[i]) + ''.join(bloque_b(*b, estres=True) for b in estres[i])
        cols += f'<ul class="col" role="list" aria-labelledby="pb{i}">{lis}</ul>'
    html = ('<div class="dia-b" id="diab"><div class="malla" role="group" aria-label="Agenda del lunes 24 de agosto, hora por hora y por instalador">'
            + cab + eje + cols + '</div></div>')
    ini = s.index('<div class="dia-caja"><table>')
    fin = s.index('</table></div>', ini) + len('</table></div>')
    s = s[:ini] + html + s[fin:]
    # §13.9 parte 2: retirar líneas completas por prioridad, DESPUÉS de insertar el bloque en el documento
    js = """
<script>
(function(){
var q=new URLSearchParams(location.search);
var caja=document.getElementById('diab');
if(q.get('sinplan'))caja.setAttribute('data-sinplan','1');
if(!q.get('estres'))caja.querySelectorAll('li[data-estres]').forEach(function(li){li.remove();});
function ajusta(){
  if(q.get('sinplan'))return;
  caja.querySelectorAll('.ev').forEach(function(ev){
    var ls=[].slice.call(ev.children).sort(function(a,b){return a.dataset.prio-b.dataset.prio;});
    ls.forEach(function(l){l.hidden=false;});
    for(var i=0;i<ls.length-1 && ev.scrollHeight>ev.clientHeight+0.5;i++){ls[i].hidden=true;}
  });
}
/* la vista de día arranca oculta (display:none): se mide cuando el bloque ya tiene caja, no antes */
if(window.ResizeObserver)new ResizeObserver(function(){ajusta();}).observe(caja);
document.fonts.ready.then(ajusta);
})();
</script>
"""
    s = sub1(s, '</body>', js + '</body>')
    s = sub1(s, '</style>\n</head>', CSS_B + '</style>\n</head>')
    return s

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / '34-A-prima-cambio-minimo.html').write_text(hacer_aprime(), encoding='utf-8')
    (OUT / '34-B-dia-proporcional-13-9.html').write_text(hacer_b(), encoding='utf-8')
    (OUT / '34-C-propuesta-previa.html').write_text(hacer_c(), encoding='utf-8')
    print('ok')
