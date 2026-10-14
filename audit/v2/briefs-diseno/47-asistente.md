# Brief de diseño · `47_asistente` — El asistente

**Estado:** propuesta de 2894 Studio · 2026-10-14 · sistema de diseño v2.15.0 · maqueta del cliente sin tocar.
**Observación de la persona** (hoja 17): «rediseño crítico; ¿sección “Chat”?; ¿por qué dos colores, blanco y gris?» (captura: la última línea sigue tocando la franja).
**Criterio por el que es crítico:** 5 — marcado «rediseño crítico» y viable (`audit/v2/INSTRUCCIONES-AUDITOR-v2.md`, regla 1); además 5 destinos <24 px (criterio 1).

**Cómo leer las pruebas.** `l.NNN` = línea de `47_asistente.html` (`grep -n`). `[m47]` = `prototipos/medir47.cjs` → `prototipos/medidas-47.json` (Playwright; original servido en `127.0.0.1:8732`, prototipos en `127.0.0.1:8777`). `§x` = `sistema-diseno.md` v2.15.0 (todos verificados con `grep -n "^### x"`). `pp-NNN` = `data/insights/<doc>.json` (verificados). Lo que no se puede afirmar queda como «sin datos».

---

## 0. Decisión en cinco líneas

1. **«Chat» no merece sección propia ni rótulo.** Es solo el nombre de una clase (`.chat`, l.654, l.714). La pantalla se llama «Asistente» y se abre desde el lanzador del cromo, que la ficha da por decidido.
2. **La franja se conserva.** Hace lo que la investigación pide de una IA (enseñar de dónde sale lo que dice). Lo que falla es cómo está montada y que una sola clase sirve para dos cosas.
3. **El defecto tiene una causa de una línea:** `margin-top:-12px` en `.fuentes` (l.669). Monta la franja **8,9 px** sobre la última línea de texto, a 1440, 1280, 1024 y 390 px [m47].
4. **Mínimo que lo resuelve:** cambiar ese margen a `+var(--sp-3)` y dar 24 px a los 5 destinos pequeños (Opción A). **Recomendado:** las dos zonas como hermanas, sin márgenes negativos, y el paso a seguir como botón (Opción B).
5. **Veredicto: viable con condiciones.** La condición no es de diseño: DPROMA tiene que decidir si el asistente solo consulta (47) o consulta y ejecuta con confirmación (`10_dprimi_asistente`) antes de construir.

---

## 1. Diagnóstico

### 1.1 Qué hay hoy

| Zona | Marcado y clases | Línea |
|---|---|---|
| Cabecera | `<header class="p4"><div class="p4-t">` · `h1 Asistente` · `.resumen «Consulta y resume · no modifica nada»` · `.btn.p «Nueva conversación»` | 704 |
| Contenedor | `.conv` = grid `minmax(260px,300px) 1fr`; a ≤1024 px una columna, `.hist{max-height:30vh}` | 637-640 |
| Historial | `.hist` → `.hh` (buscador `<div class="search">` + «5 conversaciones») + `<ol>` de 5 enlaces | 709-711 |
| Hilo | `<section class="chat" aria-labelledby="h-chat">` · `h2.sr «Conversación con el asistente»` · `.mensajes` (sin `role` ni `aria-live`) | 714-716 |
| Turno del usuario | `.msg.yo` → avatar «AR» + `.qn «Tú · hoy 10:31»` + `.tx` **sin tarjeta** (sobre `--bg`) | 718-720 |
| Turno del asistente | `.msg.ia` → avatar con isotipo + `.qn «Asistente · …»` + `.tx` **tarjeta** (`--surface`, borde, `--r-card`, relleno 12/16) | 723-733, 740-748 |
| Franja | `.fuentes` dentro de `.tx`: `--surface-2`, borde superior, margen `calc(var(--sp-3) * -1) calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)` | 667-669 |
| Compositor | `.rapido` ×4 · `textarea#preg` · `.btn.p «Enviar»` · `.aviso-ia` | 757-766 |
| Estados | `state-ok`, `state-loading` (esqueleto con texto), `state-empty`, `state-error` | 705-793 |

