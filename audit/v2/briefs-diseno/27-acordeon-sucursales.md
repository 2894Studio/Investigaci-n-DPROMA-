# Brief de diseño · Padrón de clientes (`27_padron_clientes`) · acordeón de sucursales

| | |
|---|---|
| **Pantalla** | `27_padron_clientes.html` (paquete `Actualizacion-12-10-26`, 931 líneas) |
| **Qué pidió la persona** | Hoja 12: «rediseño crítico del acordeón de sucursales: no es usable ni estético; diseñarlo y documentarlo». |
| **Sistema de referencia** | `sistema-diseno.md` v2.15.0 (`L1442` = línea 1442 de ese archivo) |
| **Prototipos** | `prototipos/27-acordeon-sucursales.html` (recomendado) · `prototipos/27-acordeon-opcion1-minimo.html` (opción 1) |
| **Veredicto** | **viable** (§6) |
| **Recomendación en una línea** | Cinco filas hijas que existen y se abren; lista de sucursales de 560 px alineada con el nombre de la razón social, sin tarjeta dentro de la tabla, estado solo cuando la sucursal no puede recibir órdenes y «Ver órdenes» junto a cada una. |

La maqueta del cliente no se tocó: los prototipos son copias generadas con `prototipos/medicion/generar-27-acordeon*.py`.

---

## 1. Diagnóstico

### 1.1 Qué hay hoy

Columna «Sucursales» de la tabla (`<col style="width:10%">`): un botón `.suc-btn` (pin + número + chevron) por razón social, y debajo una fila `<tr class="hijas"><td colspan="7">` con una tarjeta blanca (`.caja`: borde, `--r-card`, fondo `--surface`) dentro de una banda gris (`.hijas td{background:var(--surface-2)}`, L660–L661). La tarjeta tiene un encabezado `.enc` («Sucursales de esta razón social», L662–L665) y una lista `.suc-lista` donde cada `<li>` es `flex`: nombre + dirección (`.nom{…flex:1}`, L669) y a la derecha una pill «Puede recibir órdenes» y el botón «Ver órdenes» (`.der{margin-left:auto…}`, L672). Marcado: L785–L796.

### 1.2 Qué falla (maqueta servida en `:8732`; `prototipos/medicion/27a-original.json`)

| # | Falla | Evidencia reproducible |
|---|---|---|
| F1 | **No funciona.** 4 de 5 botones apuntan a un `id` que no existe; solo hay un `<tr class="hijas">`. `aria-expanded` no cambia al pulsar. | `aria-controls` en L776 (`suc-gav`, existe), L799 `suc-cvb`, L811 `suc-aca`, L835 `suc-rda`, L847 `suc-dpa` (no existen). `27a-original.json`: 5 botones, 1 con destino, `alterna: false`. Verificado: `audit/v2/verif/verif-2.json`, `v2-27padron-03`. Es el fallo que §6.15 `L1460` describe literalmente. |
| F2 | **Hueco enorme entre nombre y estado.** | Texto de la sucursal → pill: **578–654 px** a 1440 y **469–545 px** a 1280/1024 (`huecoTextoPill`). Lo empuja `.suc-lista .nom{flex:1}` (L669), **no** `margin-left:auto` (`.der` computa 0 px): corrección de `verif-2.json`, `27_padron_clientes-obs12`. |
| F3 | **Acciones fuera de la vista.** El panel mide lo que el `colspan` (1204 px a 1440; 1095,3 a 1280 y 1024) y la caja visible 1044 (1280) y 960 (1024). | Botones «Ver órdenes» fuera de la caja visible: **0 / 4 / 4 / 0** a 1440 / 1280 / 1024 / 390; a 1280 terminan en x≈1298 con la caja en 1280 (18 px). |
| F4 | **El botón flotante lo pisa.** | `.fab` de 52 px; hay botones del panel dentro de su zona (+16 px): 2 a 1440 y 1 a 1280. El sistema no documenta zona segura (búsqueda de «flotante»/«fab» en `sistema-diseno.md`: solo velos y sombras, ningún componente). |
| F5 | **Tarjeta dentro de banda dentro de tabla.** | §6.3 `L758–L760`: la tabla principal no va en tarjeta, y «no se anidan tarjetas dentro de tarjetas». |
| F6 | **El estado no informa.** Los cuatro renglones dicen lo mismo. | 4 de 4 pills «Puede recibir órdenes». |
| F7 | **Nombre accesible con plural erróneo**: «Ver las 1 sucursales de…» | L811 y L847. |
| F8 | Destino del botón de sucursales de 24 px de alto (justo el mínimo). | `suc-btn` mínimo 62,7×24 (`27a-original.json`, `calidad.sucBtn`). |

