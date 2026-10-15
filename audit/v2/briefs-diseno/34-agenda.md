# 34 · Agenda de instaladores — ¿cambiar la del cliente por la del sistema?

Pantalla: `34_instaladores.html` (Grupo B). Sistema de referencia: 2.15.0. Preguntas de la persona: «¿vale cambiarla por la del sistema? ¿Son combinables? ¿Cuál es más efectiva?».

## Respuesta corta

1. **No vale cambiarla.** La agenda del cliente funciona y no tiene ningún fallo crítico que dependa de ella. Los tres fallos críticos medidos de la pantalla son del cromo o de un token, y se arreglan igual con cualquier agenda (§4.1).
2. **«La agenda del sistema» no existe en 2.15.0.** El sistema no tiene componente de agenda: su índice termina en §6.23, `grep -n "6\.24" sistema-diseno.md` no devuelve nada, y «calendario» solo aparece dentro de §13.9 (líneas 2655 y 2662). Lo que hay para comparar es una regla (B) y nuestra propuesta anterior (C), que no está vigente.
3. **Son combinables.** C es A más piezas aditivas; B no choca con A mientras el alto de los bloques no venga de un dato, y hoy no viene. Lo que se conserva de A en C es casi todo (§3.3).
4. **Más efectiva: no hay datos de uso.** Medí proxies (texto, contraste, recorte, semántica, lectura de disponibilidad). Con ellos, la agenda del cliente **más un cambio mínimo (A′)** supera a A, a B y a C. Efectividad en tarea real: «sin datos» (§8).

---

## 1. Diagnóstico de lo que hay (A)

Evidencia: `grep -n` sobre `34_instaladores.html` y mediciones con Playwright (`prototipos/34-medir-agenda.cjs`, resultados en `prototipos/34-medidas-A.json`). Los números coinciden con los del auditor v2 y con `verif-3.json` (`v2-34inst-01`, `v2-34inst-text3-contraste-hover-y-dia`).

| Aspecto | Lo medido | Dónde |
|---|---|---|
| Estructura | Dos `<table>`, no rejilla de `<div>`. Semana: `<caption>`, 8 `th scope="col"`, 4 `th scope="row"`, 28 `td`. Día: 5 `th scope="col"`, 8 `th scope="row"`, 32 `td` | L721, L743 |
| Ancho | `table-layout:fixed`, `min-width:1040px`, primera columna 210 px y primera columna fija | L641 |
| Densidad a 1440 | Tabla de 1154 px; siete columnas de 135 px; 4 filas de 92 px; 9 visitas de 118×38 px y 19 huecos «—» de 28 celdas | medido |
| Recorte | A 1280, 30 px ocultos y el domingo visible 89 de 119 px. A 1024, 114 px ocultos y 5 px de domingo. A 390, 684 px ocultos y la primera columna ocupa el 59 % de la caja | medido |
| Tamaño de texto | **53 de 62 nodos de la semana y 19 de 23 del día por debajo de 12 px** (mínimo 10,5 px) | L642, L648, L657, L683, L687 |
| Contraste | Semana en reposo 4,82:1. Al pasar el cursor por una fila, 4,21:1 en «Interno · Querétaro» y «órdenes abiertas». En la vista día, «4 h» y «5 h» a 4,21:1 permanente | L68 (`--text-3:#66717F`) |
| Lector de pantalla | 0 de 19 huecos «—» con texto para lector. La visita «Sin instalador» está en la fila de «Mauricio Ríos Cantú» y el árbol de accesibilidad la anuncia así: `row "Mauricio Ríos Cantú … 10:00 Sin instalador"` | `aria34.cjs` |
| Vista día | Los bloques de 3, 4 y 5 h ocupan **una sola fila de hora**. **9 de las 32 celdas** quedan dentro de una visita y se dibujan vacías (Olvera 09–11, Beltrán 10–13, Ríos 11–12). Las filas con bloque miden 85 px y las vacías 35 | L683, medido |
| Cabecera fija | Con 8 y con 20 filas clonadas en memoria y 400 px de scroll, la cabecera **no se pega** (`thead` en top 62 y 32 frente a 209 de la región) | `34-medir-estres.cjs` |
| Estrecho | El modo tarjeta de ≤860 px es solo para `.tabla-caja` (L415); `.agenda` y `.dia-caja` no lo reciben | L415 |