Tokens en juego: `--surface #FAFCFD`, `--surface-2 #E7EDF3`, `--bg #F2F5F7`, `--link #2F6B3C`, `--text-3 #5C6675` (todos en el `:root` de la maqueta, l.60-86).

### 1.2 Qué falla (con prueba)

| # | Hallazgo | Prueba | Nivel |
|---|---|---|---|
| F1 | **La franja se monta sobre la última línea.** Aire entre el texto y la franja: **−8,9 px** en las dos respuestas, a los 4 anchos. Es lo que la persona vio en la captura. | `[m47] original, respuestas[].aireUltimaLineaFranja = -8.9` · `l.669` · captura `prototipos/47-original-respuesta1.png` | Crítico (5) |
| F2 | **Una clase, dos significados.** `.fuentes` rotula «De dónde salió» (l.729, enlaces de lectura) y «Para hacerlo» (l.745, pasos a seguir). Mismo aspecto, mismo tipo de control. | `grep -n 'class="fuentes"' 47_asistente.html` → 729, 745 | Sistema/diseño |
| F3 | **Tres tonos para dos conceptos.** Cuerpo blanco (`--surface`), franja gris (`--surface-2`), y el turno del usuario sin tarjeta sobre el lienzo (`--bg`). Entre sí: 1,15 : 1 (surface/surface-2), 1,06 : 1 (surface/bg), 1,08 : 1 (bg/surface-2); en oscuro 1,10 / 1,10 / 1,21. El tono **no** separa nada por sí solo: separan el borde de 1 px, el rótulo y el avatar. | `prototipos/contraste-tonos.py` (cálculo sobre los tokens del `:root`) · `[m47] respuestas[].tarjetaFondo/franjaFondo` | Estético / comprensión |
| F4 | **5 destinos <24 px.** `input#buscar` 216×16 y cuatro enlaces de la franja de 780×19,8. | `[m47] original, destinos.bajo24` (5, a los 5 anchos) · §7.3 | Crítico (1) |
| F5 | **El hilo no anuncia nada nuevo** (cero `aria-live`/`role="log"`) y el buscador es un `<div>`, no una `<label>` (la región pulsable es el `<input>` de 16 px). | `[m47] ariaLive=false, buscarEsLabel=false` · l.709, l.716 · §6.4 regla 1, §10 («El destino táctil es la región que acepta la pulsación») | Accesibilidad |
| F6 | **Isotipo recortado** en el avatar del asistente (y en el logo del cromo): `viewBox` repetido en el `<svg>`. Desplazamiento del `<use>`: −11,4 px (avatar) y −32,5 px (logo). | `[m47] isotipoAvatar.dx=-11.4, isotipoLogo.dx=-32.5` · l.692, l.723, l.740 · §10 («Un `<symbol>` ya trae su `viewBox`…») · `grep -l 'viewBox="740 0 970 932" aria-hidden="true"><use href="#dproma-mark"/>' *.html` → 35 archivos | Estético / sistema |
| F7 | **Cabecera sin relleno inferior:** el botón «Nueva conversación» toca el borde (aire 0). Misma causa que Mi día. | `[m47] cabecera.aireBotonBorde=0` · l.308-309 · §3.1 · el bloque idéntico está en 36 archivos y 30 lo renderizan (`grep -l 'class="p4"' *.html` → 30) | Sistema |
| F8 | **El hilo queda estrecho a ≤1024 px:** 32 % de la altura a 1024×768, 25 % a 390×844 (215 px). | `[m47] altura.hiloPct` | Mejora (no crítico) |
| F9 | **Dos asistentes con contratos opuestos.** 47: «no modifica nada» (l.704) y «Eso no lo puedo hacer yo» (l.743). 10: «las acciones siempre se confirman antes de ejecutarse» (`10_dprimi_asistente.html:487`), «Notificar a los responsables» (:509), «Acción que requiere tu confirmación … Confirmar y enviar» (:519-522). Nombre distinto («Asistente» / «Asistente D-PRIMI») y el lanzador de las pantallas originales dice «Abrir D-PRIMI» (`02_dashboard.html:548`) frente a «Abrir el asistente del sistema» (`20_tablero.html:952`). | `grep -n` en los tres archivos | Producto (no se resuelve con CSS) |
| F10 | **El lanzador no está en 47.** Su CSS existe (l.268-275) y su marcado no (`grep -c 'class="fab' 47_asistente.html` → 0). La ficha dice que está «portado al armazón, deshabilitado y con su aviso de “entrega posterior”»; en `20_tablero.html:952` el `.fab` no lleva `disabled` y `grep -c "entrega posterior" *.html` da 0 en todo el paquete. | `grep` indicado | Contradicción ficha ↔ marcado |
| F11 | **Sombra del cajón de menú que se cuela a ≤860 px.** El `.side` fuera de pantalla conserva `box-shadow:var(--sh-modal)` (l.296): a 390 px el píxel x=0 mide `219,223,226` frente a `242,245,247` sin sombra, y llega hasta x≈40-50. Se ve como un degradado gris en el borde izquierdo de todas las capturas a 390. | `prototipos/medir-sombra-cajon.cjs` · 36 archivos con `translateX(-101%)` | Estético / sistema |
| F12 | La tarjeta de respuesta es una **séptima implementación de la receta de tarjeta**, sin `overflow:hidden` ni `--sh-rest`. | §6.3 («Es una clase, no un patrón que cada pantalla reimplementa») · l.665 | Causa raíz de F1 |