Contraste del panel actual: 5,04:1 (claro), 5,53:1 (oscuro). Sin fallo.

### 1.3 Causa raíz

La suma de cinco causas, de las que solo la 1 es de comportamiento: (1) falta el manejador y las cuatro filas hijas; (2) el contenido vive en un `colspan` cuyo ancho es el de la tabla, y la alineación a la derecha lo lleva al borde, fuera de la vista a 1280; (3) ninguna parte del panel se alinea con la fila que lo abre; (4) el estado por sucursal solo dibuja el caso positivo; (5) no hay zona segura del botón flotante en el sistema.

Dato de contexto que reduce el coste: **la entrega de Studio del 8-sep ya tenía el comportamiento**. `web/entregables/propuestas/padron-clientes.html` dibuja las cinco filas hijas con `hidden` (L933 y siguientes) y el manejador con Escape y retorno de foco (L1501–L1522). La `27` del cliente heredó el dibujo y perdió el comportamiento. El diseño visual (F2, F5) sí viene de nuestra propia entrega: lo corregimos nosotros.

---

## 2. Requisitos

| # | Requisito | Fuente |
|---|---|---|
| R1 | Cada `aria-controls` apunta a un `id` que existe; el control abre y cierra; Escape cierra y devuelve el foco al botón | §6.15 `L1460`, `L1464`; hoja 12 |
| R2 | El contenido del panel no depende del ancho de la tabla; legible sin desplazar a 1280 y 1024 | §6.11 regla 5 `L1248`; auditoría R2 |
| R3 | Cada sucursal dice su propio estado cuando no puede recibir órdenes («el bloqueo se dice en la sucursal») y ofrece «Ver órdenes» **de esa sucursal** | FICHAS L697 (dictamen 9, 17); `pp-098`, `pp-097` |
| R4 | Un renglón por sucursal: nombre · municipio, dirección en una línea, a lo sumo una pill con icono + texto + color | §6.10 `L1154`; §6.11 regla 7 `L1266`; §8 |
| R5 | Destinos ≥24×24 px | §7.3 `L1957` |
| R6 | Relación visible fila madre ↔ panel; sin tarjeta propia dentro de la tabla | §6.3 `L758–L760` |
| R7 | Una razón social sin sucursales no muestra control («Sin sucursales») | FICHAS D2 (L1247) |
| R8 | Nombre accesible correcto en singular y plural | auditoría F7 |
| R9 | No colocar acciones en la esquina inferior derecha | auditoría `v2-27padron-05` (el sistema no lo documenta) |
| R10 | No dibujar «Reenviar liga», vigencia ni duplicados dentro del panel | FICHAS D6 (L1251), D7 (L1252), D8 (L1253) |
| R11 | Conservar «fila de sucursales desplegable en vez del contador» y la casilla dentro de la celda de razón social | FICHAS L693 (dictamen 29); FICHAS L671 |
| R12 | Contraste ≥4,5:1, nada bajo 12 px, en los dos temas | §1.7 `L421`, §2.1 `L487` |
| R13 | Modo tarjeta por debajo de 860 px sigue funcionando | §6.11 «Modo tarjeta» |
| R14 | La completitud de documentos es de la razón social, no de la sucursal | FICHAS L1024 |

**Investigación.** `pp-098` («se identifica manualmente qué sucursal generó el servicio», `2026-07-16_soporte-administrativo-transversal.json`): el acordeón con «Ver órdenes» por sucursal es la respuesta, y hoy no funciona en 4 de 5 filas. `pp-097` (misma fuente): «Instalaciones debe validar manualmente el padrón antes de la visita técnica»: respalda decir en la sucursal si puede recibir órdenes.

---

## 3. Opciones evaluadas

Medidas en tema claro (`27a-original.json`, `27a-opcion1.json`, `27a-prototipo.json`).

