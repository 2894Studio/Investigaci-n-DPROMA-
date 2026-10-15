# Brief de diseño · `28_instalador_mi_dia` — Mi día

**Estado:** propuesta de 2894 Studio · 2026-10-14 · sistema de diseño v2.15.0 · maqueta del cliente sin tocar.
**Observación de la persona** (hoja 13): «barra superior sin espacio bajo «Mi día»; contrastar con el flujo de la investigación».
**Criterio por el que es crítico:** 5 — marcado «rediseño crítico» y viable (`audit/v2/INSTRUCCIONES-AUDITOR-v2.md`, regla 1). Además, la falta de `--sp-5` contradice **D-39** de DPROMA (criterio 4, ver F2).

**Cómo leer las pruebas.** `l.NNN` = línea de `28_instalador_mi_dia.html` (`grep -n`). `[m28]` = `prototipos/medir28.cjs` → `prototipos/medidas-28.json` (Playwright; original en `127.0.0.1:8732`, prototipos en `127.0.0.1:8777`). **390×844 es el formato principal**; 1440/1280/1024 se miden también. `§x` = `sistema-diseno.md` v2.15.0 (verificado con `grep -n`). `pp-NNN` = `data/insights/<doc>.json` (verificado). Lo que no se puede afirmar queda como «sin datos».

---

## 0. Decisión en seis líneas

1. **La causa es `.p4-t` con `padding-bottom:0` (l.314)** y un `.p4` sin relleno (l.313) cuyo único hijo es `.p4-t` (l.718; la l.719, donde irían `.p4-b`/`.p4-f`, está vacía). Es el caso exacto que describe §3.1. **`--sp-5` no es la causa**: con `:root{--sp-5:20px}` la cabecera sigue en 33/38 px (`prototipos/refuta-sp5-28.cjs`).
2. **Mínimo que lo resuelve (Opción A):** `.p4{padding-bottom:var(--sp-3)}`. Una línea; la cabecera pasa de 33 a 45 px a 390 y de 38 a 50 px a 1440, con 12 px arriba y 12 abajo.
3. **Contraste con el flujo real:** el contenido de la cabecera es correcto —de los pain points «alta» que tocan esta pantalla, uno es que la operación se detiene por recursos externos (pp-028) y otro el plazo del viático (pp-113)—, pero el dato del bloqueo es el texto más pequeño (12 px, gris) y más pegado al borde de toda la pantalla.
4. **El aire cuesta pliegue:** a 390×844 los 12 px extra empujan la línea roja «Te faltan 2 tramos de canaleta» de 763,5 a 775,5 px de borde inferior; la barra fija empieza en 763, así que pasa de «a ras» a 12,5 px bajo la barra. Se compensa quitando lo que el pliegue repite (Opción C).
5. **Recomendación:** exigir **B** (A + 3 correcciones de sistema que no cuestan pliegue); proponer **C** como rediseño (fecha y bloqueo suben a la cabecera, se retira la tarjeta de fecha) sujeto a una decisión de producto.
6. **Veredicto: B viable; C viable con condiciones.**

---

## 1. Diagnóstico

### 1.1 Qué hay hoy

| Zona | Marcado y clases | Línea |
|---|---|---|
| Cromo | Barra superior (63 px a 390): hamburguesa 46 px, tema, cuenta | `html data-tacto="dedo"` (l.2); `:root[data-tacto="dedo"] .iconbtn{width:46px;height:46px}` (l.285) |
| Cabecera | `<div class="p4"><div class="p4-t"><h1>Mi día</h1><span class="resumen"><b>2</b> citas · <b>7 h</b> de trabajo · <b>1</b> con material incompleto</span></div></div>` | 717-719 |
| Reglas de cabecera | `.p4{background;border-bottom;flex-shrink:0}` · `.p4-t{…padding:var(--sp-3) var(--sp-6) 0…}` · `.resumen{color:var(--text-3);font-size:var(--fs-meta)}` · h1 20 px (16 px a ≤860) | 313-317, 447 |
| Aviso | `.senal` «Sin señal: puedes leer lo descargado, pero lo que marques no se guarda hasta que vuelva la conexión.» (100 caracteres) | 723 |
| Fecha | `<article class="tarjeta-tel">` «Hoy · viernes 21 de agosto» + «2 citas» | 725-727 |
| Citas | `.cita-tel`: hora 26 px · duración · pastilla (`p-ok` «Siguiente», `p-block` «Falta material») · cliente · equipo y domicilio · `.aviso-fila` (roja) · 2 `.gordo` + 1 `.gordo.p` | 730-754 |
| Lo que llevas | 3 cifras + `.gordo` «Ver lo que traigo del almacén» | 757-768 |
| Barra fija | `.pie-accion{position:sticky;bottom:0}` con `.gordo.p` «Ir a la cita de las 08:00» (81 px) | 653-659, 770-773 |
| Estados | `state-ok / loading / empty / error` | 721-790 |