### 1.3 Las tres preguntas de la persona, respondidas

**«¿Sección “Chat”?» — No existe.** Títulos y regiones nombradas de la pantalla: `H1 «Asistente»`, `H2.sr «Conversaciones»`, `H2.sr «Conversación con el asistente»`, `LABEL.sr «Escribe tu pregunta»`. «Chat» solo aparece en `.chat{…}` (l.654) y `<section class="chat">` (l.714). `grep -n -i chat 47_asistente.html` → 654, 714, 715 (este último es «h-chat»).

**«¿Por qué dos colores, blanco y gris?» — No es «quién habla».** Dentro de la respuesta hay dos zonas con significado distinto: el **cuerpo** (lo que dice el asistente, `--surface`) y la **franja** (de dónde salió o qué puedes hacer, `--surface-2`). Quien habla lo dicen el rótulo `.qn` («Tú» / «Asistente», l.719, l.724), el avatar (iniciales / isotipo) y la tarjeta (solo el asistente la lleva). Sí hay un matiz: como el turno del usuario no tiene tarjeta, «blanco = asistente, lienzo = tú» también se puede leer, aunque blanco/lienzo midan 1,06 : 1. Por eso conviven dos lecturas.

**«La última línea sigue tocando la franja» — Confirmado, y es peor que tocar:** se monta. Causa en l.669: el margen superior es **negativo** (−12 px); los de izquierda, derecha y abajo compensan el relleno de `.tx` (l.666) y son correctos; el superior no separa, sube la franja sobre un párrafo que no tiene margen inferior.

### 1.4 Causa raíz

- **(a) Relleno repartido.** La tarjeta declara su relleno en el contenedor (`.tx`) y un hijo lo deshace con márgenes negativos: es el caso de §3.1 («el relleno de un contenedor lo declara el contenedor»).
- **(b) Un componente, dos significados** (F2).
- **(c) Producto sin resolver:** consulta-sola (47) frente a consulta+acción confirmada (10). La ficha lo dice así: S-19 (consulta y no modifica) y S-20 (cada respuesta enseña de dónde salió) son «lo que decidí yo», y «Las decisiones sin ratificar están además en `SUPUESTOS.md`» (`FICHAS_TECNICAS.md`, cabecera y sección 47). **No son D-n de DPROMA.**
- **(d) Bloques de armazón del sistema** que no están corregidos (cabecera §3.1, isotipo §10, sombra del cajón): se repiten en 30-36 archivos.

---

## 2. Requisitos

