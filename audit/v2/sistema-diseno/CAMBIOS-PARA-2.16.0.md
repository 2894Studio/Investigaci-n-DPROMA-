# Cambios propuestos al sistema de diseño SIO-DPROMA · de la 2.15.0 a la 2.16.0

Documento de traspaso para el chat del sistema de diseño. Es autocontenido: cada cambio dice dónde va, qué dice hoy el documento (citado literal), qué evidencia lo respalda, qué texto proponer y a quién afecta.

## 0. Contexto en seis líneas

- **Origen.** Revisión de las 50 pantallas HTML del paquete del 12-oct-2026 (carpeta `html_v2/` del cliente, que declara estar «alineada a design-rules v2.15.0») contra el md de la **2.15.0**. Todas las citas de este documento se contrastaron con ese texto.
- **Base.** `docs/sistema-diseno-sio-dproma.md` **2.15.0**, idéntico (sha `a4b43d7a3f3e`) en 4 ramas remotas. La rama de trabajo de la auditoría sigue en 2.13.3 y **no sirve de base**. Falta elegir en cuál de las cuatro se commitea.
- **Versión.** **2.16.0** (minor: reglas nuevas y contradicciones corregidas). Hay un cambio de valor visible, el de `.tip` (S-07); si se prefiere, ese solo va en patch.
- **Propagación.** La skill `sio-dproma-design-sync`: `docs/sistema-diseno-sio-dproma.md` (fuente) → `web/entregables/design-rules.md` → `web/entregables/reglas-de-diseno.html` (si cambia una variable de `:root` o un componente visible) → fila de historial en `design-rules.md` y en `#historial` → front matter (`version`, `last_updated`). Si se adoptan los tokens de interlineado (S-09), regenerar `web/design-tokens.json` con `scripts/gen-design-tokens.py`.
- **Historial.** Lo lee el cliente: cambio neto, una sola fila por fecha, sin narrar el proceso ni mencionar la revisión. Hay una fila propuesta en la sección 5.
- **Qué no entra.** Nada que sea del proceso de revisión. Las plantillas que el cliente copia a cada pantalla (`ARQ-P4`, `ARQ-CROMO`) **no están en este md**: sus defectos son del cliente y van en el informe de ingeniería, no aquí.

## 1. Resumen: 22 cambios, y a quién afecta cada uno

«Solo documentación» no obliga al ingeniero a tocar ningún archivo. «Pantallas nuevas» es una exigencia para lo que construya desde ahora; ninguna obliga a rehacer las 50 actuales.

| # | Cambio | Dónde | Afecta a |
|---|---|---|---|
| **A · Contradicciones del propio documento** | | | |
| S-01 | Admitir el sprite SVG de iconos; retirar el `<link>` de Material Symbols | §6.5 | Solo documentación (ajusta el texto a lo que ya hay) |
| S-02 | Aclarar el 10,5 px de `.grp` | §2.1 y §7.2 | Solo documentación |
| S-03 | `.banda-info` → `.banda.b-info` (y las otras tres variantes) | §6.9 | Solo documentación |
| S-04 | `.tabla-caja{overflow-x:auto}` y `thead th{position:sticky;top:0}` se anulan entre sí | §6.11 | Pantallas nuevas |
| S-05 | `warn` frente a `err` en «falta un documento» | §1.3 | Solo documentación |
| S-06 | Quitar «Reenviar liga de registro» del menú de ejemplo | §6.14 | Solo documentación |
| S-07 | `.tip` a 11,5 px contradice «ningún texto baja de 12 px» | §6.23 | Valor visible (11,5 → 12 px) |
| **B · Reglas nuevas con evidencia medida** | | | |
| S-08 | Estados por eje y variante `.p-neutro` = «sin dato» | §6.10, §6.12 | Pantallas nuevas |
| S-09 | Escala de interlineado | §2 (+ tokens) | Pantallas nuevas |
| S-10 | Botón flotante del asistente y su zona segura | §6.19 o sección nueva | Pantallas nuevas |
| S-11 | Fila desplegable: diseño visual de la fila hija | §6.15, §13.3 | Pantallas nuevas |
| S-12 | Cabecera en vacío, error y cargando; hilo que recibe mensajes | §6.4 | Pantallas nuevas |
| S-13 | Cabecera con solo título: caso medido | §3.1 | Solo documentación |
| S-14 | `.banda` sin margen propio; una regla de permisos informa, no advierte | §6.9 | Pantallas nuevas |
| S-15 | Agenda (rejilla persona × día) | §6.24 (nueva) | Solo documentación (adopta la del cliente) |
| S-16 | Tarjeta con pie | §6.3 | Pantallas nuevas |
| S-17 | Hilo de conversación | §6.25 (nueva) | Pantallas nuevas |
| S-18 | Un registro se escribe literal; un filtro histórico no es un filtro aplicado | §6.21 | Pantallas nuevas |
| S-19 | `i-info` en el sprite de iconos | §6.23 | Solo documentación |
| S-20 | Trampa 11: nombre corto que ya existe (`.cuerpo`) | §10 | Solo documentación |
| S-21 | Tres preguntas nuevas en el checklist | §11 | Solo documentación |
| S-22 | Estado «Inactivo» con `p-pause` | §6.10 | Solo documentación |

