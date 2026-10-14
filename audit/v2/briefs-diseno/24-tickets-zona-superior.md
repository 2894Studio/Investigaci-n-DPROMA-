# Brief de diseño · Tickets TI (`24_tickets`) · zona superior

| | |
|---|---|
| **Pantalla** | `24_tickets.html` (paquete `Actualizacion-12-10-26`, sha256 `d110a181…`, 836 líneas) |
| **Qué pidió la persona** | Hoja 9: «rediseño crítico, parte superior: las dos cajas amarillas no se distribuyen bien». Hoja 10: «Abiertos/Míos/Todos + Nuevo ticket chocan con la línea inferior; debe haber siempre margen». |
| **Sistema de referencia** | `sistema-diseno.md` v2.15.0 (cada § se cita con su línea: `L1707` = línea 1707 de ese archivo) |
| **Prototipos** | `prototipos/24-tickets-zona-superior.html` (recomendado) · `prototipos/24-tickets-opcion1-minimo.html` (opción 1) |
| **Veredicto** | **viable con condiciones** (§6) |
| **Recomendación en una línea** | Un solo bloque ámbar (el plazo) a ancho declarado junto a los datos, la regla de cierre en una banda neutra de una frase bajo los botones, el resto a toggletip; y `padding-bottom` en la cabecera. |

Reproducir: `grep -n` sobre `24_tickets.html` para las líneas citadas; mediciones en `prototipos/medicion/24-*.json` (comandos en §5). La maqueta del cliente no se tocó: los prototipos son copias con `generar-24.py`.

---

## 1. Diagnóstico

### 1.1 Qué hay hoy

**Cabecera de pantalla (hoja 10).** `<div class="p4"><div class="p4-t">` (L684) con `h1`, `.resumen`, y `.acc` que lleva el segmentado `.seg` «Abiertos · Míos · Todos» y `.btn.p` «Nuevo ticket». Reglas: `.p4{…border-bottom:1px solid var(--border);flex-shrink:0}` (L308) y `.p4-t{…padding:var(--sp-3) var(--sp-6) 0;…}` (L309). La pantalla no tiene `.p4-b` ni `.p4-f`, así que nadie aporta relleno inferior.

**Las dos cajas amarillas (hoja 9).** Primer hijo de `.det-cuerpo` (L657: `padding:var(--sp-4) var(--sp-6); display:flex; flex-direction:column; gap:var(--sp-4)`):

| Caja | Marcado | Estilo | Contenido |
|---|---|---|---|
| 1 · plazo | `<div class="caja-plazo">` L727 | `.caja-plazo{…background:var(--warn-bg);color:var(--warn-ink)}` L647; cifra a `26px` (L650), texto a `11.5px` (L652) | «Vence hoy / 24 AGO 2026» + dos párrafos (420 caracteres: regla de 1 día hábil, el plazo no cambia) |
| 2 · permisos | `<div class="banda b-warn">` L732, icono `#i-users` | `.b-warn{background:var(--warn-bg);color:var(--warn-ink)}` | «Tú puedes marcarlo resuelto; cerrarlo no…» + cierre automático a 5 días hábiles (366 caracteres) |

### 1.2 Qué falla (medido; maqueta servida en `:8732`, `medicion/24-original.json`)

| Medida | 1440 | 1280 | 1024 | 390 |
|---|---|---|---|---|
| Caja 1: x · ancho | 641 · 775 | 633 · 631 | 80 · 928 | 16 · 358 |
| Caja 2: x · ancho | 665 · 727 | 649 · 599 | 96 · 896 | 32 · 326 |
| Caja 2 queda dentro de la 1 a cada lado | 24 | 16 | 16 | 16 |
| Separación vertical entre las dos | 32 | 32 | 32 | 32 |
| Aire entre el control más bajo de la cabecera y su línea | **0** | **0** | **0** | **0** |
| Aire encima (hasta el control más alto) | 12 | 12 | 12 | 12 |
| Texto visible en las dos cajas | 810 caracteres | = | = | = |
| Elementos ámbar en la zona alta del panel (con la píldora «En atención») | 3 | 3 | 3 | 3 |