| # | Requisito | Fuente |
|---|---|---|
| R1 | Cuerpo y pie de la tarjeta son zonas separadas, sin márgenes negativos, con ≥12 px entre la última línea y el pie. | §3.1; §6.3 (anatomía: banda `--surface-2` + `.interior` con relleno propio, `overflow:hidden`) |
| R2 | Procedencia (solo lectura) y paso a seguir se distinguen por la **forma**, no solo por el rótulo. | Auditoría v2 R2; §11 («lo que ejecuta es un `<button>` y lo que navega un `<a>`») |
| R3 | Todo destino ≥24 px; el buscador es una `<label>`. | §7.3; §10 |
| R4 | Lo nuevo del hilo se anuncia; los estados llevan encabezado real y los cargando no llevan texto dentro de las barras. | §6.4 reglas 1-2; §6.7. El propio `10_dprimi_asistente.html:490` ya lleva `aria-live="polite"` en su hilo. |
| R5 | Una sola definición del asistente (consulta o consulta+acción) y el límite se dice una vez, donde condiciona la acción. | §8 (nivel 1); F9 |
| R6 | Textos ≤140 caracteres. | §8 |
| R7 | Sin hex en componentes; todo por tokens. | `sistema-diseno.md` cabecera («La regla de fondo») |
| R8 | El lanzador es cromo y vive en el armazón. | FICHAS 47: «Que el lanzador sea **cromo** y viva en el armazón está ya decidido y portado.» |
| R9 | Las 14 originales (`01`–`14`) **no se tocan**. `10_dprimi_asistente` queda como está. | FICHAS: «Las 14 originales (`01_`–`14_`) no tienen ficha: se copiaron sin tocar» (l.12); «ésas no se tocan por encargo» (l.662) |

**De la investigación:**

| pp | Qué dice | Qué pide a la pantalla | Estado en 47 |
|---|---|---|---|
| pp-050 (`2026-07-23_comercial-administracion-vehicular.json`) | La IA entregó agencias inexistentes sin verificación. En `ai_adoption.barreras` del mismo documento: «desconfianza por experiencia de un colega que recibió información falsa sobre agencias inexistentes». | Procedencia visible y comprobable. | **Cubre** («De dónde salió»), pero los enlaces miden 19,8 px y no distinguen dato consultado de inferido. |
| pp-070 (`2026-07-31_direccion-general-supervision-operativa.json`) | «…fallas del asistente virtual queden sin contingencia definida». | Estado de error con contingencia. | **Cubre** (l.790: «los módulos del menú funcionan con normalidad»). |
| pp-038 (`2026-07-20_gestion-almacen-inventario.json`) | IA personal «sin lineamientos». | Alcance acotado y visible. | **Cubre** (l.704, l.765, l.784). |
| pp-064, pp-066 (mismo doc de Dirección General) | «más de 70 grupos de WhatsApp sin historial estructurado»; «flujo manual por chat». | **Lectura nuestra, no dato:** en DPROMA «chat» nombra los grupos de WhatsApp. Un rótulo «Chat» en SIO se puede leer como canal entre personas. | Argumento contra el rótulo (§3, Opción 4). |
| `tools_inventory` del mismo doc, ts 00:47:08 | Dirección planea consultar el asistente «vía tableta». | Hilo usable en tableta. | F8: 30 % de altura a 1024×768. |

---

## 3. Opciones evaluadas

| | **1 · A — Mínimo cambio** | **2 · B — Dos zonas hermanas** (recomendada) | **3 · Burbujas como en `10`** | **4 · «Chat» como sección/ruta propia** |
|---|---|---|---|---|
| Qué cambia | `.fuentes{margin-top:+var(--sp-3)}`; `.fuentes a{min-height:24px}`; `<label class="search">`; `role="log"` en `.mensajes`; `.p4{padding-bottom}` | A, pero el pie es hermano del cuerpo (`overflow:hidden` en la tarjeta, `.tx-cuerpo` con su relleno); el paso a seguir son `.btn.mini`; isotipo y sombra del cajón corregidos | Usuario a la derecha en `--chrome`, asistente a la izquierda en tarjeta | Entrada de menú «Chat» y/o título visible del hilo |
| Resuelve F1 | Sí (+15,1 px de aire hasta la tinta) | Sí, **por construcción** | No por sí sola | No |
| Resuelve F2 | No | Sí | No | No |
| Coste | 5 ediciones, ~6 líneas | ~20 líneas de CSS + un envoltorio por respuesta en la plantilla | Reescribe `.msg`; reintroduce un cuarto tono y un color de marca para el usuario | Contradice R8 (un segundo punto de entrada) |
| Riesgo | Deja el margen negativo en izquierda/derecha/abajo: si cambia el relleno de `.tx`, vuelve el defecto | `.cuerpo` **ya existe** en la maqueta (l.483, contenedor de página): usarlo como nombre triplicó el aire entre párrafos al prototipar. Se usa `.tx-cuerpo` | Más cambio sobre lo del cliente para resolver menos; el turno del usuario ya se identifica por rótulo y avatar | Lectura «canal entre personas» (pp-064/066, inferencia) |
| Veredicto | **Piso exigible** | **Recomendada** | Descartada | Descartada |