Los cambios que dependen de una decisión ajena (Legal, DPROMA) están en la sección 4 con su texto ya redactado, para llevarlos cuando se resuelvan.

---

## 2. A · Contradicciones del propio documento

### S-01 · §6.5 Iconos: admitir el sprite SVG y retirar el `<link>` de Google Fonts

- **Hoy dice** (§6.5): «Material Symbols Rounded, variante rellena (`FILL@1`)… Se cargan por subconjunto… `<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:…&icon_names=…" rel="stylesheet">`».
- **Choca con D116** (§2, «Las fuentes se autoalojan»): «un CDN que no responde falla **en silencio**… la pantalla cae a `system-ui` sin ningún error visible». §6.5 prescribe exactamente ese modo de fallo para los iconos: si la fuente no carga, el icono se pinta como texto («dashboard», «group»).
- **Evidencia.** Las **50 de 50** pantallas del cliente usan un sprite SVG en línea y **ninguna** usa `.msi`. `27_padron_clientes`: 39 símbolos, `<symbol id="i-pin" viewBox="0 0 24 24">…</symbol>`, uso `<svg class="ico ico-sm" aria-hidden="true"><use href="#i-pin"/></svg>`, y estas medidas: `.ico{width:18px;height:18px;stroke:currentColor;stroke-width:1.6;fill:none;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}`, `.ico-sm{width:13px;height:13px}`, `.ico-xs{width:11px;height:11px}`. En el repo de Studio ya hay dos familias: Material Symbols en el padrón y el acceso; sprite en las pantallas de Finanzas.
- **Propuesta.** Reescribir §6.5 como «Iconos (`.ico`, sprite SVG)»: el sprite va en línea una sola vez al inicio del `<body>` (`<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>…</defs></svg>`); cada icono es un `<symbol id="i-…" viewBox="0 0 24 24">`; se usa con `<svg class="ico" aria-hidden="true"><use href="#i-…"/></svg>`; hereda `currentColor`; tres tamaños (18, 13, 11 px). Conservar de la sección actual la parte que sigue siendo cierta: el icono acompaña a un texto salvo que sea un botón-icono con nombre (§6.19), y la comprobación análoga a la de `icon_names`: **todo `<use href="#i-…">` apunta a un `<symbol>` que existe** (`[...document.querySelectorAll('use')].filter(u => !document.querySelector(u.getAttribute('href')))` sale vacío). Eliminar `.msi`, el `<link>` y la regla del subconjunto.
- **Ojo.** El md usa `.msi` en 24 sitios (ejemplos de §6.9, §6.10, §6.12, §6.14, §6.19 y otros); hay que migrarlos a `.ico` en la misma pasada.
- **Afecta a.** Solo documentación: ajusta el texto a lo que las 50 pantallas ya hacen.

### S-02 · §2.1 y §7.2: el 10,5 px de `.grp`

- **Hoy dice** (§2.1): «Se admite una excepción, y solo una: 10,5px en mayúsculas con `letter-spacing` para los **rótulos de grupo** de la barra lateral y las etiquetas de campo del modo tarjeta». §7.2 declara `.grp{margin:14px 8px 4px;font-size:10.5px;font-weight:700;letter-spacing:.1em;color:var(--chrome-dim)}` **sin** `text-transform:uppercase`.
- **Evidencia.** La medición automática cuenta 240 textos de 10,5 px sin mayúsculas en 45 de las 50 pantallas. Medidos de nuevo por clase, 197 de los 252 elementos con ese tamaño y sin mayúsculas son `p.grp`, los rótulos de grupo del menú (Principal, Operación, ICEV, Trámites vehiculares, Dirección y Administración, Soporte). El resto son `span.prio`, `span.tag`, `span.badge`, `span.when`, `p.lb` y `span.vigencia`, y esos sí quedan fuera de la excepción.
- **Propuesta (recomendada, porque el cliente decide en lo no crítico).** Dejar `.grp` como está y reescribir la excepción: «10,5px con `letter-spacing` para los rótulos de grupo de la barra lateral —en mayúsculas o en caja de frase, según el rótulo— y las etiquetas de campo del modo tarjeta». Añadir: «La excepción no alcanza a nada que no sea esos dos rótulos» (la agenda de S-15 lo necesita explícito).
- **Alternativa.** Añadir `text-transform:uppercase` a `.grp` en §7.2. Exige que los 45 archivos cambien.
- **Pendiente antes de cerrar.** Medir el contraste de `--chrome-dim` sobre el fondo del cajón a 10,5 px.
- **Afecta a.** Solo documentación con la propuesta recomendada.

### S-03 · §6.9: `.banda-info` frente a `.banda.b-info`

- **Hoy dice** (§6.9): el CSS declara `.banda-info`, `.banda-warn`, `.banda-err`, `.banda-ok`; el párrafo siguiente habla de «`.banda` + una de sus cuatro variantes» y menciona `.banda.b-info`. El documento usa los dos nombres.
- **Evidencia.** El cliente usa `.banda.b-info` (clase compuesta) en **39 de 50** archivos y **ninguno** usa `.banda-info`.
- **Propuesta.** Adoptar la forma del cliente: `.banda.b-info`, `.banda.b-warn`, `.banda.b-err`, `.banda.b-ok`. Reescribir el bloque CSS de §6.9 con esos selectores. Esos nombres solo aparecen en ese bloque (cuatro líneas); el resto del documento ya habla de «`.banda` + variante».
- **Afecta a.** Solo documentación.