Medidas del original [m28]: cabecera **33 px** a 390 (h1 16 px + resumen en una línea; 12 px arriba, **0** abajo) y **38 px** a 1440/1280/1024 (12 + 25 + 1 de borde); caja de texto a 0-1 px del borde. Mismo hueco a los cuatro anchos.

### 1.2 Qué falla (con prueba)

| # | Hallazgo | Prueba | Nivel |
|---|---|---|---|
| F1 | **Cabecera sin relleno inferior.** 12 px de aire arriba, 0 abajo. Causa: relleno repartido entre filas opcionales (§3.1). El bloque idéntico está en 36 archivos; 30 renderizan `.p4`, todos con `padding-bottom` 0. | `[m28] original, cabecera.airAbajo=0` · l.313-314 · `grep -l 'class="p4"' *.html` → 30 · §3.1: «la cabecera se quedó con **5px** entre el título y su propio borde» | **Crítico (5)** |
| F2 | **`--sp-5` no está declarado** en el `:root` de la maqueta, y `_sio-tokens.css` de DPROMA sí: `--sp-5: 20px; /* D-39 — faltaba, y no se ve porque no da error */` (l.45). Lo usan sin declarar: 28, 29, 51, 57, 58. Efecto en Mi día: `.gordo{padding:0 var(--sp-5)}` (l.645) computa 0 en las 8 `.gordo`. **Sin efecto visible medido** a 320/360/390 (el texto, centrado, conserva ≥22,5 px de holgura). | `prototipos/refuta-sp5-28.cjs` (`gordoPadL` 0 → 20) · `prototipos/medir28-extra.cjs` (holgura mínima 22,5-23,6 px a 320 y 360, sin recortes) · `for f in *.html; do grep -c "var(--sp-5)" $f; grep -c "\-\-sp-5:" $f; done` · §3 («Un `var()` que no resuelve … invalida **la declaración entera**»); §10 (trampa de tokens no declarados) | Crítico (4, D-39) pero sin efecto visible |
| F3 | **Cola de la lista sin aire:** al final del scroll la última tarjeta queda a −0,4 px (1440) / −0,2 px (390) de la barra fija. `.tel` con `padding-bottom:0`. | `[m28] original, cola.airUltimaTarjetaBarra` · l.642-643 · §3.1 | Mejora (misma causa que F1) |
| F4 | **El resumen no sobrevive a su estado.** En «vacío» y «error» el título sigue (correcto, §6.4: «la barra lateral, la superior y el título siguen ahí, porque siguen siendo verdad»), pero el resumen sigue diciendo «2 citas · 7 h de trabajo · 1 con material incompleto» sobre «Hoy no tienes ninguna cita». | `[m28] original, resumenPorEstado.empty/error` · captura `prototipos/28-original-390-empty.png` | Mejora |
| F5 | **Primer pliegue (390×844):** antes de la primera cita hay 173,5 px (aviso 84,5 + fecha 53 + 3 huecos de 12) de los **667 px** que quedan sobre la barra fija (844 − 63 cromo − 33 cabecera − 81 barra). «2 citas» aparece dos veces (cabecera y tarjeta de fecha). | `[m28] primerPliegue.antesDeLaPrimeraCita=173.5` · `prototipos/medir28-extra.cjs` (`senal` 84,5, `fechaCard` 53, `pie` 81, `cromoTop` 63, `citasTexto` = [«2 citas · 7 h…», «2 citas»]) | Mejora |
| F6 | **El bloqueo del día está en tres sitios, con tres colores y tres redacciones:** resumen gris 12 px «con material incompleto» (l.718), pastilla violeta `--block` «Falta material» (l.745), línea roja `--err-ink` «Te faltan 2 tramos de canaleta…» (l.748). | `grep -n` indicado · §1.3 (`block` = «Bloqueado por una condición externa»; `err` = «Falta lo que impide operar») | Mejora |
| F7 | **Tres botones primarios verdes** (l.739, l.753, l.772) frente a la ficha: «una sola acción grande para salir». La barra fija repite el icono de «Cómo llegar» (l.736, l.750, l.772). | `grep -n 'gordo p' 28_instalador_mi_dia.html` | Decisión de diseño (no se prototipa) |
| F8 | **`.senal` reinventa un componente que está en el mismo archivo** (`.banda`, l.518). | §6.9: «Antes de escribir una clase nueva para un aviso de ancho completo, se verifica si `.banda` + una de sus cuatro variantes ya lo cubre»; y: «Va con `role="status"`» | Menor |
| F9 | **Sombra del cajón de menú que se cuela a ≤860 px** (l.300-301): a 390 el píxel x=0 mide `219,223,226` frente a `242,245,247` sin sombra; llega a x≈40-50. Es el degradado gris del borde izquierdo en las capturas a 390. 36 archivos. | `prototipos/medir-sombra-cajon.cjs` | Estético / sistema |
| F10 | **Isotipo del logo del cromo recortado** (`viewBox` repetido en el `<svg>`, l.705): −32,5 px de desplazamiento del `<use>`. 35 archivos. | `[m28] original, logoDx=-32.5` · §10 («se pinta 32,5px a la izquierda de su caja») | Sistema |
| F11 | **Estados:** esqueleto con texto dentro de las barras (l.774), sin `aria-live`, títulos en `<b>` (l.777, l.783). | `grep -n` indicado · §6.4 reglas 1-2 · §6.7 | Sistema (no se prototipa) |

