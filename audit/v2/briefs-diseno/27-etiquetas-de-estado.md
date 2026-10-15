# Brief de diseño · Padrón de clientes (`27_padron_clientes`) · etiquetas de estado de la tabla

| | |
|---|---|
| **Pantalla** | `27_padron_clientes.html` (paquete `Actualizacion-12-10-26`, 931 líneas) |
| **Qué dijo la persona** | Hoja 3: los estados son «demasiado específicos» («Falta documento», «Incompleto»). *No es un rediseño marcado como crítico: es una evaluación.* |
| **Sistema de referencia** | `sistema-diseno.md` v2.15.0 (`L1154` = línea 1154 de ese archivo) |
| **Prototipos** | `prototipos/27-etiquetas-de-estado.html` (recomendado) · `prototipos/27-estados-opcion1-minimo.html` (opción 1) |
| **Veredicto** | **viable con condiciones** (§6) |
| **Recomendación en una línea** | La fila dice **un estado por eje** (expediente: *Completos · Pendientes · Sin calcular*; comercial: *Activo · Inactivo*); el documento que falta es una línea de ≤34 caracteres, no un estado; «Por vencer» no se dibuja hasta D7. |

La maqueta del cliente no se tocó: los prototipos son copias generadas con `prototipos/medicion/generar-27-estados*.py`.

---

## 1. Diagnóstico

### 1.1 Qué hay hoy

Una fila de la tabla lleva tres cosas con forma de estado, más un recuento: «Documentos fiscales» (expediente), «Comercial» (activo/inactivo) y «Sucursales» («Sin sucursales» cuando es 0). Encima de la tabla, cuatro chips de filtro.

| Dónde | Etiqueta | Variante | Línea de `27_padron_clientes.html` |
|---|---|---|---|
| Documentos fiscales | **Los dos** | `p-ok` | L777, L824 |
| | **Falta 1** | `p-warn` (reloj) | L800 |
| | **Por vencer** | `p-warn` (reloj) | L812 |
| | **Faltan los 2** | `p-err` | L836 |
| | **Sin calcular** | `p-neutro` (aviso) | L848 |
| Comercial | **Activo** / **Inactivo** | `p-ok` / `p-neutro` | L850 (Inactivo) |
| Chips (L730) | «42 sin los dos documentos» `c-err` · «7 con un documento por vencer» `c-warn` · «9 agencias sin órdenes en 90 días» `c-neutro` · «1,189 activos» `c-ok` | | L730 |

Cada etiqueta de «Documentos fiscales» arrastra una explicación en la misma celda, y tres notas al pie (L861, L863, L865) repiten parte de ella.

### 1.2 Qué dice la persona frente a lo que hay

- **Las etiquetas literales «Falta documento» e «Incompleto» no están en la pantalla.** `grep -n -i "falta documento" 27_padron_clientes.html`: sin resultados. «incompleto» aparece una sola vez, dentro de la prosa de «Sin calcular» (L848). Lo que sí hay son las cinco etiquetas de la tabla de arriba (verificado también por la auditoría: `audit/v2/raw/27_padron_clientes.json`, hoja 3).
- **Esas dos palabras sí están en nuestro propio sistema.** §6.10 `L1154`: «`.pill` = estado… vigente, **falta un documento**, inactivo» y §6.12 `L1315` (diagrama): «⏱ 42 **incompletos**». Puede que la persona esté reaccionando a un vocabulario que viene de aquí, no de DPROMA.
- **Interpretación que uso (la persona no lo precisó):** «demasiado específicos» = la fila nombra el *recuento y la causa* («Falta 1», «Faltan los 2», «Por vencer», más prosa) en vez del *estado*. Si quería otra cosa, p. ej. una sola columna de estado, la opción 3 de §3 lo cubre y está descartada por el dictamen 5.

### 1.3 Hallazgos (todos medidos o con línea)