| Medida | Maqueta | **Opción 1** · mínimo | **Opción 2** · recomendada |
|---|---|---|---|
| Botones con `aria-controls` válido | 1 de 5 | 5 de 5 | 5 de 5 |
| El control abre/cierra; Escape devuelve el foco | no | sí | sí (también desde dentro del panel) |
| Nombre accesible | «Ver las 1 sucursales de…» | «Ver la sucursal de…» | «1 sucursal de…» |
| Panel «Grupo Automotriz Vértice», alto (1440) | 246 px | 291 px | **200 px** |
| Ancho útil de la lista (1440 · 1280 · 1024) | 1170 · 1061 · 1061 | 558 | 560 |
| Hueco texto→pill (1440) | 578–654 | **30–72** | **8** (la pill va junto al nombre) |
| Hueco texto→acción (1440) | 749–824 | 201–242 | **112–187** |
| Botones fuera de la caja visible (1440·1280·1024·390) | 0·4·4·0 | 0·0·0·0 | **0·0·0·0** |
| Botones dentro de la zona del `.fab` (1440 · 1280) | 2 · 1 | 0 · 0 | **0 · 0** |
| Alto del panel a 390 (modo tarjeta) | 413 | 413 | **353** |
| Pills idénticas en el panel de 4 sucursales | 4 | 4 | **0** |

**Opción 1 · mínimo cambio sobre lo del cliente.** Cinco filas con `id` real y `hidden`, el manejador que Studio ya escribió el 8-sep, nombre accesible en singular/plural y `.hijas .caja{max-width:560px}`. Se conserva la tarjeta, el encabezado y las pills. Ventajas: resuelve F1, F2 (en parte), F3, F4 y F7 con una línea de CSS, el JS ya existente y cinco filas de marcado. Costes: a 560 px la dirección se parte en dos y tres líneas (alto 291 px frente a 246: se ve en `capturas/27a-opcion1--1440.png`); sigue la tarjeta dentro de la tabla (F5) y las pills iguales (F6). *No medí con una anchura mayor de 560 px.* Riesgo: la fila «Comercializadora Vértice del Bajío» está «Falta 1» y su panel sigue diciendo «Puede recibir órdenes» (así lo dibujó la entrega del 8-sep, L952–L960 de `padron-clientes.html`): el panel contradice a la fila.

**Opción 2 · recomendada.** Rediseño de la fila hija: sin tarjeta, banda `--surface-2` con el riel de acento de la fila madre, lista de 560 px alineada bajo el nombre de la razón social, pill pegada al nombre y solo cuando la sucursal **no** puede recibir órdenes. Resuelve F1–F8. Coste: ~20 líneas de CSS que sustituyen el bloque `.hijas`/`.suc-lista`, marcado de las filas hijas y el JS. Riesgo: quitar la pill positiva («Puede recibir órdenes») cambia lo que el cliente dibujó; si DPROMA la quiere explícita, es una línea (§7).

**Opción 3 · sub-tabla alineada a las columnas de la madre.** *No prototipada.* Los renglones de sucursal reutilizarían el `<colgroup>` (26 · 11 · 10 · 23 · 15 · 10 % + 136 px): nombre bajo la columna 1, estado bajo «Documentos fiscales», acción bajo «Acciones». Se descarta: «Acciones» es justo la columna que queda fuera de la vista a 1280 y 1024 (`v2-27padron-04`, verificado), la columna «Documentos fiscales» es del expediente de la razón social (FICHAS L1024), no de la sucursal, y exige desplazar a la vez dos filas con el desplazamiento horizontal de D-6.

---

## 4. Recomendación y especificación (Opción 2)

### 4.1 Marcado

```html
<td data-et="Sucursales">
  <button class="suc-btn" type="button" aria-expanded="false" aria-controls="suc-cvb"
          aria-label="2 sucursales de Comercializadora Vértice del Bajío">
    <svg class="ico ico-sm" aria-hidden="true"><use href="#i-pin"/></svg>2
    <svg class="ico ico-xs chev" aria-hidden="true"><use href="#i-down"/></svg></button></td>
…
<tr class="hijas" id="suc-cvb" hidden>
  <td colspan="7" data-et="Sucursales">
    <ul class="suc-lista" aria-label="Sucursales de Comercializadora Vértice del Bajío">
      <li><span class="nom"><span class="l1"><b translate="no">Irapuato · Guanajuato</b>
            <span class="pill p-warn"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-clock"/></svg>Bloqueada: faltan documentos</span></span>
          <span class="dir" translate="no">Blvd. Díaz Ordaz 1450, 36660 Irapuato, Gto.</span></span>
        <span class="acc"><button class="btn mini" type="button" aria-label="Ver órdenes de Irapuato · Guanajuato">Ver órdenes</button></span></li>
```

