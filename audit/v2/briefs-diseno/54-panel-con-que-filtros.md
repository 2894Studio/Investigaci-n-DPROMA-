# 54 · Panel «CON QUÉ FILTROS» de la bitácora de descargas

Pantalla: `54_bitacora_descargas.html` (Grupo B). Sistema de referencia: 2.15.0. Pregunta de la persona: «¿Estos filtros tienen sentido para el flujo?».

## Respuesta corta

1. **Sí tienen sentido, como registro.** El panel no es un conjunto de controles: es el rastro de lo que se aplicó en cada descarga. Es lo que dice la ficha y lo que hace la pantalla (0 elementos enfocables en las celdas, medido).
2. **Cumple su propósito de auditoría en lo esencial**: quién, qué reporte, con qué valores, en qué formato y cuándo. Dos debilidades, ninguna crítica: «plaza 2 de 5» no se puede leer solo, y la ausencia de marca de dato personal no está definida (§3.1).
3. **Sí mezcla dos cosas** bajo un rótulo: 9 filtros aplicados y 3 campos con dato personal entregado (L693, L700, L721).
4. **El color no es correcto según §1 y §1.3.** El ámbar es «falta algo, o vence pronto» y aquí no falta nada. No es un fallo crítico: el chip lleva texto y contrasta 5,25:1. Es una **causa raíz del sistema**: 2.15.0 no tiene patrón de «sensibilidad de un dato».
5. **Cambio mínimo** (§4): separar las dos cosas dentro de la misma celda, marcar el dato personal con forma y texto en vez de ámbar, y escribir los valores literales. Se queda en 6 columnas. Más una regla de sistema para la marca de sensibilidad (§7).

---

## 1. Diagnóstico de lo que hay

Evidencia: `grep -n` sobre `54_bitacora_descargas.html` y Playwright (`prototipos/54-medir-panel.cjs`, resultados en `prototipos/54-medidas.json`). Coincide con el auditor v2 (`audit/v2/raw/54_bitacora_descargas.json`, `v2-54bit-ambar-clasificacion`) y con las verificaciones de `verif-1.json`.

| Aspecto | Lo medido | Dónde |
|---|---|---|
| Qué es el panel | Columna «Con qué filtros» de una tabla de 6 columnas × 5 filas. **12 chips**: 9 filtros («marca todas», «corte 31 jul 2026», «plaza 2 de 5», «estado activos», «mes julio 2026», «estado cerradas», «semana 17 – 23 ago», «plaza Bajío», «plaza Querétaro») y 3 «incluye …» («razón social y RFC», «domicilio fiscal», «VIN y titular») | L687–L725 |
| ¿Es operable? | No. 0 elementos enfocables en las celdas de filtros (`tabbablesEnCeldas: 0`). Los chips son `<span>`. Lo único operable de la fila es «Ver el detalle» | medido |
| Color | `.f-chip.pers{border-color:var(--warn);background:var(--warn-bg);color:var(--warn-ink)}` en los 3 chips «incluye». Fuera de la tabla, `.schip.c-warn` pinta «41 con dato personal» y la nota dice «Los filtros en ámbar incluyen dato personal» | L652, L682, L730 |
| Cómo se sabe que es dato personal | **Solo por el ámbar y la leyenda.** El texto del chip dice «incluye domicilio fiscal»; no dice «dato personal» | L693–L721 |
| Tamaño y contraste | 12 px (suelo cumplido); texto de los chips 5,97:1 sobre `--surface-2`; chip ámbar 5,25:1 en claro y 7,14:1 en oscuro. **Borde ámbar 2,86:1 en claro** (<3:1) | medido |
| Lector de pantalla | La celda se anuncia seguida y sin separar: `cell "marca todas corte 31 jul 2026 incluye razón social y RFC"` | `ariaSnapshot` |
| Jerarquía | El chip ámbar es el objeto más saturado de la pantalla en ambos temas | `54-A--1440-{light,dark}.png` |
| Cabida | Columna de 322 px a 1440 y de 276 px a 1280; filas de 75–76 px las que envuelven. Tabla `min-width:1080px`: 36 px ocultos a 1280 y 120 a 1024, con primera columna anclada | L637, medido |
| Nota al pie | 95 caracteres, una sola frase con dos cláusulas (§8: ≤~140) | L730 |

---

## 2. Requisitos

