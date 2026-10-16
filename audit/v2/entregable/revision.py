"""Genera «Revisión de pantallas SIO DPROMA»: una sola página HTML que sirve como web y, impresa, como PDF.

Uso: python3 -I revision.py            (escribe web/entregables/revision-de-pantallas.html)
Las imágenes viven en web/entregables/img/revision/ (las genera imagenes.cjs).
Los árboles de accesibilidad del cambio 1 salen de ev-datos.json (medido con Playwright en 27_padron_clientes a 1000 px).
"""
import html, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
WEB = os.path.join(REPO, 'web', 'entregables')
IMG = '/entregables/img/revision/'
MED = json.load(open(os.path.join(REPO, 'web', 'entregables', 'img', 'revision', '_medidas.json')))
ARIA = json.load(open(os.path.join(AQUI, 'ev-datos.json')))
BAR = json.load(open(os.path.join(AQUI, '..', 'mediciones', 'v2', 'barrido.json')))
E = html.escape
TITULO = 'Revisión de pantallas SIO DPROMA'
PDF = 'SIO-DPROMA-revision-de-pantallas-oct2026.pdf'

# ---------------------------------------------------------------- piezas
def img(clave, alt):
    w, h = MED[clave]
    return f'<img src="{IMG}{clave}.jpg" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy">'

def panel(rotulo, cuerpo, tipo):
    return f'<div class="lado {tipo}"><h4>{rotulo}</h4>{cuerpo}</div>'

def par(antes, despues, apilado=False):
    return f'<div class="par{" apilado" if apilado else ""}">{antes}{despues}</div>'

def a_d(clave, alt_a, alt_d, rot_a, rot_d, apilado=False):
    return par(panel(rot_a, img(clave + '-antes', alt_a), 'antes'), panel(rot_d, img(clave + '-despues', alt_d), 'despues'), apilado)

def pre(t):
    return f'<pre class="cod">{E(t)}</pre>'

def arbol(clave):
    return '\n'.join(ARIA[clave].split('\n')[:9])

TAGS = {'pide': 'Se pide', 'rec': 'Recomendado', 'dis': 'Propuesta de diseño', 'menor': 'Menor'}
cambios = []  # (parte, dict)

def cambio(parte, titulo, tag, donde, que, porque=None, visual='', cod=None, comprueba=None, extra=()):
    cambios.append((parte, dict(titulo=titulo, tag=tag, donde=donde, que=que, porque=porque, visual=visual, cod=cod, comprueba=comprueba, extra=extra)))

def archivos(lista):
    return ' '.join(f'<code>{a}</code>' for a in lista)

# ================================================================ A · SE PIDE
A = 'A'
cambio(A, 'El menú lateral dice a dónde lleva cada enlace', 'pide',
  'La regla <code>.side .et{display:none}</code> está en 36 archivos, y en 35 de ellos los enlaces del menú no llevan nombre propio. Lista completa, con línea, en el anexo.',
  'Entre 861 y 1100 px la barra lateral se reduce a iconos y los quince enlaces del menú se quedan sin nombre. Quien navega con lector de pantalla oye «enlace» quince veces seguidas y no sabe a dónde va ninguno.',
  '<code>.side .et{display:none}</code> quita el texto de la vista y también del árbol de accesibilidad, y los enlaces <code>.it</code> no llevan <code>aria-label</code> ni <code>title</code>. El sistema pide que la etiqueta no desaparezca (§7.2).',
  par(panel('Antes — lo que anuncia un lector de pantalla', pre(arbol('ariaantes')), 'antes'), panel('Después — con el texto oculto solo a la vista', pre(arbol('ariadespues')), 'despues')),
  '.side .et{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}\n/* o, en cada enlace: <a class="it" aria-label="Padrón de clientes" …> */',
  'A 1000 px, <code>ariaSnapshot()</code> del <code>.side</code> debe devolver <code>link "Tablero"</code>, <code>link "Padrón de clientes"</code>… y ningún <code>link:</code> vacío. Medido en <code>27_padron_clientes</code>.')

cambio(A, 'El icono del botón verde deja de verse gris', 'pide',
  'La regla descendiente <code>.state .ico{…}</code> está en 21 de las 50 pantallas. El fallo se midió en ' + archivos(['22', '24', '26', '32', '51', '58']) + '. Lista completa, con línea, en el anexo.',
  'En el estado de error de gestoría, el botón verde «Reintentar» lleva un icono gris que casi desaparece sobre el verde.',
  '<code>.state .ico</code> alcanza a cualquier <code>.ico</code> del bloque y no solo al grande que cuelga del estado, así que el icono pequeño del botón hereda el gris. El PDF de cambios lo da por corregido (C3); en estos archivos la regla antigua sigue ahí.',
  a_d('obs01', 'Estado de error de gestoría: el botón Reintentar con el icono gris sobre el verde', 'El mismo botón con el icono blanco', 'Antes — icono gris, 1,03:1', 'Después — icono blanco, 4,89:1'),
  '/* antes */\n.state .ico{width:30px;height:30px;color:var(--text-3)}\n\n/* después (y .esp > .ico en el catálogo 26) */\n.state > .ico{width:30px;height:30px;color:var(--text-3)}',
  'El icono del botón mide 4,89:1 contra el verde. El mínimo para un gráfico es 3:1.')

cambio(A, 'El gris del texto auxiliar llega a 4,5:1', 'pide',
  '29 de las 50 pantallas declaran <code>--text-3: #66717F</code>; las otras 20 ya traen <code>#5C6675</code>. El fallo se midió en ' + archivos(['02', '04', '13', '24', '26', '30', '33', '34', '36']) + '. Lista completa, con línea, en el anexo.',
  'El texto auxiliar (rótulos pequeños, el departamento bajo un nombre) queda por debajo del mínimo cuando cae sobre el fondo de una fila con el cursor encima, o sobre el fondo rosado de un aviso de error. Casos medidos: «Referencia: SYNC-0119-ERR-408» en <code>04</code> (4,14:1, línea 281), la hora de las alertas bajo el cursor en <code>02</code> y <code>30</code> y el SKU bajo el cursor en <code>36</code> (4,21:1), y <code>.cuando</code> y <code>.quien</code> en <code>33</code> (4,21:1 y 4,24:1).',
  'El token conserva el valor anterior. <code>_sio-tokens.css</code>, que viene en el mismo paquete, ya declara <code>#5C6675</code> y lo documenta con 4,93:1.',
  par(panel('Antes — <code>#66717F</code> sobre <code>--surface-2</code>', '<div class="muestra" style="background:#E7EDF3;color:#66717F">Texto auxiliar de ejemplo · <b>4,21:1</b> · no llega a 4,5:1</div>', 'antes'),
      panel('Después — <code>#5C6675</code> sobre <code>--surface-2</code>', '<div class="muestra" style="background:#E7EDF3;color:#5C6675">Texto auxiliar de ejemplo · <b>4,93:1</b> · cumple</div>', 'despues')),
  '--text-3:#5C6675;',
  'Sobre <code>--surface-2</code> pasa de 4,21:1 a 4,93:1; sobre <code>--bg</code>, de 4,61:1 a 5,41:1.')

cambio(A, 'Las fuentes dejan de pedirse a Google', 'pide',
  '12 archivos: ' + archivos(['01', '02', '03', '04', '05', '06', '08', '10', '11', '12', '13', '14']) + '.',
  'Si Google no responde, el texto se pinta con la fuente de respaldo y nadie se entera. El sistema retiró esos <code>&lt;link&gt;</code> por eso (D116).',
  'Estos archivos conservan el <code>&lt;link&gt;</code> a <code>fonts.googleapis.com</code> que las demás pantallas ya sustituyeron por <code>@font-face</code>.',
  '',
  "@font-face{font-family:'Inter';font-style:normal;font-weight:400 700;font-display:swap;\n  src:url('../../apps/web/public/fuentes/inter-variable.woff2') format('woff2')}\n@font-face{font-family:'Michroma';font-style:normal;font-weight:400;font-display:swap;\n  src:url('../../apps/web/public/fuentes/michroma.woff2') format('woff2')}",
  'El archivo no debe contener <code>fonts.googleapis.com</code> ni <code>fonts.gstatic.com</code>. El <code>@font-face</code> es el de <code>27_padron_clientes</code>, líneas 9 y 10.')

cambio(A, 'Cada campo del formulario tiene un identificador único', 'pide',
  'Tres archivos: <code>58_altas_como_modal</code>, <code>59_editar_cliente</code> y <code>21_ficha_cliente</code>. Es el resultado de buscar identificadores repetidos en las 50 pantallas.',
  'En <code>58</code>, los 14 <code>id</code> del formulario «Nuevo cliente» (<code>rs</code>, <code>rfc</code>, <code>tipo</code>, <code>cp</code>, <code>reg</code>, <code>dom</code>, <code>csf</code>, <code>idr</code>, <code>grp</code>, <code>mar</code>, <code>per</code>, <code>rol</code>, <code>cor</code>, <code>tel</code>) se repiten en la versión de teléfono. Cada <code>label for</code> resuelve al primero, así que 12 de los 14 controles del teléfono se quedan sin nombre. En <code>59</code>, <code>nombre-legal</code> y <code>rfc-ro</code> aparecen cuatro veces cada uno, y el <code>label for</code> resuelve al primero. En <code>21</code>, <code>tope-CORREO</code>, <code>tope-TELEFONO</code>, <code>tope-DIRECCION</code> (destinos de <code>aria-describedby</code>) y <code>l-DIRECCION-16</code> aparecen dos veces; el efecto es menor porque el contenido repetido es idéntico.',
  None, '',
  '/* en la versión de teléfono */\n<label for="rs-tel">Razón social</label>\n<input id="rs-tel" …>',
  '<code>document.querySelectorAll(\'[id]\')</code> no debe devolver identificadores repetidos (§11).')