### S-04 · §6.11: la cabecera fija y el desplazamiento horizontal se anulan

- **Hoy dice** (§6.11): `.tabla-caja{overflow-x:auto;position:relative}` y, a la vez, `thead th{…;position:sticky;top:0;z-index:5}`.
- **Problema.** Un `overflow-x:auto` en el contenedor convierte a ese contenedor en el ámbito del `position:sticky`: la cabecera se queda fija contra la caja, no contra la página. Cuando la caja no desplaza en vertical, la cabecera «fija» no se fija a nada. Medido en la agenda de instaladores (`34`).
- **Propuesta.** Añadir a §6.11: «`overflow-x:auto` anula el `position:sticky` contra la página: la tabla desplaza por dentro. Una tabla con cabecera fija y desplazamiento horizontal fija la altura de su caja (`max-height`) y desplaza la caja entera, o renuncia a la cabecera fija». Mantener la primera columna fija (`left:0`), que sí funciona.
- **Afecta a.** Pantallas nuevas.

### S-05 · §1.3 Semáforo: `warn` frente a `err` en «falta un documento»

- **Hoy dice** (§1.3): «puede estar en espera de un documento (`warn`), bloqueado por una condición que no depende de quien mira (`block`), o simplemente inactivo (`pause`)».
- **Evidencia.** En `27_padron_clientes` la misma celda usa `warn` para «Falta 1» y `err` para «Faltan los 2», con el mismo texto de consecuencia. §1.3 no dice dónde cambia el estado.
- **Propuesta.** Añadir a §1.3: «`warn` mientras se pueda seguir trabajando el registro; `err` se reserva para lo que impide operar en la pantalla donde se muestra. Un documento que falta es `warn` si el cliente se puede editar y consultar, y solo bloquea la acción que lo exige (programar, facturar)».
- **Afecta a.** Solo documentación.

### S-06 · §6.14: quitar «Reenviar liga de registro» del menú de ejemplo

- **Hoy dice** (§6.14): el menú de acciones por fila de ejemplo incluye «Reenviar liga de registro».
- **Razón.** El dictamen de 2894 (punto 15) la rechazó y DPROMA lo confirmó en D6: no se construye. El ejemplo del sistema la sigue mostrando como válida.
- **Propuesta.** Retirarla del ejemplo. Si hace falta una acción de relleno, usar «Exportar la ficha» (D4).
- **Afecta a.** Solo documentación.

### S-07 · §6.23 Toggletip: `.tip` a 11,5 px

- **Hoy dice** (§6.23): `.tip{… font:500 11.5px/1.5 var(--font-ui); …}`.
- **Choca con §2.1**: «Por debajo de 12px no queda nada».
- **Propuesta.** `font:500 var(--fs-meta)/1.5 var(--font-ui)`. `--fs-meta` vale 12 px (§2), así que el aumento es de 0,5 px en el texto del aviso; comprobar que el ancho de 220 px sigue sirviendo.
- **Afecta a.** Valor visible, mínimo. Si se quiere evitar la subida de versión por esto, es el único cambio de la lista que justificaría un patch separado.

---

## 3. B · Reglas nuevas con evidencia medida

### S-08 · §6.10 y §6.12: un estado por eje, y `.p-neutro`

- **Hoy** (§6.10): `.pill` = estado y `.p-type` = clasificación; las variantes son `.p-ok`, `.p-warn`, `.p-err`, `.p-block`, `.p-pause`. No existe `.p-neutro` ni una regla sobre cuántos estados lleva una fila.
- **Evidencia.** `.p-neutro` aparece definida **idéntica** en 36 de 50 archivos: `.p-neutro{background:var(--surface-2);color:var(--text-2)}`, con 5,97:1 en tema claro y 7,10:1 en oscuro. En `27_padron_clientes` la celda «Documentos fiscales» mezcla un estado con un párrafo y usa cinco estados («Los dos», «Falta 1», «Por vencer», «Faltan los 2», «Sin calcular»).
- **Propuesta para §6.10.** (1) «Una fila muestra **un estado por eje**, no uno por causa. El documento que falta es un dato —una línea de 40 caracteres como máximo bajo la etiqueta—, no un estado nuevo. “Falta un documento” y “falta otro” son el mismo estado». (2) «Un estado que depende de un dato que el producto aún no calcula no se dibuja (hoy: la vigencia)». (3) Variante nueva: «`.p-neutro` = “sin dato”, ni bueno ni malo: “Sin calcular”, “Sin sucursales”. Se mide como el resto (5,97:1 en claro, 7,10:1 en oscuro)» y el CSS de arriba.
- **Propuesta para §6.12.** Cambiar el ejemplo del diagrama «42 incompletos» por una palabra que no afirme bloqueo («con documentos pendientes») y añadir: «El chip dice lo mismo que la pastilla que filtra, con su color».
- **Afecta a.** Pantallas nuevas.

### S-09 · §2: escala de interlineado