**Complementos medidos (no sustituyen a las opciones):**
- **C — Historial compacto a ≤1024 px** (B + `.hist ol` en una fila horizontal): el hilo pasa de 30 % a 39 % (1024×768), de 24 % a 35 % (390×844) y de 42 % a 58 % (820×1180). Opcional; no crítico.
- **D — Estados de una respuesta** (B + «consultando…» y «no pude responder»), que el cliente no dibujó. Usa solo componentes existentes.

**Sobre «dos colores» (decisión):** se **conserva** el tono de la franja. Es lo que dibujó el cliente; además §6.3 ya usa `--surface-2` para la banda de cabecera de una tarjeta, así que el par `--surface` / `--surface-2` dentro de una tarjeta es del sistema. Alternativa si DPROMA prefiere una sola superficie: `.fuentes{background:transparent}` (una línea; los pies `.tfoot` y `.barra-form` de la propia maqueta, l.389 y l.591, son `--surface` con borde superior). No es crítico.

---

## 4. Recomendación y especificación (Opción B)

### 4.1 Marcado

```html
<div class="mensajes" role="log" aria-label="Mensajes" tabindex="0">
  <div class="msg ia">
    <span class="av" aria-hidden="true"><svg width="16" height="15" aria-hidden="true"><use href="#dproma-mark" width="16" height="15"/></svg></span>
    <span class="cu">
      <span class="qn">Asistente · hoy 10:31</span>
      <div class="tx">
        <div class="tx-cuerpo"><p>…</p><p>…</p></div>                    <!-- zona 1: lo que dice -->
        <div class="fuentes"><span class="et">De dónde salió</span>      <!-- zona 2: procedencia (lectura) -->
          <a href="#">Bandeja de gestoría · 6 expedientes</a> …</div>
      </div>
    </span>
  </div>
  …
  <!-- paso a seguir: mismo pie, otra forma -->
  <div class="fuentes fuentes--paso"><span class="et">Para hacerlo</span>
    <a class="btn mini" href="#">Abrir GT-2026-02417</a> <a class="btn mini" href="#">Abrir GT-2026-02416</a></div>
</div>
<label class="search"><svg …/><input id="buscar" type="search" … aria-label="Buscar conversaciones"></label>
```

### 4.2 CSS (solo tokens; el diff completo está en `prototipos/47-asistente-B-recomendado.diff`)

```css
.p4{ …; padding-bottom:var(--sp-3) }                                   /* §3.1 */
.msg.ia .tx{ background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r-card); overflow:hidden }                       /* sin padding: lo declara cada zona */
.msg.ia .tx-cuerpo{ padding:var(--sp-3) var(--sp-4) }
.fuentes{ display:flex; flex-direction:column; gap:var(--sp-1);
  padding:var(--sp-3) var(--sp-4); border-top:1px solid var(--border);
  background:var(--surface-2) }                                        /* sin margin negativo */
.fuentes--paso{ flex-direction:row; flex-wrap:wrap; align-items:center; gap:var(--sp-2) }
.fuentes--paso .et{ flex:0 0 100% }
.fuentes--paso .btn{ text-decoration:none }                            /* <a class="btn"> */
.fuentes--paso .btn:hover{ background:var(--surface-hover) }           /* sobre --surface-2 el hover de .btn no se vería */
.fuentes a:not(.btn){ display:flex; align-items:center; min-height:24px;
  font-size:var(--fs-meta); color:var(--link); font-weight:600; text-decoration:none }
/* ARQ-CROMO: la sombra del cajón solo con el cajón abierto */
:root[data-menu="abierto"] .side{ transform:none; box-shadow:var(--sh-modal) }
```

### 4.3 Estados