Lo que ya está bien y hay que conservar: `<caption>`, `th scope` en los dos ejes, primera columna fija, destino de 38 px (≥24, §7.3), columna del domingo sombreada con `--pause-bg`, visita en domingo en ámbar con texto, barra de carga junto al nombre.

---

## 2. Requisitos

### 2.1 Sistema 2.15.0 (cada § verificado con `grep -n`)

- **§2.1**: «`--fs-meta` es el tamaño más pequeño del sistema. **Nada baja de ahí.**» (L487). La excepción de 10,5 px es solo para rótulos de grupo y etiquetas de campo del modo tarjeta, no para una agenda.
- **§6.11** (tabla densa), reglas 1, 2, 4, 5 y 7: `<caption>`; `<th scope="row">`; la cabecera no se corta; ninguna columna desaparece en silencio; una celda no lleva un párrafo.
- **§7.3**: destino de 24×24 px mínimo.
- **§1.1 / §1.7**: `--text-3` pasa de `#66717F` a `#5C6675` porque sobre `--surface-2` caía a 4,21:1; hay que medir también sobre `--surface-2`.
- **§1.3**: `--pause` = «Inactivo, en pausa — no es un fallo»; `--warn` = «Falta algo, o vence pronto». Para el domingo el cliente usa `--pause-bg` y para la visita en domingo `--warn` con texto. **2.15.0 no tiene regla de calendario laborable**: es una lectura defendible del cliente, no una divergencia.
- **§6.4, regla 1**: «El cambio se anuncia y mueve el foco» (escrita para las vistas de estado; el cambio Día/Semana es el mismo caso **por analogía**, no por texto).
- **§8**: ningún bloque siempre visible pasa de ~140 caracteres. Los dos avisos de la pantalla miden 279 y 269 según el auditor (decisión del cliente, ver 2.2; no se tocan).
- **§13.9** (leído completo, L2645–L2691). Regla para un bloque **cuyo alto lo decide un dato externo** (duración × escala). Dos fallas: `overflow:hidden` que recorta a media línea, y `flex-shrink:1` por omisión que **aplasta cada línea por debajo de su `line-height`** sin que `scrollHeight > clientHeight` lo detecte. Mecanismo en dos partes: (1) `flex-shrink:0` en cada línea; (2) retirar líneas completas por prioridad hasta que quepa, **después** de insertar el bloque en el documento. La información retirada queda en `aria-label`/`title`. **No dice nada de agendas sin alto por dato.**
- **No existe** en 2.15.0: ningún componente de agenda, ninguna regla de calendario laborable, de rango temporal ni de «fila de lo no asignado».

### 2.2 FICHAS (`grep -n "34_instaladores" FICHAS_TECNICAS.md`: L359, L904, L1378, L1751)

Decisiones del cliente, literales:

- L366: «Una visita **sin instalador** va marcada y se cuenta arriba».
- L367: «El **domingo no es laborable**, y una visita en domingo **se enseña marcada** en vez de esconderse».
- L369–371: «la agenda como rejilla semanal de siete columnas con la del domingo sombreada; la barra de carga junto al nombre; que los dos avisos vayan **arriba de la agenda** y no como nota al pie; y el rango semana/quincena».
- L906: «Se esperan entre 8 y 20 instaladores en doce meses.»
- L910–912: «**Vista de día**, conmutable con la de semana: horas en las filas, instaladores en las columnas. La duración va escrita —«4 h»— en vez de estirar el bloque, porque estirarlo obliga a fusionar filas y con filas fusionadas se pierde la lectura por hora.»
- L914: «⛔ **No se dibujó agrupación por plaza ni paginación**».
- L1756: en la tanda 4 se pidió usar el componente más cercano «**sin inventar ninguno nuevo**».