### 1.3 Causa raíz

- **De sistema (F1, F3, F9, F10):** el bloque de referencia `ARQ-P4` (y `ARQ-CROMO`) que se copia a cada pantalla no incorpora lo que §3.1 y §10 ya prescriben. Mi día solo lo hace visible porque no tiene filas de búsqueda ni de chips que cierren la barra.
- **De producto (F5-F7):** la ficha promete «una sola acción grande» y «el aviso de material incompleto en la cita»; el dibujo reparte ese aviso en tres lugares y repite acciones.
- **No es** `--sp-5`: hipótesis medida y refutada (F2).

---

## 2. Requisitos

| # | Requisito | Fuente |
|---|---|---|
| R1 | La cabecera declara su relleno inferior en el contenedor; ≥12 px de aire bajo la última línea, con o sin filas opcionales. | §3.1 |
| R2 | A 390×844, la siguiente cita y la línea que explica un bloqueo quedan sobre la barra fija. | FICHAS 28: «El aviso de **material incompleto** en la cita, no en un panel aparte — Si se entera al llegar, ya condujo 40 minutos» (razón del autor, no dato de la investigación) |
| R3 | El título persiste en cualquier estado; lo que cuenta datos, no. | §6.4 («la barra lateral, la superior y el título siguen ahí, porque siguen siendo verdad») |
| R4 | Objetivos ≥24 px; 44 px si es la acción principal o uso en campo. | §7.3. La ficha fija **56 px** (S-30, «Se usa de pie, con sol y a veces con una sola mano»); es un supuesto sin ratificar. |
| R5 | Un estado se comunica con color + icono + texto; un resumen es lectura. | §6.10, §6.12 |
| R6 | `--sp-5` declarado. | D-39 (`_sio-tokens.css` l.45) |
| R7 | Textos ≤140 caracteres; sin hex. | §8; cabecera del sistema |
| R8 | Se conserva lo decidido: 56 px, acción principal fija abajo, «Cómo llegar» y «Llamar al sitio» en cada cita, «Lo que llevas encima». | FICHAS 28 (tabla de decisiones) |

### 2.1 Contraste con el flujo real del instalador