| Estado | Qué ve la persona | Qué lleva |
|---|---|---|
| Con datos | Hilo + historial | `role="log"`: lo nuevo se anuncia en `polite`. |
| Cargando (pantalla) | Esqueleto (l.769-775) | Cliente: sigue igual salvo que **el texto dentro de las barras sobra** (§6.7: «Sin texto real dentro de las barras»; hoy «buscador», «pregunta», «respuesta del asistente» en l.771-775). |
| Vacío | l.781-786 | Sin cambios. Ya dice límite y alcance en dos frases. |
| Error de pantalla | l.788-792 | Sin cambios. Cumple §6.4 regla 3 (qué pasó · qué no se perdió · qué hacer · referencia). |
| **Respuesta pendiente** (no dibujada por el cliente) | Tarjeta con dos barras `.skel` y rótulo «Asistente · consultando…» | `aria-busy="true"` en el mensaje y `role="status" aria-label="El asistente está consultando"` en `.tx-cuerpo`; barras sin texto. |
| **Respuesta fallida** (no dibujada) | «**No pude responder.** Tu pregunta se guardó y nada del sistema cambió.» (67 caracteres) + referencia + pie «Qué hacer» con `Reintentar` (`.btn.mini`) | Misma tarjeta con pie; mismo orden de §6.4 regla 3. |

### 4.4 Accesibilidad
- **Nombre accesible:** `.mensajes` = «Mensajes» (`role="log"`); cada enlace/botón de pie se nombra por su texto («Abrir GT-2026-02417»), distinto uno de otro (§6.19: el nombre accesible nombra el dato concreto).
- **Teclado:** las 34 primeras paradas de tabulación (cromo, historial, hilo, pies, compositor) siguen el orden del DOM, sin trampas; el hilo es una parada (`tabindex="0"`) porque desplaza; los 4 controles de pie y el buscador muestran contorno de 2 px (el buscador, en su `<label>`, por `:focus-within`) [`prototipos/teclado47.cjs`].
- **Foco:** el contorno (2 px + 2 px de separación) de cada control de pie cabe dentro de la tarjeta, no lo recorta `overflow:hidden` [m47 `foco`].
- **`aria-*`:** `role="log"`, `aria-busy` y `role="status"` solo donde se indica; `aria-hidden` en avatares e isotipos.

### 4.5 Comportamiento por ancho (medido, B)

| Ancho | Layout | Hilo (alto, % del viewport) | Notas |
|---|---|---|---|
| 1440 | historial 300 px + hilo | 595 px · 66 % | franja en columna; botones de paso en fila |
| 1280 | ídem (cromo 236 px) | 495 px · 62 % | ídem |
| 1024 | una columna (`.conv`, l.638) | 233 px · 30 % (original 245) | con C: 302 px · 39 % |
| 390 | una columna | 203 px · 24 % (original 215) | los dos botones de paso se apilan; con C: 295 px · 35 % |

Sin scroll horizontal de página ni elementos fuera de la tarjeta a ninguno de los 5 anchos medidos (1440, 1280, 1024, 820, 390).

### 4.6 Textos
Ningún texto nuevo de producto salvo los de D (pendiente y fallo, ≤67 caracteres) y el nombre accesible «Mensajes». Los rótulos «De dónde salió» y «Para hacerlo» del cliente se conservan.

---

## 5. Prototipo medido

Todos son **copias parcheadas de la maqueta** (la original no se toca); cada reemplazo exige un número exacto de coincidencias (`prototipos/genera-47-28.py`). Ninguna línea añadida lleva hex; `usados − declarados = ∅` en todos.

| Archivo | Qué es |
|---|---|
| `prototipos/47-asistente-A-minimo.html` (+ `.diff`, 12 líneas) | Opción A |
| `prototipos/47-asistente-B-recomendado.html` (+ `.diff`) | **Opción B** |
| `prototipos/47-asistente-C-historial-compacto.html` | B + historial en fila a ≤1024 px |
| `prototipos/47-asistente-D-estados-respuesta.html` | B + respuesta pendiente y fallida |
| Capturas | `47-original-respuesta1.png` / `47-B-recomendado-respuesta1.png` (antes/después), `47-B-recomendado-respuesta2.png` y `-oscuro.png`, `47-B-recomendado-1440.png`, `47-B-recomendado-390.png`, `47-C-historial-390.png`, `47-D-estados-1440-hilo.png` |