Cinco filas hijas por cinco botones, todas en el HTML con `hidden` (el ejemplo abierto de la maqueta lleva `aria-expanded="true"` y sin `hidden`). «Ver órdenes» conserva su texto visible dentro del nombre accesible (2.5.3). «Sin sucursales» se queda como pill sin botón (D2).

### 4.2 CSS (solo tokens; literales de maquetación: 560 px de lista, 28 px de alto mínimo, 15 px = ancho de la casilla)

```css
.suc-btn{…;min-height:28px}                                   /* era 24 px */
.hijas > td{padding:0;overflow:visible;background:var(--surface-2);box-shadow:inset 3px 0 0 var(--accent)}
tbody tr:has(> td .suc-btn[aria-expanded="true"]) > th{box-shadow:inset 3px 0 0 var(--accent)}
.suc-lista{list-style:none;max-width:560px}
.suc-lista li{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:var(--sp-1) var(--sp-4);
  padding:var(--sp-2) var(--sp-4) var(--sp-2) calc(var(--sp-4) + 15px + var(--sp-3));   /* nombre bajo el de la razón social */
  border-bottom:1px solid var(--border);font-size:var(--fs-dense)}
.suc-lista li:last-child{border-bottom:0}
.suc-lista li:hover{background:var(--surface)}
.suc-lista .nom .l1{display:flex;align-items:center;gap:var(--sp-2);flex-wrap:wrap}
.suc-lista .nom .dir{color:var(--text-2);font-size:var(--fs-meta)}   /* --text-2: --text-3 no da 4,5:1 sobre --surface-2 */
@media (max-width:860px){ .suc-lista{max-width:none} .suc-lista li{grid-template-columns:1fr;padding-left:var(--sp-4)}
  .suc-lista .acc{justify-content:flex-start} }
```

`:has()` ya la usa el cliente (`td:has(> input[type="checkbox"]:only-child)`, L370 de `27_padron_clientes.html`). **Tensión con §13.3 `L2569`** («el contenido crece con su contenedor, nunca un `max-width`»): esa regla habla de una tarjeta que declara «aquí hay algo grande» y deja una franja vacía; aquí el fondo es solo una banda y el contenido son renglones de ~300 px. Acotar es lo que evita el hueco de F2. Se documenta como excepción (§7).

### 4.3 Estados de la sucursal

| Estado | Cuándo | Pill | Fuente |
|---|---|---|---|
| Puede recibir órdenes | por omisión | **ninguna** (el silencio es lo normal) | la entrega del 8-sep la dibuja; aquí se omite por idéntica |
| Bloqueada | la razón social tiene documentos pendientes | `p-warn` + `#i-clock` · «Bloqueada: faltan documentos» | `padron-clientes.html` L995–L1012 (texto y variante); FICHAS L697; la causa es de la razón social, FICHAS L1024 |
| De baja | la sucursal está inactiva | `p-pause` + `#i-pause` · «De baja» | FICHAS D16 (L1278): «la ficha publica también las sucursales de baja, con `activo`». **Texto por confirmar.** |
| Razón social «Sin calcular» o inactiva | — | **sin datos**: el prototipo no dibuja pill | ver §8 |

Cargando: el esqueleto de la tabla ya cubre las filas; las filas hijas no se cargan aparte (los datos de sucursal vienen con la fila). Vacío: «Sin sucursales», sin botón (D2). Error: el de la pantalla.

### 4.4 Accesibilidad

`aria-expanded` + `aria-controls` a un `id` existente (§6.15 `L1460`); **Escape** cierra, tanto desde el botón como desde un botón dentro del panel, y el foco vuelve al botón (§6.15 `L1464`); `<ul aria-label>` nombra la lista; foco visible global; la pill lleva icono + texto (§6.10 `L1155`). Orden de tabulación: botón → acciones de la propia fila → panel (orden del DOM): se mantiene el de §6.15. No se probó con lector de pantalla (§8).

### 4.5 Comportamiento por ancho