(`data/insights/`; «lectura nuestra» = inferencia, no dato)

| Paso del flujo | Qué dice la investigación | Qué dibuja Mi día | Lectura |
|---|---|---|---|
| Antes de salir | La ruta se programa un día antes; la herramienta con que llega al instalador es «ninguna / verbal» (`2026-07-22_coordinacion-tecnica-instalaciones.json`, proceso «Recepción de solicitud y programación», paso 7, 00:21:12). La ruta se arma en un Word aparte y con un prompt de IA para la ruta más corta (pp-022, pp-023). | Lista de citas por hora, pastilla «Siguiente», «Cómo llegar» por cita (l.730-754). **No hay orden de ruta ni tiempo de traslado.** | Cubre «qué me toca hoy»; ignora la ruta (pp-022, ya señalado por la auditoría). |
| Material | Operaciones sube la ruta al grupo de almacén; el instalador pide el material por llamada o WhatsApp; Almacén entrega con un buffer (`2026-07-20_gestion-almacen-inventario.json`, proceso «Control diario de entradas y salidas de material», pasos 1-3, 00:10:22-00:24:50; la coordinación diaria es por WhatsApp sin trazabilidad: pp-035). Los materiales pueden salir sin las firmas de control (pp-024). | Pastilla «Falta material» + «Te faltan 2 tramos de canaleta que Almacén no ha despachado» + «4 renglones despachados». | Cubre el **aviso**; no da vía para pedir lo que falta (hoy WhatsApp) ni dice si el despacho está firmado (pp-024). |
| Si falta algo | **pp-028 (alta):** «cuando esos vistos buenos se retrasan, la operación queda completamente detenida». **pp-025:** «si falta, se compra localmente en el sitio». | Trata «falta material» como bloqueo y mantiene «Abrir la orden» como botón primario verde. | **Sin datos** de si DPROMA quiere bloqueo duro o compra local. Mi lectura: es el dato que más cuesta ignorar (alta) y es el que la cabecera dice en 12 px grises. |
| En sitio | La hoja de servicio es de papel, con cruce manual después (pp-026). | «2 pasos de ayer sin marcar» y «Abrir la orden» (hacia `29`). | Cubre. |
| Al cierre | Dos entrevistas **discrepan** sobre el sobrante: queda con el instalador para el día siguiente (pp-025) / lo devuelve al final del día (almacén, paso 4, 00:20:35). | «Lo que llevas encima: 4 renglones despachados, sin capturar el consumo». | **Sin datos** de cuál rige: la tarjeta puede estar contando algo que no existe. |
| Viáticos | Se piden y aprueban por WhatsApp (pp-027); la comprobación vence a los tres días del regreso (pp-113, alta: «No hay mecanismo que avise del plazo»). | «1 viático por comprobar · Vence el 24 ago». | Cubre el plazo; no muestra la solicitud de hoy. |

**Qué dice esto de la cabecera.** La investigación **no** tiene un pain point sobre la cabecera ni sobre la agenda en teléfono (barrido de los `pain_points` de las 11 entrevistas por «app/aplicación/móvil/celular/teléfono/pantalla/cabecera/agenda/instalador»: 6 coincidencias —pp-035, pp-020, pp-022, pp-025, pp-078, pp-112—, ninguna sobre esta pantalla; `prototipos/barrido-pp-28.py`). Lo que sí dice es qué contenido merece estar sin desplazar: el bloqueo (pp-028, alta) y el plazo del viático (pp-113, alta). La voz del instalador llega mediada: la entrevista 2026-07-22 es conjunta con «coordinación/ICEV y técnico de instalación» (`meta.rol_area`).

---

## 3. Opciones evaluadas