### 2.3 Investigación

- `pp-022` (media, `data/insights/2026-07-22_coordinacion-tecnica-instalaciones.json`, 00:34:40): «La programación y las rutas de instalación se elaboran en un Word manejado aparte». Evidencia literal: «La agenda de rutas se trabaja en un Word separado».
- Mismo documento, flujo «Solicitud … agenda»: «Arman la agenda de instalaciones **según disponibilidad, ciudad y fecha solicitada** por el cliente» (00:34:40). La tarea real es leer **disponibilidad** y **ciudad**: lo que importa a una agenda es saber quién está libre.
- `pp-020` (media, 00:22:23): «se contacta y agenda manualmente».
- Sin dato en la investigación sobre cuántas visitas hay por día, qué duración mínima tienen ni si la agenda se consulta desde teléfono.

---

## 3. Opciones evaluadas

### 3.1 Qué es cada una

- **A. La del cliente tal cual** (`34_instaladores.html`).
- **B. §13.9 aplicado a esa agenda.** Se lee de dos maneras. **B0**: lectura literal; la agenda no tiene bloques con alto por dato (`.bloque-cita` no declara `height`; `grep -n "height" ` en L683–L687 no lo muestra), así que §13.9 no tiene nada que regular y A ya cumple. **B1**: si se quisiera alto = duración × escala, el plan de §13.9 aplica a la vista día. Prototipo: `prototipos/34-B-dia-proporcional-13-9.html`. La vista semana no lleva duración y queda igual que A.
- **C. Nuestra propuesta anterior** (`audit/raw/34_instaladores.json`, `cobertura`; su «§6.24» no existe en 2.15.0). `<table>` con `<caption>` y `th scope`, eje de entidades fijo, hora a `--fs-dense` y cliente a `--fs-meta` sin bajar de 12 px, hueco con texto para lector, sin modo tarjeta (por debajo de 860 px, vista día por omisión), `aria-live` y foco al cambiar de rango, fila de «lo no asignado», rango con etiqueta concreta y navegación anterior/siguiente, **sin ofrecer un rango sin vista**, calendario laborable como dato. Prototipo: `prototipos/34-C-propuesta-previa.html`.
- **A′ (recomendada).** A más el cambio mínimo de §4. Prototipo: `prototipos/34-A-prima-cambio-minimo.html`. No es una cuarta agenda: es A con parches.

### 3.2 Tabla de criterios

Fuente de cada celda: `prototipos/34-medidas-*.json` (mediciones a 1440/1280/1024/390) y `34-medir-*.cjs`. «Sin datos» donde no se puede afirmar.

