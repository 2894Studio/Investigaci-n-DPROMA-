#!/usr/bin/env python3 -I
"""Genera los prototipos como COPIAS parcheadas de las maquetas del cliente (la maqueta original no se toca).
Cada reemplazo exige exactamente N coincidencias: si la maqueta cambia, el script falla en vez de generar algo distinto.
Uso: python3 -I genera.py <carpeta con las maquetas del cliente>
"""
import sys, pathlib, difflib

SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
    '/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/v2zip/Actualizacion-12-10-26')
OUT = pathlib.Path(__file__).resolve().parent


def aplica(txt, parches, nombre):
    for viejo, nuevo, n in parches:
        k = txt.count(viejo)
        assert k == n, f'{nombre}: se esperaban {n} coincidencias y hay {k} para: {viejo[:70]!r}'
        txt = txt.replace(viejo, nuevo)
    return txt


def escribe(nombre, original, nuevo, titulo):
    nuevo = nuevo.replace('<title>', f'<title>[PROTOTIPO {titulo}] ', 1)
    (OUT / nombre).write_text(nuevo, encoding='utf-8')
    dif = list(difflib.unified_diff(original.splitlines(), nuevo.splitlines(), 'cliente', 'prototipo', n=0, lineterm=''))
    (OUT / (nombre.replace('.html', '.diff'))).write_text('\n'.join(dif) + '\n', encoding='utf-8')
    print(nombre, 'líneas de diff:', len([d for d in dif if d[:1] in '+-' and d[:3] not in ('+++', '---')]))


# ───────────────────────────── 47 · Asistente ─────────────────────────────
o47 = (SRC / '47_asistente.html').read_text(encoding='utf-8')

# Parches comunes (los que se EXIGEN): cabecera, destinos, aviso de mensajes nuevos
comunes47 = [
    # §3.1: el relleno inferior lo declara el contenedor
    ('.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0}',
     '.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;padding-bottom:var(--sp-3)}', 1),
    # §10: el destino de un buscador es una <label>, no un <div>
    ('<div class="search"><svg class="ico ico-sm" aria-hidden="true"><use href="#i-search"/></svg><input id="buscar" type="search" placeholder="Buscar en tus conversaciones…" aria-label="Buscar conversaciones"></div>',
     '<label class="search"><svg class="ico ico-sm" aria-hidden="true"><use href="#i-search"/></svg><input id="buscar" type="search" placeholder="Buscar en tus conversaciones…" aria-label="Buscar conversaciones"></label>', 1),
    # §6.4 regla 1: lo que llega se anuncia
    ('<div class="mensajes">', '<div class="mensajes" role="log" aria-label="Mensajes" tabindex="0">', 1),
]

# A · mínimo cambio: un margen y un alto mínimo
A47 = aplica(o47, comunes47 + [
    ('margin:calc(var(--sp-3) * -1) calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)}',
     'margin:var(--sp-3) calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)}', 1),
    ('.fuentes a{font-size:var(--fs-meta);color:var(--link);text-decoration:none;font-weight:600}',
     '.fuentes a{display:flex;align-items:center;min-height:24px;font-size:var(--fs-meta);color:var(--link);text-decoration:none;font-weight:600}', 1),
], 'A47')
escribe('47-asistente-A-minimo.html', o47, A47, 'A mínimo')