cambio(A, 'Los bordes de campos y casillas se distinguen del fondo', 'pide',
  '<code>55_verificacion_pedido</code> · <code>.ren .caja</code> · línea 665, y los campos de nueve pantallas más (tabla de abajo).',
  'Las casillas sin marcar de <code>55</code> casi se funden con el fondo, y son justo las que el instalador necesita ver para saber qué le falta. En las otras nueve pantallas, el borde de buscadores, listas y cuadros de texto da entre 1,3:1 y 1,5:1 contra la tarjeta que los contiene: sin el borde, el campo no se ve.',
  'Todas pintan el borde con <code>--border</code> o <code>--border-2</code>, que es el borde de una tarjeta. El sistema tiene <code>--border-ctrl</code> (3,06:1) para el control cuya única frontera es el borde (§1.1). Seis archivos ya lo declaran y no lo usan (<code>07</code>, <code>35</code>, <code>37</code>, <code>38</code>, <code>40</code>, <code>50</code>); <code>33</code>, <code>36</code>, <code>42</code>, <code>43</code>, <code>44</code> y <code>45</code> no traen los tokens de la versión 2.15.0 y hay que declararlo primero.',
  a_d('ev55', 'Tres renglones sin marcar con la casilla en gris claro', 'Los mismos renglones con la casilla en gris oscuro', 'Antes — borde a 1,70:1', 'Después — borde a 3,1:1')
  + '<table class="mini"><thead><tr><th>Pantalla</th><th>Regla</th><th class="r">Línea</th><th class="r">Hoy</th></tr></thead><tbody>'
  '<tr><td><code>55</code></td><td><code>.ren .caja</code></td><td class="r">665</td><td class="r">1,70:1</td></tr>'
  '<tr><td><code>07</code></td><td><code>.in</code> (campos de texto)</td><td class="r">263</td><td class="r">1,50:1 y 1,32:1 en solo lectura</td></tr>'
  '<tr><td><code>35</code>, <code>36</code>, <code>37</code></td><td><code>.search</code> (buscador)</td><td class="r">336 · 331 · 334</td><td class="r">1,40:1 claro, 1,24:1 oscuro</td></tr>'
  '<tr><td><code>38</code>, <code>42</code>, <code>43</code>, <code>44</code>, <code>45</code></td><td><code>.ctrl input, .ctrl select, .ctrl textarea, .btn</code></td><td class="r">583 · 581</td><td class="r">1,41:1 claro, 1,24:1 oscuro</td></tr></tbody></table>',
  '/* antes */\n.ren .caja{… border:2px solid var(--border-2); …}\n.ctrl input,.ctrl select,.ctrl textarea{border:1px solid var(--border); …}\n\n/* después. Si el archivo no declara --border-ctrl, se añade junto a --border, con los valores del §1.1:\n   claro rgba(27,36,48,.5) · oscuro rgba(231,236,242,.37) */\n.ren .caja{… border:2px solid var(--border-ctrl); …}\n.ctrl input,.ctrl select,.ctrl textarea{border:1px solid var(--border-ctrl); …}',
  'El borde de cada control pasa de 1,3–1,7:1 a 3,06:1 contra su fondo (mínimo 3:1 para un control). Los botones secundarios de <code>.ctrl .btn</code> llevan el mismo borde y se corrigen con la misma línea.')

cambio(A, 'El contador de Asistencia se lee con claridad', 'pide',
  '<code>13_panel_asistencia_rhl</code> · <code>.it .n</code> · línea 95.',
  'El «4» junto a Asistencia es el número que le dice a RHL si hay incidencias por dictaminar. Con texto casi negro sobre rojo, a 10,5 px, cuesta leerlo.',
  'La regla fija <code>color:#2A1512</code> sobre el rojo <code>rgb(194,66,56)</code>: 3,40:1. Con <code>#FAFCFD</code> (el <code>--chrome-alerta-ink</code> del sistema) sube a 4,94:1.',
  a_d('ev13', 'Menú lateral con el contador 4 en texto oscuro sobre rojo', 'El mismo contador con texto claro', 'Antes — 3,40:1', 'Después — 4,94:1'),
  '/* antes */\n.it .n{margin-left:auto;background:var(--err);color:#2A1512;…}\n\n/* después */\n.it .n{margin-left:auto;background:var(--err);color:#FAFCFD;…}',
  'El contador pasa de 3,40:1 a 4,94:1 (mínimo 4,5:1 para texto normal).')

cambio(A, 'Los formularios del diálogo desplazan en lugar de aplastarse', 'pide',
  '<code>58_altas_como_modal</code> · <code>.modal .seccion</code> · línea 692.',
  'En el diálogo «Nuevo cliente» las secciones se encogen y se montan unas sobre otras. El campo «Tipo de cliente» desaparece y «Domicilio fiscal» queda recortado. La página cuya misión es enseñar qué formulario cabe en un diálogo muestra formularios con la mitad de los campos tapados.',
  '<code>.modal .cuerpo</code> es una columna flex con <code>overflow-y:auto</code>, pero sus <code>.seccion</code> pueden encogerse, así que nunca hay nada que desplazar: <code>scrollHeight</code> y <code>clientHeight</code> miden lo mismo, 538 px. Con <code>flex-shrink:0</code> el contenido mide 819 px y el cuerpo desplaza.',
  a_d('ev58', 'Diálogo Nuevo cliente con las secciones montadas y campos tapados', 'El mismo diálogo con todos los campos completos', 'Antes — secciones aplastadas', 'Después — con <code>flex-shrink:0</code>', apilado=False),
  '/* antes */\n.modal .seccion{border:0;padding:0;margin:0}\n\n/* después */\n.modal .seccion{border:0;padding:0;margin:0;flex-shrink:0}',
  '<code>.modal .cuerpo</code> pasa de <code>scrollHeight</code> 538 a 819 px con <code>clientHeight</code> 538: ahora desplaza. Los campos de correo y teléfono, además, caen fuera del selector <code>.ctrl input[…]</code> y miden 19 px de alto.')

cambio(A, 'La página de diálogos deja de recomendar lo que ya se decidió no hacer', 'pide',
  '<code>58_altas_como_modal</code> · aviso del 28 de septiembre, D1.',
  'El aviso fija que el alta de cliente es una página. <code>58</code> sigue proponiendo «modal en escritorio y página en el teléfono» para ella, sin ninguna marca en el HTML de que quedó superada: esa supresión solo vive en <code>FICHAS_TECNICAS.md</code>. Quien abra <code>58</code> para decidir se encuentra una respuesta distinta de la que ya se tomó.',
  'Sigue vigente para las otras cuatro altas (CFE, vehicular, gestoría y orden de instalación).',
  '',
  None,
  'La sección «Nuevo cliente» lleva una marca visible de «Superada por D1» o se retira la recomendación.')

cambio(A, 'El paso en curso del envío se lee con claridad', 'pide',
  '<code>29_instalador_orden</code> · <code>.paso-envio .ahora</code> · línea 742.',
  'En la tarjeta de fotos, el paso en curso del envío («2 · enviando 62 %») sale en verde sobre el fondo gris de la tarjeta. Es lo que le dice al instalador si la foto ya salió, y con luz de exterior cuesta leerlo.',
  '<code>--accent</code> es el color de las acciones, no el del texto: da 4,35:1 en tema claro y 3,85:1 en oscuro. Para texto verde el sistema tiene <code>--link</code>, que sobre el mismo fondo da 5,41:1 y 7,06:1.',
  par(panel('Antes — <code>--accent</code> sobre <code>--surface-2</code>', '<div class="muestra" style="background:#E7EDF3;color:#3E7A4C"><b>2 · enviando 62 %</b> · <b>4,35:1</b> · no llega a 4,5:1</div>', 'antes'),
      panel('Después — <code>--link</code> sobre <code>--surface-2</code>', '<div class="muestra" style="background:#E7EDF3;color:#2F6B3C"><b>2 · enviando 62 %</b> · <b>5,41:1</b> · cumple</div>', 'despues')),
  '/* antes */\n.paso-envio .ahora{color:var(--accent);font-weight:700}\n\n/* después */\n.paso-envio .ahora{color:var(--link);font-weight:700}',
  'El texto pasa de 4,35:1 a 5,41:1 en claro y de 3,85:1 a 7,06:1 en oscuro (mínimo 4,5:1).')