| Criterio | A · cliente | B · §13.9 | C · propuesta previa | A′ · A + mínimo |
|---|---|---|---|---|
| **Densidad a 7 columnas, 1440** | 1154 px de tabla; columnas de 135; 4 filas, caja de 400 px; 9 visitas | Semana = A. Día: 4 columnas de 273 px; bloques de 162, 216 y 270 px de alto (3, 4 y 5 h a 0,9 px/min); eje lineal | Igual que A en ancho; 5 filas, caja de 476 px | Columnas de 140; 5 filas, caja de 511 px (+111 frente a A) |
| **Densidad, 1280** | Tabla 1040 en caja de 1010: **30 px ocultos**; domingo 89 de 119 px visible; 1 nombre cortado con «…» | Semana = A | **Igual: 30 px ocultos**; **5 nombres cortados** con «…» (12 px sin envolver) | **0 ocultos**; domingo 119 de 119; 0 nombres cortados |
| **Densidad, 1024** | 114 px ocultos; domingo 5 px | Semana = A | 114 px ocultos | 34 px ocultos |
| **Legibilidad: texto <12 px** | **53/62** semana, **19/23** día | Semana 53/62 (= A). Día 0/22 | **0/65** semana, 0/23 día | **0/65** semana, 0/24 día |
| **Legibilidad: contraste mínimo** | 4,82 reposo; **4,21 con cursor**; **4,21 «4 h»/«5 h»** | Día 4,21 (`.dur` en `--text-3`) | 4,82 reposo; **4,21** con cursor y en día (no toca el token) | **5,02** reposo y cursor; **4,93** día |
| **Semántica de rejilla** | `<table>`, `caption`, `th scope` ×2. Huecos 0/19 con texto. «Sin instalador» colgada de una persona | Día: rejilla de `div` + `ul role="list"` por persona; el nombre del bloque lleva las horas, **pero se pierde la coordenada fila/columna** que anuncia la tabla. Semana = A | `<table>` + 20/20 huecos con texto + fila «Sin asignar» | Igual que C + 9 celdas de continuación con texto («Sigue ocupado hasta las 12:00: …») |
| **Lectura de disponibilidad (día)** | **9/32 celdas** dentro de una visita parecen libres | 0 (eje lineal, el bloque cubre sus horas) | 9/32 (no lo cubre) | 0/32 |
| **Estrecho 390** | 684 px ocultos; 1.ª columna 59 % | Día: 404 px ocultos | 684 px ocultos; día por omisión ≤860 pero a 390 sigue 404 ocultos | 604 px ocultos; 1.ª columna 49 % |
| **Cabecera fija con 8–20 filas** | No se pega | No se pega (semana = A) | No se pega | **Se pega** (la caja se desplaza por dentro) |
| **Esfuerzo de adopción** | 0 | +44/−28 líneas; sustituye la tabla del día por rejilla de `div`; JS de ajuste; componente nuevo sin § | +49/−14 líneas; JS; controles nuevos; quita «Quincena»; § nueva | +44/−22 líneas; 0 componentes nuevos; JS 0 |
| **Compatibilidad con FICHAS** | Es lo documentado | **Contradice** L910–912 («en vez de estirar el bloque») si se estira | **Contradice** L371 («el rango semana/quincena») al retirar Quincena. Respeta L366–367 | Respeta L366, L367, L369–371, L910–912 |
| **Efectividad en tarea real** | Sin datos | Sin datos | Sin datos | Sin datos |

Cuenta de líneas: `diff 34_instaladores.html <prototipo> | grep -c '^>'` y `'^<'` (líneas físicas; algunas son filas HTML largas).

### 3.3 Combinabilidad: qué de A se conserva

| Pieza de A | Con B (§13.9) | Con C |
|---|---|---|
| `<table>`, `<caption>`, `th scope` en los dos ejes, primera columna fija | Semana se conserva. El día cambia a rejilla de `div` y pierde `th scope` | Se conserva entera |
| Siete columnas con domingo en `--pause-bg` y visita en domingo en ámbar | Se conserva (la semana no cambia) | Se conserva; el domingo pasa de clase `.dom-col` a atributo `data-laborable` (invisible) |
| Barra de carga junto al nombre | Se conserva | Se conserva; C pide además el denominador escrito («4 de 6»), sin dato del tope: no prototipado |
| «Sin instalador» marcada y contada arriba | Se conserva | Se conserva y **mejora** (fila propia) |
| Duración escrita «4 h» (L910–912) | **No se conserva**: el alto sustituye al texto | Se conserva |
| Quincena (L371) | Se conserva | **No se conserva** (C la retira) |
| Avisos arriba de la agenda (L370) | Se conserva | Se conserva |

Lectura: **B es ortogonal** (solo toca el día y solo si el alto viene del dato). **C ⊂ A + parches**; lo único que C quita de A es Quincena, y lo único que le añade que A′ no tiene es el control de rango anterior/siguiente, el anuncio de cambio de vista y la vista día por omisión en estrecho.

### 3.4 Qué dice la prueba de §13.9