- **Hoy.** §2 y §3 definen tamaños y espaciados, no interlineado. `line-height` solo existe dentro de cinco componentes: 1,4 (`.cifras .apoyo`), 1,5 (`.paso-txt`, `.note`, `.ayuda`), 1,55 (`.banda`) y 1,6 (`.tarjeta-estado p`). No hay token ni valor por omisión en `body`.
- **Evidencia (50 pantallas, 1440 px, elementos con texto visible).** `normal` 3.410 elementos en 50 de 50 archivos; después 1,25 (633 elementos, 35 archivos), 1,55 (270), 1,50 (196), 1,35 (192), 1,65 (125), 1,45 (112), 1,40 (77), 1,30 (70), 1,00 (36), 1,60 (29), 1,10 (10), 1,05 (7). **13 valores** en uso. En `13_panel_asistencia_rhl` el título lleva 1,35 y el detalle `normal`, y de ahí la sensación de desorden.
- **Propuesta (valor a decidir por diseño; parte de los que ya usa el sistema).** Tres tokens: `--lh-compacto:1.25` (títulos y datos de una línea), `--lh-texto:1.5` (texto de varias líneas: `.note`, `.paso-txt`, `.ayuda`, `.tip`) y `--lh-lectura:1.6` (párrafos largos, `.tarjeta-estado p`). Regla: «un texto de más de una línea no se deja en `normal`». **No cambiar el `line-height` de `body`** en esta versión: cambiaría la altura de las filas de las 50 pantallas.
- **Afecta a.** Pantallas nuevas. Añade tokens a `design-tokens.json`.

### S-10 · Botón flotante del asistente y su zona segura

- **Hoy.** El documento no tiene ninguna regla sobre el botón flotante (solo menciona `--sh-float` como sombra de barra).
- **Evidencia.** Está en **31 de 50** archivos, siempre con la misma geometría: `.fab{position:absolute;right:max(26px,env(safe-area-inset-right));bottom:max(26px,env(safe-area-inset-bottom));width:52px;height:52px;border-radius:50%}`, y en móvil `right/bottom:max(16px,…)` con 46 × 46 px. En el padrón a 1280 px tapa «Siguientes» del paginador (visto en el prototipo sobre el archivo real).
- **Propuesta.** Sección nueva (o subsección de §6.19): medidas del botón (52 px, 26 px del borde; 46 px y 16 px en móvil), **zona segura**: el contenedor que desplaza reserva por debajo el alto del botón más su margen y un espacio (`padding-bottom` ≥ 52 + 26 + `--sp-3` = 90 px; valor propuesto, no medido en uso), y regla: «Ningún control ni dato de la última fila queda bajo el botón».
- **Afecta a.** Pantallas nuevas. Documenta lo que el cliente ya hace y le añade la zona segura que falta.

### S-11 · §6.15 y §13.3: la fila desplegable, con su diseño visual

- **Hoy dice** (§6.15): documenta el marcado (`<tr class="hijas" id="suc-gav" hidden><td colspan="7">…</td></tr>`) y que `aria-expanded`/`aria-controls` «tienen que apuntar a algo que exista». No dice cómo se ve la fila hija.
- **Evidencia.** `27_padron_clientes`: 4 de 5 botones apuntan a ids que no existen; el contenido vive en un `<td colspan="7">` y a 1280 px «Ver órdenes» cae fuera de la vista (0 de 4). Prototipo medido: con la regla de abajo, 4 de 4 a 1280 y a 1024 px.
- **Propuesta para §6.15 (versión vigente tras la revisión del 14-oct; sustituye a cualquier regla de «560 px alineada a la izquierda»).**
  > La fila hija ocupa el **ancho visible** de la tabla, no el de su `colspan`: `.tabla-caja{container-type:inline-size}` y `.suc-lista{list-style:none;position:sticky;left:0;width:100cqw}`. Las líneas divisorias llegan al final de la fila y la acción («Ver órdenes») va al final de cada fila, siempre a la vista aunque la tabla desplace. Es una banda, no una tarjeta: la tabla principal no va en tarjeta ni se anidan. El estado de la fila hija solo se muestra cuando es una excepción (bloqueada); decir «Puede recibir órdenes» en todas no aporta.
- **Propuesta para §13.3 (excepción).** «Una lista de renglones cortos sobre una banda no crece con el contenedor: se acota al área visible (`100cqw`), no a un ancho fijo. Acotarla a un ancho fijo deja las líneas a medias y la acción lejos del borde».
- **Opcional, sin brief propio.** Columna de acciones anclada a la derecha (`tbody tr:not(.hijas) > td:last-child, thead th:last-child{position:sticky;right:0;z-index:4;background:var(--surface)}`) cuando la tabla desplaza. Probada en el prototipo: botones de fila completos 18 de 18 a 1280 y 1024 px. Decidir antes de documentar.
- **Afecta a.** Pantallas nuevas.

### S-12 · §6.4: cabecera en vacío, error y cargando; hilo que recibe mensajes