cambio(A, 'Con movimiento reducido, la conversación de Dprimi no desaparece', 'pide',
  '<code>10_dprimi_asistente</code> · <code>.enter</code> · líneas 337 y 339.',
  'Quien tiene activado «reducir movimiento» en su sistema abre la pantalla y no ve ninguna de las cuatro burbujas: toda la conversación queda transparente.',
  'La regla que quita la animación (línea 337) está escrita antes que <code>.enter{opacity:0;…}</code> (línea 339), con la misma especificidad, así que gana la segunda. Como la animación está anulada, nada lleva la opacidad a 1. Con la preferencia desactivada la pantalla se ve bien, por eso no salta a la vista.',
  a_d('m11', 'Conversación de Dprimi con el movimiento reducido activado: el panel está vacío', 'La misma conversación con las cuatro burbujas visibles', 'Antes — no se ve nada', 'Después — se ve la conversación', apilado=True),
  '/* antes: la regla de reducción va ANTES de .enter{opacity:0} */\n@media (prefers-reduced-motion:reduce){ .enter{animation:none !important;opacity:1;transform:none} }\n.enter{opacity:0;transform:translateY(6px);animation:enter … forwards}\n\n/* después: se mueve DESPUÉS */\n.enter{opacity:0;transform:translateY(6px);animation:enter … forwards}\n@media (prefers-reduced-motion:reduce){ .msg.enter{animation:none;opacity:1;transform:none} }',
  'Con <code>prefers-reduced-motion: reduce</code>, <code>getComputedStyle(.msg).opacity</code> pasa de 0 a 1 en las cuatro burbujas. Medido en Chromium; con la preferencia desactivada no cambia nada.')

# ================================================================ B · PROPUESTAS
B = 'B'
cambio(B, 'El padrón con todos los ajustes a la vez', 'dis',
  '<code>27_padron_clientes</code>. Prototipo sobre el archivo real, que se entrega a pedido.',
  'Suma el acordeón de sucursales, los estados de documentos por eje, el aire bajo la cabecera, el buscador a 24 px, las acciones de fila ancladas a la derecha y la retirada del banner de duplicados (D8) y del chip «por vencer» (D7), que el aviso del 28 de septiembre deja pospuestos.',
  'A 1280 px, «Ver órdenes» está a la vista en 0 de 4 filas y los botones de fila completos son 6 de 18. Con los ajustes, 4 de 4 y 18 de 18. A 1024 px, de 0 de 4 y 0 de 18 a 4 de 4 y 18 de 18.',
  a_d('p27', 'Padrón de clientes tal como llega en el archivo, con banner de duplicados y chip por vencer', 'Padrón de clientes con acordeón, estados por eje y acciones ancladas', 'Antes — 1440 px', 'Después — 1440 px', apilado=True),
  None,
  'La columna de acciones anclada a la derecha es una propuesta sin brief de diseño propio. Por debajo de 1331 px la tabla no cabe junto a la barra lateral y la última columna, la de acciones, queda fuera. Sin resolver: «Acciones» alineada con su casilla, y el botón flotante, que sigue tapando parte de la última fila.',
  ('Viable con condiciones',))

cambio(B, 'El acordeón de sucursales abre y se lee', 'dis',
  '<code>27_padron_clientes</code> · <code>button.suc-btn[aria-controls]</code> · línea 799.',
  'Hoy cuatro de los cinco botones apuntan con <code>aria-controls</code> a ids que no existen (<code>suc-cvb</code>, <code>suc-aca</code>, <code>suc-rda</code>, <code>suc-dpa</code>), ningún script maneja <code>.suc-btn</code> y solo una fila tiene su <code>tr.hijas</code>. En la que funciona, el contenido vive en un <code>&lt;td colspan="7"&gt;</code> y lo que se alinea a la derecha cae fuera de la vista a 1280 px.',
  'La propuesta: cada fila hija ocupa el ancho visible de la tabla, con las líneas divisorias hasta el final y «Ver órdenes» al final de cada fila. El estado de la sucursal se muestra solo cuando está bloqueada; hoy dice «Puede recibir órdenes» en las cuatro y no aporta. El ancho se fija al área visible para que el botón no se salga al deslizar.',
  a_d('s27a', 'Fila de razón social expandida: el contenido queda a la derecha y se sale de la vista', 'Filas hijas a todo el ancho con Ver órdenes al final de cada una', 'Antes — 1280 px', 'Después — 1280 px', apilado=True),
  '.tabla-caja{container-type:inline-size}\n.suc-lista{list-style:none;position:sticky;left:0;width:100cqw}',
  '«Ver órdenes» a la vista a 1280 px: de 0 de 4 a 4 de 4. Brief de diseño: <code>27-acordeon-sucursales</code>, que se entrega a pedido.',
  ('Viable',))

cambio(B, 'Los estados de documentos dicen una sola cosa', 'dis',
  '<code>27_padron_clientes</code> · columna «Documentos fiscales».',
  'La celda mezcla un estado con un párrafo («Falta la constancia de situación fiscal. Se puede seguir trabajando con el cliente; no se le puede programar ni facturar hasta que esté») y usa cinco estados distintos, entre ellos «Por vencer», que D7 pospone.',
  'Un estado por eje: Completos, Pendientes o Sin calcular. El documento que falta se escribe en una línea corta bajo la etiqueta. «Por vencer» se dibuja cuando D7 deje de estar pospuesta.',
  a_d('s27e', 'Tabla del padrón con estados como Los dos, Falta 1, Por vencer y Faltan los 2, cada uno con un párrafo', 'La misma tabla con Completos, Pendientes y Sin calcular y una línea de texto', 'Antes — cinco estados y párrafos', 'Después — un estado por eje', apilado=True),
  None,
  'Brief de diseño: <code>27-etiquetas-de-estado</code>, que se entrega a pedido.',
  ('Viable con condiciones',))

cambio(B, 'Tickets TI: un solo bloque ámbar', 'dis',
  '<code>24_tickets</code> · <code>.detalle .banda</code> línea 560 · <code>.caja-plazo</code>.',
  'La cabecera del detalle apila dos cajas amarillas, de 420 y 366 caracteres. La segunda describe una regla de permisos con el color de «vence pronto», cuando nada vence.',
  'Tres causas apiladas: el selector <code>.detalle .banda</code> pone margen a cualquier banda y se suma al padding del cuerpo; <code>.caja-plazo</code> reinventa un aviso que <code>.banda.b-warn</code> ya cubre; y los textos superan por mucho el tope de 140 caracteres y una frase (§8). La propuesta deja un solo bloque ámbar, el del plazo, con ancho propio junto a los datos del ticket; la regla de cierre pasa a una banda neutra de una frase y el resto a un aviso que se abre al pulsar.',
  a_d('t24', 'Detalle de un ticket con dos cajas amarillas apiladas', 'Detalle con un bloque ámbar de plazo y una banda neutra', 'Antes — dos cajas', 'Después — un bloque de plazo', apilado=True),
  None,
  'Condición: resolver qué manda sobre el plazo. La ficha de la tanda 3 dice que el reloj de plazo salió y que la antigüedad va en gris; la de la tanda 4 dice que tickets conserva su semáforo de plazo; el archivo dibuja el plazo. Brief de diseño: <code>24-tickets-zona-superior</code>, que se entrega a pedido.',
  ('Viable con condiciones',))

cambio(B, 'Mi día: la barra superior respira', 'dis',
  '<code>28_instalador_mi_dia</code> · <code>.p4-t</code> · línea 314.',
  'La barra que abre la pantalla no tiene aire debajo: el título y el resumen, donde vive el aviso de material incompleto, quedan pegados a la línea divisoria, con 12 px de aire arriba y ninguno abajo. Es la pantalla que el instalador mira de pie y con sol.',
  '<code>.p4-t</code> lleva <code>padding-bottom:0</code> a la espera de que una fila hermana cierre el bloque, y en Mi día esa fila no existe. La hipótesis de que el culpable fuera <code>--sp-5</code> se comprobó y no se sostiene aquí. La opción B cuesta 12 px del primer pliegue en el teléfono; la C los recupera subiendo la fecha a la cabecera, y eso pide una decisión de producto.',
  a_d('m28', 'Pantalla Mi día a 390 px con el título pegado a la línea', 'La misma pantalla con aire bajo la barra', 'Antes — 390 px', 'Después — opción B, 390 px'),
  '.p4{padding-bottom:var(--sp-3)}\n:root{--sp-5:20px}   /* hoy sin declarar: 67 elementos afectados en 7 pantallas */',
  'Brief de diseño: <code>28-mi-dia</code>, que se entrega a pedido.',
  ('Opción B: viable', 'Opción C: con condiciones'))