| # | Hallazgo | Evidencia |
|---|---|---|
| H1 | **Granularidad por recuento, no por consecuencia.** «Falta 1» (ámbar) y «Faltan los 2» (rojo) tienen la **misma consecuencia**: no se puede programar. | L800: «no se le puede programar ni facturar»; L836: «programarle una instalación, no». El color codifica cuántos faltan, no qué se puede hacer. |
| H2 | **Prosa en la celda: 85 a 236 caracteres**, filas de 99 a 167 px a 1440 (115 a 200 a 1280). | `27e-original.json`. Contra §6.11 regla 7 `L1266` («una celda no lleva un párrafo») y §6.12 regla 9 `L1365` («la razón de un estado va al detalle, no a la celda»). La corrección de `verif-2.json` (`v2-27padron-06`) aplica: «Falta 1» son 139 caracteres y 5 líneas, no 7; las 7 líneas son «Sin calcular». |
| H3 | **«Por vencer» está dibujado y D7 lo pospone.** Además la prosa dice «Jurídico ya recibió el aviso de 30 días» (L812). | FICHAS L1252: «Vigencia de documentos («por vencer», 60/30/7 días) — se pospone… No hay columna de vigencia en `archivos`»; aviso L21; FICHAS L710–L711 («la `27` los dibuja, pero no entran en esta tanda»). |
| H4 | **El mismo dato se dice en cuatro sitios**: pill, prosa de la celda, chip y nota al pie. | «no se le puede programar ni facturar»: celda L800, nota L861, chip «42 sin los dos documentos» (L730). Dos chips replican etiquetas de fila con otras palabras. |
| H5 | **`Inactivo` usa `p-neutro`, no `p-pause`.** | L850. §1.3 `L240`: `--pause` = «Inactivo, en pausa — no es un fallo»; §6.10 `L1154` cita «inactivo» como estado. |
| H6 | **`.p-neutro` no existe en §6.10** (que define cinco variantes), y se usa para «Sin calcular» y «Sin sucursales». | `.p-neutro` en L456; §6.10 `L1156–L1164` (cinco variantes: `ok`, `warn`, `err`, `block`, `pause`). Es un estado real («no se pudo comprobar») sin variante documentada. |
| H7 | **Emoji ⛔ como icono dentro de la prosa de «Sin calcular».** | L848. §6.5 `L927` define los iconos del sistema (`.msi`); un emoji no es uno de ellos, y ⛔ dice «prohibido» donde el estado es «no se pudo comprobar» (§6.5 `L1000–L1001`: el significado de un icono «no cambia de contexto»). |
| H8 | **El sistema se contradice** sobre «falta un documento»: §1.3 `L242` dice «en espera de un documento (`warn`)»; la fila de la tabla de §1.3 dice `err` = «falta lo que impide operar». | La maqueta eligió `warn` para uno y `err` para dos. |

### 1.4 Causa raíz

(1) La pill y la celda mezclan **estado** (qué es) con **causa y consecuencia** (qué falta, qué no se puede hacer): lo segundo no cambia el estado y debería decirse una vez, fuera de la fila. (2) §1.3 deja sin resolver si «falta un documento» es `warn` o `err`, y no tiene variante neutra para «no se pudo comprobar». (3) Se dibujó un estado que depende de datos que no existen (D7).

---

## 2. Requisitos

| # | Requisito | Fuente |
|---|---|---|
| R1 | Una pill por eje; la etiqueta dice el estado; color + icono + texto, nunca color a secas | §6.10 `L1154–L1155`; FICHAS L690 (dictamen 5: estado partido en expediente y comercial) |
| R2 | Decir **qué documento falta**, no «incompletos» | FICHAS L691 (dictamen 6); y la acción masiva «Pedir por correo lo que falta» **depende** de ello (L696, dictamen 32) |
| R3 | «Sin calcular» **no** es «faltan»: sigue siendo un estado propio | FICHAS L1019–L1022 («un «incompleto» falso bloquearía una instalación que sí se podía programar») |
| R4 | No dibujar «Por vencer» ni su chip en esta tanda | FICHAS L1252 (D7); aviso de conformidad L21 |
| R5 | No añadir ningún estado de fila por duplicados | FICHAS L1253 (D8). Si D8 vuelve, es un atributo del par, no un estado del cliente |
| R6 | Color según el semáforo; `Inactivo` = `pause` | §1.3 `L240`; §1 `L43` (un color de estado no se reutiliza para una categoría) |
| R7 | Una celda no lleva un párrafo; la consecuencia común va una vez, a toggletip de la cabecera | §6.11 regla 7 `L1266`; §6.12 regla 9 `L1365`; §8 `L2034–L2035`; §6.23 |
| R8 | Los chips usan el vocabulario y el color de la pill que filtran | §6.12 regla 2 (un filtro, un sitio) |
| R9 | Contraste ≥4,5:1 y nada bajo 12 px en los dos temas | §1.7 `L421`, §2.1 `L487` |
| R10 | Los documentos son opcionales para dar de alta y obligatorios para programar o facturar | FICHAS L1016–L1017 |
| R11 | La completitud es de la razón social, no de la sucursal | FICHAS L1024 |
| R12 | Cada estado tiene un nombre y una consecuencia definidos una sola vez | `pp-116`, `pp-018` (abajo) |