| | **1 · A — Mínimo cambio** | **2 · B — A + sistema** (recomendada) | **3 · C — Primer pliegue** (propuesta) | **4 · Rediseño del flujo** |
|---|---|---|---|---|
| Qué cambia | `.p4{padding-bottom:var(--sp-3)}` | A + `--sp-5` + `.tel{padding-bottom}` + el resumen se oculta si la vista no es «con datos» + sombra del cajón solo abierto + isotipo del logo | B + fecha y bloqueo en la cabecera (`.pill.p-block`), se retira la tarjeta «Hoy · viernes…» (añade `h2.sr`) | Una sola primaria por pliegue, ruta del día, vía para pedir material |
| Cabecera 390 / 1440 | 45 / 50 px | 45 / 50 px | 99 / 50 px | — |
| Antes de la 1.ª cita (cabecera + hasta la cita) a 390 | 219 px (+12) | 219 px | **208 px** (≈ original 207) | — |
| Línea roja de material a 390: borde inferior (la barra empieza en 763; original 763,5) | 775,5 → 12,5 px bajo la barra | ídem | **764,5 → a ras** | — |
| Coste | 1 línea | ~10 líneas | ~15 líneas más y quitar un componente del cliente | Alto; toca decisiones del cliente |
| Riesgo | Pierde 12 px de pliegue | Pierde 12 px de pliegue; `:has()` (el archivo ya usa `:has`, l.375) | Decide por el cliente que la fecha vive en la cabecera; cabecera de 3 filas a 390 | Contradice o reabre lo decidido en la ficha |
| Veredicto | Piso | **Exigible** | **Viable con condiciones** | Deuda, no crítico |

**Por qué no más:** la regla de trabajo es cambiar lo mínimo que resuelva el problema. A resuelve la observación; B añade solo lo que comparte causa raíz (§3.1, D-39, §6.4) sin coste de pliegue; C responde a «contrastar con el flujo» y se propone, no se exige.

---

## 4. Recomendación y especificación

**Recomendación:** adoptar **B**. Proponer **C** a DPROMA como siguiente iteración si confirma (a) que la tarjeta de fecha no cumple otra función y (b) que el bloqueo del día debe leerse sin desplazar.

### 4.1 Marcado

B no cambia el marcado de la maqueta. C cambia solo la cabecera y retira la tarjeta de fecha:

```html
<div class="p4"><div class="p4-t"><h1>Mi día</h1>
  <span class="resumen">Viernes 21 de agosto · <b>2</b> citas · <b>7 h</b> de trabajo
    <span class="pill p-block"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-pause"/></svg><b>1</b> con material incompleto</span></span>
</div></div>
…
<div class="tel">
  <div class="senal">…</div>
  <h2 class="sr">Citas de hoy</h2>        <!-- sustituye al h2 de la tarjeta de fecha; evita saltar de h1 a h3 -->
  <article class="tarjeta-tel cita-tel">…</article>
```

### 4.2 CSS (solo tokens; diff completo en `prototipos/28-mi-dia-B-recomendado.diff` y `prototipos/28-mi-dia-C-primer-pliegue.diff`)

```css
:root{ …; --sp-5:20px; … }                                          /* D-39 */
.p4{ …; padding-bottom:var(--sp-3) }                                /* §3.1 — y las filas hijas, solo relleno superior */
.tel{ …; padding:var(--sp-4) var(--sp-6) var(--sp-4) }              /* aire al final del scroll */
@media (max-width:860px){ .tel{ padding:var(--sp-3) var(--sp-3) var(--sp-3) } }
.main:has(#contenido:not([data-state="ok"])) .p4-t .resumen{ display:none }   /* §6.4: el título se queda; el dato, no */
/* ARQ-CROMO */
:root[data-menu="abierto"] .side{ transform:none; box-shadow:var(--sh-modal) }  /* y se quita de .side cerrado (l.301) */
/* solo C */
.p4-t .resumen .pill b{ color:inherit }
```
(En producción el resumen se pinta desde el dato y no existe en vacío/error; la regla `:has()` solo hace verdad la maqueta.)

### 4.3 Estados

| Estado | Cabecera | Cuerpo |
|---|---|---|
| Con datos | `h1` + resumen (en C, fecha + pastilla de bloqueo) | Lista de citas |
| Cargando | `h1` solo | Esqueleto (cliente: quitar el texto de las barras, §6.7; **no prototipado**) |
| Vacío | `h1` solo (medido: resumen `(oculto)`) | «Hoy no tienes ninguna cita» (cliente, sin cambios) |
| Error | `h1` solo | «No se pudo traer tu día» (cliente, sin cambios; cumple §6.4 regla 3) |