cambio(B, 'Asistente: la última línea ya no cruza la franja gris', 'dis',
  '<code>47_asistente</code> · <code>.fuentes</code> · línea 669.',
  'La última línea de cada respuesta suele ser la conclusión o el dato que alguien va a copiar, y queda cruzada por el borde de la franja «De dónde salió». Se lee como un error de pintado.',
  '<code>.fuentes</code> lleva <code>margin:calc(var(--sp-3) * -1) …</code> dentro de un contenedor que ya tiene su relleno: la franja sube 12 px y la última línea entra 8,9 px en ella. Quitar el margen negativo y tratar cuerpo y franja como zonas hermanas. Los dos tonos marcan el cuerpo de la respuesta y su pie de procedencia. «Chat» no necesita sección propia.',
  a_d('a47', 'Respuesta del asistente con la última línea tocando la franja de procedencia', 'Respuesta con la franja separada del texto', 'Antes — la franja pisa la última línea', 'Después — cuerpo y pie separados'),
  '/* quitar el margen negativo de .fuentes */\n.fuentes{margin:0 calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)}',
  'Los cuatro enlaces <code>.fuentes a</code> miden 19,8 px de alto («Abrir GT-2026-02417» es la salida que el asistente ofrece cuando se niega a actuar): 24 px mínimo. Condición: decidir si el asistente solo consulta (<code>47</code>) o ejecuta con confirmación (<code>10</code>), porque hoy se contradicen. Brief de diseño: <code>47-asistente</code>, que se entrega a pedido.',
  ('Viable con condiciones',))

cambio(B, 'Agenda de instaladores: se queda la de DPROMA, con un cambio mínimo', 'dis',
  '<code>34_instaladores</code>.',
  'No se sustituye por otra. Se añade una fila «Sin asignar» para la visita que no tiene instalador, el texto sube a 12 px o más (hoy 53 de 62 nodos de texto están por debajo) y el domingo se ve completo a 1280 px.',
  'La «agenda del sistema» no existe en la 2.15.0: no hay §6.24 y §13.9 solo regula bloques con alto fijado por un dato. Ningún hallazgo crítico depende de esta pantalla.',
  a_d('g34', 'Agenda semanal de instaladores tal como llega', 'Agenda con la fila Sin asignar y el domingo completo', 'Antes — 1440 px', 'Después — 1440 px', apilado=True),
  None,
  'Brief de diseño: <code>34-agenda</code>, que se entrega a pedido.',
  ('Viable con condiciones',))

cambio(B, '«Con qué filtros»: dato personal sin ámbar', 'dis',
  '<code>54_bitacora_descargas</code> · columna «Con qué filtros».',
  'El panel es un registro de lo que se aplicó en cada descarga, no controles, y debe seguir siéndolo. Lo que falla es que mezcla filtros aplicados con datos personales entregados, usa el ámbar del semáforo para una clasificación y escribe «2 de 5» donde haría falta el valor.',
  'Dos grupos en la misma celda: los filtros, y aparte la marca «Dato personal» con un escudo, sin color de estado. Los valores se escriben completos: «Querétaro y Celaya» en lugar de «2 de 5».',
  a_d('f54', 'Tabla de la bitácora con chips de filtros en ámbar', 'Tabla con filtros y marca de dato personal en dos grupos', 'Antes — 1440 px', 'Después — 1440 px', apilado=True),
  None,
  'Brief de diseño: <code>54-panel-con-que-filtros</code>, que se entrega a pedido.',
  ('Viable con condiciones',))

# ================================================================ C · SENCILLAS
C = 'C'
cambio(C, 'Las cajas de cabecera dejan de chocar con la línea inferior', 'rec',
  'La plantilla de cabecera <code>.p4</code> (bloque ARQ-P4) está copiada en 36 archivos. Visto en <code>24_tickets</code>.',
  'Las pestañas «Abiertos, Míos, Todos» y el botón «Nuevo ticket» tocan la línea que cierra la cabecera. Siempre debería haber margen.',
  'La plantilla no tiene relleno inferior y deja el cierre a la última fila hija; cuando la cabecera solo lleva título y acciones, nadie la cierra. §3.1 prescribe este arreglo y el bloque no lo incorporó. Es la causa común de este cambio, de Tickets TI y de Mi día.',
  a_d('obs10', 'Cabecera de Tickets TI con las pestañas pegadas a la línea', 'La misma cabecera con 12 px de aire', 'Antes — 0 px de aire', 'Después — 12 px de aire'),
  '.p4{padding-bottom:var(--sp-3)}',
  'En la medición automática hay 51 barras sin holgura inferior en 20 pantallas.')

cambio(C, 'Incidencias de RHL: el texto se separa de los botones', 'rec',
  '<code>13_panel_asistencia_rhl</code> · <code>.inc .body span</code> · línea 181.',
  'Las filas de incidencias se ven desordenadas: el texto de detalle se pega a los botones y algunas frases se parten.',
  'Una regla pensada para la línea de detalle también alcanza a la fila de botones y a los <code>&lt;span translate="no"&gt;</code> de dentro de la frase. La fila de acciones pierde su <code>display:flex</code>, su <code>gap</code> de 6 px y su margen superior de 8 px, y las frases pasan a bloque. Acotar el selector devuelve los 8 px.',
  a_d('obs05', 'Bandeja de incidencias con el texto pegado a los botones', 'La misma bandeja con 8 px entre el texto y los botones', 'Antes — 1 px', 'Después — 8 px', apilado=True),
  '/* antes */\n.inc .body span{ … display:block; margin-top:1px }\n\n/* después */\n.inc .body > span:not(.acts){ … display:block; margin-top:var(--sp-1) }',
  'Es la pantalla 13, no la 48. Distancia del texto a los botones: de 1 px a 8 px.')

cambio(C, '«Siguiente» queda entera, por fuera de la tarjeta', 'rec',
  '<code>55_verificacion_pedido</code> · <code>.ren.siguiente::before</code> · línea 678.',
  'La etiqueta «SIGUIENTE» queda cortada a la altura del borde de la tarjeta; debería ir por fuera.',
  'El rótulo se coloca con <code>position:absolute</code> sin <code>top</code> ni <code>bottom</code> y un <code>translateY(-32px)</code> fijo calibrado a ojo: cae a mitad del borde (−4,5 px) y cambia con el alto de la tarjeta.',
  a_d('obs19', 'Renglón siguiente con la etiqueta cortada por el borde', 'Renglón con la etiqueta entera, por encima del borde', 'Antes — cortada', 'Después — por fuera'),
  '.ren.siguiente::before{top:auto;bottom:calc(100% + var(--sp-2));left:var(--sp-4);transform:none}\n.ren.siguiente{margin-top:var(--sp-6)}',
  'Probado a 390 px con una y dos líneas de nombre.')

cambio(C, 'Datos fiscales: el botón sube a la línea del título', 'rec',
  '<code>21_ficha_cliente</code> · <code>.fiscal-acc</code>.',
  'La caja de «Datos fiscales» es innecesariamente alta y «Editar datos fiscales» está al final de la línea, lejos del rótulo que lo explica.',
  'El botón ocupa una fila propia (<code>.fiscal-acc</code>, con <code>justify-content:flex-end</code> y 16 px de margen) en una tarjeta cuyo contenido real mide 31,5 px: eso añade 52 px. Además <code>.campos</code> usa <code>auto-fit minmax(190px,1fr)</code>, pensado para el formulario, para tres valores de lectura. La edición sigue siendo en línea (D9).',
  par('', panel('Así queda', img('q-ficha', 'Sección Datos fiscales con el botón Editar en la línea del título'), 'despues'), True),
  None, 'La tarjeta pierde la fila del botón: unos 52 px menos.')

cambio(C, 'Consumo de material: sin semáforo donde no hay un juicio', 'rec',
  '<code>25_consumo_de_material</code>.',
  'Hay demasiados colores, y varios de ellos son del semáforo sin que haya un juicio de estado detrás.',
  'El contrato de diseño no tiene color para tres cosas que la pantalla necesita: «derivado», el color físico de un material y «total». La pantalla las resolvió con el semáforo, que era lo único que había. La propuesta: banda informativa, «derivado» con un punto neutro, el total sin ámbar y con una línea superior, y el bloque comparativo de ejemplo fuera, porque es andamio. Queda el acento del producto más el color físico de cada cable.',
  par('', panel('Así queda', img('q-consumo', 'Tabla de consumo de material sin colores de semáforo'), 'despues'), True),
  None, 'Cuatro cambios, unas 8 líneas. Se pierde el realce ámbar del total; el peso y la línea lo mantienen.')

cambio(C, 'Tablero: las barras comparten línea base', 'rec',
  '<code>20_tablero</code> · gráfica «Volumen de las últimas 12 semanas» · <code>.sem .et</code>, líneas 725 a 732.',
  'Las barras de la gráfica no comparten línea y el texto se amontona sobre ellas.',
  '<code>.sem</code> es una columna flex cuyo rótulo existe en 2 de 12 columnas: ocupa 15 px en esas dos y 0 en las otras, y <code>justify-content:flex-end</code> baja cada pila hasta su propio rótulo. Además <code>.sem .et{white-space:nowrap}</code> con 74 px de texto en una columna que a 900 px mide 57. Todas las columnas deben reservar el mismo hueco.',
  par('', panel('Así queda', img('q-tablero', 'Gráfica de 12 semanas con las barras alineadas'), 'despues'), True),
  None, 'Solo se corrigió la alineación. Sigue pendiente la tabla equivalente de la gráfica (§12.3) y una escala declarada.')