`prototipos/34-medir-bloques-13-9.cjs`, 13 bloques en la vista día de B (los 3 del cliente de 180, 240 y 300 min, más 10 de **banco de pruebas** de 30–120 min que **no son dato del cliente**), a 1440 y 1024:

| Variante | Bloques ≤60 min (7) | Resultado |
|---|---|---|
| Con el plan de §13.9 (`flex-shrink:0` + retirar por prioridad tras insertar) | 30 y 45 min → solo cliente; 60 min → cliente y sucursal | **0 líneas comprimidas, 0 cortadas, 0 solapadas** |
| Sin plan (flex por omisión) | Las 3 líneas dentro de 27, 40,5 o 54 px | **7 de 13 bloques con 2 líneas comprimidas por debajo de su `line-height` y texto solapado** (3 pares en los de 30 y 45 min, 1 en los de 60). `scrollHeight > clientHeight` del bloque solo lo delata en los dos de 30 min; los de 45 y 60 min «caben» (41/41 y 54/54) y se ven rotos, como describe §13.9 (`34-medir-solape-13-9.cjs`) |
| Con los datos del cliente (3, 4, 5 h) | Ninguno es corto | **El plan nunca se activa**: los tres bloques ya caben con todas sus líneas |

Detalle de orden de ejecución que §13.9 anuncia y se reprodujo: la vista día arranca `display:none`; medir en ese momento retira líneas de más o ninguna. Se resolvió con `ResizeObserver` sobre la caja.

---

## 4. Recomendación y especificación

**Mantener la agenda del cliente (A) y aplicar el cambio mínimo A′.** No sustituir por B ni por C. Orden de prioridad:

### 4.1 Críticos medidos (valen con cualquier agenda; no son de la agenda)

| # | Hallazgo | Medido | Criterio (Regla 1 de la persona) | Cambio mínimo |
|---|---|---|---|---|
| K1 | `--text-3:#66717F` a 4,21:1 sobre `--surface-2` (cursor sobre fila; «4 h» y «5 h» del día) | `verif-3.json` `v2-34inst-text3-contraste-hover-y-dia`: confirmada | Texto <4,5:1 medido | Una línea en `:root` claro: `--text-3:#5C6675` (valor de 2.15.0, §1.1). Resultado medido: 4,93:1 |
| K2 | Buscador: `input` de 329×16 px dentro de `div.search`; clic en el relleno no lo enfoca | `v2-34inst-buscador-16px`: confirmada. Matiz de la verificación de la misma pieza en otras pantallas (`v2-24tickets-04`, `v2-54bit-buscador-16px`): **no incumple WCAG 2.5.8** (excepción de espaciado); sí §7.3 y §10 trampa 4 | Destino <24 px (criterio del auditor) | Cambiar `<div class="search">` por `<label class="search" for="buscar">` |
| K3 | Menú colapsado (861–1100 px): 15 enlaces sin nombre accesible | `v2-34inst-menu-colapsado-sin-nombre`: confirmada | Control sin nombre | `aria-label` y `title` en cada `.it`, en la plantilla del cromo |

K2 y K3 son del cromo copiado en todas las pantallas; se arreglan en la plantilla, no en esta agenda.

### 4.2 Cambios sencillos de la agenda (no críticos, causa raíz clara)