**Investigación.** `pp-116` (`2026-09-10_administracion-finanzas.json`): se manejan estados de factura «sin una definición común ni un flujo documentado que diga quién los cambia, cuándo y con qué consecuencia» (es de facturas, no del padrón; lo uso como criterio de método). `pp-018` (`2026-07-28_juridico-recursos-humanos.json`): «ambigüedad terminológica entre áreas sobre conceptos operativos clave (ej. qué es el «padrón»)». `pp-044` y `pp-013` (`2026-07-23_comercial-administracion-vehicular.json`, `2026-07-28_juridico-recursos-humanos.json`): la documentación del cliente vive dispersa y sin «control automatizado de vigencias», que es lo que D7 pospone. `pp-097` (`2026-07-16_soporte-administrativo-transversal.json`): Instalaciones valida a mano el padrón antes de la visita: lo que decide la tarea es «¿se puede programar?». **Sin datos** de si comercial lee bien «Pendientes»: no hay prueba con usuarios.

---

## 3. Opciones evaluadas

Medidas en tema claro a 1440 (`27e-original.json`, `27e-opcion1.json`, `27e-prototipo.json`).

| Medida | Maqueta | **Opción 1** · mínimo | **Opción 2** · recomendada |
|---|---|---|---|
| Etiquetas de «Documentos fiscales» | 5 | 4 | **3** |
| Etiquetas distintas en las filas (con Comercial y «Sin sucursales») | 8 | 7 | **6** |
| Caracteres por celda de documentos | 85–236 | 7–12 | **9–44** |
| Alto de fila | 98,9–166,6 px | 58,8–75,6 | **58,8–75,6** |
| Alto de la tabla (6 filas) | 1008,7 px | 714 | **715** |
| Chips de filtro | 4 | 3 | **3** |
| Notas al pie | 3 (96·84·84 car.) | 3 | **1** (84 car.) |
| ¿Dice qué documento falta, de forma que se lea con teclado y táctil? | sí (prosa) | **no** (solo en `title`) | **sí** (una línea) |
| ¿El color codifica recuento o consecuencia? | recuento (ámbar/rojo) | recuento | **consecuencia** (un solo ámbar) |

**Opción 1 · mínimo cambio sobre lo del cliente.** Conserva las etiquetas del cliente, pasa la prosa de la celda a `title` (como hizo Studio el 8-sep: `padron-clientes.html` L929) y retira «Por vencer» y su chip (D7). Ventajas: cambio pequeño y seguro; filas de 59–76 px. Costes: «Falta 1» **no dice qué documento falta** (dictamen 6 queda sin cumplir a la vista); el `title` no se abre con teclado ni con el dedo; siguen cuatro etiquetas de expediente, dos colores para una misma consecuencia y tres notas.

**Opción 2 · recomendada.** Un estado por eje y una línea con lo que falta. Detalle en §4. Ventajas: cumple R1–R12; reduce las etiquetas de expediente de 5 a 3; la causa que pide el dictamen 6 sigue visible pero como dato, no como estado. Costes: cambia palabras que el cliente dibujó («Los dos», «Falta 1», «Faltan los 2» → «Completos», «Pendientes») y exige el toggletip (componente nuevo para el cliente).

**Opción 3 · una sola columna «Estado» que fusione expediente y comercial.** *No prototipada.* Descartada: el dictamen 5 (FICHAS L690) parte el estado en expediente y comercial porque un cliente puede estar activo comercialmente y con documentos pendientes; fusionarlos esconde justo la combinación que importa («a quién le falta papel»).

**Opción 4 · solo la etiqueta, sin línea de «qué falta».** *No prototipada.* Descartada: incumple el dictamen 6 y deja a «Pedir por correo lo que falta» (dictamen 32) sin un dato visible en el que apoyarse.

---

## 4. Recomendación y especificación (Opción 2)

### 4.1 Qué estados muestra una fila