cambio(C, 'Viáticos: la tabla queda solo con datos', 'rec',
  '<code>23_viaticos</code> · celda «Monto y excedente» y celdas vecinas.',
  'Las celdas de la tabla llevan frases explicativas, y no deberían. Hay una <a href="/entregables/propuestas/viaticos">versión limpia de Viáticos</a>.',
  'Las frases salen de la celda: la justificación del excedente (hasta 141 caracteres), el motivo del rechazo, «No puedes aprobar tu propia solicitud» y «Mientras están en revisión…». §6.11, regla 7: una celda no lleva un párrafo. Cada celda deja solo el dato o el estado, y el texto va a la ficha del viático o a un toggletip.',
  par('', panel('Así queda', img('q-viaticos', 'Tabla de viáticos con montos, estados y botones, sin frases explicativas'), 'despues'), True),
  None, 'Coste: «Aprobar» deshabilitado ya no dice por qué en la fila. El detalle del paquete (<code>39</code>) solo dibuja el viático 0715 y no tiene sitio para la justificación ni el motivo del rechazo: hay que diseñarlos ahí.')

cambio(C, 'Cuentas por cobrar: las tarjetas de indicadores no se estiran', 'rec',
  '<code>46_cuentas_por_cobrar</code> · <code>.minis</code> y <code>.kpis</code>.',
  'Las tres tarjetas pequeñas se estiran hasta la altura de la primera y quedan con un gran vacío interior.',
  'Tres factores: <code>.minis</code> omite <code>align-items:start</code>, el valor por omisión de §13.4; <code>.kpis</code> está en dos columnas con el hero en la primera, así que las tres mini heredan sus 349 px en vez de su altura (92 a 169); y esa altura la fija el <code>.pie</code> del hero, con 523 caracteres en dos párrafos a 11 px. La propuesta ya existente mueve esas explicaciones a un toggletip y usa <code>.kpis-d</code>.',
  par('', panel('Así queda', img('q-cxc', 'Fila de indicadores de Cuentas por cobrar con las tarjetas a su altura'), 'despues'), True),
  '.minis{align-items:start}',
  'Es la fila que ya se había optimizado para esta pantalla; §13.2 a §13.4 la protegen. Propuesta de referencia: <a href="/entregables/propuestas/cuentas-por-cobrar">Cuentas por cobrar</a>.')

cambio(C, 'Los destinos de pulsación llegan a 24 px', 'rec',
  '134 destinos bajo 24 px en 29 de las 50 pantallas.',
  'El buscador, el folio, las migas y las casillas son difíciles de acertar con ratón impreciso o con tableta, y en el padrón una casilla errada selecciona la fila equivocada antes de una acción masiva.',
  'No se exige como fallo de accesibilidad: con la excepción de espaciado de WCAG 2.5.8 se cumple en la mayoría de los casos, y es una divergencia de §7.3 (en <code>06</code>, <code>11</code> y los buscadores el espaciado no alcanza para salvarlos). Se recomienda porque es un cambio de una línea.',
  a_d('d28', 'Listado de órdenes con el buscador y los folios marcados en rojo por medir menos de 24 px', 'El mismo listado con los destinos marcados en verde, de 24 px o más', 'Antes — en rojo, menos de 24 px', 'Después — en verde, 24 px o más', apilado=True)
  + '<p class="nota">Ejemplo en <code>30_ordenes_listado</code>. En el resto de pantallas es igual; esta tabla dice dónde.</p>'
  '<table class="mini"><thead><tr><th>Pantalla</th><th>Elemento</th><th class="r">Medida</th></tr></thead><tbody>'
  '<tr><td><code>27</code>, <code>06</code></td><td>casillas <code>input.rowsel</code></td><td class="r">15 × 15 px</td></tr>'
  '<tr><td><code>42</code>, <code>44</code></td><td>casillas de «Documentos» (5 por pantalla)</td><td class="r">15 × 15 px</td></tr>'
  '<tr><td><code>27</code>, <code>30</code>, <code>35</code>, <code>36</code>, <code>37</code>, <code>40</code>, <code>47</code>, <code>50</code></td><td>buscador <code>.search input</code>, dentro de un <code>&lt;div&gt;</code></td><td class="r">216 a 329 × 16 px</td></tr>'
  '<tr><td><code>03</code>, <code>30</code>, <code>35</code>, <code>50</code></td><td>folios <code>a.folio</code> y <code>a.lnk</code></td><td class="r">119 a 127 × 16 px</td></tr>'
  '<tr><td><code>08</code>, <code>33</code>, <code>38</code>, <code>39</code>, <code>42</code>, <code>43</code>, <code>44</code>, <code>45</code></td><td>migas <code>.migas a</code> y <code>.crumb a</code></td><td class="r">43 a 123 × 15 px</td></tr>'
  '<tr><td><code>06</code></td><td>acciones de la barra de selección <code>.selbar a</code></td><td class="r">67 a 120 × 16 px</td></tr>'
  '<tr><td><code>11</code></td><td>«Reenviarlo» <code>#resend</code> (el código 2FA no llegó)</td><td class="r">64,7 × 22 px</td></tr>'
  '<tr><td><code>27</code></td><td>botones de orden de la cabecera</td><td class="r">160 × 21 px</td></tr>'
  '<tr><td><code>47</code></td><td>enlaces <code>.fuentes a</code></td><td class="r">780 × 19,8 px</td></tr>'
  '<tr><td><code>58</code></td><td>correo y teléfono <code>.ctrl input</code></td><td class="r">335 × 19 px</td></tr></tbody></table>',
  '.folio,.lnk,.migas a,.crumb a{display:inline-flex;align-items:center;min-height:24px}\n/* el buscador: el contenedor pasa de <div class="search"> a <label class="search"> para que pulsarlo enfoque el campo (§10, trampa 4) */\n.search{min-height:34px}\ninput[type="checkbox"]{width:24px;height:24px}',
  'Ningún destino de pulsación mide menos de 24 px de alto.')

cambio(C, 'El botón flotante no tapa «Crear expediente»', 'rec',
  '<code>42_alta_tramite_gestoria</code>, <code>43_alta_tramite_vehicular</code> y <code>44_alta_tramite_cfe</code> · <code>.fab</code> (línea 268) y <code>.barra-form</code> (línea 592).',
  'El botón redondo del asistente cae sobre la esquina del botón verde de la barra de acciones y le tapa el final del rótulo: «Cre…» en lugar de «Crear expediente». Cubre el 33 % del botón (el 38 % en «Ingresar a CFE» de <code>44</code>) y recibe el clic en esa zona. El botón verde sigue pulsable por el resto y con el teclado.',
  '<code>.fab</code> está en <code>position:absolute</code> a 26 px del borde, y <code>.barra-form</code> no reserva sitio a su derecha. <code>27_padron_clientes</code> ya resuelve lo mismo en su <code>.nota</code> con <code>padding-right:calc(var(--sp-6) + 68px)</code>.',
  a_d('f29', 'Barra de acciones con el botón redondo del asistente encima del final de «Crear expediente»', 'La misma barra con los botones desplazados a la izquierda del botón redondo', 'Antes — el círculo tapa «…ar expediente»', 'Después — el botón se lee entero', apilado=True),
  '.barra-form{padding-right:calc(var(--sp-6) + 68px)}\n@media (max-width:1280px){.barra-form{padding-right:calc(var(--sp-4) + 68px)}}',
  'El solape del botón primario con el <code>.fab</code> pasa de 52 × 20 px a 0 en las tres pantallas, a 1440, 1280 y 1024 px. Medido en Chromium con la regla inyectada.')

cambio(C, 'Padrón (06): las acciones y los estados caben sin cortarse', 'rec',
  '<code>06_padron_clientes</code> · <code>&lt;colgroup&gt;</code> de la tabla (líneas 474 a 478) y celdas <code>.pill</code> de «Datos fiscales» (línea 527) y «Estado» (línea 529).',
  'En la columna Acciones, el primer icono (ver ficha) queda con el borde izquierdo mordido en las seis filas. Las pastillas de estado se cortan a mitad de palabra: «Falta carátula banc…» y «Registro inco…». A 1280 px quedan cortados 5 iconos y 7 pastillas; a 1024 px, 12 pastillas, hasta «Activo» y «Completos».',
  'Tres columnas están más estrechas que su contenido. Acciones mide 104 px y sus tres botones necesitan 120 (3 × 28 px, dos huecos de 6 px y 24 px de relleno): como la celda corta lo que sobra, se pierde el borde del primero. Las columnas de estado miden un porcentaje del ancho (10 % y 14 %) y no alcanzan para el rótulo: «Registro incompleto» pide 203 px y recibe 111. Además, «Falta carátula bancaria» y «Registro incompleto» dicen lo mismo en dos columnas seguidas.',
  a_d('t06', 'Tabla del padrón con el primer icono de acciones mordido y las pastillas «Falta carátula banc…» y «Registro inco…» cortadas', 'La misma tabla con los iconos completos y las pastillas «Incompletos» y «Registro incompleto» enteras', 'Antes — iconos y pastillas cortados', 'Después — todo cabe', apilado=True),
  '/* 1 · Acciones: 3 × 28 + 2 × 6 + 24 = 120 px */\n<col style="width:128px">                 /* antes: 104px */\n\n/* 2 · anchos en píxeles para las columnas de pastillas */\ntipo 140 · sucursales 130 · datos fiscales 150 · última orden 112 · estado 205\n\n/* 3 · el estado por documento, corto; el detalle va al title y a la ficha */\n<span class="pill p-warn" title="Falta carátula bancaria">… Incompletos</span>\n\n/* 4 · con menos ancho, se ocultan columnas secundarias en vez de cortar */\n@media (max-width:1366px){.col-contacto{display:none}}\n@media (max-width:1100px){ /* columna «Última orden» */ display:none }',
  'A 1440, 1366, 1280, 1180, 1100 y 1024 px, ningún icono ni pastilla queda cortado (antes: 5 iconos a 1440, 1366 y 1280, y entre 2 y 12 pastillas en todos los anchos). Medido en Chromium con los cambios inyectados. «Registro incompleto» se mantiene porque es el vocabulario que DPROMA confirmó en su versión 1 (comentario de la línea 165). Lo que cambia es el estado de datos fiscales: pasa de «Falta carátula bancaria» a «Incompletos», con el detalle al pasar el cursor.')