- **Hoy** (§6.4, regla 1): «Un solo contenedor, las vistas dentro como hermanas».
- **Evidencia.** En el estado vacío de `28_instalador_mi_dia` la cabecera sigue diciendo «2 citas · 7 h de trabajo · 1 con material incompleto» encima de «Hoy no tienes ninguna cita». Ocurre igual en el estado de error.
- **Propuesta.** Añadir regla: «El título de la cabecera persiste en cualquier estado; el resumen de datos, no. En vacío, error y cargando el resumen se retira: decir “2 citas” sobre “Hoy no tienes ninguna cita” contradice la pantalla». Añadir a la regla 1: «un hilo que recibe mensajes se anuncia con `role="log"`».
- **Afecta a.** Pantallas nuevas.

### S-13 · §3.1: caso medido de una cabecera con solo título

- **Hoy.** §3.1 ya prescribe `.p4{padding-bottom:var(--sp-3)}` y explica por qué el relleno lo declara el contenedor.
- **Evidencia.** El bloque de cabecera que el cliente copia a cada pantalla no lo incorpora: **36 archivos** tienen `.p4` sin relleno inferior; `28` mide 38 px de alto con 12 px de aire arriba y ninguno abajo. Ese bloque no vive en el md (es plantilla del cliente), así que la regla **ya está escrita**.
- **Propuesta.** Añadir a §3.1 el caso: «Una pantalla con solo `.p4-t` queda con 12 px entre su control más bajo y la línea, igual que arriba. Se comprueba midiendo: el control a 0 px de la línea es el síntoma».
- **Afecta a.** Solo documentación.

### S-14 · §6.9: `.banda` sin margen propio; una regla de permisos informa

- **Evidencia.** `24_tickets`: `.detalle .banda` (línea 560) pone margen a cualquier banda dentro de `.detalle`, y la banda de esa pantalla vive en `.det-cuerpo`, que ya tiene relleno: el margen se suma. Además, la segunda caja de la zona superior es una regla de permisos pintada con el color de «vence pronto».
- **Propuesta.** Añadir a §6.9: «`.banda` no lleva margen propio salvo como hijo directo de la zona que la aloja (`.detalle > .banda`). Un selector de margen escrito para un contenedor se aplica también a cualquier descendiente: dentro de otro contenedor con relleno, suma». Y: «Una regla de permisos informa, no advierte: va en `.banda.b-info`, no en `warn`».
- **Afecta a.** Pantallas nuevas.

### S-15 · §6.24 (nueva): Agenda, la rejilla persona × día

- **Hoy.** No existe. §13.9 solo regula bloques cuyo alto viene de un dato; `34_instaladores` tiene su agenda propia.
- **Evidencia.** `34_instaladores`: 53 de 62 nodos de texto por debajo de 12 px; el domingo no cabe a 1280 px.
- **Propuesta (se adopta la del cliente y se documenta).**
  > **Agenda (rejilla persona × día).** Es una tabla de comparación entre filas: lleva `<caption>`, `th scope` en los dos ejes y primera columna fija. **No pasa a modo tarjeta**: convertirla destruye la comparación. Nada de la rejilla baja de 12 px; el nombre se parte, no se corta con puntos suspensivos. El hueco vacío se escribe con texto para lector.
  > **Lo no asignado tiene su fila.** Colgarlo de una persona le atribuye trabajo que no tiene.
  > **Una visita que dura varias franjas marca cada franja que cubre**, sin fusionar filas; si el alto del bloque lo fija la duración, manda §13.9.
  > **El calendario laborable es un dato**, no una clase del componente.
  > La excepción de 10,5 px de §2.1 no alcanza a una agenda.
- **Afecta a.** Solo documentación; el cambio mínimo en `34` está en el informe de ingeniería.

### S-16 · §6.3: tarjeta con pie

- **Evidencia.** `47_asistente`: `.fuentes{margin:calc(var(--sp-3) * -1) …}` dentro de una tarjeta que ya lleva su relleno: la franja sube 12 px y la última línea de cada respuesta entra 8,9 px en ella, a los cuatro anchos.
- **Propuesta.** Subsección nueva tras «Cuándo usar una tarjeta, y cuál»:
  > **Tarjeta con pie.** Son dos zonas hermanas, cada una con su relleno: el cuerpo (`.interior`) y el pie, una banda `--surface-2` con borde superior, como la cabecera pero al final. El pie no se sangra con márgenes negativos. Un pie dice una sola cosa: la procedencia («De dónde salió») son enlaces de lectura; el paso a seguir («Para hacerlo») son botones `.btn.mini`. Se distinguen por la forma, no solo por el rótulo.
- **Afecta a.** Pantallas nuevas.

### S-17 · §6.25 (nueva): Hilo de conversación

- **Hoy.** No existe; hay dos asistentes en el paquete (`47` y `10`) que no comparten ni una clase.
- **Propuesta.**
  > **Hilo de conversación.** El contenedor de mensajes lleva `role="log"`, nombre y `tabindex="0"` si desplaza. Cada turno se rotula con quién habla y cuándo («Tú · hoy 10:31»); el tono no identifica al hablante (las superficies miden entre 1,06 y 1,15 : 1). Una respuesta en curso es una tarjeta con `role="status"` y barras sin texto; una fallida dice qué pasó, qué no se perdió y qué hacer (§6.4, regla 3).
- **Se puede llevar sin esperar** la decisión sobre el contrato del asistente (sección 4): esta regla es de marcado.
- **Afecta a.** Pantallas nuevas.