Coincide con el hallazgo verificado (`audit/v2/verif/verif-1.json`, `24_tickets-obs9`: x=641/665, ancho 775/727, 32 px frente a un `gap` de 16) y con `24_tickets-obs10` (control a 0 px de la línea).

Dentro del panel de detalle, el plazo se dice así: `24 ago` ×2, `Vence hoy` ×1, `1 día hábil` ×2 (medido con `textContent`; la auditoría decía «cinco veces» y la verificación no pudo fijar cuáles, así que aquí solo cuento lo reproducible). Antes del primer dato del ticket («Reporta», a 451 px de la cima de un panel de 674 px de alto a 1440) hay 810 caracteres de política.

### 1.3 Causa raíz

1. **Geometría.** `.detalle .banda{margin:var(--sp-4) var(--sp-6) 0}` (L560; y L561 a ≤1280) se escribió para una banda hija directa de `.detalle`. La banda de esta pantalla vive dentro de `.det-cuerpo`, que ya pone 24 px de relleno y 16 px de `gap` (L657): el margen se suma. De ahí 48 px menos de ancho y el doble de separación. Verificado (`verif-1.json`, `24_tickets-obs9`).
2. **Componente.** `.caja-plazo` es una clase propia que repite el par `--warn-bg`/`--warn-ink` de `.banda b-warn`, a ancho completo, con cifra a 26 px (no es un token: la escala tiene `--fs-title` 20 px y `--fs-kpi` 30 px) y texto a 11,5 px (suelo del sistema: 12 px, §2.1 `L487`). §6.9 `L1133` pide buscar primero si `.banda` + variante ya lo cubre; §6.20 `L1713` pide que el indicador declare su ancho.
3. **Contenido.** Cuatro significados de ámbar (plazo, prioridad Alta, estatus «En atención», regla de permisos). La verificación corrigió «cinco» a cuatro y dejó firme solo lo claro: la banda de permisos no es «falta o vence» (§1 `L43`; §1.3 `L240`) y su icono de personas no coincide con la variante (§6.9 `L1130`) (`verif-1.json`, `v2-24tickets-06`, «exagerada»). Y 420 + 366 caracteres contra el tope de una frase y ~140 (§8 `L2046`, `L2052`).
4. **Plantilla.** Cabecera sin relleno inferior: §3.1 `L553` manda `.p4{padding-bottom:var(--sp-3)}`. La plantilla ARQ-P4 de DPROMA no lo trae. El barrido de las 30 pantallas con `.p4` midió `padding-bottom:0` en todas y el control a 0 px en 8 (20, 21, 24, 33, 36, 38, 45, 47): `verif-1.json`, `24_tickets-obs10`. Es la causa de «en múltiples páginas».

### 1.4 Conflicto en FICHAS: ¿existe el plazo?

| Línea (`FICHAS_TECNICAS.md`) | Dice |
|---|---|
| L206–L207 | «con plazo»; «El semáforo lo **calcula el servidor**… `Tickets.tsx:32-37`. **Conservado**» |
| L864–L874 (Tanda 3) | «se retiró el reloj de plazo»; «No hay compromiso de respuesta escrito. Lo que había medía contra un número que me inventé»; «la píldora se quedó sin color a propósito» |
| L1032 | «No hay contrato de plazos de tickets» (`SUPUESTOS.md · S-07`) |
| L1735 (Fase 2, tanda 4, 29-sep) | «tickets ya tiene su propio semáforo de plazo (`.plazo`/`.rojo`/`.ambar`…)» |

**Cómo se resuelve sin decidir por la persona.** Las cuatro líneas son compatibles si se separan el mecanismo y los valores: el servidor calcula un semáforo (L207, L1735) pero no hay contrato escrito de cuánto dura un plazo (L866, L1032). Por tanto: la pantalla puede pintar **lo que el servidor devuelve** (estado y fecha) y **no debe afirmar reglas** como «un crítico tiene 1 día hábil». Esa cifra no tiene fuente (L866, L1032) y sale de la pantalla. Además la maqueta recibida es una variante previa a ambas tandas: no trae el cambio de la Tanda 3 ni el de la 4 (`audit/v2/raw/24_tickets.json`, `v2-24tickets-14`, `sin_datos`). El rediseño funciona con las dos lecturas (modo «plazo» y modo «solo antigüedad», §4); la persona o Jhon decide cuál se publica.