cambio(C, 'Los botones hermanos del portal del cliente se parecen', 'rec',
  '<code>05_app_cliente</code> · <code>.abtn</code> · líneas 246 a 249.',
  '«Contactar a DPROMA» y «Reagendar cita» no se ven iguales: en uno el icono está junto al texto y en el otro apartado, y el botón es más alto.',
  'Los dos son <code>.abtn</code> con el mismo CSS. El texto de «Contactar a DPROMA» (120 px) no cabe en la media celda de la rejilla, envuelve a dos líneas y el nodo de texto ocupa todo el ancho restante: el icono se queda a la izquierda, lejos de su palabra, y el botón sube de 44 a 52 px. Falta <code>white-space:nowrap</code> o un rótulo más corto.',
  a_d('b30', 'Portal del cliente: «Contactar a DPROMA» en dos líneas y con el icono lejos del texto', 'Los dos botones con el rótulo en una línea', 'Antes — dos líneas, botón más alto', 'Después — una línea, iguales', apilado=False), '.abtn{white-space:nowrap}   /* o rotular «Contactar» */',
  'Los dos botones miden 44 px de alto y el icono queda junto a su palabra.')

cambio(C, 'Dashboard: las cajas de actividad y alertas cierran a la misma altura', 'menor',
  '<code>02_dashboard</code> · <code>.row2</code> (línea 178) y la tarjeta «Alertas» (líneas 459 a 476).',
  'En el tablero principal, la tarjeta «Actividad de los últimos 7 días» termina unos 128 px antes que «Alertas» y deja un hueco debajo. Es un asunto meramente estético: no impide nada ni falla ninguna medición, y no tiene prioridad. Se propone para que la primera pantalla del sistema se vea más cuidada.',
  '<code>.row2</code> usa <code>align-items:start</code>, el valor por omisión del sistema (§13.4), así que cada tarjeta conserva su altura: 218 px la de actividad, con gráficas de 120 px fijos, y 346 px la de alertas, que lista cinco. Estirar la tarjeta corta sin más dejaría un rectángulo vacío por dentro (§13.8). Por eso la propuesta usa contenido: «Alertas» muestra las tres más recientes, con un botón «Ver todas (5)» arriba a la derecha como el «Ver todo» de «Actividad reciente», y las gráficas se ensanchan hasta llenar su tarjeta sin deformarse.',
  a_d('d02', 'Dashboard con la tarjeta de actividad más baja que la de alertas, que lista cinco', 'El mismo dashboard con tres alertas, el botón Ver todas (5) y las dos tarjetas a la misma altura', 'Antes — 218 px y 346 px', 'Después — 247 px las dos', apilado=True),
  '/* solo con dos columnas (a 1180 px o menos ya se apilan) */\n@media (min-width:1181px){\n  .row2{align-items:stretch}\n  .row2 > .panel{display:flex;flex-direction:column}\n  .row2 .charts{flex:1}\n  .row2 .chart{display:flex;flex-direction:column}\n  .row2 .chart svg{flex:1;height:auto;min-height:120px}   /* antes: height="120" */\n}\n\n/* Alertas: las tres más recientes y el resto tras el botón */\n<button class="btn" style="margin-left:auto">Ver todas (5)</button>',
  'A 1440, 1366 y 1280 px las dos tarjetas miden lo mismo (247, 240 y 240 px) y las gráficas conservan su proporción. A 1180 px o menos no cambia nada. Con cuatro alertas no funciona: las gráficas tendrían que crecer más de lo que su dibujo permite.',
  ('Estético, sin prioridad',))

# ================================================================ D · AVISO
D = 'D'
cambio(D, 'El padrón dibuja lo que se pospuso: vigencia y duplicados', 'pide',
  '<code>27_padron_clientes</code> · D7 y D8 del aviso del 28 de septiembre.',
  'D7 pospone la vigencia por documento (no existe la columna) y D8 pospone los duplicados. En el estado por defecto, <code>27</code> pinta el chip «7 con un documento por vencer», la pastilla «Por vencer» con su fecha y un aviso de 30 días, y la tarjeta «Dos pares de razones sociales se parecen demasiado» con dos botones «Comparar y decidir». La ficha reconoce que <code>27</code> lo dibuja.',
  'Se retiran, como en el prototipo del cambio ' + '@@padron@@' + ', y se vuelven a dibujar cuando D7 y D8 dejen de estar pospuestas.',
  a_d('p31', 'Padrón con el chip «7 con un documento por vencer» y la tarjeta de duplicados con «Comparar y decidir»', 'El mismo padrón sin el chip ni la tarjeta de duplicados', 'Antes — dibuja lo pospuesto', 'Después — se retira', apilado=True), None, 'En el estado por defecto no aparece ni «por vencer» ni «Comparar y decidir».')

cambio(D, 'El padrón de la bandeja sigue dibujando «Reenviar liga de registro»', 'pide',
  '<code>06_padron_clientes</code> · botón de fila, línea 533 · D6 del aviso del 28 de septiembre.',
  'D6 dice que «Reenviar liga de registro» no se construye. En <code>06</code>, la fila «Autos del Valle SAPI» la dibuja como tercera acción de la columna Acciones (un botón con icono de cadena y <code>aria-label="Reenviar liga de registro a Autos del Valle"</code>). La misma pantalla trae «Liga de auto-registro» en la cabecera (línea 424) y en la nota inferior (línea 592). <code>FICHAS_TECNICAS.md</code> (líneas 124 y 701) dice que esa liga también cayó bajo el rechazo del punto 15.',
  '<code>06</code> es otra versión del padrón y no está en la tabla de arriba; por eso se comprobó aparte.',
  a_d('l32', 'Padrón con «Liga de auto-registro» en la cabecera y un tercer icono de cadena en la fila de Autos del Valle', 'El mismo padrón sin la liga: la fila trae solo ver y editar', 'Antes — con «Reenviar liga»', 'Después — sin ella', apilado=True), None,
  'La fila tiene dos acciones (ver y editar), la cabecera no trae «Liga de auto-registro» y la nota inferior no la menciona.')

cambio(D, 'La alta de cliente dice la frase del aviso', 'menor',
  '<code>41_alta_cliente</code> · D2.',
  'La sucursal es opcional, pero falta la frase literal «Sin sucursal no se le puede programar una orden; se puede añadir después desde la ficha». La sección dice el todo o nada y el estado vacío omite la consecuencia.',
  'Es una omisión de texto; el fondo está bien.',
  a_d('a33', 'Sección Sucursal del alta de cliente sin la frase sobre qué pasa sin sucursal', 'La misma sección con la frase del aviso debajo del título', 'Antes — falta la frase', 'Después — con la frase', apilado=True), None,
  'La frase aparece en la sección «Sucursal» del alta.')

PARTES = {
 'A': ('Parte A', 'Lo que se pide', 'Once cambios. Los seis primeros son sustituciones que se repiten en muchos archivos; los cinco siguientes son problemas propios de una pantalla o una contradicción con el aviso del 28 de septiembre. Cada uno cumple alguna de las cinco condiciones de crítico.'),
 'B': ('Parte B', 'Propuestas de diseño', 'Ocho rediseños. Cada uno parte de lo que dibujó DPROMA, evalúa al menos dos opciones (la primera siempre es el mínimo cambio sobre su dibujo) y se probó en el navegador a 1440, 1280, 1024 y 390 px. Son prototipos: ningún archivo de DPROMA se modificó.'),
 'C': ('Parte C', 'Mejoras sencillas', 'Trece cambios que no se exigen. Cada uno mejora algo visible y, varias veces, delata una causa que se repite en otras pantallas.'),
 'D': ('Parte D', 'El aviso del 28 de septiembre', 'Se comprobaron los doce puntos del aviso contra las cinco pantallas del padrón. Casi todo está donde debe. Tres cosas no, y las tres tienen que ver con lo que se pospuso. Aparte, una pantalla que la tabla no cubre, <code>06</code>, sigue dibujando lo que el aviso rechazó.'),
}