# B · recomendado: dos zonas hermanas, sin márgenes negativos; el paso a seguir es un botón
B47 = aplica(o47, comunes47 + [
    ('.msg.ia .tx{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-card);\n  padding:var(--sp-3) var(--sp-4)}',
     '.msg.ia .tx{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-card);overflow:hidden}\n'
     '.msg.ia .tx-cuerpo{padding:var(--sp-3) var(--sp-4)}', 1),
    ('.fuentes{display:flex;flex-direction:column;gap:5px;padding:var(--sp-3) var(--sp-4);\n'
     '  border-top:1px solid var(--border);background:var(--surface-2);border-radius:0 0 var(--r-card) var(--r-card);\n'
     '  margin:calc(var(--sp-3) * -1) calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)}',
     '.fuentes{display:flex;flex-direction:column;gap:var(--sp-1);padding:var(--sp-3) var(--sp-4);\n'
     '  border-top:1px solid var(--border);background:var(--surface-2)}\n'
     '.fuentes--paso{flex-direction:row;flex-wrap:wrap;align-items:center;gap:var(--sp-2)}\n'
     '.fuentes--paso .et{flex:0 0 100%}\n'
     '.fuentes--paso .btn{text-decoration:none}\n'
     '.fuentes--paso .btn:hover{background:var(--surface-hover)}', 1),
    ('.fuentes a{font-size:var(--fs-meta);color:var(--link);text-decoration:none;font-weight:600}\n.fuentes a:hover{text-decoration:underline}',
     '.fuentes a:not(.btn){display:flex;align-items:center;min-height:24px;font-size:var(--fs-meta);color:var(--link);text-decoration:none;font-weight:600}\n'
     '.fuentes a:not(.btn):hover{text-decoration:underline}', 1),
    # marcado: el cuerpo de la respuesta es su propia zona
    ('<div class="tx">\n<p>', '<div class="tx"><div class="tx-cuerpo">\n<p>', 2),
    ('</p>\n<div class="fuentes">', '</p></div>\n<div class="fuentes">', 2),
    ('<div class="fuentes"><span class="et">Para hacerlo</span>', '<div class="fuentes fuentes--paso"><span class="et">Para hacerlo</span>', 1),
    ('<a href="#">Abrir GT-2026-02417</a>', '<a class="btn mini" href="#">Abrir GT-2026-02417</a>', 1),
    ('<a href="#">Abrir GT-2026-02416</a>', '<a class="btn mini" href="#">Abrir GT-2026-02416</a>', 1),
    # §10: el isotipo lleva sus medidas en el <use>, sin viewBox repetido en el <svg> (avatar y logo del cromo)
    ('<svg width="16" height="15" viewBox="740 0 970 932" aria-hidden="true"><use href="#dproma-mark"/></svg>',
     '<svg width="16" height="15" aria-hidden="true"><use href="#dproma-mark" width="16" height="15"/></svg>', 2),
    ('<svg width="44" height="42" viewBox="740 0 970 932" aria-hidden="true"><use href="#dproma-mark"/></svg>',
     '<svg width="44" height="42" aria-hidden="true"><use href="#dproma-mark" width="44" height="42"/></svg>', 1),
    # ARQ-CROMO: la sombra del cajón solo existe con el cajón abierto (cerrado, se cuela en el borde izquierdo a ≤860 px)
    ('    transform:translateX(-101%);transition:transform var(--dur-base) var(--ease-out);\n    box-shadow:var(--sh-modal)}\n  :root[data-menu="abierto"] .side{transform:none}',
     '    transform:translateX(-101%);transition:transform var(--dur-base) var(--ease-out)}\n  :root[data-menu="abierto"] .side{transform:none;box-shadow:var(--sh-modal)}', 1),
], 'B47')
escribe('47-asistente-B-recomendado.html', o47, B47, 'B recomendado')


# C · opcional: B + historial en una sola fila horizontal a ≤1024 px (devuelve altura al hilo)
C47 = aplica(B47, [
    ('.fuentes--paso .btn:hover{background:var(--surface-hover)}',
     '.fuentes--paso .btn:hover{background:var(--surface-hover)}\n'
     '@media (max-width:1024px){\n'
     '  .hist{max-height:none}\n'
     '  .hist ol{display:flex;overflow-x:auto;overflow-y:hidden;flex:none}\n'
     '  .hist li{flex:0 0 220px;border-right:1px solid var(--border)}\n'
     '  .hist li a{border-bottom:0;height:100%}\n'
     '}', 1),
], 'C47')
escribe('47-asistente-C-historial-compacto.html', o47, C47, 'C historial compacto')

# ───────────────────────────── 28 · Mi día ─────────────────────────────
o28 = (SRC / '28_instalador_mi_dia.html').read_text(encoding='utf-8')

# A · mínimo: la línea que corrige §3.1 (lo que la observación pide)
A28 = aplica(o28, [
    ('.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0}',
     '.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;padding-bottom:var(--sp-3)}', 1),
], 'A28')
escribe('28-mi-dia-A-minimo.html', o28, A28, 'A mínimo')