### 2.1 FICHAS (`grep -n "54_bitacora" FICHAS_TECNICAS.md`: L1129; también L1590)

Literal, L1131 y L1135–L1140:

- «Quién descargó qué reporte, con qué filtros y cuándo. Sale de Legal.»
- «**Tabla** — 6 columnas × 5 filas, **se desliza con la primera columna anclada** (`D-6`): una auditoría se lee comparando filas.»
- «**Lo que decide** — Que **un renglón no se edita ni se borra**. Una bitácora que se puede corregir después no acredita nada, y ésta existe para acreditar. Los reportes no se almacenan: se construyen cada vez, así que este renglón es lo único que queda de una entrega.»

De aquí salen tres requisitos: el panel es **registro**, no control; el registro es **lo único que queda** de la entrega; y la tabla se queda en **6 columnas** con la primera anclada.

### 2.2 Sistema 2.15.0 (cada § verificado con `grep -n`)

- **§1** (L28–L48): «Antes de elegir un color, decide qué trabajo hace el dato». Si tiene juicio, semáforo (§1.3); si solo distingue, categórica (§1.4); «**Si es un dato sobre el dato** —de qué conjunto habla una cifra— **no lleva color propio: va en tinta de texto** (§6.22)». Y: «**Un color de estado no se reutiliza para una categoría, ni al revés.**»
- **§1.3** (L240): `--warn` = «Falta algo, o vence pronto».
- **§6.10** (L1147): `.pill` = estado; `.p-type` = clasificación «sin connotación de bueno ni malo», con series (§1.4). «Cuando haya que poner varias etiquetas seguidas, **se agrupan por significado y se separan visualmente** … y, si el sitio lo permite, un rótulo por grupo.»
- **§6.21** (L1760): la pastilla «nombra la dimensión y el valor —«Plaza: Celaya»—». «Las dimensiones sin juicio —plaza, responsable, trámite— van en texto plano; **ponerles color inventaría un significado que el dato no tiene**.»
- **§6.12, regla 4**: los filtros aplicados «se ven y se quitan uno a uno, como etiquetas con «×»». **No aplica a un filtro histórico**: aquí no se quita nada. 2.15.0 no tiene un chip histórico (la propuesta previa lo llamaba «§6.21.1», que no existe).
- **§6.22** (L1820): «cuatro avisos de que falta algo, cuando no faltaba nada. Cuatro avisos falsos por pantalla desgastan el aviso de verdad.» Es el mismo patrón: ámbar para algo que no es un aviso.
- **§1.7**: texto 4,5:1; elementos gráficos 3:1. **§2.1**: suelo de 12 px. **§8**: ≤~140 caracteres.
- **No existe** en 2.15.0 ningún patrón de «sensibilidad de un dato» (`grep -n -i "sensib\|dato personal\|datos personales" sistema-diseno.md`: 0 coincidencias).

### 2.3 Investigación

- La entrevista de Jurídico y RH (`data/insights/2026-07-28_juridico-recursos-humanos.json`) **no menciona descargas, filtros, exportaciones ni bitácora**: el único «descarga» es el formato de solicitud de viáticos (L251). Ningún otro documento de `data/insights/` lo hace (grep de `descarg|exporta|bitácora|dato personal|privacidad` sobre los 11 JSON). «Sale de Legal» **no tiene fuente verificable**.
- Lo más cercano: `pp-016` (media): uso de IA «sin política formal sobre qué datos incluir»; y `ai_adoption.barreras`: «nunca introduce datos reales del cliente en la IA». Es cautela con datos reales de clientes, no con descargas.
- `pp-012` y `op-011` (Jurídico): pérdida de «trazabilidad estructurada» en la negociación de cláusulas. Es trazabilidad de otro proceso.
- Conclusión: no puede afirmarse que el panel responda a una necesidad investigada. Lo que lo sostiene es la ficha del cliente.

---

## 3. Evaluación

### 3.1 ¿Cumple su propósito de auditoría? Reconstruir qué se descargó y con qué datos personales

Prueba por columna, sobre las 5 filas:

| Dato que una auditoría necesita | ¿Está? | Observación |
|---|---|---|
| Quién | Sí | Nombre y área («Dirección», «Facturación»…). Si el nombre o el área cambian después: sin datos de si se guarda una copia |
| Qué reporte | Sí | Nombre y ámbito («Todas las marcas», «Querétaro y Celaya») |
| Con qué filtros | **Casi** | 8 de 9 filtros son valores concretos. **«plaza 2 de 5» no dice cuáles**: los nombres solo están en el subtítulo de otra columna. En la fila 2 coincide («Querétaro y Celaya»); «marca todas» repite «Todas las marcas». El renglón «es lo único que queda de una entrega», así que cada chip debe poder leerse solo |
| Con qué datos personales | **Sí, si hay** | «incluye razón social y RFC» dice qué campos salieron. **Sin marca, la fila no dice «no incluye»**: puede ser ausencia real o ausencia de registro. Sin datos de si el servidor siempre calcula la marca |
| Cuándo | Sí | Fecha y hora (sin segundos ni zona; sin datos de si hacen falta) |
| En qué formato | Sí | Excel o PDF |
| Cuántas filas salieron, huella del archivo | No | La ficha no lo pide; no se propone |
| Detalle completo | Sin datos | «Ver el detalle» no está dibujado |

**Veredicto:** sí cumple en lo esencial. Las dos debilidades son de **contenido del dato** («2 de 5») y de **definición** (qué significa no tener marca); ninguna impide la tarea, así que no son críticas. «marca todas» es un valor que depende del momento (si mañana hay otra marca, «todas» designa un conjunto distinto): sin datos de si el servidor guarda el conjunto resuelto.

### 3.2 ¿Mezcla dos cosas?

**Sí.** Los filtros son parámetros con los que se consultó («plaza», «corte», «estado»). Los 3 «incluye…» son campos con dato personal que llevó el reporte. Comparten lista, cabecera («Con qué filtros»), forma y fila, y el lector de pantalla los lee seguidos. §6.10 pide agrupar por significado y separar visualmente.

Matiz que no puedo cerrar: si en el producto «incluir razón social y RFC» es una opción del reporte (parámetro) o un hecho derivado del reporte elegido. El flujo de construir un reporte («Ver reportes disponibles») no está dibujado: **sin datos**. En ambos casos conviene que el registro los separe, porque responden a preguntas distintas: «¿cómo lo pidió?» y «¿qué salió?».

### 3.3 ¿Es correcto el color según §1.3 y §6.10?

**No.** Aplicando el árbol de §1:

1. **¿Tiene juicio?** No. Entregar un reporte con dato personal puede estar permitido y completo. `--warn` es «falta algo»: aquí nada falta. Es el fallo que §6.22 ya describió para el ámbito.
2. **¿Solo distingue?** Tampoco del todo. `.p-type` (§6.10) es clasificación «sin connotación de bueno ni malo», y marcar dato personal sí pide atención. Además hay que inventar un mapeo serie ↔ categoría sin leyenda natural.
3. **¿Es un dato sobre el dato?** Sí: dice algo del contenido entregado, no del trabajo. §1: sin color propio, en tinta de texto.

Dos agravantes menores medidos: (a) **la clase «dato personal» solo la lleva el color y la leyenda**; el chip dice «incluye domicilio fiscal», no «dato personal»; la nota nombra la clase por el color («los filtros en ámbar»). (b) El borde ámbar da 2,86:1 sobre `--surface`, por debajo de 3:1 (§1.7), aunque el texto lo compensa.

**Gravedad:** media, no crítica (hay texto; 5,25:1). Decisión del auditor: `ajustar_sistema`. Estoy de acuerdo en que es causa raíz del sistema (falta el patrón) y en que el cliente reutilizó lo único a mano. La misma familia: «318 este mes» va con `c-ok` (verde y check) y es un conteo, no un juicio (L682); se corrige igual y se deja como observación.

### 3.4 ¿Es legible y está bien jerarquizado?

- **Legible:** sí. 12 px, 5,97:1 en el texto base de los chips, 5,25:1 en el ámbar.
- **Jerarquía de la celda:** la etiqueta tenue y el valor en negrita («plaza **Bajío**») sigue lo que pide §6.21. Es correcto.
- **Jerarquía de la pantalla:** el ámbar convierte «incluye…» en lo más llamativo de la tabla. La **intención** es acertada: para Legal, qué dato personal salió es lo que más importa. El **vehículo** es el equivocado: grita «aviso» en renglones sin nada pendiente.
- **Estrecho:** la columna de filtros pasa de 322 a 276 px y crece la altura de las filas; la tabla recorta 36 px a 1280 y 120 a 1024, con la primera columna anclada como pide `D-6`. A 390 pasa a tarjetas.