| Eje | Estado | Semáforo (§1.3) | Icono | Línea inferior (≤40 car.) | Origen |
|---|---|---|---|---|---|
| Expediente | **Completos** | `ok` | `#i-check` | — | dictamen 5; FICHAS L1016 |
| | **Pendientes** | `warn` | `#i-clock` («en espera de un documento», §1.3 `L242`) | «Falta **constancia**» · «Falta **identificación**» · «Faltan **constancia** e **identificación**» (34 car. máx.) | dictamen 6 (L691); sustituye «Falta 1» y «Faltan los 2» |
| | **Sin calcular** | neutro (no es juicio) | `#i-alert` | «No se pudo comprobar» (20 car.) | FICHAS L1019–L1022 |
| | *(no se dibuja)* «Por vencer» | `warn` | `#i-clock` | — | **D7** (L1252). Cuando exista vigencia vuelve **con la misma variante** `warn`: no necesita una etiqueta nueva de color |
| Comercial | **Activo** | `ok` | `#i-check` | — | dictamen 5 |
| | **Inactivo** | `pause` (antes `neutro`) | `#i-pause` | — | §1.3 `L240` |
| Sucursales | «Sin sucursales» | se queda como el cliente la dibujó | — | — | D2 (L1247); es un recuento en cero, no un estado |

**Por qué `warn` y no `err` para «Pendientes».** §1.3 `L242` dice literalmente «en espera de un documento (`warn`)», y la propia celda del cliente aclara que el cliente «se puede seguir trabajando» (L800) y «existe y se puede editar» (L836): lo que falta impide **programar y facturar**, no operar el padrón. Con una sola variante desaparece la distinción rojo/ámbar entre «uno» y «dos» documentos, que no cambia lo que la persona puede hacer. El `err` queda libre para lo que sí impide operar en esta pantalla.

**Por qué «Pendientes» y no «Incompletos».** La persona citó «Incompleto» como demasiado específico, y FICHAS L1019–L1022 trata «incompleto» como una afirmación de bloqueo que no se debe emitir si no se pudo calcular. «Pendientes», bajo la cabecera «Documentos fiscales», dice que se espera algo sin afirmar el bloqueo. **El texto exacto es una decisión de DPROMA** (§8).

### 4.2 Marcado (solo cambia el contenido de la celda y de la cabecera)

```html
<td data-et="Documentos fiscales"><span class="exp">
  <span class="pill p-warn"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-clock"/></svg>Pendientes</span>
  <span class="falta">Faltan <b>constancia</b> e <b>identificación</b></span></span></td>
…
<th scope="col"><span class="thx">Documentos fiscales
  <button class="infob" type="button" aria-expanded="false" aria-controls="tip-docs" aria-describedby="tip-docs"
          aria-label="Más información sobre documentos fiscales"><svg class="ico ico-xs" aria-hidden="true"><use href="#i-info"/></svg></button>
  <span class="tip" id="tip-docs" role="tooltip" hidden>Opcionales para dar de alta, obligatorios para programar o facturar. «Sin calcular» significa que no se pudo comprobar, no que falten.</span></span></th>
```

Chips: «**N** con documentos pendientes» (`c-warn`, `#i-clock`) sustituye a «42 sin los dos documentos» (`c-err`); «7 con un documento por vencer» sale (D7). `Inactivo` pasa de `p-neutro` a `p-pause`.

### 4.3 CSS

No hay CSS nuevo para las etiquetas: `.pill`, `.p-ok`, `.p-warn`, `.p-pause`, `.p-neutro` y `.exp .falta` (12 px, `--text-2`) ya están en el archivo. Solo el toggletip de §6.23 (`.infob`, `.tip` a `var(--fs-meta)`) y `.thx{display:inline-flex;align-items:center;gap:var(--sp-1);white-space:normal}`. `white-space:normal` importa: con la cabecera en una línea, el botón ⓘ ensancha la tabla 28 px y a 1280 aumenta el desplazamiento horizontal; con `normal` la tabla mide 1058 px frente a 1095 de la maqueta.

### 4.4 Estados de la pantalla

Con datos: arriba. Vacío («Ningún cliente coincide con los filtros»): su texto nombra el chip «agencias sin órdenes en 90 días», que se queda. Cargando y error: sin cambio. **Estado de fila no calculable:** «Sin calcular» es la forma de decir «no hay dato» y no hereda el color de «Pendientes».

### 4.5 Accesibilidad