**Reproducir:** `python3 -m http.server 8777 --bind 127.0.0.1 --directory …/prototipos` (el 8741 estaba ocupado por otro proceso) y `cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node …/prototipos/medir47.cjs`.

**Resultados** (1440 / 1280 / 1024 / 820 / 390; `m47`):

| Medida | Original | A | B | C | D |
|---|---|---|---|---|---|
| Aire texto → franja (hasta la tinta) | **−8,9 px** | +15,1 | +15,1 | +15,1 | +15,1 |
| Solapes entre zonas / hijos | 2 | 0 | 0 | 0 | 0 |
| Elementos fuera de la tarjeta / recorte horizontal | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Destinos <24 px | **5** | 0 | 0 | 0 | 0 |
| Alto mínimo de un destino del hilo/historial | 16 px | 24 px | 24 px (botón de paso 28) | ídem | ídem |
| Aire botón «Nueva conversación» → borde de cabecera | 0 | 12 | 12 | 12 | 12 |
| Anuncia mensajes nuevos (`role="log"`) | no | sí | sí | sí | sí |
| Desplazamiento del isotipo (avatar / logo) | −11,4 / −32,5 | sin cambio | **+0,5 / +0,9** | ídem | ídem |
| Contraste claro: rótulo / enlace / botón de paso | 4,93 / 5,41 / — | 4,93 / 5,41 / — | 4,93 / 5,41 / 15,21 | ídem | ídem |
| Contraste oscuro: rótulo / enlace / botón de paso | 5,03 / 7,06 / — | ídem | 5,03 / 7,06 / 13,93 | ídem | ídem |
| Estados D: «consultando» (`.qn`), referencia de error | — | — | — | — | 5,31 / 5,65 (claro) · `role=status` sí · barras sin texto |
| Hilo a 1024×768 / 390×844 | 32 % / 25 % | 30 % / 24 % | 30 % / 24 % | **39 % / 35 %** | 30 % / 24 % |

Mínimo exigido: 4,5 : 1 texto; 3 : 1 gráficos (§1.7). Cumplen todos los pares medidos. El contorno de foco de los 4 controles de pie cabe en la tarjeta (4 de 4).

---

## 6. Veredicto de viabilidad: **viable con condiciones**

| Criterio | Respuesta |
|---|---|
| **Alcance dentro del sistema** | Sí. Cero tokens nuevos (`--surface`, `--surface-2`, `--surface-hover`, `--sp-*`, `--r-card`, `--link`) y cero componentes nuevos: `.btn.mini` (§6.2), anatomía de §6.3. Las clases nuevas (`.tx-cuerpo`, `.fuentes--paso`) son modificadores locales. |
| **Esfuerzo** | A: 5 ediciones (~6 líneas). B: ~20 líneas de CSS, un envoltorio por respuesta en la plantilla, 3 `<svg>` de isotipo. Proporcionado: el defecto F1 es el que la persona vio. |
| **Compatibilidad con DPROMA** | No toca ningún D-n. Conserva S-19 y S-20 (supuestos sin ratificar, FICHAS 47). Respeta «Que el lanzador sea **cromo** y viva en el armazón está ya decidido y portado» y «Las 14 originales … se copiaron sin tocar». |
| **Condiciones** | (1) DPROMA decide si el asistente **solo consulta** (47) o **consulta y ejecuta con confirmación** (10) antes de construir; B es compatible con ambos (el pie de paso admite botones que ejecutan). (2) Según la ficha, `47` queda «fuera» de lo portado porque depende «de la decisión pendiente de Jhon … o de piezas sin backend» (FICHAS, «Fase 2, tanda 2 · Lo que sigue sin copiar», l.1456-1459): se diseña, no se construye aún. (3) Probar `role="log"` con un lector de pantalla real (no medido). |

**Lo no viable ahora, documentado como deuda (no crítico):** (i) unificar 47 y 10 en un solo asistente (decisión de producto); (ii) reconstruir la respuesta como `.tarjeta` + `.interior` + pie (el objetivo del sistema, F12) en lugar de `.tx`; (iii) historial plegable en móvil con `<details>` (C lo mitiga con CSS).