---

## 2. Requisitos

| # | Requisito | Fuente |
|---|---|---|
| R1 | Los dos bloques de la zona alta comparten borde izquierdo y derecho y un único origen de espaciado | §3 `L507`, §13.3 `L2569`; hoja 9 |
| R2 | El indicador de plazo declara su ancho y va junto a los datos del ticket, no a ancho completo encima de todo | §6.20 `L1713`; §13.2 `L2552` («fr acotado») |
| R3 | Ámbar solo para lo que vence pronto o falta; una regla de permisos no es advertencia | §1 `L43`, §1.3 `L240` |
| R4 | Bandas: una frase, sin punto y coma, ≤140 caracteres; la aclaración va a toggletip | §8 `L2046`, `L2052`, `L2035` |
| R5 | Icono de la banda coincide con su variante | §6.9 `L1130` |
| R6 | El plazo se dice una vez en el panel | Hoja 9; §8 |
| R7 | Nada bajo 12 px en los bloques nuevos | §2.1 `L487` |
| R8 | La cabecera cierra con aire inferior igual al superior, siempre | §3.1 `L553`; hoja 10 |
| R9 | Toggletip: `aria-describedby` siempre puesto, 24×24 mínimo, cierra con Escape/clic fuera/tab, uno abierto a la vez | §6.23 `L1895–L1909`; §7.3 `L1957` |
| R10 | No afirmar reglas de plazo sin contrato | FICHAS L866, L1032 |
| R11 | Conservar: semáforo del servidor, bitácora inmutable, «quién cierra» (S-10), prioridad con forma + color | FICHAS L207, L213 |
| R12 | Contraste ≥4,5:1 texto, ≥3:1 gráficos, en los dos temas | §1.7 `L421` |
| R13 | Sin recorte ni solape a 1440/1280/1024/390 | §13 |

Investigación: **sin datos específicos**. `grep -il "ticket\|mesa de ayuda\|helpdesk" data/insights/*` no devuelve ningún archivo (la auditoría v2 llegó a lo mismo). Apoyo indirecto, no de TI: `pp-064` y `pp-082` (WhatsApp sin historial estructurado / «ambigüedad sobre quién responde», `2026-07-31_direccion-general-supervision-operativa.json` y `2026-07-31_administracion-vehicular-equipo.json`) respaldan que quién confirma el cierre quede dicho, no cuánto dura un plazo. `pp-103` (soporte) trata del uso de IA, no de tickets: no lo uso.

---

## 3. Opciones evaluadas

Medidas en tema claro. Las columnas «Opción 1» y «Opción 2» salen de los prototipos servidos en `:8740` (`medicion/24-opcion1.json`, `24-prototipo.json`); la de la maqueta, de `24-original.json`.

| Medida | Maqueta | **Opción 1** · mínimo | **Opción 2** · recomendada |
|---|---|---|---|
| Aire control→línea de la cabecera | 0 px | **12 px** | **12 px** |
| Alto de `.p4` (1440·1280·1024 / 390) | 47 / 109 | 59 / 121 | 59 / 121 |
| Dispersión del borde izquierdo de los 6 bloques apilados (1440 / resto) | 24 / 16 | **0** | **0** |
| Separación vertical entre las dos cajas | 32 | **16** | no hay dos cajas apiladas |
| Elementos ámbar en la zona alta | 3 | 3 | **2** (píldora + plazo) |
| Caracteres visibles en las cajas | 810 | 810 | **98** |
| y del primer dato «Reporta» (1440·1280·1024·390) | 451·489·434·754 | 435·473·418·738 | **198·198·198·404** |
| `24 ago` / `1 día hábil` en el panel | 2 / 2 | 2 / 2 | **1 / 0** |
| Texto < 12 px en las cajas | 4 | 4 | **0** |

**Opción 1 · mínimo cambio sobre lo del cliente.** Dos selectores y una declaración: `.detalle .banda` → `.detalle > .banda` (L560, L561) y `.p4{padding-bottom:var(--sp-3)}` (L308). Ventajas: tres líneas, cero componentes nuevos, resuelve literalmente «no se distribuyen bien» (bordes a 0 px, separación 16) y «chocan con la línea». Costes: las dos cajas siguen siendo dos bloques ámbar de 420 y 366 caracteres y el primer dato sube solo 16 px. Riesgo: ninguno técnico; el riesgo es de producto (la persona marcó «rediseño», y esto lo deja igual de pesado).

