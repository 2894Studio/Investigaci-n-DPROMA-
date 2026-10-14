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
  '19 de las 23 pantallas revisadas a fondo. La medición automática lo encuentra en 35 de las 42 que llevan menú, y la regla <code>.side .et</code> está en 36 archivos. Revisadas: ' + archivos(['20', '21', '22', '23', '24', '25', '26', '27', '28', '32', '34', '41', '46', '47', '48', '54', '55', '58', '59']),
  'Entre 861 y 1100 px la barra lateral se reduce a iconos y los quince enlaces del menú se quedan sin nombre. Quien navega con lector de pantalla oye «enlace» quince veces seguidas y no sabe a dónde va ninguno.',
  '<code>.side .et{display:none}</code> quita el texto de la vista y también del árbol de accesibilidad, y los enlaces <code>.it</code> no llevan <code>aria-label</code> ni <code>title</code>. El sistema pide que la etiqueta no desaparezca (§7.2).',
  par(panel('Antes — lo que anuncia un lector de pantalla', pre(arbol('ariaantes')), 'antes'), panel('Después — con el texto oculto solo a la vista', pre(arbol('ariadespues')), 'despues')),
  '.side .et{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}\n/* o, en cada enlace: <a class="it" aria-label="Padrón de clientes" …> */',
  'A 1000 px, <code>ariaSnapshot()</code> del <code>.side</code> debe devolver <code>link "Tablero"</code>, <code>link "Padrón de clientes"</code>… y ningún <code>link:</code> vacío. Medido en <code>27_padron_clientes</code>.')

cambio(A, 'El icono del botón verde deja de verse gris', 'pide',
  'Seis archivos con el fallo medido: ' + archivos(['22', '24', '26', '32', '51', '58']) + '. La regla descendiente <code>.state .ico{…}</code> aparece en 21 de las 50 pantallas.',
  'En el estado de error de gestoría, el botón verde «Reintentar» lleva un icono gris que casi desaparece sobre el verde.',
  '<code>.state .ico</code> alcanza a cualquier <code>.ico</code> del bloque y no solo al grande que cuelga del estado, así que el icono pequeño del botón hereda el gris. El PDF de cambios lo da por corregido (C3); en estos archivos la regla antigua sigue ahí.',
  a_d('obs01', 'Estado de error de gestoría: el botón Reintentar con el icono gris sobre el verde', 'El mismo botón con el icono blanco', 'Antes — icono gris, 1,03:1', 'Después — icono blanco, 4,89:1'),
  '/* antes */\n.state .ico{width:30px;height:30px;color:var(--text-3)}\n\n/* después (y .esp > .ico en el catálogo 26) */\n.state > .ico{width:30px;height:30px;color:var(--text-3)}',
  'El icono del botón mide 4,89:1 contra el verde. El mínimo para un gráfico es 3:1.')

cambio(A, 'El gris del texto auxiliar llega a 4,5:1', 'pide',
  '29 de las 50 pantallas declaran <code>--text-3: #66717F</code>; las otras 20 ya traen <code>#5C6675</code>. El fallo se midió en ' + archivos(['13', '24', '26', '34']) + '.',
  'El texto auxiliar (rótulos pequeños, el departamento bajo un nombre) queda por debajo del mínimo cuando cae sobre el fondo de una fila con el cursor encima.',
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
  '<code>58_altas_como_modal</code> y <code>59_editar_cliente</code>.',
  'En <code>58</code>, los 14 <code>id</code> del formulario «Nuevo cliente» (<code>rs</code>, <code>rfc</code>, <code>tipo</code>, <code>cp</code>, <code>reg</code>, <code>dom</code>, <code>csf</code>, <code>idr</code>, <code>grp</code>, <code>mar</code>, <code>per</code>, <code>rol</code>, <code>cor</code>, <code>tel</code>) se repiten en la versión de teléfono. Cada <code>label for</code> resuelve al primero, así que 12 de los 14 controles del teléfono se quedan sin nombre. <code>59</code> repite el mismo defecto.',
  None, '',
  '/* en la versión de teléfono */\n<label for="rs-tel">Razón social</label>\n<input id="rs-tel" …>',
  '<code>document.querySelectorAll(\'[id]\')</code> no debe devolver identificadores repetidos (§11).')