---

## 7. Cómo se adopta

### 7.1 Qué cambiaría el cliente (mínimo)

**Exigir (Opción A, criterios 1 y 5):**
1. l.669: `margin:calc(var(--sp-3) * -1) …` → `margin:var(--sp-3) calc(var(--sp-4) * -1) calc(var(--sp-3) * -1)`.
2. l.671: `.fuentes a{display:flex;align-items:center;min-height:24px; …}`.
3. l.709: `<div class="search">…</div>` → `<label class="search">…</label>`.
4. l.716: `<div class="mensajes" role="log" aria-label="Mensajes" tabindex="0">`.
5. l.308: `.p4{…;padding-bottom:var(--sp-3)}`.

**Recomendar (Opción B):** lo anterior más el diff de `prototipos/47-asistente-B-recomendado.diff` (pie hermano, botones de paso, isotipo en 3 `<svg>`, sombra del cajón). Si el cliente prefiere no tocar marcado: A basta para cerrar el defecto medido.

### 7.2 Qué documentaríamos nosotros (reglas en el tono del sistema; lugares propuestos)

**En §6.3 (Tarjeta), tras «Cuándo usar una tarjeta, y cuál» — subsección «Tarjeta con pie».**
> Una tarjeta con pie son dos zonas hermanas, cada una con su relleno: el cuerpo (`.interior`, §6.3) y el pie, una banda `--surface-2` con borde superior, como la cabecera pero al final. El pie no se sangra con márgenes negativos: en el Asistente, `margin-top:-12px` montó la franja 8,9 px sobre la última línea de cada respuesta, a los cuatro anchos. Un pie dice una sola cosa: la procedencia («De dónde salió») son enlaces de lectura; el paso a seguir («Para hacerlo») son botones `.btn.mini`. Se distinguen por la forma, no solo por el rótulo.

**Nueva sección tras §6.23 — «Hilo de conversación».**
> El contenedor de mensajes lleva `role="log"`, nombre y `tabindex="0"` si desplaza. Cada turno se rotula con quién habla y cuándo («Tú · hoy 10:31»); el tono no identifica al hablante (las superficies miden 1,06 – 1,15 : 1). Una respuesta en curso es una tarjeta con `role="status"` y barras sin texto; una fallida dice qué pasó, qué no se perdió y qué hacer (§6.4, regla 3).

**En §6.4, regla 1:** añadir «un hilo que recibe mensajes se anuncia con `role="log"`».
**En §10, trampa de nombres cortos:** añadir el caso `.cuerpo` (ya definido como contenedor de página en la propia maqueta, l.483; un modificador nuevo con ese nombre heredó `display:flex` y `gap:16px`).
**En §7.2 Cromo (bloque `ARQ-CROMO`):** «la sombra del cajón solo existe con el cajón abierto; cerrado, entra ~50 px en el borde izquierdo a ≤860 px» (36 archivos) y el isotipo del logo con las medidas en el `<use>` (35 archivos).
**En §11 (checklist):** «¿Algún `margin` negativo compensa el relleno de un contenedor?».

---

## 8. Lo que no sé / sin datos

- **Qué quiere DPROMA que sea el asistente** (consulta o consulta+acción): la ficha solo dice «hay maqueta original y no hay pantalla»; S-19/S-20 son supuestos del autor, sin ratificar. Sin datos sobre la intención de la persona al preguntar por «Chat».
- **Cómo leería un usuario de DPROMA un rótulo «Chat»:** mi argumento (pp-064/066) es una inferencia, no un dato.
- **Uso real en teléfono o tableta:** solo consta que Dirección planea consultar «vía tableta» (`tools_inventory`, 00:47:08). Sin datos de tamaños de pantalla.
- **Qué preguntas hará la gente al asistente** (más allá de los accesos rápidos de la maqueta).
- **Si la persona vio una captura distinta de este archivo:** el solape medido coincide con su descripción.
- **Lector de pantalla real y navegadores distintos de Chromium:** no medido; solo DOM, contornos y orden de tabulación.
- **Rendimiento:** no evaluado.
- **Texto dentro de las barras del esqueleto** (l.771-775): la corrección es de §6.7 y no se prototipó.