**Opción 2 · recomendada.** Opción 1 + indicador de plazo a ancho declarado (`minmax(200px,240px)`) en una fila con los datos, regla de cierre en `.banda b-info` de una frase bajo los botones, aclaraciones a toggletip (§6.23) y el campo «Plazo» duplicado fuera. Ventajas: el primer dato sube 253 px, una sola caja ámbar, cumple R1–R13. Costes: un componente nuevo para el cliente (toggletip: ~25 líneas de CSS y ~20 de JS, que ninguna maqueta suya trae) y un símbolo `i-info` (que §6.23 ya usa y el sprite del cliente no tiene). Riesgo: la persona que lea la regla de cierre tendrá que pulsar ⓘ para ver los 5 días hábiles.

**Opción 3 · §6.20 al pie de la letra** (indicador a la derecha del bloque de identidad dentro de `.dh`, `minmax(0,1.6fr) minmax(300px,360px)`). *No prototipada.* Aritmética con medidas de la maqueta: ancho útil del panel 775 px a 1440 y 631 a 1280; con 24 de `gap` y 300 de columna derecha, la identidad queda en 451 y 307 px. Las tres acciones suman 493,6 px y el título 434,9: a 1440 las acciones ya envuelven y a 1280 el título también. §6.20 rompe a 1080 px de *viewport* (`L1720`), pero aquí el panel mide 824 px con un viewport de 1440 (57%), así que haría falta un punto de ruptura por contenedor que el sistema no documenta. Se descarta por coste y por no poder resolverse con lo existente.

---

## 4. Recomendación y especificación (Opción 2)

### 4.1 Estructura de la zona alta

```
.p4  (cabecera)              h1 · .resumen · .acc[.seg · .btn.p]            ← +padding-bottom
.detalle
  .dh                        .meta-l · h2 · .acciones · .banda.b-info(+ⓘ)   ← regla de cierre bajo los botones
  .det-cuerpo
    .resumen-ticket          .plazo-ind (240) | .campos (Reporta · Atiende · Abierto)
    .descrip · bitácora · notas   (sin cambios)
```

### 4.2 Marcado semántico

```html
<div class="banda b-info"><svg class="ico" aria-hidden="true"><use href="#i-info"/></svg>
  <p>Marcarlo resuelto no lo cierra: el cierre lo confirma quien lo reportó.</p>
  <button class="infob" type="button" aria-expanded="false" aria-controls="tip-cierre"
          aria-describedby="tip-cierre" aria-label="Más información sobre el cierre automático">
    <svg class="ico ico-xs" aria-hidden="true"><use href="#i-info"/></svg></button>
  <span class="tip" id="tip-cierre" role="tooltip" hidden>Si quien lo reportó no responde, el ticket se cierra solo a los 5 días hábiles.</span></div>

<div class="resumen-ticket">
  <div class="plazo-ind ambar" role="group" aria-labelledby="pz-et">
    <span class="et" id="pz-et">Plazo</span><b class="cifra">Vence hoy</b><span class="fecha">24 ago 2026</span>
    <button class="infob" …aria-label="Más información sobre el plazo"> … </button>
    <span class="tip" id="tip-plazo" role="tooltip" hidden>Se fijó al abrir el ticket y no cambia. El sábado y el domingo no cuentan.</span></div>
  <div class="campos"> … Reporta · Atiende · Abierto … </div>
</div>
```

La variante de color usa las clases que la maqueta ya tiene (`.rojo`, `.ambar`, `.verde`, `.gris`, L641–L645): **rojo** si venció, **ámbar** si vence hoy o mañana, **verde** el resto, **gris** si no hay plazo («Sin plazo registrado», ya dibujado en la fila 6 de la bandeja). Modo «solo antigüedad» (Tanda 3, L870): `Lleva abierto · 3 días · desde el 21 ago 2026, 08:12`, en gris.

### 4.3 CSS (solo tokens; valores literales de maquetación: 240/200 px de columna, 24 px de `.infob`, 220 px de `.tip`, tomados de §6.20/§6.23)