La pill no depende del color (icono + texto). En la celda, la etiqueta se anuncia bajo la cabecera «Documentos fiscales» y la línea inferior es texto normal (no `title`). Toggletip: `aria-expanded`, `aria-controls`, `aria-describedby` siempre puestos; 24×24; Escape cierra y devuelve el foco; clic fuera y tabular a otro control cierran. **En modo tarjeta (<860 px) la cabecera no se ve** y con ella el toggletip: la línea «No se pudo comprobar» cubre «Sin calcular», pero «obligatorios para programar o facturar» no se muestra en móvil (§8).

### 4.6 Comportamiento por ancho

| Ancho | Resultado |
|---|---|
| 1440 | Filas de 58,8–75,6 px; sin desplazamiento horizontal |
| 1280 y 1024 | Filas 58,8–82,6 px («Faltan constancia e identificación» pasa a dos líneas); la cabecera «Documentos fiscales» pasa a dos líneas (46,5 px); la tabla se desliza 14 px a 1280 (antes 51) |
| 390 | Modo tarjeta: filas de 317–337 px frente a 361–432; la celda muestra pill y línea con su rótulo `data-et` |
| 861–1200 | Medido: ninguna celda de documentos recortada (`medicion/intermedios.json`) |

### 4.7 Textos

«Completos» · «Pendientes» · «Sin calcular» · «Activo» · «Inactivo» · líneas de ≤34 caracteres · toggletip de 134 caracteres · chip «N con documentos pendientes». Ninguno pasa de 140.

---

## 5. Prototipo medido

**Archivos.** `prototipos/27-etiquetas-de-estado.html` (49 líneas distintas respecto a la maqueta) · `…/27-estados-opcion1-minimo.html` · `prototipos/medicion/` (`generar-27-estados.py`, `generar-27-estados-min.py`, `medir-27e.cjs`, `medir-lib.cjs`, `intermedios.cjs`, `tokens-huerfanos.py`, JSON) · capturas `prototipos/capturas/27e-tabla-{original,opcion1,prototipo}--{1440,1280,1024,390}.png`. Tokens: 0 sin declarar, 0 hex fuera de `:root`. El «42» del chip es el de la maqueta: **no es el conteo de «pendientes»** (§8).

```
cd audit/v2/briefs-diseno/prototipos && python3 -m http.server 8740 --bind 127.0.0.1 &
NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medicion/medir-27e.cjs http://127.0.0.1:8740/27-etiquetas-de-estado.html prototipo salida.json
```

| Criterio | Maqueta | Prototipo |
|---|---|---|
| Contraste de las pills de la fila (claro) | mín. 5,02 (`err`); `ok` 5,04; `warn` 5,25; neutro 5,97 | **ok 5,04 · warn 5,25 · neutro 5,97 · pause 6,30** |
| Contraste (oscuro) | mín. 4,59 (`err`) | **ok 5,67 · warn 7,14 · neutro 7,10 · pause 5,25** (coinciden con la tabla de §1.3, `L271–L275`) |
| Contraste de chips (claro / oscuro) | 5,78 / 5,54 | **5,78 / 7,28** |
| Toggletip: contraste del globo · icono ⓘ · abre · Escape + foco · cabe en el viewport | — | **15,21 / 13,93 · 5,65 / 5,53 · sí · sí · sí** |
| Texto <12 px en la tabla y en los chips | 0 | **0** |
| Destinos <24 px en la tabla | 9 | **9** (siete casillas de 15×15 y dos botones de orden de 21 px: `v2-27padron-01`, previos; ⓘ mide 24×24) |
| Celdas de documentos recortadas | 0 | **0** |
| Scroll horizontal del documento | no | **no** |
| Solapes (pill/línea, chips, celdas de la fila) | 0 | **0** en los 4 anchos |
| Alto de fila / de tabla (1440) | 98,9–166,6 / 1008,7 | **58,8–75,6 / 715** |

`capturas/27e-tabla-prototipo--1440.png` frente a `27e-tabla-original--1440.png`.

---

## 6. Veredicto de viabilidad: **viable con condiciones**