cambio(A, 'El contador de Asistencia se lee con claridad', 'pide',
  '<code>13_panel_asistencia_rhl</code> · <code>.it .n</code> · línea 95.',
  'El «4» junto a Asistencia es el número que le dice a RHL si hay incidencias por dictaminar. Con texto casi negro sobre rojo, a 10,5 px, cuesta leerlo.',
  'La regla fija <code>color:#2A1512</code> sobre el rojo <code>rgb(194,66,56)</code>: 3,40:1. Con <code>#FAFCFD</code> (el <code>--chrome-alerta-ink</code> del sistema) sube a 4,94:1.',
  a_d('ev13', 'Menú lateral con el contador 4 en texto oscuro sobre rojo', 'El mismo contador con texto claro', 'Antes — 3,40:1', 'Después — 4,94:1'),
  '/* antes */\n.it .n{margin-left:auto;background:var(--err);color:#2A1512;…}\n\n/* después */\n.it .n{margin-left:auto;background:var(--err);color:#FAFCFD;…}',
  'El contador pasa de 3,40:1 a 4,94:1 (mínimo 4,5:1 para texto normal).')

cambio(A, 'Las casillas sin marcar se distinguen con sol', 'pide',
  '<code>55_verificacion_pedido</code> · <code>.ren .caja</code> · línea 665.',
  'Las casillas que aún no se han marcado casi se funden con el fondo. Son justo las que el instalador necesita ver para saber qué le falta.',
  'El borde usa <code>--border-2</code>, que contra el fondo da 1,70:1. El archivo ya declara <code>--border-ctrl</code> (línea 90), el token para el borde de un control, y esta regla no lo usa: con él llega a 3,1:1. La casilla marcada ya cumple, con 5,78:1.',
  a_d('ev55', 'Tres renglones sin marcar con la casilla en gris claro', 'Los mismos renglones con la casilla en gris oscuro', 'Antes — borde a 1,70:1', 'Después — borde a 3,1:1'),
  '/* antes */\n.ren .caja{… border:2px solid var(--border-2); …}\n\n/* después */\n.ren .caja{… border:2px solid var(--border-ctrl); …}',
  'El borde pasa de 1,70:1 a 3,1:1 contra el fondo (mínimo 3:1 para un control).')

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

# ================================================================ B · PROPUESTAS
B = 'B'
cambio(B, 'El padrón con todos los ajustes a la vez', 'dis',
  '<code>27_padron_clientes</code>. Prototipo sobre el archivo real, que se entrega a pedido.',
  'Suma el acordeón de sucursales, los estados de documentos por eje, el aire bajo la cabecera, el buscador a 24 px, las acciones de fila ancladas a la derecha y la retirada del banner de duplicados (D8) y del chip «por vencer» (D7), que el aviso del 28 de septiembre deja pospuestos.',
  'A 1280 px, «Ver órdenes» está a la vista en 0 de 4 filas y los botones de fila completos son 6 de 18. Con los ajustes, 4 de 4 y 18 de 18. A 1024 px, de 0 de 4 y 0 de 18 a 4 de 4 y 18 de 18.',
  a_d('p27', 'Padrón de clientes tal como llega en el archivo, con banner de duplicados y chip por vencer', 'Padrón de clientes con acordeón, estados por eje y acciones ancladas', 'Antes — 1440 px', 'Después — 1440 px', apilado=True),
  None,
  'La columna de acciones anclada a la derecha es una propuesta de Studio sin brief propio. Por debajo de 1331 px la tabla no cabe junto a la barra lateral y la última columna, la de acciones, queda fuera. Sin resolver: «Acciones» alineada con su casilla, y el botón flotante, que sigue tapando parte de la última fila.',
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
  'No se exige como fallo de accesibilidad: con la excepción de espaciado de WCAG 2.5.8 se cumple, y es una divergencia de §7.3. Se recomienda porque es un cambio de una línea.',
  '<table class="mini"><thead><tr><th>Pantalla</th><th>Elemento</th><th class="r">Medida</th></tr></thead><tbody>'
  '<tr><td><code>27</code></td><td>casillas <code>.selfila input.rowsel</code></td><td class="r">15 × 15 px</td></tr>'
  '<tr><td><code>27</code></td><td>buscador <code>#buscar</code></td><td class="r">329 × 16 px</td></tr>'
  '<tr><td><code>27</code></td><td>botones de orden de la cabecera</td><td class="r">160 × 21 px</td></tr>'
  '<tr><td><code>47</code></td><td>buscador <code>.hist .search</code></td><td class="r">216 × 16 px</td></tr>'
  '<tr><td><code>47</code></td><td>enlaces <code>.fuentes a</code></td><td class="r">780 × 19,8 px</td></tr>'
  '<tr><td><code>58</code></td><td>correo y teléfono <code>.ctrl input</code></td><td class="r">335 × 19 px</td></tr></tbody></table>',
  'input[type="search"],.folio,.migas a{min-height:24px;padding-block:var(--sp-1)}',
  'Ningún destino de pulsación mide menos de 24 px de alto.')

