#!/usr/bin/env python3
# Opción 1 (mínimo cambio) de las etiquetas de estado: conserva las etiquetas del cliente, pasa la prosa de la celda a `title`
# (como en la entrega de Studio del 8-sep, padron-clientes.html:931) y retira lo que D7 pospone («Por vencer» y su chip).
import sys, re, pathlib
ORIG = pathlib.Path(sys.argv[1]); DEST = pathlib.Path(sys.argv[2])
s = ORIG.read_text(encoding='utf-8')
def sub(viejo, nuevo, n=1):
    global s
    c = s.count(viejo); assert c == n, f'{c} coincidencias: {viejo[:70]!r}'
    s = s.replace(viejo, nuevo)
sub('<title>SIO-DPROMA — Padrón de clientes</title>', '<title>SIO-DPROMA — Padrón de clientes (opción 1: mínimo cambio en estados)</title>')
ICO = lambda n: f'<svg class="ico ico-xs" aria-hidden="true"><use href="#i-{n}"/></svg>'
T_OK = 'Constancia e identificación, revisadas y vigentes. Puede programar y facturar.'
cel = [
 ('p-ok', 'check', 'Los dos', T_OK),
 ('p-warn', 'clock', 'Falta 1', 'Falta la constancia de situación fiscal. Se puede seguir trabajando el cliente; no se le puede programar ni facturar hasta que esté.'),
 ('p-ok', 'check', 'Los dos', T_OK),                 # «Por vencer» retirado (D7)
 ('p-ok', 'check', 'Los dos', T_OK),
 ('p-err', 'alertc', 'Faltan los 2', 'No hay constancia ni identificación. El cliente existe y se puede editar; programarle una instalación, no.'),
 ('p-neutro', 'alert', 'Sin calcular', 'El servidor no pudo calcularlo en esta consulta: no equivale a que falten.'),
]
it = iter(cel)
def f(m):
    c, i, t, ti = next(it)
    return f'<td data-et="Documentos fiscales"><span class="exp" title="{ti}"><span class="pill {c}">{ICO(i)}{t}</span></span></td>'
s, n = re.subn(r'<td data-et="Documentos fiscales">.*?</td>', f, s, flags=re.S); assert n == 6
c2 = re.search(r'<button class="schip c-warn"[^>]*data-f="documento-por-vencer">.*?</button>', s, flags=re.S).group(0)
sub(c2, '')
DEST.write_text(s, encoding='utf-8'); print('escrito', DEST, len(s))