- **Alcance en el sistema actual.** Las etiquetas usan variantes que ya existen (`p-ok`, `p-warn`, `p-pause`, `p-neutro`) y la línea inferior ya tiene su clase (`.exp .falta`). El único componente que el cliente no tiene en ninguna maqueta es el toggletip.
- **Esfuerzo.** Cambia 6 celdas, 1 cabecera, 2 chips, 2 notas y 1 clase; 49 líneas de diferencia.
- **Compatibilidad con DPROMA.** Respeta D7 (no dibuja «Por vencer» ni su chip), D8 (no añade estado por duplicados), D2, el dictamen 5 (dos ejes), el 6 (dice qué falta) y FICHAS L1019 («sin calcular no es faltan»). No toca D6 en esta pantalla (la 27 ya no dibuja la liga).

**Condiciones:**
1. **DPROMA confirma el vocabulario** («Completos / Pendientes» en lugar de «Los dos / Falta 1 / Faltan los 2»): son palabras de su maqueta y del dictamen. La persona debe precisar qué le parecía «demasiado específico» (§1.2).
2. **Recalcular el conteo del chip** («con documentos pendientes» ≠ «sin los dos documentos»): sin datos.
3. **Aceptar el toggletip** como componente nuevo, o quedarse con la opción 1 (con sus costes de §3).

---

## 7. Cómo se adopta

### 7.1 Qué cambiaría el cliente

1. Seis celdas de «Documentos fiscales» (L777, L800, L812, L824, L836, L848): pill + línea según §4.1; «Por vencer» pasa a «Completos».
2. `Inactivo` (L850): `p-neutro` → `p-pause`.
3. Chips (L730): sustituir el primero por «con documentos pendientes» (`c-warn`) y quitar «con un documento por vencer».
4. Quitar las notas de L861 y L863 (su contenido vive en el toggletip).
   **Hasta aquí es la opción 1 si, en lugar de la línea, se usa `title`.**
5. Cabecera con toggletip: `.infob`/`.tip`, símbolo `i-info`, ~20 líneas de JS (el mismo bloque del brief de Tickets).

### 7.2 Qué documentaríamos nosotros (reglas en el tono del sistema; sin número de §)

- **En «Etiqueta de estado» (§6.10):** *Una fila muestra un estado por eje, no uno por causa. El documento que falta es un dato —una línea de 40 caracteres como máximo bajo la etiqueta—, no un estado nuevo. «Falta un documento» y «falta otro» son el mismo estado.* Y: *Un estado que depende de un dato que el producto aún no calcula no se dibuja (hoy: la vigencia).*
- **En la misma §6.10, variante nueva:** *`.p-neutro` = «sin dato», no «bueno» ni «malo»: «Sin calcular», «Sin sucursales». Se mide como el resto (5,97:1 en claro, 7,10:1 en oscuro).*
- **En «Semáforo» (§1.3):** aclarar la contradicción de H8: *«en espera de un documento» es `warn` mientras se pueda seguir trabajando el registro; `err` se reserva para lo que impide operar en la pantalla donde se muestra.*
- **En «Resumen de estatus y barra de filtros» (§6.12):** cambiar el ejemplo del diagrama («42 incompletos», `L1315`) por una palabra que no afirme bloqueo, y añadir: *El chip dice lo mismo que la pill que filtra, con su color.*
- **En §6.14 (`L1435`):** quitar «Reenviar liga de registro» del menú de ejemplo (D6, FICHAS L1251).
- **En «Toggletip» (§6.23):** `.tip` a `var(--fs-meta)` (hoy 11,5 px, contra §2.1) e `i-info` en el sprite.

---

## 8. Lo que no sé / sin datos

- **A qué se refería la persona con «demasiado específicos».** Las dos etiquetas que citó no están en la pantalla (§1.2). Mi interpretación puede estar equivocada.
- **Si el listado real puede decir qué documento falta por fila.** FICHAS L696 sugiere que sí (la acción masiva depende de ello); no he leído `completitud-fiscal.ts`, así que no sé qué forma tiene lo que devuelve el servidor.
- **El texto «Pendientes»**: ni DPROMA ni la investigación lo han validado; no hay prueba de lectura con comercial.
- **El conteo del chip nuevo.** El «42» de la maqueta cuenta «sin los dos»; no sé cuántos tienen solo uno.
- **Modo tarjeta (<860 px):** sin cabecera no hay toggletip. No sé cuánto se usa el padrón en móvil.
- **Qué hace D7 cuando vuelva:** supongo `warn` sin etiqueta nueva; no está decidido.
- **Lector de pantalla:** verificado en atributos y comportamiento del DOM, no con NVDA/VoiceOver.
- **Modo oscuro:** medido en contraste; capturas solo en claro.
- **Rendimiento:** no evaluado.