cambio(C, 'Los botones hermanos del portal del cliente se parecen', 'rec',
  '<code>05_app_cliente</code> · <code>.abtn</code> · líneas 246 a 249.',
  '«Contactar a DPROMA» y «Reagendar cita» no se ven iguales: en uno el icono está junto al texto y en el otro apartado, y el botón es más alto.',
  'Los dos son <code>.abtn</code> con el mismo CSS. El texto de «Contactar a DPROMA» (120 px) no cabe en la media celda de la rejilla, envuelve a dos líneas y el nodo de texto ocupa todo el ancho restante: el icono se queda a la izquierda, lejos de su palabra, y el botón sube de 44 a 52 px. Falta <code>white-space:nowrap</code> o un rótulo más corto.',
  '', '.abtn{white-space:nowrap}   /* o rotular «Contactar» */',
  'Los dos botones miden 44 px de alto y el icono queda junto a su palabra.')

# ================================================================ D · AVISO
D = 'D'
cambio(D, 'El padrón dibuja lo que se pospuso: vigencia y duplicados', 'pide',
  '<code>27_padron_clientes</code> · D7 y D8 del aviso del 28 de septiembre.',
  'D7 pospone la vigencia por documento (no existe la columna) y D8 pospone los duplicados. En el estado por defecto, <code>27</code> pinta el chip «7 con un documento por vencer», la pastilla «Por vencer» con su fecha y un aviso de 30 días, y la tarjeta «Dos pares de razones sociales se parecen demasiado» con dos botones «Comparar y decidir». La ficha reconoce que <code>27</code> lo dibuja.',
  'Se retiran, como en el prototipo del cambio ' + '@@padron@@' + ', y se vuelven a dibujar cuando D7 y D8 dejen de estar pospuestas.',
  '', None, 'En el estado por defecto no aparece ni «por vencer» ni «Comparar y decidir».')

cambio(D, 'La alta de cliente dice la frase del aviso', 'menor',
  '<code>41_alta_cliente</code> · D2.',
  'La sucursal es opcional, pero falta la frase literal «Sin sucursal no se le puede programar una orden; se puede añadir después desde la ficha». La sección dice el todo o nada y el estado vacío omite la consecuencia.',
  'Es una omisión de texto; el fondo está bien.', '', None,
  'La frase aparece en la sección «Sucursal» del alta.')