| # | Cambio | Por qué | Evidencia |
|---|---|---|---|
| S1 | Pasar a `--fs-meta` los textos de la agenda (`.vt`, `.libre`, `.agenda thead th`, `.dos small`, la etiqueta «órdenes abiertas», y en el día `th`, `.bloque-cita`, `.dur`) | §2.1. Según el auditor v2 (`audit/v2/raw/34_instaladores.json`), el PDF del cliente declara 0 declaraciones <12 px y el archivo trae 34 (`verif-3.json`, confirmada) | 53/62 → **0/65** |
| S2 | Fila «Sin asignar» (y columna en el día) | La visita sin instalador no se cuelga de una persona. Respeta L366 | Árbol de accesibilidad: fila propia |
| S3 | Huecos con texto: `—` + `<span class="sr">sin visitas</span>` | Lector de pantalla | 0/19 → **20/20** |
| S4 | **Vista día: celdas de continuación** en cada hora que cubre una visita, **sin fusionar filas** ni estirar el bloque | Lectura de disponibilidad, que es la tarea (`pp-022`: «según disponibilidad»). Respeta L910–912 | 9/32 celdas libres falsas → **0** |
| S5 | Primera columna a 176 px, `min-width:960px`, y que el nombre del cliente y del instalador **se parta en líneas** en vez de cortarse | El domingo es la columna que el aviso manda corregir | 1280: 30 → **0 px** ocultos; 0 nombres cortados |
| S6 | `.agenda{overflow:auto;max-height:min(70vh,640px)}` | `overflow-x:auto` obliga a `overflow-y:auto`; el `thead` sticky de §6.11 se pega a la caja, no a la página. El cliente espera 8–20 instaladores (L906) | 8 y 20 filas: no fijada → **fijada** |

Costo medido de S1–S6: la caja de la agenda pasa de 400 a 511 px (+111 px: 60 de la fila «Sin asignar», 51 de 12 px y nombres en dos líneas). A 1280×800 caben 3 filas enteras en ambas; con A′ una de ellas es «Sin asignar». `34-medir-pliegue.cjs`.

### 4.3 Marcado

```html
<!-- S2: fila propia para lo no asignado -->
<tr class="sin-asignar">
  <th scope="row"><span class="dos"><b>Sin asignar</b><small>1 visita sin instalador</small></span></th>
  <td></td><td></td>
  <td><div class="cel"><a class="vt sin" href="#"><b>10:00</b><span>Sin instalador</span></a></div></td>
  <td></td><td></td><td></td><td class="dom-col"></td>
</tr>
<!-- S3: hueco con texto -->
<span class="libre">—<span class="sr">sin visitas</span></span>
<!-- S4: continuación, una por hora cubierta -->
<span class="ocupa"><span class="sr">Sigue ocupado hasta las 12:00: Vértice del Bajío</span></span>
```

### 4.4 CSS (solo tokens del `:root`; sin hex)

```css
/* :root claro */  --text-3:#5C6675;            /* K1 */

.agenda thead th{font-size:var(--fs-meta)}      /* S1 */
.agenda .dos small,.agenda .et-carga{font-size:var(--fs-meta)}
.vt,.libre{font-size:var(--fs-meta)}
.dia-caja thead th,.dia-caja tbody th,.bloque-cita,.bloque-cita .dur{font-size:var(--fs-meta)}

.agenda thead th:first-child{width:176px}       /* S5 */
.agenda table{min-width:960px}
.vt span{white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere}
.agenda .dos b{white-space:normal}
.dia-caja table{min-width:820px}

.ocupa{display:block;min-height:19px;border-radius:var(--r-ctrl);   /* S4 */
  background:var(--surface-2);border-left:3px solid var(--serie-1)}
.ocupa.sin{background:var(--err-bg);border-left-color:var(--err)}

.agenda{overflow:auto;max-height:min(70vh,640px)}                    /* S6 */
```

`--serie-1` conserva el valor del `:root` de la maqueta (`#2C6CA8`); 2.15.0 lo cambia por ΔE (§1.4), y esa actualización llega con el resto de tokens.

### 4.5 Accesibilidad

- `<caption>` y `th scope` se conservan. Cada cita sigue nombrada «hora + cliente»; el día y la persona los da la tabla.
- Los huecos y las continuaciones llevan texto para lector (`.sr`), no `aria-label` sobre un `span` sin rol.
- Contraste de los textos nuevos: 5,02:1 en reposo y con cursor en la semana; 4,93:1 en el día (`34-medidas-A-prima.json`).
- Destino de cita: 42 px de alto y 95 px de ancho como mínimo en los cuatro anchos medidos (≥24, §7.3).
- **No incluido** y documentado: anuncio y foco al cambiar Día/Semana (§6.4, regla 1 por analogía; el cliente lo recibe en el script compartido), que es lo que C sí prototipa. Medido en C: al cambiar de vista el foco va al `h2` y el `role="status"` dice «Vista de semana: 24 al 30 de agosto».