### S-18 · §6.21: dos reglas de la bitácora

- **Propuesta.** (1) «Lo que se registra se escribe literal. Un registro inmutable guarda valores, no cuentas: “Querétaro y Celaya”, no “2 de 5”». (2) «Un filtro histórico no es un filtro aplicado: va sin “×”, sin `aria-pressed` y sin cursor de puntero; nombra dimensión y valor como en §6.21».
- **Afecta a.** Pantallas nuevas.

### S-19 · §6.23: `i-info` en el sprite de iconos

- **Propuesta.** Añadir `i-info` al conjunto de símbolos del sistema, que es lo que usa el toggletip. Depende de S-01.
- **Afecta a.** Solo documentación.

### S-20 · §10: una trampa nueva, el nombre corto que ya existe

- **Evidencia.** En `47_asistente` un modificador nuevo se llamó `.cuerpo`, que la propia maqueta ya definía como contenedor de página (línea 483): heredó `display:flex` y `gap:16px`.
- **Propuesta.** Añadir como trampa 11 y retitular la sección «Once trampas comprobadas»: «Antes de nombrar una clase corta (`.cuerpo`, `.caja`, `.fila`), se busca si ya existe en el archivo: un modificador con el nombre de un contenedor hereda su `display` y su `gap`». Es el mismo mecanismo que la trampa 10.
- **Afecta a.** Solo documentación.

### S-21 · §11 Checklist: tres preguntas nuevas

- **Propuesta.** Añadir: «¿La cabecera mide ≥ 12 px bajo su última línea, medida sola?»; «Si la pantalla gana aire en la cabecera, ¿se volvió a medir qué queda sobre la barra fija a 390 × 844?»; «¿Algún `margin` negativo compensa el relleno de un contenedor?».
- **Afecta a.** Solo documentación.

### S-22 · §6.10: «Inactivo» con `p-pause`

- **Evidencia.** `27_padron_clientes` pinta «Inactivo» con `.p-neutro`; §1.3 dice que inactivo es `pause` y que no es un error.
- **Propuesta.** Añadir una línea al ejemplo de §6.10: «Inactivo → `.p-pause`, nunca `.p-neutro`: “sin dato” y “apagado” son cosas distintas».
- **Afecta a.** Solo documentación.

---

## 4. No llevar todavía (con el texto listo para cuando se resuelva)

| Tema | Qué falta | Texto o dato |
|---|---|---|
| **Marca de sensibilidad de un dato** | Que **Legal** confirme el término «dato personal» para razón social, RFC, domicilio fiscal, VIN y titular. Es el cliente quien lo usa; no se afirma la clasificación legal. Además, que **la marca la publique el servidor** y no la infiera la pantalla. | «**Marca de sensibilidad de un dato.** Que un dato sea personal o reservado es un hecho sobre el dato, no un juicio sobre el trabajo: entregarlo puede estar permitido y completo. Por eso no lleva color de estado ni de serie: `--warn` es “falta algo” y las series no tienen connotación. **Forma y texto:** pastilla `.sens` con icono de escudo, borde `--border-fuerte`, fondo `--surface` y tinta `--text`; dice la categoría con palabras, «Dato personal: razón social y RFC». **Dónde:** pegada al dato que califica, en su propia línea, nunca mezclada con filtros ni atributos de la misma celda. **Qué no significa:** no avisa de un problema; si una acción sobre el dato no está permitida, eso se dice aparte, con semáforo y texto. El escudo se reserva para esta marca.» Contraste medido: texto 15,21:1 y 13,93:1; borde 3,26:1 y 3,41:1 (claro y oscuro). |
| **Indicador de plazo en un detalle** (§6.20, caso «bandeja con detalle») | Que DPROMA decida qué manda sobre el plazo de los tickets: la ficha de la tanda 3 retira el reloj de plazo, la de la tanda 4 dice que tickets conserva su semáforo, y el archivo dibuja el plazo. | «El plazo se dice una vez, en un indicador de ancho declarado (`minmax(200px,240px)`) junto a los datos del ticket: figura, fecha y nada más. Ámbar si vence hoy o mañana, rojo si venció, verde el resto, gris si no hay plazo. Cómo se calcula va a toggletip. El indicador pinta lo que el servidor devuelve; no enuncia reglas de plazo que el servidor no publique.» |
| **Contrato del asistente** | Que DPROMA decida si el asistente solo consulta (`47`) o también ejecuta con confirmación (`10`). Los dos se abren desde el mismo botón flotante y hoy se contradicen. | Sin texto: la regla es de producto, no de interfaz. |
| **Sección «Pantallas de campo»** (tras §7.3) | Es una propuesta basada solo en lo medido en `28`; conviene validar con más pantallas de campo (`09`, `11`, `12`, `14`, `29`). | «Una pantalla de campo se mide a 390 × 844 descontando el cromo (63 px) y la barra de acción fija (81 px): quedan 667 px menos la cabecera. Lo que decide la jornada queda sobre esa línea». |
| **Antigüedad de saldo por tramos: §1.4 frente a §12.5** | No lo pude confirmar en el texto de la 2.15.0. El auditor lo marcó, pero §12.5 («Reglas de lectura») no menciona la antigüedad. | Regla propuesta, si se confirma: «una distribución por tramos de tiempo (0–30, 31–60, 61–90, +90) usa `--serie-1…4` con leyenda de rangos; el semáforo solo se aplica a un umbral declarado sobre una cifra». |
| **`--sp-5`** | Nada que documentar: ya está en `_sio-tokens.css` y falta en el `:root` embebido de cinco maquetas (`28`, `29`, `51`, `57`, `58`). Es un defecto del cliente. | La comprobación `usados − declarados = ∅` ya existe en §3 y §10. |