### 3.5 ¿Hay algún fallo crítico del panel?

**No.** Los dos críticos que el auditor midió en esta pantalla son del cromo, iguales en las demás pantallas, y se arreglan en la plantilla (`v2-54bit-buscador-16px`, `v2-54bit-menu-colapsado-sin-nombre`, ambos confirmados en `verif-1.json`). Para el buscador, la verificación señala que no incumple WCAG 2.5.8 (hueco de 18,5 px) y sí §7.3 y §10 trampa 4.

---

### 3.6 Opciones evaluadas

| Criterio | **O1 · Cliente tal cual** | **O2 · Cambio mínimo (recomendada)** | **O3 · Columna propia «Datos personales»** | **O4 · Marca con paleta categórica (`.p-type`)** |
|---|---|---|---|---|
| Qué cambia | Nada | Dos grupos dentro de la celda; marca neutra con icono y texto; valores literales; contador neutro; nota sin color | Pasa a 7 columnas | Marca con punto de serie |
| Cumple el propósito de auditoría | Sí, con la salvedad de «2 de 5» | Sí; **«plaza Querétaro y Celaya»** se lee solo | Sí; mejor para escanear «filas con dato personal» | Igual que O2 |
| Separa filtros y datos entregados | No | **Sí** (`<ul aria-label="Filtros aplicados">` + `<p>` aparte) | Sí | Sí |
| Color conforme a §1 | **No** (`--warn` para una clase) | **Sí** (ningún token de color; 0 usos de ámbar en la zona de contenido, antes 15) | Depende de cómo se marque | Parcial: categoría con connotación; mapeo arbitrario |
| Lector de pantalla | Run-on | Lista nombrada + párrafo | Celda propia | Run-on si no se agrupa |
| Contraste | Texto 5,25:1; borde 2,86:1 | Texto 15,21:1, borde 3,26:1 (claro); 13,93:1 y 3,41:1 (oscuro) | n/a | Sin medir |
| Densidad a 1440 | Filas 75–76/61 px (suma 334) | Filas 78–79/61 px (suma **358**, +7 %) | +1 columna: 1080 de `min-width` pasa a más; peor a 1280 | Igual que O2 |
| Esfuerzo | 0 | +15/−8 líneas en un archivo; 0 componentes nuevos; sin JS | Cambia estructura y anchos | Requiere decidir mapeo de series |
| Compatibilidad con FICHAS | Es lo documentado | **Respeta** 6 columnas y `D-6`; conserva «no se edita ni se borra» | **Contradice** «6 columnas × 5 filas» (L1135) | Respeta |
| Efectividad en tarea real | Sin datos | Sin datos | Sin datos | Sin datos |

O3 queda como opción futura si Legal necesita escanear por esta propiedad; hoy contradice la ficha y empeora el ancho. O4 se descarta por §1 (connotación) y porque no resuelve que la clase se diga con palabras.

---

## 4. Recomendación y especificación

**O2.** Dejar los chips como texto no interactivo (es lo pedido por la ficha). Cuatro cambios:

1. **Separar** dentro de la misma celda: lista de filtros aplicados y, debajo, la marca de dato personal. La cabecera «Con qué filtros» se mantiene: la marca es un rasgo de la fila, no un filtro.
2. **Marca neutra con forma y texto:** pastilla con icono de escudo, borde `--border-fuerte`, fondo `--surface`, tinta `--text`, y la clase dicha con palabras: «Dato personal: razón social y RFC». Sin `--warn`, sin series.
3. **Valores literales:** «plaza **Querétaro y Celaya**» en vez de «plaza 2 de 5».
4. **El contador «41 con dato personal» pasa a `c-neutro`** y la nota queda solo con lo que importa: «Un renglón de la bitácora no se edita ni se borra.» (50 caracteres). Su icono pasa de escudo a libro, para reservar el escudo a la marca.

### 4.1 Marcado

```html
<td data-et="Con qué filtros">
  <ul class="filtros" aria-label="Filtros aplicados">
    <li class="f-chip">marca <b>todas</b></li>
    <li class="f-chip">corte <b>31 jul 2026</b></li>
  </ul>
  <p class="sens">
    <svg class="ico ico-xs" aria-hidden="true"><use href="#i-shield"/></svg>
    <span>Dato personal: <b>razón social y RFC</b></span>
  </p>
</td>
```