### 4.6 Comportamiento por ancho (medido en A′)

| Ancho | Semana | Día |
|---|---|---|
| 1440 | Cabe entera; 7 columnas de 140 px; domingo 140/140; 0 nombres cortados | Cabe; 5 columnas |
| 1280 | **Cabe entera** (A recortaba 30 px); domingo 119/119 | Cabe |
| 1024 | 34 px ocultos con desplazamiento; domingo 78/112 visibles; primera columna fija | Cabe |
| 390 | 604 px ocultos; la primera columna ocupa el 49 % de la caja. **Sin cambio de fondo**: ni A, ni B, ni C resuelven 390 | 464 px ocultos |

Para estrecho no se propone cambio: la coordinación trabaja la agenda en escritorio y el instalador tiene sus propias pantallas (`28_instalador_mi_dia`, `29_instalador_orden`, FICHAS L802–L817). «Sin datos» de uso desde teléfono.

---

## 5. Prototipo medido

Todos son copias de la maqueta del cliente con sus tokens y su cromo, para conservar los anchos reales; **la maqueta original no se tocó**. Se reconstruyen con `prototipos/34-construir-prototipos.py` (lee `34_instaladores.html`; variable `MAQUETAS`).

| Archivo | Qué es |
|---|---|
| `prototipos/34-A-prima-cambio-minimo.html` | A′ (recomendada) |
| `prototipos/34-C-propuesta-previa.html` | C con sus piezas |
| `prototipos/34-B-dia-proporcional-13-9.html` | B1. `?estres=1` añade 10 bloques cortos de prueba; `?sinplan=1` desactiva el plan (control) |
| `prototipos/34-{A,Aprima,B,C}--{1440,1280,390}-{semana,dia}.png` | Capturas |
| `prototipos/34-medir-agenda.cjs`, `-estres.cjs`, `-bloques-13-9.cjs`, `-pliegue.cjs`, `-aria.cjs` | Instrumentos |
| `prototipos/34-medidas-*.json` | Resultados |

Reproducir: `cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node 34-medir-agenda.cjs A http://127.0.0.1:8732/34_instaladores.html '.agenda' '.dia-caja' A.json` (a los prototipos, `python3 -m http.server 8764` dentro de `prototipos/`).

Medición de estrés, vista día con N personas (1440 / 1280): con **8** columnas, 134 / 116 px por columna y bloques de 117 / 99 px en A y A′. Con **20**: 53 / 46 px, bloques de 37 / 30 px y de 212 a 293 px de alto, y desborde de 22 / 29 px en A y de 28 / 35 px en A′. B a 20 columnas: 55 / 47 px. La nota de la propia pantalla dice «El día cabe siempre»; **se cumple hasta unas 8 columnas, no con 20.** Lo que lo reduce en el diseño del cliente es el filtro por ciudad (L908); cuántos instaladores hay por ciudad: sin datos.

---

## 6. Veredicto de viabilidad

**Mantener la agenda del cliente con cambio mínimo (A′): `viable con condiciones`.**

- Alcance: dentro del sistema actual; 0 componentes nuevos; CSS y HTML de un archivo; sin JS nuevo.
- Esfuerzo: K1–K3 de una línea cada uno; S1–S6 en un solo archivo (+44/−22 líneas).
- Compatibilidad con decisiones citadas literal: respeta L366, L367, L369–371 y L910–912.
- **Condiciones**: (a) que el cliente acepte la fila «Sin asignar» y las celdas de continuación (cambian lo dibujado, no lo decidido); (b) que acepte perder una fila por pliegue en 1280×800; (c) que confirme si usa la agenda fuera de escritorio.