## 5. Fila propuesta para el historial (2.16.0)

Tono de las entradas existentes, cambio neto, sin narrar el proceso. Fecha: la del día en que se aplique.

> | 2.16.0 | AAAA-MM-DD | §6.5 pasa a documentar los iconos como sprite SVG (`.ico`) y retira la carga de Material Symbols por `<link>`; §6.9 adopta `.banda.b-info` y las otras tres variantes y fija que `.banda` no lleva margen propio; §2.1 acota el 10,5 px a los rótulos de grupo y las etiquetas del modo tarjeta; §6.23 lleva `.tip` a la escala de texto. Reglas nuevas: un estado por eje y `.p-neutro` (§6.10), escala de interlineado (§2), botón flotante y su zona segura, diseño de la fila hija en la fila desplegable (§6.15), cabecera en vacío y error (§6.4), tarjeta con pie (§6.3), agenda (§6.24) e hilo de conversación (§6.25). §10 pasa a once trampas y §11 gana tres preguntas. |

## 6. Orden recomendado para aplicarlo

1. **S-01** primero, porque S-19 y casi todos los ejemplos de código dependen de `.ico` y `.msi`.
2. **S-03, S-02, S-07, S-05, S-06** (correcciones de texto).
3. **S-08 a S-18** (reglas nuevas), de la más medida a la menos: S-08, S-10, S-11, S-13, S-14, S-12, S-09, S-15, S-16, S-17, S-18.
4. **S-19 a S-22** y la fila de historial.
5. Regenerar `web/design-tokens.json` si se adopta S-09. Comprobar que el front matter de `design-rules.md` coincide con la última fila del historial.

## Anexo · Otros 58 patrones que las fichas marcaron como «sin regla»

Backlog no priorizado: patrones que el cliente usa en 22 pantallas y que el documento no regula. Los que ya tienen cambio arriba (botón flotante, estados de la tabla, fila desplegable, agenda, hilo, marca de sensibilidad, interlineado) no se repiten aquí como pendientes; el resto queda para una segunda tanda.