```css
.p4{…;padding-bottom:var(--sp-3)}                         /* §3.1: el contenedor cierra */
.detalle > .banda{margin:var(--sp-4) var(--sp-6) 0}       /* hijo directo, como se escribió */
.resumen-ticket{display:grid;grid-template-columns:minmax(200px,240px) minmax(0,1fr);gap:var(--sp-4)}
@media (max-width:560px){.resumen-ticket{grid-template-columns:1fr}}
.resumen-ticket .campos{display:flex;flex-wrap:wrap;gap:var(--sp-3) var(--sp-4);align-content:center}
.plazo-ind{position:relative;display:flex;flex-direction:column;justify-content:center;gap:var(--sp-1);
  padding:var(--sp-3) var(--sp-4);border-radius:var(--r-card);background:var(--warn-bg);color:var(--warn-ink)}
.plazo-ind.rojo{background:var(--err-bg);color:var(--err-ink)}   .plazo-ind.verde{background:var(--ok-bg);color:var(--ok-ink)}
.plazo-ind.gris{background:var(--surface-2);color:var(--text-2)}
.plazo-ind .cifra{font-size:var(--fs-title);font-weight:800;line-height:1.15;font-variant-numeric:tabular-nums}
.plazo-ind .et{font-size:var(--fs-meta);font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.campo .et{font-size:var(--fs-meta);…}                    /* era 10,5 px */
/* .infob y .tip: tal cual §6.23, con .tip a var(--fs-meta) en vez de 11,5 px */
```

### 4.4 Estados

- **Con datos / modo antigüedad:** arriba. **Sin plazo registrado:** `.plazo-ind.gris` con «Sin plazo registrado» en la cifra y sin fecha.
- **Cargando:** el esqueleto `.sk-det` (L765–L768: `<span class="skel" style="width:100%;height:44px">caja del plazo</span>`, con texto dentro) pasa a un bloque de 240 px de ancho y 86 px de alto junto a tres líneas, sin texto en las barras (ya pedido en `v2-24tickets-11`).
- **Vacío / error:** son de la bandeja y no cambian.

### 4.5 Accesibilidad

`role="group"` + `aria-labelledby` en el indicador; `aria-expanded`, `aria-controls` y `aria-describedby` siempre en `.infob`; abre con clic/Enter/Espacio; **Escape** cierra y devuelve el foco al botón; clic fuera y tabular a otro control cierran; un solo globo abierto. Destino 24×24 (46 en `data-tacto="dedo"`). Foco: el global `:focus-visible` del sistema. **No se probó con lector de pantalla** (§8); el panel conserva el `aria-live="polite"` que la maqueta ya declara sobre toda la `<section>` (L718).

### 4.6 Comportamiento por ancho

| Ancho | Resultado |
|---|---|
| 1440 | Indicador 240 px + campos en una fila (519 px; los tres caben) |
| 1280 | Indicador 240 + campos en 375 px: «Abierto» baja a una segunda fila (sin recorte ni solape) |
| 1024 | La bandeja se apila sobre el detalle (regla existente `max-width:1024px`); el panel ocupa todo el ancho |
| 390 | `.resumen-ticket` a una columna; indicador de 358×86 |
| 561–1200 | Medido a 560, 760, 861, 900, 1100, 1101, 1200: sin recorte, sin solape, cabecera a 12 px (`medicion/intermedios.json`) |

### 4.7 Textos (voz §8)

| Texto | Caracteres |
|---|---|
| «Marcarlo resuelto no lo cierra: el cierre lo confirma quien lo reportó.» (banda) | 71 |
| «Si quien lo reportó no responde, el ticket se cierra solo a los 5 días hábiles.» (toggletip) | 79 |
| «Se fijó al abrir el ticket y no cambia. El sábado y el domingo no cuentan.» (toggletip) | 74 |
| «Lleva abierto · 3 días · desde el 21 ago 2026, 08:12» (modo antigüedad) | 27 en la línea de fecha |

La regla de 1 día hábil, el «por qué no cambia el plazo» y la explicación de por qué lo cierra otra persona **salen de la pantalla** (§8 `L2014`: «si el texto explica una decisión, no va en pantalla»). Los 5 días hábiles y «el plazo no cambia» vienen de la maqueta del cliente: no tengo su fuente (§8 de este brief).