Los chips siguen sin `tabindex`, `role` ni `aria-pressed`, y sin cursor de puntero (§6.12, regla 8). Las filas sin dato personal no llevan `<p class="sens">`; qué significa esa ausencia está en §8.

### 4.2 CSS (solo tokens)

```css
.filtros{list-style:none;margin:0;padding:0}
.sens{display:inline-flex;align-items:center;gap:5px;margin:var(--sp-2) 0 0;
  font-size:var(--fs-meta);line-height:1.4;
  background:var(--surface);border:1px solid var(--border-fuerte);
  border-radius:var(--r-ctrl);padding:2px 8px;color:var(--text)}
.sens .ico{color:var(--text-2)}
.sens b{font-weight:700}
```

`.f-chip.pers` deja de usarse y se retira.

### 4.3 Accesibilidad

- Lista con nombre «Filtros aplicados» y párrafo aparte; medido en el árbol de accesibilidad (`cell "Filtros aplicados Dato personal: razón social y RFC"`).
- La clase «dato personal» ya no depende del color ni de una leyenda.
- Contraste medido: texto de la marca 15,21:1 (claro) y 13,93:1 (oscuro); icono 6,84:1 y 7,80:1; borde 3,26:1 y 3,41:1 (≥3:1, §1.7).
- Sin destinos táctiles nuevos; no hay controles.

### 4.4 Por ancho

| Ancho | Qué pasa (medido) |
|---|---|
| 1440 | Filas 78, 79, 61, 61, 79 px (A: 75, 76, 61, 61, 61). Sin recorte de tabla |
| 1280 | Fila 2 sube a 106 px porque «plaza Querétaro y Celaya» envuelve; suma 396 frente a 360. Tabla con 36 px de desplazamiento, como antes |
| 1024 | Igual que 1280; 120 px de desplazamiento, primera columna anclada (`D-6`) |
| 390 | Modo tarjeta; suma 1782 px frente a 1573 (+13 %) porque la marca ocupa su propia línea |

Tema oscuro: los dos temas se midieron; la marca sigue siendo reconocible por forma y texto, no por color.

---

## 5. Prototipo medido

Copias de la maqueta del cliente; **la original no se tocó**. Se reconstruyen con `prototipos/54-construir-prototipos.py`.

| Archivo | Qué es |
|---|---|
| `prototipos/54-panel-con-que-filtros.html` | Pantalla con el cambio mínimo (O2) |
| `prototipos/54-marca-sensibilidad.html` | La marca en tres contextos (celda, contador, ficha), con «antes» y «después»; botón de tema |
| `prototipos/54-{A,propuesta}--{1440-light,1440-dark,390-light}.png` | Capturas de la tabla |
| `prototipos/54-marca-sensibilidad--{light,dark}.png` | Capturas de la marca |
| `prototipos/54-medir-panel.cjs`, `54-medidas.json` | Instrumento y resultados |

Resultados comparados (1440, claro):

| Medida | Cliente | O2 |
|---|---|---|
| Usos del ámbar en la zona de contenido | 15 (3 chips) | **0** |
| Tamaño mínimo de texto en la columna | 12 px | 12 px |
| Contraste mínimo de texto en la columna | 5,25:1 | 5,97:1 |
| Borde de la marca contra su entorno | 2,86:1 | 3,26:1 |
| Elementos enfocables en las celdas | 0 | 0 |
| Longitud de la nota | 95 | 50 |
| Anuncio de la celda | una sola cadena | lista nombrada + párrafo |
| Suma de altura de filas | 334 px | 358 px |

Comando: `cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node 54-medir-panel.cjs` (cliente en `127.0.0.1:8732`, prototipos con `python3 -m http.server 8764` dentro de `prototipos/`).

---

## 6. Veredicto de viabilidad

**`viable con condiciones`.**

- **Alcance:** dentro del sistema actual; 0 componentes nuevos; +15/−8 líneas en un archivo; sin JS.
- **Compatibilidad con decisiones del cliente, citadas literal:** conserva «6 columnas × 5 filas, se desliza con la primera columna anclada (`D-6`)» y «un renglón no se edita ni se borra». Cambia el vehículo de la marca (ámbar → forma y texto), no lo decidido.
- **Esfuerzo:** bajo para el cliente; la regla de sistema es nuestra.
- **Condiciones:**
  1. Que Legal confirme el término «dato personal» para razón social, RFC, domicilio fiscal, VIN y titular. Es el cliente quien lo usa («41 con dato personal»); no afirmo la clasificación legal.
  2. Que la marca **la publique el servidor** y no la infiera la pantalla (patrón que el cliente ya usa en otras pantallas, p. ej. el texto del estado vacío en `36_recetas_despacho`, FICHAS L399–L400: ««Completa» viene **derivado del servidor**» y «El texto del estado vacío **lo publica el servidor**»).
  3. Que se defina qué significa una fila sin marca (§8).
  4. Que el cliente acepte +24 px de altura de tabla (+7 %) a 1440.