PARTES = {
 'A': ('Parte A', 'Lo que se pide', 'Nueve cambios. Los cinco primeros son sustituciones que se repiten en muchos archivos; los cuatro siguientes son problemas propios de una pantalla o una contradicción con el aviso del 28 de septiembre. Cada uno cumple alguna de las cinco condiciones de crítico.'),
 'B': ('Parte B', 'Propuestas de diseño', 'Ocho rediseños. Cada uno parte de lo que dibujó DPROMA, evalúa al menos dos opciones (la primera siempre es el mínimo cambio sobre su dibujo) y se probó en el navegador a 1440, 1280, 1024 y 390 px. Son prototipos: ningún archivo de DPROMA se modificó.'),
 'C': ('Parte C', 'Mejoras sencillas', 'Diez cambios que no se exigen. Cada uno mejora algo visible y, varias veces, delata una causa que se repite en otras pantallas.'),
 'D': ('Parte D', 'El aviso del 28 de septiembre', 'Se comprobaron los doce puntos del aviso contra las cinco pantallas del padrón. Casi todo está donde debe. Tres cosas no, y las tres tienen que ver con lo que se pospuso.'),
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
indice_html = ''
for k in 'ABCD':
    indice_html += f'<h3 class="idx-parte">{PARTES[k][0]} · {PARTES[k][1]}</h3><ol class="indice" start="{[i for p, i, t, g in indice if p == k][0]}">' + ''.join(
        f'<li><a href="#c{i}"><span class="n">{i}</span><span class="t">{t}</span><span class="g g-{g if g != "menor" else "rec"}">{PCT[g]}</span></a></li>' for p, i, t, g in indice if p == k) + '</ol>'

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
 ('Textos de 10,5 px que no están en mayúsculas', '240', '45 de 50', 'El sistema solo prevé ese tamaño para rótulos en mayúsculas (§2.1). Fuera de ahí cuesta leerlo.', 'Sin cambio para DPROMA: el sistema se contradice (§7.2) y lo resuelve Studio'),
 ('Variables de color o espaciado que se usan y nunca se definen', '9', '7 de 50', 'El navegador ignora la variable y el elemento pierde ese valor.', 'El caso de <code>--sp-5</code> está en el ' + c('Mi día')),
 ('Elementos que usan <code>--sp-5</code>, que nadie define', '67', '7 de 50', 'Quedan con 0 px de espaciado donde debería haber 20 px.', 'Ver ' + c('Mi día')),
 ('Parejas de botones de distinta altura o con el icono en otro sitio', '5', '5 de 50', 'Dos botones que hacen cosas parecidas se ven distintos.', 'Ver ' + c('Los botones hermanos')),
]
tabla_med = ('<table class="t t-med"><colgroup><col style="width:27%"><col style="width:9%"><col style="width:11%"><col style="width:31%"><col style="width:22%"></colgroup>'
  '<thead><tr><th>Qué se contó</th><th class="r">Cuántos</th><th>En cuántas pantallas</th><th>Por qué importa</th><th>Dónde se resuelve</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td class="r">{b}</td><td>{c_}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c_, d, e in MEDIDAS) + '</tbody></table>')

NO_SE_PIDE = [
 ('Iconos como sprite SVG (<code>&lt;use href="#i-…"&gt;</code>)', 'Se adopta. Funciona sin red y sin el parpadeo de una fuente que carga tarde. Quien debe corregirse es el sistema: §6.5 pedía Material Symbols por <code>&lt;link&gt;</code>, y eso contradice a D116.'),
 ('<code>.banda.b-info</code>', 'Se adopta el nombre de clase.'),
 ('Agenda de instaladores propia', 'Se queda. Solo cambio mínimo (cambio ' + ref('Agenda de instaladores') + ').'),
 ('Panel «Con qué filtros» como registro', 'Se queda como registro de auditoría, sin controles.'),
 ('<code>.grp</code> a 10,5 px sin mayúsculas', 'Contradicción del sistema: §2.1 lo limita a mayúsculas y §7.2 lo usa sin ellas. La resuelve Studio.'),
 ('Antigüedad de saldo por tramos', 'Contradicción del sistema entre §1.4 y §12.5. La resuelve Studio.')]
tabla_no = ('<table class="t"><colgroup><col style="width:34%"><col style="width:66%"></colgroup><thead><tr><th>Decisión de DPROMA</th><th>Qué ocurre</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in NO_SE_PIDE) + '</tbody></table>')

partes_html = [x.replace('@@padron@@', ref('El padrón con todos')) for x in partes_html]
# ---------------------------------------------------------------- documento
CSS = open(os.path.join(AQUI, 'revision.css'), encoding='utf-8').read()
DOC = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITULO} — 2894 Studio</title>
<meta name="description" content="Lo que se midió en las 50 pantallas del paquete del 12 de octubre, explicado cambio por cambio con capturas del antes y del después." />
<style>{CSS}</style>
</head>
<body>
<nav class="sitio" aria-label="Navegación"><a class="marca" href="/">2894 <span>Studio × DPROMA</span></a><span class="enlaces"><a href="/entregables">← Entregables</a><a href="#indice">Índice</a><a href="/entregables/revisiones/{PDF}">PDF</a></span></nav>

<main>
<section class="portada">
  <div class="regla"></div>
  <p class="eyebrow">SIO-DPROMA · 2894 Studio</p>
  <div class="medio">
    <h1>{TITULO}</h1>
    <p class="sub">Lo que se midió en las 50 pantallas del paquete del 12 de octubre, explicado cambio por cambio: dónde está, qué se ve, qué cambiar y cómo comprobarlo, con capturas del antes y del después.</p>
  </div>
  <p class="fecha">14 oct 2026 · Informe para el equipo de ingeniería de DPROMA</p>
</section>

<section class="como" id="indice">
  <header class="ph"><span class="eyebrow">Antes de empezar</span><h2>Cómo leer este informe</h2></header>
  <p class="lede">Llegaron 50 pantallas HTML y se midieron todas en el navegador, con las fuentes reales. Veintitrés se revisaron una por una; las otras veintisiete pasaron solo por los medidores automáticos. Es la primera revisión de estas pantallas: describe lo que hay en los archivos recibidos.</p>
  <div class="stats">
    <div class="stat"><b>5</b><h3>sustituciones que cierran 32 críticos</h3><p>Se repiten en muchos archivos y se aplican igual. Son los cambios 1 a 5.</p></div>
    <div class="stat"><b>4</b><h3>cambios propios de una pantalla</h3><p>Seis pantallas tienen además un problema que ninguna sustitución arregla. Son los cambios 6 a 9.</p></div>
    <div class="stat"><b>134</b><h3>destinos de pulsación bajo 24 px</h3><p>En 29 pantallas. No se exige, pero es lo más repetido: cambio {ref('Los destinos de pulsación')}.</p></div>
  </div>
  <p>Cada cambio lleva una etiqueta que dice cuánto pesa:</p>
  <ul class="plano">
    <li><span class="tag tag-pide">Se pide</span> cumple al menos una de las cinco condiciones de crítico: falla de accesibilidad medida; impide la tarea u oculta la acción principal; acción irreversible o de dinero sin protección; contradice una decisión de DPROMA o expone datos personales; o es un rediseño que Studio marcó como crítico y es viable.</li>
    <li><span class="tag tag-dis">Propuesta de diseño</span> es un rediseño probado en un prototipo. El veredicto de viabilidad lo acompaña.</li>
    <li><span class="tag tag-rec">Recomendado</span> no se exige. Mejora algo visible y a veces delata una causa que se repite.</li>
  </ul>
  <p>Varios defectos nacen en un bloque que se copia de pantalla en pantalla, y con cada copia se repiten. La cabecera <code>.p4</code> sin relleno inferior está en 36 archivos, la regla <code>.state .ico</code> en 21 y el menú lateral colapsado deja sin nombre sus quince enlaces en 35 de las 42 pantallas que lo llevan. Corregir el bloque de origen y repetir la corrección es más barato que perseguir cada síntoma.</p>
  <h3 class="sub">Qué se contó en las 50 pantallas</h3>
  <p>Antes de revisar nada a mano, un programa abrió cada pantalla en un navegador y contó lo que se puede contar sin criterio humano: botones pequeños, contrastes, menús sin nombre. Sirve para saber qué tan extendido está cada problema.</p>
  <p class="nota">Que algo se cuente no significa que sea un error: son candidatos. Los cambios de las partes A y B son los que una persona reprodujo en el archivo y otra intentó refutar.</p>
  {tabla_med}
  <h2 class="idx">Los {n} cambios</h2>
  {indice_html}
</section>

{chr(10).join(partes_html)}

<section class="parte" id="no-se-pide">
  <header class="ph"><span class="eyebrow">Parte E</span><h2>Lo que no se pide, y por qué</h2><p class="lede">De los 268 puntos de cumplimiento revisados, 128 son decisiones de DPROMA que se adoptan tal como están y pasan a documentarse en el sistema de diseño. Estas son las que más se notan.</p></header>
  {tabla_no}
</section>

<section class="parte" id="abierto">
  <header class="ph"><span class="eyebrow">Parte F</span><h2>Lo que falta y lo que queda abierto</h2><p class="lede">Cinco puntos que ninguna medición resuelve y un aviso sobre la ficha. Dos piden un archivo, uno pide una respuesta de DPROMA y dos son decisiones de diseño sin resolver.</p></header>
  <article class="cambio abierto"><header><h3><code>49_alta_orden</code> no viene en el ZIP</h3></header><p class="que">El PDF de cambios dice que se actualizó, y no está entre las 50 pantallas. Dos observaciones sobre esa pantalla (la caja de «Croquis y anexos» cortada y la sombra sobre la barra de acciones) quedan sin respuesta hasta recibirla.</p></article>
  <article class="cambio abierto"><header><h3><code>SUPUESTOS.md</code> no viene en el ZIP</h3></header><p class="que"><code>FICHAS_TECNICAS.md</code> remite a él para las decisiones sin ratificar (S-25, S-28, S-30, S-31…). Sin ese archivo no se puede saber qué se dio por bueno y qué sigue pendiente.</p></article>
  <article class="cambio abierto"><header><h3>¿Qué manda sobre el plazo de los tickets?</h3></header><p class="que">La ficha de <code>24_tickets</code> en la tanda 3 dice que se retiró el reloj de plazo y que la antigüedad va en gris, igual en los seis renglones. La tanda 4 habla de que tickets conserva su propio semáforo de plazo. El archivo dibuja el plazo: «Vence hoy», con una regla de cálculo de 420 caracteres. El cambio {ref('Tickets TI')} depende de cuál sea la respuesta.</p></article>
  <article class="cambio abierto"><header><h3>«Acciones» alineada con su casilla</h3></header><p class="que">En el padrón, el encabezado «Acciones» es solo para lectores de pantalla y los botones se alinean a la derecha. No hay una solución evaluada para alinearla con su casilla.</p></article>
  <article class="cambio abierto"><header><h3>El botón flotante tapa la última fila</h3></header><p class="que">El botón del asistente cubre «Siguientes» en el paginador del padrón a 1280 px. El sistema no documenta una zona segura para él, y el mismo botón está en <code>21</code>, <code>24</code>, <code>27</code> y <code>41</code>.</p></article>
  <div class="aviso"><b>Nueve arreglos que la ficha da por hechos y que el archivo no tiene.</b> <code>FICHAS_TECNICAS.md</code> lista correcciones de accesibilidad «encontradas y corregidas», verificadas con axe-core. Se buscó cada una en el ZIP y las nueve faltan. Cinco son el <code>&lt;header class="p4"&gt;</code> que duplicaba <code>role="banner"</code> y debía ser <code>&lt;div class="p4"&gt;</code>: <code>26</code>, <code>33</code>, <code>42</code>, <code>43</code> y <code>44</code>, todos con la etiqueta <code>header</code> aún presente. Tres son <code>--text-3-fuerte</code> en <code>24</code>, <code>33</code> y <code>01</code>, que no aparece ni una vez; en esos tres archivos <code>--text-3</code> sigue en <code>#66717F</code> (4,21:1). La novena es <code>57</code>: la ficha dice que sus dos variantes pasaron de <code>role="menu"</code> a <code>role="group"</code>, y el archivo conserva <code>role="menu"</code> en las dos. Lo más probable es que las correcciones vivan en otra copia del código.</div>
</section>

<section class="parte" id="firmeza">
  <header class="ph"><span class="eyebrow">Parte G</span><h2>Qué tan firme es todo esto</h2><p class="lede">Bastante en lo medido y menos en lo exhaustivo. Conviene decir las dos cosas.</p></header>
  <ul class="plano">
    <li><b>Medido en el navegador, con las fuentes reales.</b> Los medidores de contraste, tamaño táctil, menú y espaciado se probaron antes con HTML de respuesta conocida y acertaron 15 de 15.</li>
    <li><b>Probado por otra persona.</b> 119 afirmaciones altas o críticas pasaron por revisores que intentaron refutarlas con medición propia: 110 confirmadas, 9 exageradas y ya corregidas, ninguna refutada.</li>
    <li><b>No es una lista exhaustiva.</b> Una segunda pasada ciega sobre dos pantallas coincidió en solo el 43 % de las reglas citadas y reprodujo 5 de los 10 hallazgos altos del original, además de encontrar otros nuevos. Lo que ambas pasadas hallan es sólido; lo demás puede existir.</li>
    <li><b>Veintisiete pantallas solo con medición mecánica.</b> Sus hallazgos son candidatos hasta que alguien los mire. Las sustituciones de la parte A se contaron además sobre las 50 por búsqueda en el código.</li>
    <li><b>Todo se refiere a los archivos recibidos.</b> No a lo que DPROMA tenga en otra carpeta o rama.</li>
  </ul>
</section>
</main>
<footer class="pie"><span>SIO-DPROMA · 2894 Studio</span><span>{TITULO}</span></footer>
</body>
</html>
'''
destino = os.path.join(WEB, 'revision-de-pantallas.html')
open(destino, 'w', encoding='utf-8').write(DOC)
print('escrito', destino, len(DOC) // 1024, 'KB;', n, 'cambios')