---

## 5. Prototipo medido

**Archivos.** `prototipos/24-tickets-zona-superior.html` (83 líneas distintas respecto a la maqueta) · `…/24-tickets-opcion1-minimo.html` (8 líneas distintas) · `prototipos/medicion/` (`generar-24.py`, `medir-24.cjs`, `medir-lib.cjs`, `captura-24.cjs`, `intermedios.cjs`, `tokens-huerfanos.py`, JSON de resultados) · capturas `prototipos/capturas/24-zona-{original,prototipo}--{1440,1280,1024,390}.png` y `24-{original,opcion1,prototipo}--*.png`. Tokens: los del `:root` de la maqueta; `tokens-huerfanos.py` da **0 tokens sin declarar y 0 hex fuera de `:root`** (§10, trampa de `--sp-5`).

**Reproducir:**
```
cd audit/v2/briefs-diseno/prototipos && python3 -m http.server 8740 --bind 127.0.0.1 &    # la maqueta, en :8732
NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medicion/medir-24.cjs http://127.0.0.1:8740/24-tickets-zona-superior.html prototipo salida.json 1
```

**Resultados (1440 · 1280 · 1024 · 390, claro y oscuro, modos «plazo» y «antigüedad»):**

| Criterio | Maqueta | Prototipo |
|---|---|---|
| Aire control→línea de la cabecera | 0 | **12 px en los 4 anchos** |
| Bordes izq./der. de banda y descripción (dispersión) | 24 · 16 · 16 · 16 | **0** |
| Contraste del bloque ámbar (claro / oscuro) | 5,25 / 7,14 | **5,25 / 7,14** |
| Contraste de la banda informativa | — | **5,97 / 7,10** |
| Contraste del globo | — | **15,21 / 13,93** (coincide con §6.23 `L1905`: 15,2 y 13,9) |
| Contraste del icono ⓘ (gráfico, ≥3) | — | **4,21–5,25 / 5,03–7,14** |
| Destinos <24 px en cabecera y en `.dh` | 0 | **0**; ⓘ mide 24×24 |
| Solapes entre bloques hermanos | 0 | **0** |
| Recorte horizontal del panel / scroll de documento | no / no | **no / no** |
| Toggletip: abre, `aria-describedby`, Escape cierra y devuelve el foco, cabe en el viewport (ancho) | — | **sí, en 2 botones × 4 anchos × 2 temas** |
| Texto <12 px dentro de las cajas | 4 | **0** |

**Lo que sigue bajo 12 px en la zona y no es de este rediseño:** `Crítica` 10,5 px y `En atención` 11 px en `.meta-l` (`.prio`, `.pill`). Es `v2-24tickets-08`; el PDF del cliente declara 0 y el archivo recibido no lo trae.

---

## 6. Veredicto de viabilidad: **viable con condiciones**

**Alcance dentro del sistema actual.** Sí. Todo con tokens existentes (`--warn-*`, `--err-*`, `--ok-*`, `--surface-2`, `--sp-*`, `--fs-meta`, `--fs-title`) y componentes documentados: `.banda` (§6.9), indicador de §6.20, toggletip §6.23. El único elemento no presente en las maquetas del cliente es el toggletip (ninguna lo implementa: `grep infob` en el paquete solo devuelve `.infobox` de otro componente).
**Esfuerzo.** La opción 1 son 3 líneas. La opción 2, ~25 líneas de CSS, 6 de marcado y ~20 de JS; el `.p4` se corrige una vez en la plantilla para 36 archivos.
**Compatibilidad con DPROMA.** No toca ninguna D-n. Conserva FICHAS L207 («semáforo lo calcula el servidor. Conservado»), la bitácora inmutable y S-10.

**Condiciones:**
1. **Decidir si el plazo se publica** (FICHAS L864–L874 frente a L1735, §1.4). El diseño no cambia, el texto del indicador sí. Hasta entonces, usar el modo «solo antigüedad» o el semáforo del servidor sin reglas.
2. **Aceptar el toggletip como componente nuevo** en las maquetas del cliente (CSS §6.23 + JS + símbolo `i-info`). Si no, la opción 1 (3 líneas) cierra lo que la persona vio, sin aligerar el texto.
3. **Corregir `.p4` en la plantilla compartida**, no pantalla por pantalla.