---

## 7. Cómo se adopta

**El cliente cambia** (solo `54_bitacora_descargas.html`):

1. Sustituir `<span class="filtros">` por `<ul class="filtros" aria-label="Filtros aplicados">` con `<li class="f-chip">`.
2. Sacar los chips `.f-chip.pers` a `<p class="sens">…Dato personal: …</p>` bajo la lista.
3. Valores literales en los chips de conteo («plaza Querétaro y Celaya»).
4. `c-warn` → `c-neutro` en «41 con dato personal» (y `c-ok` → `c-neutro` en «318 este mes»).
5. Nota: «Un renglón de la bitácora no se edita ni se borra.»; icono de libro.

**Nosotros documentamos en el sistema**, en tono del sistema y sin número de § hasta ubicarlo:

> **Marca de sensibilidad de un dato.** Que un dato sea personal o reservado es un hecho sobre el dato, no un juicio sobre el trabajo: entregarlo puede estar permitido y completo. Por eso **no lleva color de estado ni de serie**. `--warn` es «falta algo» y las series no tienen connotación.
>
> - **Forma y texto.** Pastilla `.sens` con icono de escudo, borde `--border-fuerte`, fondo `--surface` y tinta `--text`. Dice la categoría con palabras: «Dato personal: razón social y RFC». La marca no necesita leyenda de color.
> - **Dónde.** Pegada al dato que califica, en su propia línea, nunca mezclada con filtros ni atributos de la misma celda. Si hay más de una, van agrupadas bajo la misma marca.
> - **Quién decide.** El servidor publica la marca; la pantalla no la infiere.
> - **Qué no significa.** No avisa de un problema. Si una acción sobre el dato no está permitida, eso se dice aparte, con semáforo y texto.
> - **El escudo se reserva** para esta marca.
> - **Contraste verificado:** texto 15,21:1 y 13,93:1; borde 3,26:1 y 3,41:1 (claro y oscuro).

Dos reglas más que salen de esta pantalla:

- **Lo que se registra se escribe literal.** Un registro inmutable guarda valores, no cuentas: «Querétaro y Celaya», no «2 de 5».
- **Un filtro histórico no es un filtro aplicado.** Va sin «×», sin `aria-pressed` y sin cursor de puntero; nombra dimensión y valor como en §6.21.

---

## 8. Lo que no sé / sin datos

- **Si Legal pidió este registro.** «Sale de Legal» no tiene fuente en `data/insights/`; ninguna entrevista habla de descargas.
- **Qué significa una fila sin marca.** ¿«No incluye» o «no registrado»? Depende de si el servidor siempre calcula la marca. Si la respuesta es «siempre», una fila sin marca ya dice «no incluye»; si no, habría que escribirlo.
- **Si «incluir razón social y RFC» es un parámetro del reporte o un hecho derivado.** «Ver reportes disponibles» no está dibujado.
- **Si el servidor guarda el conjunto resuelto de «todas las marcas»** (valor que cambia con el tiempo).
- **Si el nombre y el área de quien descargó se guardan como copia** o se leen del directorio actual.
- **Qué muestra «Ver el detalle»** (no está dibujado) y si completa los filtros resumidos.
- **Clasificación legal** de razón social, RFC, domicilio fiscal, VIN y titular como dato personal. Uso el término del cliente.
- **Si Legal escanea visualmente por esta marca** o usa el contador «41 con dato personal» como filtro; de eso depende que O3 valga la pena.
- **Efectividad en tarea real:** no hay prueba con Legal; todo son proxies medidos.
- **Lo que la pantalla no ofrece** y queda fuera del panel: ningún control para acotar la bitácora por periodo, persona o reporte (`v2-54bit-sin-filtros-de-periodo`, decisión del auditor «decidir_diseño»). La ficha no dice que no deba existir.