| Ancho | Resultado |
|---|---|
| 1440 | Tabla sin desplazar; lista de 560 px a la izquierda; nada en la zona del `.fab` |
| 1280 y 1024 | La tabla se desliza (1095 px > 1044/960) pero el panel termina en x=796 y x=624: **0 botones fuera** |
| 390 (<860) | Modo tarjeta: la fila hija es otra tarjeta con el riel de acento; el botón baja bajo la dirección; 353 px de alto frente a 413 |
| 560–1200 | Medido en 560, 760, 861, 900, 1100, 1101, 1200 con los cinco paneles abiertos: 0 elementos fuera de la caja visible (`medicion/intermedios.json`) |

### 4.6 Textos (≤140 caracteres, una frase)

«Bloqueada: faltan documentos» (28) · «De baja» (7) · «Ver órdenes» · nombres accesibles «N sucursales de X» / «1 sucursal de X». Se retira el encabezado «Sucursales de esta razón social» (el botón y el `aria-label` de la lista ya lo dicen).

---

## 5. Prototipo medido

**Archivos.** `prototipos/27-acordeon-sucursales.html` (82 líneas distintas respecto a la maqueta) · `…/27-acordeon-opcion1-minimo.html` · `prototipos/medicion/` (`generar-27-acordeon.py`, `generar-27-acordeon-min.py`, `medir-27a.cjs`, `medir-lib.cjs`, `intermedios.cjs`, `tokens-huerfanos.py`, JSON) · capturas `prototipos/capturas/27a-{original,opcion1,prototipo}--{1440,1280,1024,390}.png`. Datos de ejemplo: los nombres y direcciones de las cinco filas salen de la propia entrega de Studio (`padron-clientes.html` L933–L1012) y de la `27`; **el estado «De baja» de «Aguascalientes» es un dato de demostración mío** (la `27` no lo dibuja). Tokens: 0 sin declarar, 0 hex fuera de `:root`.

```
cd audit/v2/briefs-diseno/prototipos && python3 -m http.server 8740 --bind 127.0.0.1 &
NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medicion/medir-27a.cjs http://127.0.0.1:8740/27-acordeon-sucursales.html prototipo salida.json
```

| Criterio | Maqueta | Prototipo |
|---|---|---|
| `aria-controls` válidos | 1 / 5 | **5 / 5** |
| Clic alterna `aria-expanded` y `hidden`; Escape cierra y devuelve el foco (botón y desde dentro) | no | **5 / 5, en los 4 anchos y 2 temas** |
| Texto→pill (1440) | 578–654 px | **8 px** (junto al nombre) |
| Botones fuera de la caja visible (1440·1280·1024·390) | 0·4·4·0 | **0·0·0·0** |
| Elementos del panel fuera de la caja visible | 15 (1280) · 19 (1024) | **0** |
| Botones en la zona del `.fab` (1440 · 1280) | 2 · 1 | **0 · 0** |
| Destinos <24 px en el panel | 0 | **0**; «Ver órdenes» 92,3×28; `suc-btn` mín. 62,7×**28** |
| Contraste mínimo del panel (claro / oscuro) | 5,04 / 5,53 | **5,25 / 5,25** (pill `warn` y `pause`); texto 5,97 / 7,10 |
| Texto <12 px en el panel | 0 | **0** |
| Solapes entre renglones | 0 | **0** |
| Alto del panel de 4 sucursales (1440) | 246 | **200** |

Ver `capturas/27a-prototipo--1440.png` (riel de acento, pills solo en las bloqueadas) y `27a-original--1280.png` (el «Ver órdene» cortado).

---

## 6. Veredicto de viabilidad: **viable**

- **Alcance en el sistema actual.** Todo con tokens y componentes que ya existen: `.suc-btn`, `.btn.mini`, `.pill` y sus variantes `p-warn`/`p-pause`, la fila desplegable de §6.15. No hay componente nuevo.
- **Esfuerzo.** El comportamiento ya está escrito (Studio, 8-sep, 22 líneas de JS). El CSS son ~20 líneas que sustituyen las del bloque `.hijas`/`.suc-lista`; el marcado de las filas hijas se reescribe 5 veces.
- **Compatibilidad con DPROMA.** Respeta dictamen 29 (FICHAS L693), dictamen 9/17 (L697), D2 (sin sucursales, sin control), D6/D7/D8 (nada de liga, vigencia ni duplicados) y la jerarquía vigente del padrón (FICHAS: «la entrega de Studio del 8-sep manda»).
- **No bloquea nada.** El estado «De baja» y los textos de bloqueo se pueden confirmar después; la maqueta funciona sin ellos (el mínimo es la opción 1).