Lo que **no** cubre este brief y sigue abierto en la misma pantalla (críticos de `audit/v2/raw/24_tickets.json`): `v2-24tickets-01` contraste de tres textos (regresión), `-02` icono de «Abrir un ticket»/«Reintentar» a 1,03:1, `-03` quince enlaces del menú sin nombre a 1000 px, `-04` buscador de 16 px de alto.

---

## 7. Cómo se adopta

### 7.1 Qué cambiaría el cliente (diff mínimo, en este orden; cada paso es independiente)

1. `.p4{…;padding-bottom:var(--sp-3)}` (L308) y, en la plantilla ARQ-P4 compartida, `.p4-b`/`.p4-f` con solo relleno superior (en 27 el `.p4-f` ya cierra a 12 px: por aritmética el resultado no cambia, sin medir).
2. `.detalle .banda` → `.detalle > .banda` (L560 y L561).
   **Hasta aquí es la opción 1.**
3. Mover la banda a `.dh`, cambiar `b-warn` por `b-info`, icono `#i-info`, una frase (§4.2).
4. Sustituir `.caja-plazo` (L647–L653 y L727) por `.resumen-ticket` + `.plazo-ind`; quitar el campo «Plazo» (L738); `.campo .et` a `var(--fs-meta)`.
5. Añadir `.infob`/`.tip`, el símbolo `i-info` y el JS del toggletip.

### 7.2 Qué documentaríamos nosotros (reglas en el tono del sistema; sin número de §)

- **En «El relleno de un contenedor no vive en un hijo opcional» (§3.1):** *La plantilla de cabecera que entregamos ya trae `.p4{padding-bottom:var(--sp-3)}`. Una pantalla con solo `.p4-t` queda con 12 px entre su control más bajo y la línea, igual que arriba. Se comprueba midiendo: el control a 0 px de la línea es el síntoma.*
- **En «Avisos: inline y banda» (§6.9):** *`.banda` no lleva margen propio salvo como hijo directo de la zona que la aloja (`.detalle > .banda`). Un selector de margen escrito para un contenedor se aplica también a cualquier descendiente: dentro de otro contenedor con relleno, suma.* Y: *una regla de permisos informa, no advierte: va en `.banda-info`, no en `warn`.*
- **En «Ficha de detalle» (§6.20), nuevo caso «bandeja con detalle»:** *El plazo se dice una vez, en un indicador de ancho declarado (`minmax(200px,240px)`) junto a los datos del ticket: figura, fecha y nada más. Ámbar si vence hoy o mañana, rojo si venció, verde el resto, gris si no hay plazo. Cómo se calcula va a toggletip. El indicador pinta lo que el servidor devuelve; no enuncia reglas de plazo que el servidor no publique.*
- **En «Toggletip» (§6.23):** corregir `.tip` de `11.5px` a `var(--fs-meta)` (contradice §2.1) y añadir `i-info` al sprite de iconos del sistema.

---

## 8. Lo que no sé / sin datos

- **Si el plazo existe.** FICHAS lo contradice (§1.4); no es mía la decisión.
- **De dónde sale «5 días hábiles»** (cierre automático) y «el sábado y el domingo no cuentan»: están en la maqueta; no encuentro su fuente en FICHAS (`grep "5 días"` sin resultado). `S-10` cubre solo «quién cierra».
- **«3 días»** del modo antigüedad es el cálculo calendario entre el 21 y el 24 ago; no sé si se cuenta en días hábiles u horas.
- **Investigación de TI: sin datos** (0 pain points sobre tickets o mesa de ayuda; §2).
- **Lector de pantalla:** verifiqué atributos y comportamiento en el DOM, no con NVDA/VoiceOver. Con el `aria-live` de toda la `<section>`, no sé qué anuncia al abrir un globo.
- **Anchos 1101–1279 con la barra lateral completa:** medidos sin recorte (§4.6), pero en 1101 los campos se apilan en tres filas; no lo vi con datos de longitud real.
- **Modo oscuro:** medido en contraste; las capturas del repositorio son solo en claro.
- **Rendimiento:** no evaluado.