# ---------------------------------------------------------------- render
def render_cambio(n, c):
    cls = {'pide': 'pide', 'rec': 'rec', 'dis': 'dis', 'menor': 'rec'}[c['tag']]
    extra = ''.join(f'<span class="tag tag-ok">{E(t)}</span>' for t in c['extra'])
    s = [f'<article class="cambio" id="c{n}"><header><span class="n">{n}</span><h3>{c["titulo"]}</h3></header>',
         f'<div class="tags"><span class="tag tag-{cls}">{TAGS[c["tag"]]}</span>{extra}</div>',
         f'<p class="donde"><b>Dónde.</b> {c["donde"]}</p>',
         f'<p class="que"><b>Qué se ve.</b> {c["que"]}</p>']
    if c['porque']: s.append(f'<p class="porque"><b>Por qué y qué cambia.</b> {c["porque"]}</p>')
    if c['visual']: s.append(c['visual'])
    if c['cod']: s.append(pre(c['cod']))
    if c['comprueba']: s.append(f'<p class="comprueba"><b>Cómo comprobarlo.</b> {c["comprueba"]}</p>')
    s.append('</article>')
    return '\n'.join(s)

partes_html, indice = [], []
n = 0
for k in 'ABCD':
    rot, titulo, lede = PARTES[k]
    bloque = [f'<section class="parte" id="parte-{k.lower()}"><header class="ph"><span class="eyebrow">{rot}</span><h2>{titulo}</h2><p class="lede">{lede}</p></header>']
    for p, c in cambios:
        if p != k: continue
        n += 1
        bloque.append(render_cambio(n, c))
        indice.append((k, n, c['titulo'], c['tag']))
    bloque.append('</section>')
    partes_html.append('\n'.join(bloque))

AVISO_FILAS = [
 ('D6 · «Reenviar liga de registro» no se construye', 'ok', 'ok', 'ok', 'ok', 'na'),
 ('D5 · Sección «Unidades» en la ficha', 'na', 'ok', 'na', 'na', 'na'),
 ('D9 · Datos fiscales editables en la ficha; <code>editar-cliente</code> en dos renglones', 'na', 'ok', 'na', 'na', 'ok'),
 ('D3 · Grupo y marca son de la sucursal; en la ficha el grupo se deriva', 'na', 'sv', 'ok', 'no', 'na'),
 ('D2 · Sucursal opcional en el alta, con su aviso', 'na', 'na', 'no', 'no', 'na'),
 ('D1 · El alta es una página, no un diálogo', 'sv', 'na', 'ok', 'no', 'na'),
 ('D10 · «Último movimiento» en el listado, ocultable desde «Columnas»', 'ok', 'na', 'na', 'na', 'na'),
 ('D13 · Contacto «De la empresa»; sucursal todo o nada', 'na', 'ok', 'ok', 'no', 'na'),
 ('D15 · Ficha inactiva en solo lectura, con banda y «Reactivar»', 'na', 'ok', 'na', 'na', 'na'),
 ('D7 · Vigencia por documento: pospuesta, no debe aparecer', 'ap', 'ok', 'ok', 'ok', 'na'),
 ('D8 · Duplicados y «Comparar y decidir»: pospuestos, no deben aparecer', 'ap', 'ok', 'ok', 'ok', 'na'),
 ('D4 · Exportar la ficha como PDF de una hoja', 'na', 'sv', 'na', 'na', 'na'),
]
TXT = {'ok': 'Cumple', 'no': 'No cumple', 'sv': 'Sin verificar', 'na': '—', 'ap': 'Aparece'}
CLS = {'ok': 'ok', 'no': 'no', 'sv': 'sv', 'na': 'na', 'ap': 'no'}
tabla_aviso = ('<table class="t t-aviso"><colgroup><col style="width:6%"><col style="width:38%"><col style="width:11.2%"><col style="width:11.2%"><col style="width:11.2%"><col style="width:11.2%"><col style="width:11.2%"></colgroup>'
  '<thead><tr><th class="r">#</th><th>Decisión del aviso</th><th class="c">27 padrón</th><th class="c">21 ficha</th><th class="c">41 alta</th><th class="c">58 modal</th><th class="c">59 editar</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="r">{i}</td><td>{f[0]}</td>' + ''.join(f'<td class="c {CLS[x]}">{TXT[x]}</td>' for x in f[1:]) + '</tr>' for i, f in enumerate(AVISO_FILAS, 1))
  + '</tbody></table><p class="nota">Los «No cumple» de <code>58</code> hablan del diálogo «Nuevo cliente» de esa página, que según <code>FICHAS_TECNICAS.md</code> ya no gobierna el alta de cliente (<code>41</code>) y sí las otras cuatro altas.</p>')
# la tabla del aviso va justo después del encabezado de la parte D
partes_html[3] = partes_html[3].replace('</header>', '</header>\n' + tabla_aviso, 1)

REFS = {t: i for p, i, t, g in indice}
def ref(parte_titulo):
    for t, i in REFS.items():
        if t.startswith(parte_titulo): return str(i)
    raise KeyError(parte_titulo)
PCT = {'pide': 'Se pide', 'rec': 'Recomendado', 'dis': 'Propuesta de diseño', 'menor': 'Menor'}
def c(t): return '<a href="#c' + ref(t) + '">cambio ' + ref(t) + '</a>'
MEDIDAS = [
 ('Botones, enlaces y casillas más pequeños de 24 × 24 px', '134', '29 de 50', 'Cuesta acertarlos con ratón impreciso o con tableta, y una pulsación errada puede activar otra cosa.', 'Ver ' + c('Los destinos de pulsación')),
 ('Entradas del menú lateral que un lector de pantalla no sabe nombrar, a 1000 px', '525', '35 de 42', 'A ese ancho el menú queda en iconos y no hay texto que decir a dónde lleva cada uno. Solo se contó en las 42 pantallas que llevan menú.', 'Ver ' + c('El menú lateral')),
 ('Iconos casi del mismo color que el relleno del botón', '51', '23 de 50', 'El icono se funde con el botón y casi no se ve, como el gris sobre el verde de «Reintentar».', 'Ver ' + c('El icono del botón verde')),
 ('Cabeceras cuyos controles tocan la línea inferior', '51', '20 de 50', 'Falta el aire que sí hay arriba. Viene de una plantilla de cabecera que se copió.', 'Ver ' + c('Las cajas de cabecera')),
 ('Textos con contraste por debajo de 4,5:1, tema claro', '19', '11 de 50', 'Se leen mal con poca luz o con baja visión.', 'Ver ' + c('El gris del texto') + ' y ' + c('El contador de Asistencia')),
 ('Textos con contraste por debajo de 4,5:1, tema oscuro', '2', '2 de 50', 'Lo mismo, con el tema oscuro activado.', 'Sin cambio asociado todavía'),
 ('Celdas de tabla que llevan un párrafo', '24', '7 de 50', 'Una celda debe llevar un dato, no una frase (§6.11, regla 7).', 'Ver ' + c('Viáticos: la tabla')),
 ('Textos siempre visibles de más de 140 caracteres', '25', '14 de 50', 'El sistema pone un tope de 140 caracteres y una frase para los avisos (§8). Pasado ese tope, el texto explica en lugar de indicar.', 'Se atiende caso por caso, por ejemplo en los ' + c('Tickets TI') + ' y en ' + c('Viáticos: la tabla')),
 ('Textos de 10,5 px que no están en mayúsculas', '240', '45 de 50', 'El sistema solo prevé ese tamaño para rótulos en mayúsculas (§2.1). Fuera de ahí cuesta leerlo.', 'No se pide cambio por ahora'),
 ('Variables de color o espaciado que se usan y nunca se definen', '9', '7 de 50', 'El navegador ignora la variable y el elemento pierde ese valor.', 'El caso de <code>--sp-5</code> está en el ' + c('Mi día')),
 ('Elementos que usan <code>--sp-5</code>, que nadie define', '67', '7 de 50', 'Quedan con 0 px de espaciado donde debería haber 20 px.', 'Ver ' + c('Mi día')),
 ('Parejas de botones de distinta altura o con el icono en otro sitio', '5', '5 de 50', 'Dos botones que hacen cosas parecidas se ven distintos.', 'Ver ' + c('Los botones hermanos')),
]
tabla_med = ('<table class="t t-med"><colgroup><col style="width:27%"><col style="width:9%"><col style="width:11%"><col style="width:31%"><col style="width:22%"></colgroup>'
  '<thead><tr><th>Qué se contó</th><th class="r">Cuántos</th><th>En cuántas pantallas</th><th>Por qué importa</th><th>Dónde se resuelve</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td class="r">{b}</td><td>{c_}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c_, d, e in MEDIDAS) + '</tbody></table>')

lista_no = ('<ul class="plano">'
  '<li><b>Los iconos como sprite SVG</b> (<code>&lt;use href="#i-…"&gt;</code>) se mantienen. Funcionan sin red y sin el parpadeo de una fuente que carga tarde.</li>'
  '<li><b>La clase <code>.banda.b-info</code></b> se mantiene.</li>'
  '<li><b>La agenda de instaladores propia</b> se mantiene. Solo lleva el cambio mínimo del cambio ' + ref('Agenda de instaladores') + '.</li>'
  '<li><b>El panel «Con qué filtros»</b> se mantiene como registro de auditoría, sin controles.</li></ul>')

def anexo_html():
    P = BAR['por_archivo']
    def chips(items):
        return ' '.join(f'<code>{a}{(":" + str(l)) if l else ""}</code>' for a, l in items)
    filas = [
     ('1', 'Menú lateral sin nombre (<code>.side .et{display:none}</code>)', [(a, P[a]['menu_et_display_none'][0]) for a in BAR['resumen']['menu_et_display_none']]),
     ('2', 'Icono gris (<code>.state .ico</code> descendiente)', [(a, P[a]['state_ico_descendiente'][0]) for a in BAR['resumen']['state_ico_descendiente']]),
     ('3', 'Gris de texto (<code>--text-3: #66717F</code>)', [(a, P[a]['text3_linea']) for a in BAR['resumen']['text3_66717F']]),
     ('4', 'Fuentes por <code>&lt;link&gt;</code> a Google', [(a, P[a]['google_fonts_link'][0]) for a in BAR['resumen']['google_fonts_link']]),
     ('5', 'Identificadores repetidos', [(a + ' (' + ', '.join(f'{k} ×{v}' for k, v in P[a]['ids_repetidos'].items()) + ')', None) for a in BAR['resumen']['ids_repetidos']]),
     (ref('Las cajas de cabecera'), 'Cabecera <code>.p4</code> sin relleno inferior', [(a, P[a]['p4_sin_padding_bottom'][0]) for a in BAR['resumen']['p4_sin_padding_bottom']]),
    ]
    cuerpo = ''.join(f'<tr><td class="r">{n}</td><td>{t}<br><span class="cuenta">{len(it)} archivos</span></td><td class="chips">{chips(it)}</td></tr>' for n, t, it in filas)
    return ('<table class="t t-anexo"><colgroup><col style="width:10%"><col style="width:24%"><col style="width:66%"></colgroup>'
            '<thead><tr><th class="r">Cambio</th><th>Qué se busca</th><th>Archivos, con la línea de la regla</th></tr></thead><tbody>' + cuerpo + '</tbody></table>')

# ---------------------------------------------------------------- documento
CSS = open(os.path.join(AQUI, 'revision.css'), encoding='utf-8').read()
DOC = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITULO} · octubre 2026 — 2894 Studio</title>
<meta name="description" content="Lo que se midió en las 50 pantallas del paquete del 12 de octubre, explicado cambio por cambio con capturas del antes y del después." />
<style>{CSS}</style>
</head>
<body>
<nav class="sitio" aria-label="Navegación"><a class="marca" href="/">2894 <span>Studio × DPROMA</span></a><span class="enlaces"><a href="/entregables">← Entregables</a><a href="#indice">Cómo leer</a><a href="/entregables/revisiones/{PDF}">PDF</a></span></nav>