| Pantalla | Patrón sin regla |
|---|---|
| `01_login` | Escena de fondo del acceso con ~20 hex sin token (azules y teal de la ilustración) |
| `05_app_cliente` | Par de botones de acción hermanos en tarjeta móvil (`.abtn`): rótulos de distinta longitud, uno envuelve y el icono queda apartado |
| `05_app_cliente` | Google Fonts por <link> en una pantalla móvil (línea 10) |
| `05_app_cliente` | Tamaños < 12 px en móvil: `.abtn`, `.stbtn`, `.tile` a 11,5 px y etiquetas de la barra de pestañas a 10 px (línea 264) |
| `05_app_cliente` | Marco de teléfono y barra de estado simulados dentro del DOM |
| `05_app_cliente` | Tokens del antecesor en pantalla de cliente (--text-3 #66717F, 14 más) |
| `13_panel_asistencia_rhl` | Selector descendiente de elemento (`.componente span`, `.componente b`) dentro de un componente cuyas filas contienen <span> con otro rol (acciones, texto en línea). Medido en la bandeja de Asistencia RHL: el span genérico anuló display, gap y margin-top de la fila de botones y partió frases. |
| `13_panel_asistencia_rhl` | Escala de interlineado: el sistema no la define (§2 y §3 solo tienen tamaños y espaciados). En esta pantalla conviven `normal` (≈1,25), 1, 1,05, 1,3, 1,35 y 1,55, y los bloques de texto multilínea del sistema usan 1,4, 1,5, 1,55 y 1,6 sin nombre (§6.7, §6.9, §6.16, §12.4.1). |
| `13_panel_asistencia_rhl` | Fila de bandeja de dictamen (icono-badge 26px + título + detalle + acciones), no descrita en el sistema. Aparece en esta pantalla y es el equivalente de §6.15/§6.12 para colas de decisión. |
| `13_panel_asistencia_rhl` | El 10px de padding (y 9px) aparece en componentes del propio sistema (§6.9 `.note`, §7.2 `.it`) sin estar en la escala --sp-*, por lo que los clientes lo reproducen. |
| `20_tablero` | Columnas de una gráfica que no comparten línea base porque el rótulo del eje vive dentro de la columna |
| `20_tablero` | Gráfica dibujada en CSS o SVG sin tabla equivalente |
| `21_ficha_cliente` | Bloque de lectura con edición en línea (datos fiscales) |
| `21_ficha_cliente` | Banda de estado inactivo (.banda.b-pause) |
| `21_ficha_cliente` | Tabla concepto → icono para dominio de contacto |
| `21_ficha_cliente` | Botón flotante del asistente y su zona segura |
| `22_gestoria` | El folio como enlace de 16 px frente a la regla de que la fila entera navega |
| `23_viaticos` | Estado «pendiente de decisión de otra persona» (Por aprobar, Sin comprobar) sin color de significado |
| `23_viaticos` | Matiz de una celda (justificación, motivo de rechazo, porqué de un botón deshabilitado) |
| `24_tickets` | Indicador de plazo dentro de un detalle (cifra grande + fecha + regla de cálculo) |
| `24_tickets` | Prioridad ordinal (Crítica · Alta · Media · Baja) con forma + color |
| `24_tickets` | Botón flotante del asistente (FAB) y su zona segura |
| `24_tickets` | Plantilla de cabecera .p4 (ARQ-P4) |
| `25_consumo_de_material` | Etiqueta de «dato calculado/derivado» sobre una fila de tabla |
| `25_consumo_de_material` | Color físico de un material (cable rojo, negro, blanco) dentro de una tabla |
| `25_consumo_de_material` | Presupuesto de color de una pantalla de datos |
| `26_estados_de_pantalla` | Muestra de catalogo `.muestra` con rotulo `.rot` y variantes de vacio (filtro / alcance / de verdad) |
| `26_estados_de_pantalla` | Estado «bloqueado» / sin permiso |
| `26_estados_de_pantalla` | Icono dentro de un boton de estado |
| `27_padron_clientes` | Fila desplegable con lista de hijas (acordeón de sucursales) |
| `27_padron_clientes` | Columna de acciones de fila cuando la tabla se desliza |
| `27_padron_clientes` | Estado de expediente en celda (pill específica + consecuencia común) |
| `27_padron_clientes` | Botón flotante del asistente y su zona segura |
| `28_instalador_mi_dia` | Boton de campo `.gordo` (56px) y barra de accion fija `.pie-accion` (decision S-30 de la ficha) |
| `28_instalador_mi_dia` | Tarjeta de cita (`.cita-tel`) con hora, cliente, aviso de material y tres acciones |
| `28_instalador_mi_dia` | Aviso de «sin conexion» permanente en teléfono (`.senal`) |
| `32_cfe_bandeja` | El folio como enlace de 16 px frente a la regla de que la fila entera navega |
| `41_alta_cliente` | Etiqueta de nivel de obligatoriedad por campo («para dar de alta», «para facturar», «para programar») |
| `41_alta_cliente` | Zona segura del botón flotante en pies de formulario |
| `41_alta_cliente` | Excepción a la regla de una frase cuando un aviso del cliente exige una consecuencia |
| `46_cuentas_por_cobrar` | Antigüedad de saldo por tramos: la regla de color de §1.4 y la de §12.5 se contradicen |
| `46_cuentas_por_cobrar` | Fila de KPIs con una tarjeta de texto largo y otras de cifra única |
| `47_asistente` | Burbuja de respuesta de asistente con pie de procedencia (`.msg.ia .tx` + `.fuentes`) |
| `47_asistente` | Hilo de conversacion (`.mensajes`) con turnos de usuario sin tarjeta y de asistente con tarjeta |
| `47_asistente` | Accesos rapidos tipo chip (`.rapido`) y compositor |
| `47_asistente` | Contradiccion entre 10_dprimi_asistente y 47_asistente |
| `48_asistencia_rhl` | Interlineado de interfaz: el sistema no tiene escala ni valor por omisión. Hay `line-height` solo dentro de cinco componentes (1,4; 1,5; 1,55; 1,6) y las pantallas fijan además 1,25, 1,3 y 1,35 por su cuenta; lo demás computa `normal`. El brief I5 cuenta 4–5 interlineados distintos por pantalla en las cuatro de este lote. |
| `51_acceso` | Entrada de tarjeta unica sin columna de marca (`.acceso > .caja-acc`) |
| `51_acceso` | Estado de error de autenticacion con variantes |
| `54_bitacora_descargas` | Marca de sensibilidad del dato (dato personal, confidencial) en un registro o una fila. El sistema tiene el semáforo (§1.3, juicios de estado) y las series (§1.4 y `.p-type`, clasificaciones sin connotación), pero nada para decir «esto tocó dato personal» sin juzgar. 54 usa `--warn` para «incluye razón social y RFC». |
| `55_verificacion_pedido` | Etiqueta de «siguiente paso» sobre el renglón activo de una lista de verificación (`.ren.siguiente::before` con `translateY(-32px)`). El sistema no tiene un patrón para señalar cuál es el próximo elemento a atender dentro de una lista; el cliente lo resolvió con un pseudo-elemento anclado a ojo. |
| `58_altas_como_modal` | Cuerpo de dialogo con secciones que desplaza (`.modal .cuerpo > .seccion`) |
| `58_altas_como_modal` | Marco de dialogo ilustrado en una pagina de referencia (sin <dialog>) |
| `58_altas_como_modal` | Seccion de registro historico dentro de una maqueta de decision (D1: 41 ya no es dialogo) |
| `58_altas_como_modal` | Tabla de medidas con columnas numericas (`.medida`) |
| `59_editar_cliente` | Hoja de especímenes de un diálogo (varios estados del mismo diálogo en una página) |
| `59_editar_cliente` | Campo de solo lectura con motivo |
| `59_editar_cliente` | Nombre del botón que abre un diálogo parcial |
