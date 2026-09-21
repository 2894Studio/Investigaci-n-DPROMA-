---
name: sio-dproma-design-audit
description: Audita un export real de una pantalla de SIO-DPROMA (HTML+CSS de producción, subido por el usuario) contra el sistema de diseño documentado. Produce un informe en PDF con evidencia visual: qué cumple, qué diverge (con severidad), y una propuesta de regla nueva para cada patrón de UI real que el sistema todavía no documenta. Úsalo cuando el usuario pida "audita esta pantalla", "revisa si esto cumple el sistema de diseño", "compara este build contra SIO-DPROMA", o suba un HTML/CSS de producción pidiendo una revisión de diseño/UX.
---

# Auditoría de conformidad y cobertura — SIO-DPROMA

## Qué resuelve esta skill

Dos preguntas distintas, en un solo informe:
1. **Cumplimiento** — de lo que el build real implementa, ¿sigue la receta que ya documentamos?
2. **Cobertura** — de lo que el build real implementa, ¿hay patrones que el sistema *todavía no documenta*? (Esto no es un fallo del build — es un hueco en la fuente de verdad, y esta skill debe proponer cómo cerrarlo, no solo señalarlo.)

El material auditado **no vive en este repo** — son archivos subidos por el usuario (export de una app externa, p. ej. `sio-qa.dproma.com`). No se toca el repo ni el build real; el único artefacto que se produce es el informe.

**Pendiente de esta skill, a fecha de su creación:** no existe todavía un catálogo canónico de "qué pantallas debería tener SIO-DPROMA" integrado aquí (vive en documentos externos del equipo DPROMA, ej. los citados como "doc 14"/"doc 43" en comentarios de CSP del propio HTML de producción). Sin ese catálogo, esta skill audita **la(s) pantalla(s) que el usuario suba**, no puede decir qué pantallas *faltan por subir*. Si en algún momento el usuario aporta ese catálogo, añadir una sección "Cobertura de pantallas" al informe cruzando pantallas auditadas hasta la fecha contra el catálogo — mientras tanto, omitir esa sección sin inventarla.

## Fuentes de verdad a leer siempre

| Archivo | Para qué |
|---|---|
| `docs/sistema-diseno-sio-dproma.md` | Reglas duras del dashboard: tokens exactos, componentes §6, trampas §10, accesibilidad. |
| `docs/sistema-diseno-acceso-sio-dproma.md` | Tokens/componentes específicos de la pantalla de acceso, si el build auditado es login. |
| `docs/decisiones-producto-padron.md`, `docs/patron-dialogo-sio-dproma.md`, `docs/criterios-de-animacion.md` | Reglas complementarias (formularios, diálogo modal, movimiento) — leer las que apliquen según qué patrones aparezcan en el build. |

No asumas de memoria los valores de hex/px — se han visto casos reales de tokens con el mismo nombre y distinto valor entre `acceso-sio-dproma.html` y el resto del dashboard (`--text-3` es el ejemplo documentado). Lee el archivo correspondiente a la pantalla que se está auditando.

## Proceso

### 1. Preparar el material
Copia los archivos subidos al scratchpad de la sesión (nunca al repo ni a `/tmp`). Si el HTML referencia su CSS con una ruta relativa que no coincide con dónde copiaste el CSS, reescribe el `<link>` para que apunte al archivo local.

### 2. Investigación en paralelo (dos agentes Explore, un solo mensaje)
- **Agente A — inventario del build real.** Lee el HTML y el CSS subidos (con Grep si son grandes/minificados — no intentar leerlos enteros de una vez). Extrae: (a) toda variable `var(--x)` usada, con conteo de apariciones; (b) cada definición de clase que coincide con un nombre de componente conocido del sistema (`.pill`, `.tarjeta`, `.btn`, `.modal`, `.p-type`, `.chip`, `.iconbtn`, etc.) — selector completo y reglas CSS literales, incluidas TODAS las variantes/overrides por página si el mismo nombre de clase se redefine en distintas secciones del archivo; (c) si hay `<dialog>` nativo en el HTML o solo el patrón manual `div` + overlay; (d) uso de `aria-live`, `aria-hidden`, `hidden`, `tabindex="-1"`, `aria-sort`, `role="status"` y similares.
- **Agente B — checklist del sistema.** Lee completos los documentos de la tabla de arriba que apliquen a esta pantalla. Extrae un checklist compacto y literal (hex exactos claro/oscuro, escalas de tipografía/espaciado/movimiento, regla de "cuándo usar" y accesibilidad de cada componente §6 que vaya a auditarse, las trampas de §10, reglas de iconos, objetivos táctiles).

No hagas tú mismo la lectura completa de los documentos grandes si puedes delegarla — pero si el build es pequeño y ya conoces bien el sistema por trabajo previo en la sesión, un solo agente (o ninguno, y tú directo con Grep) puede bastar. Usa criterio: no dupliques investigación que ya tengas fresca en contexto.

### 3. Reconstruir evidencia visual (obligatorio, no opcional)
Los informes de esta skill siempre llevan capturas, no solo tablas de texto — pedido explícito y recurrente del usuario.