### 4.4 Accesibilidad
- **Nombre y estructura:** `h1` «Mi día»; en C, `h2.sr` «Citas de hoy» antes de las citas, y «Lo que llevas encima» (`h3`) deja de colgar de un `h1` directo.
- **Estado = color + icono + texto:** la pastilla de C lleva icono `#i-pause`, texto «1 con material incompleto» y `--block-ink` sobre `--block-bg` (5,41 : 1 claro, 6,10 : 1 oscuro).
- **Teclado/foco:** la cabecera no tiene controles; el orden de tabulación de la maqueta no cambia.
- **Objetivos:** sin cambios; mínimo medido 46 px (hamburguesa) y 56 px (`.gordo`).
- **Pendiente del cliente (no prototipado):** `role="status"` en `.senal` (§6.9) y `aria-live` al cambiar de estado (§6.4 regla 1).

### 4.5 Comportamiento por ancho (medido)

| Ancho | Original | A / B | C |
|---|---|---|---|
| **390×844** | cabecera 33 px (una línea) | 45 px (una línea) | 99 px (3 filas: título / fecha·citas·horas / pastilla) |
| 1440 / 1280 / 1024 | 38 px | 50 px | 50 px (una fila) |
| Hasta la 1.ª cita (desde el inicio de `main`) | 173,5 px (390) · 147 px (≥1024) | igual | 108,5 px (390) · **78 px** (≥1024) |
| Cola al final del scroll | −0,2 / −0,4 px | B: **+11,8 px** (390) · **+15,6 px** (≥1024) | ídem B |

### 4.6 Textos
Sin textos nuevos de producto. C reordena los existentes («Viernes 21 de agosto · 2 citas · 7 h de trabajo · 1 con material incompleto», 75 caracteres) y añade el nombre accesible «Citas de hoy».

---

## 5. Prototipo medido

Copias parcheadas de la maqueta (la original no se toca; `prototipos/genera-47-28.py`). Sin hex en las líneas añadidas; `usados − declarados = ∅` en B y C (en A, `--sp-5` sigue sin declarar: es la maqueta original).

| Archivo | Qué es |
|---|---|
| `prototipos/28-mi-dia-A-minimo.html` (+ `.diff`, 4 líneas) | Opción A |
| `prototipos/28-mi-dia-B-recomendado.html` (+ `.diff`) | **Opción B** |
| `prototipos/28-mi-dia-C-primer-pliegue.html` (+ `.diff`) | Opción C |
| Capturas | `28-original-390.png`, `28-B-recomendado-390.png`, `28-C-primer-pliegue-390.png`, `28-B-recomendado-390-final.png` (cola), `28-original-390-empty.png` / `28-B-recomendado-390-empty.png` (coherencia), `…-1440.png` |

**Reproducir:** `python3 -m http.server 8777 --bind 127.0.0.1 --directory …/prototipos` y `NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node …/prototipos/medir28.cjs` (también `refuta-sp5-28.cjs`, `medir28-extra.cjs`, `medir-sombra-cajon.cjs`, `barrido-pp-28.py`).

**Resultados** (390×844 / 1440×900; entre paréntesis 1280 y 1024 cuando difieren):