**Sustituir por B: `no viable ahora`.** §13.9 no aplica mientras el alto no venga de un dato; hacerlo vendría contra L910–912 («en vez de estirar el bloque»); crea un componente que 2.15.0 no documenta; y no resuelve los 53 nodos <12 px de la semana.

**Sustituir por C: `no viable ahora`.** Su «§6.24» no existe en 2.15.0; retirar «Quincena» contradice L371; no corrige el recorte de 1280. Sus piezas aditivas (S2, S3, S1) sí entran, vía A′.

---

## 7. Cómo se adopta

**El cliente cambia** (solo en `34_instaladores.html`, y K2/K3 en la plantilla del cromo):

1. `--text-3:#5C6675` en el `:root` claro.
2. Textos de la agenda a `var(--fs-meta)` (S1).
3. Añadir la fila y la columna «Sin asignar», y mover ahí la visita sin instalador (S2).
4. `.sr` en los huecos (S3) y celdas de continuación en el día (S4).
5. Primera columna a 176 px, `min-width:960px`, nombres que se parten (S5).
6. `overflow:auto` con `max-height` en `.agenda` (S6).
7. `<label class="search">` y `aria-label` del menú (K2, K3).

**Nosotros documentamos en el sistema**, en tono del sistema y sin número de § hasta ubicarlo:

- **Agenda (rejilla persona × día).** Es una tabla de comparación entre filas. Lleva `<caption>`, `th scope` en los dos ejes y primera columna fija. **No pasa a modo tarjeta**: convertirla destruye la comparación. Nada de la rejilla baja de 12 px; el nombre se parte, no se corta con puntos suspensivos. El hueco vacío se escribe con texto para lector.
- **Lo no asignado tiene su fila.** Colgarlo de una persona le atribuye trabajo que no tiene.
- **Una visita que dura varias franjas marca cada franja que cubre**, sin fusionar filas. Si el alto del bloque sí lo fija la duración, manda la regla del alto que viene del dato.
- **Tabla con desplazamiento horizontal y cabecera fija:** `overflow-x:auto` anula el `position:sticky` contra la página; la caja se desplaza por dentro. Esto corrige también §6.11, que declara `.tabla-caja{overflow-x:auto}` y `thead th{position:sticky;top:0}` a la vez.
- **El calendario laborable es un dato**, no una clase del componente.
- La excepción de 10,5 px de §2.1 no alcanza a una agenda (ya lo decía C; se promueve).

---

## 8. Lo que no sé / sin datos

- **Efectividad real** de cualquiera de las cuatro: no hay prueba con coordinación (tiempo, errores de doble reserva). Todo lo anterior son proxies medidos.
- **Duración mínima real de una visita.** Con los datos del cliente (3–5 h) §13.9 nunca se activa. Con visitas de ≤60 min, sí.
- **Instaladores por ciudad y por día.** Decide si «el día cabe siempre» se sostiene.
- **Uso desde teléfono o tableta** por parte de coordinación.
- **Qué hace «Quincena»** (no tiene vista dibujada, L371) y cómo se compone la agenda con más de cuatro instaladores.
- **El «calendario de instalaciones» que cita §13.9**: no hay maqueta ni especificación en 2.15.0 más que el texto de la regla; no puedo compararlo con la agenda del cliente más allá de ella.
- **Tope de la barra de carga** (≈6 órdenes, no escrito): 4/6 y 5/6 son 66 % y 83 % y el ámbar aparece al pasar un umbral que ninguna pantalla rotula. No evaluado como cambio.
- **Datos de la maqueta que no cuadran** (la semana dibuja 9 visitas y el resumen dice 11; el lunes 24 del día tiene 3 y la semana 1). No afectan a la comparación; el cliente debería saberlo.
- **Que 12 px más nombres partidos** resulten aceptables al cliente frente a los 10,5 px actuales: es una decisión suya.