# B · recomendado: A + token faltante + aire al final de la lista + el resumen no sobrevive a su estado (§6.4)
B28 = aplica(A28, [
    ('--sp-4: 16px;\n  --sp-6: 24px;', '--sp-4: 16px; --sp-5: 20px;\n  --sp-6: 24px;', 1),
    ('.tel{display:flex;flex-direction:column;gap:var(--sp-4);padding:var(--sp-4) var(--sp-6) 0}',
     '.tel{display:flex;flex-direction:column;gap:var(--sp-4);padding:var(--sp-4) var(--sp-6) var(--sp-4)}', 1),
    ('@media (max-width:860px){.tel{padding:var(--sp-3) var(--sp-3) 0;gap:var(--sp-3)}}',
     '@media (max-width:860px){.tel{padding:var(--sp-3) var(--sp-3) var(--sp-3);gap:var(--sp-3)}}', 1),
    ('.p4-t .resumen b{color:var(--text)}',
     '.p4-t .resumen b{color:var(--text)}\n'
     '.main:has(#contenido:not([data-state="ok"])) .p4-t .resumen{display:none}', 1),
    # ARQ-CROMO: la sombra del cajón solo existe con el cajón abierto (cerrado, se cuela en el borde izquierdo a ≤860 px)
    ('    transform:translateX(-101%);transition:transform var(--dur-base) var(--ease-out);\n    box-shadow:var(--sh-modal)}\n  :root[data-menu="abierto"] .side{transform:none}',
     '    transform:translateX(-101%);transition:transform var(--dur-base) var(--ease-out)}\n  :root[data-menu="abierto"] .side{transform:none;box-shadow:var(--sh-modal)}', 1),
], 'B28')
escribe('28-mi-dia-B-recomendado.html', o28, B28, 'B recomendado')

# C · opcional (decisión de diseño): B + el bloqueo del día es una etiqueta de estado en la cabecera y la fecha sube a ella
#     (se retira la tarjeta «Hoy · viernes 21 de agosto», que repite «2 citas»)
C28 = aplica(B28, [
    ('.p4-t .resumen b{color:var(--text)}',
     '.p4-t .resumen b{color:var(--text)}\n.p4-t .resumen .pill b{color:inherit}', 1),
    ('<span class="resumen"><b>2</b> citas · <b>7 h</b> de trabajo · <b>1</b> con material incompleto</span>',
     '<span class="resumen">Viernes 21 de agosto · <b>2</b> citas · <b>7 h</b> de trabajo <span class="pill p-block"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-pause"/></svg><b>1</b> con material incompleto</span></span>', 1),
    ('<article class="tarjeta-tel">\n<div class="cab"><svg class="ico" aria-hidden="true"><use href="#i-clock"/></svg><h2>Hoy · viernes 21 de agosto</h2><span class="n tnum">2 citas</span></div>\n</article>',
     '<h2 class="sr">Citas de hoy</h2>', 1),
], 'C28')
escribe('28-mi-dia-C-primer-pliegue.html', o28, C28, 'C primer pliegue')

# D · estados de una respuesta (no los dibujó el cliente): B + una respuesta pendiente y una que falló. Solo componentes existentes.
AV = '<span class="av" aria-hidden="true"><svg width="16" height="15" aria-hidden="true"><use href="#dproma-mark" width="16" height="15"/></svg></span>'
EXTRA = (
    '<div class="msg yo"><span class="av" aria-hidden="true">AR</span><span class="cu">\n<span class="qn">Tú · hoy 10:35</span>\n'
    '<div class="tx"><p>¿Y cuántas órdenes siguen sin instalador?</p></div>\n</span></div>\n\n'
    '<div class="msg ia" aria-busy="true">' + AV + '<span class="cu">\n<span class="qn">Asistente · consultando…</span>\n'
    '<div class="tx"><div class="tx-cuerpo" role="status" aria-label="El asistente está consultando">'
    '<span class="skel" style="width:92%"></span><span class="skel" style="width:64%;margin-top:var(--sp-2)"></span></div></div>\n</span></div>\n\n'
    '<div class="msg yo"><span class="av" aria-hidden="true">AR</span><span class="cu">\n<span class="qn">Tú · hoy 10:36</span>\n'
    '<div class="tx"><p>Resume la cobranza de Marca A.</p></div>\n</span></div>\n\n'
    '<div class="msg ia">' + AV + '<span class="cu">\n<span class="qn">Asistente · hoy 10:36</span>\n'
    '<div class="tx"><div class="tx-cuerpo"><p><b>No pude responder.</b> Tu pregunta se guardó y nada del sistema cambió.</p>'
    '<p class="ref-err" translate="no">Referencia del error: ASI-20260821-1036</p></div>\n'
    '<div class="fuentes fuentes--paso"><span class="et">Qué hacer</span><button class="btn mini" type="button">Reintentar</button></div></div>\n</span></div>\n\n'
)
D47 = aplica(B47, [
    ('</span></div>\n\n</div>\n\n<div class="compositor">', '</span></div>\n\n' + EXTRA + '</div>\n\n<div class="compositor">', 1),
    ('.fuentes--paso .btn{text-decoration:none}', '.fuentes--paso .btn{text-decoration:none}\n.msg .ref-err{font-size:var(--fs-meta);color:var(--text-3);font-variant-numeric:tabular-nums}', 1),
], 'D47')
escribe('47-asistente-D-estados-respuesta.html', o47, D47, 'D estados de respuesta')