---

## 7. Cómo se adopta

### 7.1 Qué cambiaría el cliente (mínimo → recomendado)

1. Añadir cinco `<tr class="hijas" id="suc-…" hidden>` (un `id` por cada `aria-controls`: L776, L799, L811, L835, L847) y el manejador de L1501–L1522 de `padron-clientes.html`.
2. Nombre accesible singular/plural (L776, L799, L811, L835, L847).
   **Hasta aquí + `.hijas .caja{max-width:560px}` es la opción 1.**
3. Sustituir el bloque CSS L660–L672 (y la línea de modo tarjeta `.pad .hijas .caja`, L704) por el de §4.2; `.suc-btn{min-height:28px}`.
4. Cambiar el marcado de cada `<li>`: `.nom` con `.l1` (nombre + pill condicional) y `.dir`; `.acc` con el botón. Quitar `.caja` y `.enc`.
5. Si DPROMA quiere la pill positiva explícita: `<span class="pill p-ok">…Puede recibir órdenes</span>` dentro de `.l1`, sin más cambios de CSS.

### 7.2 Qué documentaríamos nosotros (en el tono del sistema; sin número de §)

- **En «Fila desplegable» (§6.15)**, añadir: *La fila hija declara su propio ancho de lectura —unos 560 px— y se alinea a la izquierda, bajo el nombre de la fila madre; no hereda el del `colspan`. Es una banda, no una tarjeta: la tabla principal no va en tarjeta ni se anidan. La fila madre abierta y su hija comparten un riel de acento de 3 px. Un renglón por hija: nombre, estado solo si es distinto del normal, dirección en una línea y la acción a la derecha. El nombre accesible del botón cuenta lo que abre: «4 sucursales de X», «1 sucursal de X».* Y: *Cada fila hija existe en el HTML con `hidden`; un `aria-controls` sin destino es un control que miente.*
- **En «Un contenedor no cede el ancho a un descendiente» (§13.3)**, la excepción: *una lista de renglones cortos sobre una banda sin borde no crece con el contenedor; acotarla evita el hueco entre el nombre y su acción.*
- **Zona segura del botón flotante** (hueco de sistema, también en `v2-27padron-05`): *ninguna acción se ancla a la derecha de un contenedor que llegue a la esquina inferior derecha; la lista de sucursales queda a la izquierda por construcción.* Es una regla que el sistema aún no tiene; la propuesta completa es de otro brief.
- **Corrección a nuestro propio ejemplo:** §6.14 `L1435` muestra «Reenviar liga de registro» en el menú de fila, que D6 rechaza (FICHAS L1251). Hay que quitarlo del ejemplo.

---

## 8. Lo que no sé / sin datos

- **Cuántos estados de sucursal tiene el producto real.** La `27` solo dibuja el positivo; el 8-sep dibuja «Bloqueada: faltan documentos». «De baja» sale de D16 (L1278) y es **texto por confirmar**; no sé si también existe «municipio provisional» (D16 lo menciona en el modelo) como estado visible.
- **Qué muestra una sucursal cuya razón social está «Sin calcular» o inactiva.** La entrega del 8-sep dibuja «Bloqueada: faltan documentos» para «Distribuidora Peña y Asociados» (L1012), que es justo el caso que FICHAS L1019 dice que «sin calcular» **no** es «faltan». El prototipo no pinta pill ahí; la decisión es de DPROMA.
- **Si «Puede recibir órdenes» silenciosa es aceptable** para quien lo usa: no hay prueba con usuarios.
- **Lector de pantalla:** verificado en atributos y comportamiento del DOM, no con NVDA/VoiceOver.
- **Anchos de la caja entre 1101 y 1279 con la barra lateral completa:** medidos sin recorte; no revisados visualmente.
- **Opción 1 con un ancho mayor de 560 px:** no medida.
- **Modo oscuro:** medido en contraste; capturas solo en claro.
- **Rendimiento:** no evaluado.
- **Qué ancho de pantalla tenía la persona:** el recorte de «Ver órdenes» ocurre por debajo de ~1331 px de viewport; no puedo afirmar el suyo (`audit/v2/raw/27_padron_clientes.json`, `sin_datos`).