| Medida | Original | A | B | C |
|---|---|---|---|---|
| Alto de cabecera | 33 / 38 px | 45 / 50 | 45 / 50 | 99 / 50 |
| Aire arriba / abajo hasta el contenido | 12 / **0** | 12 / **12** | 12 / **12** | 12 / **12** |
| Aire bajo la caja de texto | 0 / 1 | 12 / 13 | 12 / 13 | 12 / 12,5 |
| Solape cabecera-contenido, recorte, scroll horizontal, elementos fuera del ancho | no / no / no / 0 | no / no / no / 0 | ídem | ídem |
| Hasta la 1.ª cita (px) | 173,5 / 147 | 173,5 / 147 | 173,5 / 147 | **108,5 / 78** |
| Cabecera + hasta la 1.ª cita, a 390 | 207 | 219 | 219 | **208** |
| Acciones de la 1.ª cita visibles sin desplazar | sí | sí | sí | sí |
| Línea roja de material, borde inferior a 390 (barra en 763) | 763,5 (a ras) | **775,5 (12,5 px bajo la barra)** | 775,5 | 764,5 (a ras) |
| Cola: aire última tarjeta → barra | −0,2 / −0,4 | −0,2 / −0,4 | **+11,8 / +15,6** | +11,8 / +15,6 |
| Destinos <24 px · mínimo · `.gordo` mínimo | 0 · 46 · 56 | ídem | ídem | ídem |
| `--sp-5` / `.gordo` padding lateral | — / 0 px | — / 0 | **20 px / 20 px** | 20 / 20 |
| Resumen en «cargando / vacío / error» | visible, dice «2 citas…» | visible | **oculto** | oculto |
| Contraste claro: resumen / pastilla de cabecera | 5,65 / — | 5,65 / — | 5,65 / — | 5,65 / **5,41** |
| Contraste oscuro: resumen / pastilla de cabecera | 5,53 / — | ídem | ídem | 5,53 / **6,10** |
| Contraste claro / oscuro de `.senal`, `.aviso-fila`, `.dura` | 5,25·5,84·5,65 / 7,14·5,54·5,53 | ídem | ídem | ídem |
| Isotipo del logo (dx del `<use>`) | −32,5 | −32,5 | **+0,9** | +0,9 |
| Sombra del cajón cerrado | sí (219,223,226 en x=0) | sí | **no** | no |

Mínimo exigido: 4,5 : 1 texto, 3 : 1 gráficos (§1.7); cumplen todos los pares medidos. La caja de texto de la cabecera no se recorta ni se solapa con la pastilla a ningún ancho (`cabecera.solapes = 0`, `recorte = false`).

---

## 6. Veredicto de viabilidad

**B: viable.** **C: viable con condiciones.** (Veredicto de la pantalla: **viable**; lo exigible es B.)

| Criterio | Respuesta |
|---|---|
| **Alcance dentro del sistema** | Sí. B usa solo tokens existentes (`--sp-3`, `--sp-4`, `--sp-5`, `--sp-6`, `--sh-modal`) y §3.1 tal como está escrito. C añade únicamente `.pill.p-block` (§6.10) con el icono que la propia pantalla ya usa en la cita (`#i-pause`). Cero componentes ni tokens nuevos. |
| **Esfuerzo** | A: 1 línea. B: ~10 líneas en 3 bloques de armazón (cabecera, lista, cromo). C: ~15 líneas más. |
| **Compatibilidad con DPROMA** | B corrige una contradicción con **D-39** (`--sp-5`). Conserva todo lo decidido en FICHAS 28 (56 px, acción fija abajo, «Cómo llegar»/«Llamar al sitio», aviso de material en la cita, «Lo que llevas encima»). C reordena la cabecera y retira una tarjeta; no toca ninguna decisión numerada. |
| **Condiciones de C** | (1) DPROMA confirma que la tarjeta «Hoy · viernes 21 de agosto» no cumple otra función; (2) decide si «falta material» es bloqueo duro o compra local (pp-028 frente a pp-025) porque eso fija qué botón es primario en la cita bloqueada; (3) se comprueba en un teléfono real, no solo a 390×844. |

**Deuda (no crítica, documentada, sin solución impuesta):** F7 (una sola acción primaria por pliegue; si DPROMA la quiere, `.cita-tel .gordo.p` pasa a variante secundaria salvo en la cita «Siguiente»), F8 (`.senal` → `.banda b-warn` con `role="status"`), F11 (estados), ruta del día (pp-022), vía para pedir el material que falta (pp-035).

---

## 7. Cómo se adopta

### 7.1 Qué cambiaría el cliente (mínimo)

**Exigir (B):**
1. l.313: `.p4{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;padding-bottom:var(--sp-3)}`.
2. l.24-25 (`:root`): declarar `--sp-5: 20px` (D-39, ya en su `_sio-tokens.css`). Igual en 29, 51, 57 y 58.
3. l.642-643: `padding-bottom` de `.tel` (`var(--sp-4)`; `var(--sp-3)` a ≤860).
4. Resumen oculto cuando la vista no es «con datos» (en producción: no pintarlo).
5. l.300-301: mover `box-shadow:var(--sh-modal)` de `.side` a `:root[data-menu="abierto"] .side`.
6. l.705: isotipo del logo con las medidas en el `<use>` y sin `viewBox` en el `<svg>` (§10).