<main>
<section class="portada">
  <div class="regla"></div>
  <p class="eyebrow">SIO-DPROMA · 2894 Studio</p>
  <div class="medio">
    <h1>{TITULO}</h1>
    <p class="sub">Lo que se midió en las 50 pantallas del paquete del 12 de octubre, explicado cambio por cambio: dónde está, qué se ve, qué cambiar y cómo comprobarlo, con capturas del antes y del después.</p>
  </div>
  <p class="fecha">14 oct 2026 · Informe para el equipo de DPROMA</p>
</section>

<section class="como" id="indice">
  <header class="ph"><span class="eyebrow">Antes de empezar</span><h2>Cómo leer este informe</h2></header>
  <p class="lede">Llegaron 50 pantallas HTML y se midieron todas en el navegador, con las fuentes reales. Las cincuenta se revisaron una por una, y cada defecto grave lo volvió a medir otra persona con intención de refutarlo. Es la primera revisión de estas pantallas: describe lo que hay en los archivos recibidos.</p>
  <div class="stats">
    <div class="stat"><b>6</b><h3>sustituciones que se repiten en muchos archivos</h3><p>Se aplican igual en cada uno: la regla del menú lateral está en 36 archivos y la del icono gris en 21. Son los cambios 1 a 6.</p></div>
    <div class="stat"><b>5</b><h3>cambios propios de una pantalla</h3><p>Afectan a las pantallas 10, 13, 29 y 58. Otras tres (27, 28 y 47) tienen su problema en la parte B, porque se arreglan con un rediseño. Son los cambios 7 a 11.</p></div>
    <div class="stat"><b>134</b><h3>destinos de pulsación bajo 24 px</h3><p>En 29 pantallas. No se exige, pero es lo más repetido: cambio {ref('Los destinos de pulsación')}.</p></div>
  </div>
  <p>Cada cambio lleva una etiqueta que dice cuánto pesa:</p>
  <ul class="plano">
    <li><span class="tag tag-pide">Se pide</span> cumple al menos una de las cinco condiciones de crítico: falla de accesibilidad medida; impide la tarea u oculta la acción principal; acción irreversible o de dinero sin protección; contradice una decisión de DPROMA o expone datos personales; o es un rediseño marcado como crítico y viable.</li>
    <li><span class="tag tag-dis">Propuesta de diseño</span> es un rediseño probado en un prototipo. El veredicto de viabilidad lo acompaña.</li>
    <li><span class="tag tag-rec">Recomendado</span> no se exige. Mejora algo visible y a veces delata una causa que se repite.</li>
  </ul>
  <p>Varios defectos nacen en un bloque que se copia de pantalla en pantalla, y con cada copia se repiten. La cabecera <code>.p4</code> sin relleno inferior está en 36 archivos, la regla <code>.state .ico</code> en 21 y el menú lateral colapsado deja sin nombre sus quince enlaces en 35 de las 42 pantallas que lo llevan. Corregir el bloque de origen y repetir la corrección es más barato que perseguir cada síntoma.</p>
  <h3 class="sub">Qué se contó en las 50 pantallas</h3>
  <p>Antes de revisar nada a mano, un programa abrió cada pantalla en un navegador y contó lo que se puede contar sin criterio humano: botones pequeños, contrastes, menús sin nombre. Sirve para saber qué tan extendido está cada problema.</p>
  <p class="nota">Que algo se cuente no significa que sea un error: son candidatos. Los cambios de las partes A y B son los que una persona reprodujo en el archivo y otra intentó refutar.</p>
  {tabla_med}
</section>

{chr(10).join(partes_html)}

<section class="parte" id="no-se-pide">
  <header class="ph"><span class="eyebrow">Parte E</span><h2>Lo que no hay que tocar</h2><p class="lede">Cuatro decisiones de DPROMA que se mantienen tal como están.</p></header>
  {lista_no}
</section>

<section class="parte" id="abierto">
  <header class="ph"><span class="eyebrow">Parte F</span><h2>Lo que necesitamos de DPROMA</h2><p class="lede">Cuatro cosas que ninguna medición resuelve.</p></header>
  <article class="cambio abierto"><header><h3>El archivo <code>49_alta_orden</code></h3></header><p class="que">El PDF de cambios dice que se actualizó, y no está entre las 50 pantallas. Dos observaciones sobre esa pantalla (la caja de «Croquis y anexos» cortada y la sombra sobre la barra de acciones) quedan sin respuesta hasta recibirla.</p></article>
  <article class="cambio abierto"><header><h3>El archivo <code>SUPUESTOS.md</code></h3></header><p class="que"><code>FICHAS_TECNICAS.md</code> remite a él para las decisiones sin ratificar (S-25, S-28, S-30, S-31…) y no viene en el ZIP. Sin ese archivo no podemos saber qué se dio por bueno y qué sigue pendiente.</p></article>
  <article class="cambio abierto"><header><h3>¿Qué asistente manda: <code>10_dprimi_asistente</code> o <code>47_asistente</code>?</h3></header><p class="que"><code>FICHAS_TECNICAS.md</code> presenta <code>47</code> como el asistente que sustituye a <code>10</code>, y fija que «el asistente consulta y no modifica» (S-19, una decisión sin ratificar). <code>10</code> sigue en el paquete y ofrece acciones que escriben: «Notificar a los responsables» y «Confirmar y enviar» un reporte por correo a Dirección. Hace falta saber si <code>10</code> se retira o si el asistente puede modificar datos.</p></article>
  <article class="cambio abierto"><header><h3>¿Qué manda sobre el plazo de los tickets?</h3></header><p class="que">La ficha de <code>24_tickets</code> en la tanda 3 dice que se retiró el reloj de plazo y que la antigüedad va en gris, igual en los seis renglones. La tanda 4 habla de que tickets conserva su propio semáforo de plazo. El archivo dibuja el plazo: «Vence hoy», con una regla de cálculo de 420 caracteres. El cambio {ref('Tickets TI')} depende de cuál sea la respuesta.</p></article>
</section>

<section class="parte" id="anexo">
  <header class="ph"><span class="eyebrow">Anexo</span><h2>Archivos de cada sustitución</h2><p class="lede">Resultado de buscar cada regla en el código de las 50 pantallas, con la línea donde está. Sirve para aplicar cada cambio de una vez en todos los archivos, y para comprobar después que ninguno se quedó atrás.</p></header>
  {anexo_html()}
</section>
</main>
<footer class="pie"><span>SIO-DPROMA · 2894 Studio</span><span>{TITULO}</span></footer>
</body>
</html>
'''
destino = os.path.join(WEB, 'revision-de-pantallas.html')
open(destino, 'w', encoding='utf-8').write(DOC)
print('escrito', destino, len(DOC) // 1024, 'KB;', n, 'cambios')