- **Capturas reales:** sirve los archivos por HTTP local (`python3 -m http.server <puerto> --bind 127.0.0.1` desde el directorio del scratchpad) — **nunca `file://`**, porque el atributo `crossorigin` en los `<link>`/`<script>` del export real dispara bloqueo CORS bajo `file://` y los tokens CSS no resuelven (fondo negro, texto pegado, ver troubleshooting abajo). Renderiza con Playwright (`/opt/pw-browsers/chromium`, ya preinstalado; Node en `/opt/node22/lib/node_modules` vía `NODE_PATH`) y captura las regiones relevantes para lo que se vaya a reportar (sidebar, cabecera, tarjetas, tablas — lo que aplique).
- **Reconstrucciones etiquetadas:** para patrones que el HTML subido no renderiza en pantalla (típicamente modales, o variantes de un componente que solo aparecen en otras páginas no subidas), arma un HTML aparte que cargue el mismo CSS real y monte marcado mínimo con las clases/selectores exactos que el Agente A encontró — nunca inventados. Estas capturas van tituladas explícitamente en el informe como *"reconstrucción a partir del CSS real — no es captura en vivo de esa pantalla"*, para no sugerir que se navegó una pantalla que no se vio.
- Antes de usar cualquier captura en el informe, revísala con la herramienta Read para confirmar que muestra lo que el texto va a decir que muestra.

**Troubleshooting típico:** si tras el render los colores salen negros/transparentes y el texto sale sin espaciado, casi siempre es que las variables CSS de `:root` no resolvieron — comprueba con `page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--bg'))`; si vuelve vacío, es el bloqueo CORS de `file://` (pasa a HTTP local) o el bloque `:root` real está en un selector distinto a `:root{` exacto (p.ej. `:root,[data-theme=light]{`) — busca con Grep el valor de un token conocido (`--bg:`) en vez de solo buscar `:root{` literal, porque el selector puede no coincidir con un patrón ingenuo.

### 4. Escribir el informe
Estructura (ver `/tmp` de la sesión de auditoría del Tablero del 2026-09-09 como referencia de tono y nivel de detalle si sigue disponible en el historial de la conversación; si no, usar esta estructura):

1. **Qué se auditó / contra qué** — 2-3 líneas, nombra los archivos exactos recibidos.
2. **Resumen ejecutivo** — veredicto en una frase (cumple / cumple parcialmente / no cumple), con la razón principal.
3. **Alcance y método** — qué se pudo verificar en vivo vs. solo por lectura de CSS; nunca ocultar esta limitación.
4. **Lo que sí cumple** — sección breve, con al menos una captura real. No dejar que el informe lea solo como lista de fallos.
5. **Hallazgos de cumplimiento**, uno por componente/token divergente: qué dice el sistema (citando §), qué hay en el build real (selector/valor literal), por qué importa, severidad (alta/media/baja). Alta = riesgo de accesibilidad real o el componente más repetido/visible de la interfaz; media = inconsistencia visible pero contenida; baja = funciona bien, solo diverge de nomenclatura.
6. **Hallazgos de cobertura** — patrones reales encontrados sin regla documentada. Para cada uno, **redactar la propuesta de regla nueva** en el mismo tono y estructura de `docs/sistema-diseno-sio-dproma.md` (no solo señalar el hueco) — lista para que el usuario la apruebe o ajuste; si se aprueba, la vía para incorporarla es la skill `sio-dproma-design-sync`, no esta.
7. **Priorización** — tabla breve de qué atender primero.
8. **Nota de alcance** — el build es de un equipo externo (DPROMA); el informe es material de conversación, no un cambio que hagamos nosotros.

Todo dato citado (hex, selector, conteo) debe ser trazable a lo que devolvió la investigación — nunca inventar una cifra al redactar.

### 5. Generar el PDF
El usuario prefiere PDF sobre Markdown suelto para este tipo de informe (pedido explícito). Pipeline:
1. Escribe el informe en Markdown con imágenes referenciadas por ruta relativa.
2. Conviértelo a HTML con `python3 -m markdown` (extensions `tables`, `fenced_code`) envuelto en una plantilla con CSS propio — tipografía legible, tablas con bordes claros, e imágenes con `max-height` acotado (una captura de sidebar completa puede salir desproporcionadamente alta si no se limita — cápala explícitamente, p. ej. `max-height:200px; object-position:top` para capturas verticales estrechas).
3. Sirve ese HTML por HTTP local igual que en el paso 3, ábrelo con Playwright y usa `page.pdf({format:'A4', printBackground:true})`.
4. Antes de entregar, toma un screenshot fullPage del mismo HTML servido y revísalo con Read para confirmar que el layout no se rompió (imágenes desbordadas, tablas cortadas) — es más rápido de verificar así que abriendo el PDF binario.

### 6. Entrega
- El PDF (y, si el usuario lo pide explícitamente, también las capturas sueltas) vía `SendUserFile`.
- Nunca commitear el informe ni los archivos subidos al repo — quedan solo en el scratchpad de la sesión.
- Al terminar, apaga cualquier servidor HTTP local que hayas levantado.

## Verificación antes de entregar
- Cada hallazgo de "no cumple" cita la sección (§) exacta de la regla que contradice — si no puedes citarla, no es un hallazgo válido, es una sospecha.
- Cada hallazgo de "hueco de cobertura" trae su propuesta de regla redactada, no solo el señalamiento.
- Las capturas reales y las reconstrucciones están etiquetadas de forma que no se puedan confundir entre sí.
- El PDF se revisó visualmente (vía el screenshot del HTML fuente) antes de mandarlo.