**Proponer (C):** el diff de `prototipos/28-mi-dia-C-primer-pliegue.diff`.

### 7.2 Qué documentaríamos nosotros (reglas en el tono del sistema; lugares propuestos)

**§3.1 y bloque de referencia `ARQ-P4`.**
> El bloque de cabecera que se copia a cada pantalla lleva el relleno inferior en `.p4`, no en sus filas. Treinta pantallas lo tenían a 0: la cabecera de Mi día medía 38 px con 12 de aire arriba y ninguno abajo. Se comprueba midiendo la cabecera sola, sin filas opcionales: ≥12 px entre su última línea de texto y su borde.

**§6.4 — regla nueva.**
> El título de la cabecera persiste en cualquier estado; el resumen de datos, no. En vacío, error y cargando el resumen se retira: decir «2 citas» sobre «Hoy no tienes ninguna cita» contradice la pantalla.

**§3 / §10 (trampa de tokens).**
> `--sp-5` (D-39) ya está en `_sio-tokens.css` y falta en el `:root` embebido de cinco maquetas (28, 29, 51, 57, 58). El embebido se comprueba contra el archivo de tokens con `usados − declarados`.

**Nueva sección tras §7.3 — «Pantallas de campo».** *(Propuesta; solo lo medido.)*
> Una pantalla de campo se mide a 390×844 descontando el cromo (63 px) y la barra de acción fija (81 px): quedan 667 px menos la cabecera. Lo que decide la jornada —la siguiente cita y lo que la bloquea— queda sobre la barra. Ganar aire en la cabecera se paga en ese pliegue (12 px a 390 empujan la línea de material bajo la barra); se compensa quitando lo que el pliegue repite, no el aire. El suelo táctil es el de §7.3; el 56 px de la ficha (S-30) es un supuesto sin ratificar y no se codifica hasta que DPROMA lo haga.

**§7.2 Cromo (`ARQ-CROMO`):** la sombra del cajón solo existe con el cajón abierto (36 archivos) y el isotipo del logo lleva las medidas en el `<use>` (35 archivos).
**§11 (checklist):** añadir «¿La cabecera mide ≥12 px bajo su última línea, medida sola?» y «Si la pantalla gana aire en la cabecera, ¿se volvió a medir qué queda sobre la barra fija a 390×844?».

---

## 8. Lo que no sé / sin datos

- **Si el aviso «Sin señal» es permanente o solo aparece sin conexión.** La maqueta lo muestra en el estado «con datos»; los 84,5 px que ocupa a 390 (casi la mitad de lo que hay antes de la primera cita) no estarían con conexión. Además «lo que marques no se guarda hasta que vuelva la conexión» puede leerse como una cola local, y la ficha de `29` dice que **no** se dibujó una cola local (S-31, «Dibujarla la habría dado por decidida»); la pregunta 14 («¿El instalador llena el checklist en el sitio, o al volver?») sigue abierta.
- **Si «falta material» es bloqueo o compra local** (pp-028 / pp-025) y **qué ocurre con el sobrante** (las dos entrevistas discrepan).
- **Los 56 px (S-30) y el uso «de pie, con sol y con una sola mano»:** supuesto del autor; los `data/insights/` no mencionan guantes, sol ni una sola mano (`grep -i "guante\|una mano"` sin resultados). Sin datos.
- **Qué lee primero un instalador, cuánto mira la cabecera, qué teléfonos usa:** sin datos; la investigación no tiene pain points sobre la cabecera ni la agenda en móvil, y la voz del instalador llegó en una entrevista conjunta.
- **Efecto de `--sp-5` a menos de 320 px o con fuentes más grandes del sistema:** no medido (a 320/360/390, ninguno).
- **Teléfono real:** zona segura (`env(safe-area-inset-bottom)`), sol y teclado no probados; solo Chromium a 390×844.
- **`:has()`** en navegadores antiguos: no medido (el archivo ya lo usa, l.375).
- **Rendimiento:** no evaluado.
