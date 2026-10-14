# Auditoría v2 · SIO-DPROMA · paquete «Actualización 12-oct-2026»

**Estudio:** 2894 Studio · **Fecha de la auditoría:** 14-oct-2026 · **Sistema de diseño de referencia:** v2.15.0 · **Solo auditoría:** ningún archivo del cliente se modificó (SHA-256 en `MANIFIESTO.json`).

## 1 · Resumen ejecutivo

1. **Alcance.** Se audita lo que contiene el ZIP: 50 pantallas. El listado de pantallas del PDF del cliente no se usa como criterio. Sí se contrastó, a modo informativo, lo que el PDF declara contra los archivos (Anexo A): 40 de sus 50 pantallas están en el ZIP y en 19 de ellas no se ven los cambios declarados.
2. **Qué se auditó.** 50 pantallas en el ZIP: **23** a fondo (observaciones, F1, F3; F4 y F5 en las de nivel A), con instrumentos medidos y fixtures validados; las otras 27 solo con regresión mecánica. 6 son idénticas a v1.
3. **Calidad de la propia auditoría.** 119 afirmaciones altas o críticas pasaron por verificadores que intentaron refutarlas con medición propia: **110 confirmadas, 9 exageradas, 0 refutadas** (precisión 92.4 %). Una réplica ciega de 2 pantallas **no** alcanzó el umbral de concordancia que nos fijamos (§8): una sola pasada no agota lo que hay.
4. **Lo que sí está medido, en una línea cada uno.**
    - El icono gris sobre «Reintentar» (obs. 1) tiene causa raíz: `.state .ico` descendiente. El arreglo es `.state > .ico`; el cliente lo declara y no lo aplicó en 6 hallazgos críticos de estas pantallas.
    - El menú lateral colapsado sigue sin nombre accesible en 19 pantallas auditadas (existía en v1).
    - La hipótesis de que `--sp-5` explica los problemas de espaciado se **refuta** para Mi día (obs. 13): la causa es `.p4-t` con `padding-bottom:0` (§3.1). Para Acceso (51) explica los huecos de 0 px entre bloques, no el interlineado.
    - Las «cajas contra la línea inferior» (obs. 10) son sistémicas: la plantilla de cabecera `.p4` no tiene relleno inferior y se copió en decenas de archivos.
    - El panel «CON QUÉ FILTROS» (obs. 18) es, según la FICHA del cliente, un **registro de auditoría**, no controles: el defecto es de color y de mezcla de conceptos, no de operabilidad.
5. **Rediseños críticos** (Tickets TI, acordeón de sucursales, Asistente, Mi día): diagnóstico y brief con veredicto de viabilidad en §7.
6. **Lo que se le pide al cliente** se limita a críticos y regresiones (§5); el resto se adopta y se documenta en nuestro sistema (§6).

## 2 · Qué contiene el ZIP

El ZIP trae 50 pantallas HTML (más `_sio-tokens.css`, `FICHAS_TECNICAS.md` y el aviso del padrón). Frente a v1: **6 idénticas** (10_dprimi_asistente, 11_app_login_2fa_offline, 12_app_checado_asistencia, 13_panel_asistencia_rhl, 14_app_checado_oficina, 56_frontera_error), **8 nuevas** (02_dashboard, 03_kanban_gestoria, 04_app_personal, 05_app_cliente, 06_padron_clientes, 07_orden_instalacion, 38_vehicular_detalle, 48_asistencia_rhl) y 36 modificadas. De las 52 de v1, 10 no están en este ZIP (31_orden_detalle, 49_alta_orden, 52_vehicular_bandeja, 53_tramite_detalle, facturacion, viaticos-adeudos-nomina, viaticos-alta-solicitud, viaticos-discrepancia-cfdi, viaticos-reembolso, viaticos-remanente); sus observaciones (4 y 15, `49_alta_orden`) quedan sin datos.

Auditoría a fondo: 23 pantallas. Solo regresión mecánica: 27.

## 3 · Regresión mecánica v1 → v2 (mismo arnés, mismas fuentes)

Se midieron las 36 pantallas modificadas comunes a v1 y v2 con los instrumentos de v1 (v1 se re-midió con el mismo arnés para que la diferencia sea honesta).

| Indicador | v1 | v2 |
|---|---:|---:|
| Destinos < 24 px | 114 | 101 |
| Fallos de contraste (claro) | 12 | 9 |
| Fallos de contraste (oscuro) | 2 | 2 |
| Enlaces de menú sin nombre a 1000 px | 465 | 480 |
| Tokens usados sin declarar | 10 | 9 |

Instrumentos nuevos (42 pantallas comunes). **Son candidatos, no veredictos:** los auditores encontraron falsos positivos (I3 e I7) y errores míos que se corrigieron (I6, I9, capturas, C1 en línea).

| Instrumento | v1 | v2 |
|---|---:|---:|
| I1 icono vs relleno del botón | 80 | 47 |
| I2 barras sin holgura inferior | 26 | 26 |
| I6 familias de color (suma por pantalla) | 137 | 139 |
| I8 grupos de botones dispares | 5 | 5 |
| I9 celdas largas | 22 | 23 |
| C2 10,5 px sin mayúsculas | 260 | 208 |
| C11 textos de más de 140 caracteres | 60 | 25 |
| `--sp-5` sin declarar: elementos afectados | 67 | 67 |

**Regresiones confirmadas por auditor (7):** `22_gestoria` (§7.2 Cromo de aplicación); `22_gestoria` (§13.3 Un contenedor no cede el ancho a un descen); `24_tickets` (§1.7 Regla de contraste); `24_tickets` (§6.4 Vistas de estado); `26_estados_de_pantalla` (FICHAS_TECNICAS.md del cliente · «Defectos reale); `51_acceso` (§6.4 regla 2 «Cada estado lleva un encabezado re); `58_altas_como_modal` (§6.4 regla 2).

## 4 · Tus 19 observaciones, una por una

Veredicto = lo que se **reprodujo** con evidencia en el archivo recibido. Ojo: los auditores conocían cada observación, así que esta tabla mide si se puede **verificar** lo que viste, no si lo habrían descubierto solos (§8).

| Hoja | Pantalla | Veredicto | Causa raíz | Cambio | Crítico | Decisión |
|---:|---|---|---|---|:-:|---|
| 1 | `22_gestoria` | confirmada | Regla de contexto descendiente `.state .ico{...color:var(--text-3)}` (línea 609) en lugar del hijo directo `.state > .ico`: el icono pequeño del `.btn.p` hereda el gris del icono grande del estado. Es el defect | sencillo | sí (criterio 1) | exigir_cambio |
| 1 | `26_estados_de_pantalla` | confirmada | Selectores descendientes en ARQ-ESTADOS: `.state .ico` (linea 609) y, en la propia muestra del catalogo, `.esp .ico` (linea 654), que apuntan a todo `.ico` del bloque y no solo al grande que cuelga directo del  | sencillo | sí (criterio 1) | exigir_cambio |
| 1 | `32_cfe_bandeja` | confirmada | Regla de contexto descendiente `.state .ico{...color:var(--text-3)}` (línea 609) en lugar del hijo directo `.state > .ico`: el icono pequeño del `.btn.p` hereda el gris del icono grande del estado. Es el defect | sencillo | sí (criterio 1) | exigir_cambio |
| 2 | `05_app_cliente` | confirmada | No es una regla distinta: ambos botones son `.abtn` con el mismo CSS (`display:inline-flex;gap:6px;justify-content:center;text-align:center`, línea 246-249). La diferencia es que el texto de «Contactar a DPROMA | sencillo | no | decidir_diseño |
| 3 | `27_padron_clientes` | parcial | Tres causas distintas. (A) Producto + forma: las decisiones del dictamen (partir expediente y comercial, «decir qué documento falta, no «incompletos»», vigencia, FICHAS 27) están bien; lo que sobra es la prosa  | medio | no | ajustar_sistema |
| 4 | `49_alta_orden` | **sin datos v2** | La pantalla no viene en el ZIP (el PDF dice que se actualizó) | — | — | pedir el archivo |
| 5 | `13_panel_asistencia_rhl` | confirmada | No es el valor de line-height ni la escala --sp-*: es la regla `.inc .body span` (línea 181), un selector descendiente de elemento (`span`) que se filtra en dos sitios: la fila de acciones `.acts` (que es un <s | sencillo | no | ajustar_sistema |
| 5 | `48_asistencia_rhl` | parcial | Tres causas, de más a menos general. (1) El sistema 2.15.0 no define ningún interlineado: solo hay `line-height` dentro de cinco reglas de componente (1,4 `.cifras .apoyo`, 1,5 `.paso-txt`/`.note`/`.ayuda`, 1,5 | sencillo | no | ajustar_sistema |
| 6 | `20_tablero` | parcial | (1) `.sem` es una columna flex cuyo rótulo `.et` existe solo en 2 de 12 columnas: el rótulo ocupa 15 px en esas dos y 0 en las otras, y `justify-content:flex-end` baja cada pila hasta su propio rótulo, de modo  | medio | no | decidir_diseño |
| 7 | `21_ficha_cliente` | confirmada | El botón de edición ocupa una fila propia (.fiscal-acc) con justify-content:flex-end y 16 px de margen: eso añade 52 px a una tarjeta cuyo contenido real son 31,5 px, y lo coloca lejos del rótulo que lo explica | sencillo | no | decidir_diseño |
| 8 | `23_viaticos` | confirmada | La celda «Monto y excedente» mezcla dato (`.montos`, 3 líneas) y explicación (`.justifica`/`.sin-just`, prosa de 51 a 112 caracteres) sin que haya un sitio para el matiz: §6.11 regla 7 lo manda a «etiqueta emer | medio | no | decidir_diseño |
| 9 | `24_tickets` | confirmada | Tres causas apiladas. (1) Geométrica: el selector .detalle .banda (línea 560) pone margen lateral y superior a CUALQUIER .banda dentro de .detalle, y la banda de esta pantalla vive dentro de .det-cuerpo, que ya | rediseño | sí (criterio 5) | decidir_diseño |
| 10 | `24_tickets` | confirmada | El bloque ARQ-P4 copiado en 36 archivos define .p4 sin padding-bottom y deja el cierre inferior a la última fila hija (.p4-f). Cuando la cabecera solo lleva .p4-t (título + acciones) no hay quien cierre. Es exa | sencillo | no | ajustar_sistema |
| 11 | `25_consumo_de_material` | parcial | El contrato no tiene color para tres cosas que la pantalla necesita: «derivado» (clasificación), el color físico de un material y «total» (énfasis). El autor las resolvió con el semáforo, que es lo único que ha | sencillo | no | ajustar_sistema |
| 12 | `27_padron_clientes` | confirmada | No es un solo defecto sino la suma de cinco: (1) falta el comportamiento (ningún manejador) y el HTML solo trae un panel con id real, así que 4 de 5 controles apuntan al vacío; (2) el contenido del panel vive e | rediseño | sí (criterio 5) | decidir_diseño |
| 13 | `28_instalador_mi_dia` | confirmada | Relleno inferior repartido entre filas opcionales (§3.1): .p4-t lleva padding-bottom:0 esperando que .p4-b/.p4-f cierren el bloque, y en Mi día no existen. NO es --sp-5 (hipotesis verificada y refutada: afecta  | sencillo | sí (criterio 5) | exigir_cambio |
| 14 | `34_instaladores` | respondida en el brief | La agenda del sistema no existe en 2.15.0 (no hay §6.24; §13.9 solo regula alto por dato). No cambiar la del cliente; cambio mínimo en texto, «Sin asignar» y domingo a 1280. | medio | no | adoptar_cliente (con cambio mínimo) |
| 15 | `49_alta_orden` | **sin datos v2** | La pantalla no viene en el ZIP (el PDF dice que se actualizó) | — | — | pedir el archivo |
| 16 | `46_cuentas_por_cobrar` | confirmada | Tres factores encadenados: (a) `.minis` omite `align-items:start`, el valor por omisión que fija §13.4 (la propuesta lo tiene en su línea 674); (b) `.kpis` está en dos columnas con el hero en la primera, de mod | medio | no | decidir_diseño |
| 17 | `47_asistente` | parcial | (a) Solape: margen superior negativo en .fuentes (linea 669) dentro de una tarjeta que lleva su relleno en el contenedor (.tx, linea 666) y no en filas hermanas: §3.1. (b) Dos tonos: el componente «respuesta» m | rediseño | sí (criterio 5) | exigir_cambio |
| 18 | `54_bitacora_descargas` | parcial | El panel cumple su función de registro (FICHA) y no debe ser operable. Los dos problemas reales son de sistema y de composición: (1) el sistema no tiene un patrón para marcar sensibilidad del dato —§1.3 es para | sencillo | no | ajustar_sistema |
| 19 | `55_verificacion_pedido` | confirmada | `.ren.siguiente::before` se coloca con `position:absolute` sin `top`/`bottom`: su posición estática la decide el `align-items:center` del botón (centro vertical de la tarjeta), y un `translateY(-32px)` fijo, ca | sencillo | no | adoptar_cliente |

Observaciones 0 son de la lista de «revisión exhaustiva» (Acceso, Altas como modal).

## 5 · Lo que se le pide al cliente: solo críticos y regresiones

Criterios de «crítico» (acordados): (1) fallo de accesibilidad medido, (2) impide la tarea u oculta la acción primaria, (3) acción irreversible o de dinero sin protección, (4) contradice una decisión de DPROMA o expone datos personales, (5) rediseño marcado y viable. Todo lo demás se adopta.

### 5.1 Arreglos transversales (una sustitución cierra muchos)

| Tema | Hallazgos críticos | Pantallas | Arreglo |
|---|---:|---|---|
| Menú lateral colapsado (861–1100 px) sin nombre accesible | 19 | 20_tablero, 21_ficha_cliente, 22_gestoria, 23_viaticos, 24_tickets, 25_consumo_de_material, 26_estados_de_pantalla, 27_padron_clientes, 28_instalador_mi_dia, 32_cfe_bandeja, 34_instaladores, 41_alta_cliente, 46_cuentas_por_cobrar, 47_asistente, 48_asistencia_rhl, 54_bitacora_descargas, 55_verificacion_pedido, 58_altas_como_modal, 59_editar_cliente | `.side .et{display:none}` deja 15 enlaces sin texto ni `aria-label`. Cambiar a ocultación visual (la técnica de `.sr`) o añadir `aria-label` a cada `.it`: §7.2 pide que la etiqueta no desaparezca. |
| Icono gris sobre botón verde en vistas de estado (obs. 1) | 6 | 22_gestoria, 24_tickets, 26_estados_de_pantalla, 32_cfe_bandeja, 51_acceso, 58_altas_como_modal | Cambiar `.state .ico` por `.state > .ico` (y `.esp > .ico` en el catálogo). El cliente ya lo declara como C3; en estos archivos no está aplicado. Verificado con contraste: 1,03:1 → 4,89:1. |
| Valor obsoleto de `--text-3` (4,21:1 sobre `--surface-2`) | 4 | 13_panel_asistencia_rhl, 24_tickets, 26_estados_de_pantalla, 34_instaladores | `--text-3: #5C6675` (el cliente ya lo declara en su tabla de tokens; en estos archivos no está aplicado o se revirtió). |
| Google Fonts por `<link>` (D116 las retira) | 1 | 01_login | Sustituir el `<link>` por `@font-face` autoalojado. El cliente lo declara como C8/C9; en `01_login` no está aplicado. |
| Identificadores duplicados en formularios (campos sin nombre accesible) | 2 | 58_altas_como_modal, 59_editar_cliente | Renumerar los `id` y sus `for`/`aria-controls` (§11: todos los `id` únicos). |

**Divergencia sencilla, no se exige como crítica (13 hallazgos que los auditores marcaron críticos):** Destinos de pulsación menores de 24 px (buscador, folio, migas, enlaces). Pantallas: 01_login, 21_ficha_cliente, 22_gestoria, 23_viaticos, 24_tickets, 27_padron_clientes, 32_cfe_bandeja, 34_instaladores, 47_asistente, 48_asistencia_rhl, 54_bitacora_descargas, 58_altas_como_modal. Dar `min-height:24px` (y relleno) al `input` del buscador y a los enlaces `.folio`/`.migas`. Verificado solo en `46`: ahí WCAG 2.5.8 se cumple por la excepción de espaciado, así que es divergencia de §7.3, **no** falla crítica de accesibilidad. Se propone arreglarla porque es un cambio de una línea (regla 2), no como fallo de accesibilidad.


### 5.2 Críticos propios de una pantalla

| Pantalla | Hallazgo | Criterio | Estado vs v1 | Verificación |
|---|---|:-:|---|---|
| `13_panel_asistencia_rhl` | §1.5 Cromo de aplicación (`--chrome-alerta` / `--chrome-alerta-ink`) + — El número «4» es el conteo de incidencias pendientes de dictamen que el menú le muestra a RHL: es el dato que dice si hay trabajo. A 3,4:1 y 10,5px, con baja visión o brillo alto, se lee mal. Hay dos lecturas: el badge es redundan | 1 | persiste | confirmada |
| `27_padron_clientes` | §6.15 Fila desplegable + §6.11 regla 5 + §13.3 — El control que el padrón eligió para saber a qué sucursal pertenece un servicio (pp-098) no funciona en 4 de 5 filas y, en la que funciona, sus acciones quedan fuera de la vista a 1280. | 5 | persiste | confirmada |
| `28_instalador_mi_dia` | §3.1 El relleno de un contenedor no vive en un hijo opcional — La barra que abre la pantalla se ve cortada: el titulo y la linea de resumen (donde esta el aviso de material incompleto) quedan pegados a la linea divisoria, mientras arriba tienen 12px. En un instalador que mira la pantalla de p | 5 | nuevo | confirmada |
| `47_asistente` | §3.1 El relleno de un contenedor no vive en un hijo opcional (el siste — La ultima linea de cada respuesta —la conclusion, el dato que se va a copiar o actuar— queda cruzada por el borde de la franja; se lee como un error de pintado y apiña la conclusion con el rotulo «DE DÓNDE SALIÓ», que queda justo  | 5 | persiste | confirmada |
| `55_verificacion_pedido` | §1.1 `--border-ctrl` — borde de control cuya única frontera es el bord — En campo, con sol, las casillas aún sin marcar —las que el instalador tiene que ver para saber qué le falta— casi no se distinguen del fondo. | 1 | nuevo | confirmada |
| `58_altas_como_modal` | FICHAS_TECNICAS.md (58): «ninguna de las cinco cabe sin desplazar» + § — La pagina cuya funcion es mostrar que formulario cabe en un dialogo muestra formularios con la mitad de los campos tapados por las cabeceras de seccion; quien decide D-15 con ese dibujo decide sobre lo que no ve. | 2 | nuevo | confirmada |
| `58_altas_como_modal` | Decision D1 del aviso del 28-sep (alta de cliente = pagina) y FICHAS_T — Quien abra 58 para decidir ve una recomendacion (modal en escritorio para el alta de cliente) que contradice la decision ya tomada; la pagina de decision da ahora una respuesta distinta de la que se decidio. | 4 | persiste | confirmada |

### 5.3 Regresiones frente a v1

| Pantalla | Hallazgo | Regla | Verificación |
|---|---|---|---|
| `22_gestoria` | Entre 860 y 1100 px (portátil pequeño, ventana partida) la navegación son 15 iconos que un lector de pantalla anuncia como «enlace» sin nombre. Es regresión: v1 lo hacía bien en esta pantalla. Es la p | §7.2 Cromo de aplicación | confirmada |
| `22_gestoria` | Quien trabaja en un portátil de 1280 px abre la bandeja y no ve ningún botón de acción; tiene que descubrir que debe desplazar la tabla. El botón «Admitir», que arranca el reloj y no se puede deshacer | §13.3 Un contenedor no cede el ancho a un descendiente + dec | exagerada — La tabla tiene 6 filas (8 botones), no '8 filas'; a 1280 los botones estan cortados 20 px, no 'fuera del area visible'. §13.3 (hijo con max-width en tarjeta) no |
| `24_tickets` | El folio, la fecha de apertura y la prioridad «Baja» son lo que se escanea en la bandeja de tickets; a 4,2:1 y 10,5–11 px cuestan lectura a quien tiene baja visión. Los tres pasaban en la entrega ante | §1.7 Regla de contraste + §1.1 Superficies y texto | confirmada |
| `24_tickets` | El título del estado no entra en la lista de encabezados y el esqueleto anuncia texto inventado a un lector de pantalla; con movimiento reducido las barras quedan a medio pintar. | §6.4 Vistas de estado | no verificada (severidad no alta) |
| `26_estados_de_pantalla` | Un lector de pantalla encuentra dos «banner» en la pagina que ensena el patron de accesibilidad. | FICHAS_TECNICAS.md del cliente · «Defectos reales de accesib | no verificada (severidad no alta) |
| `51_acceso` | La pantalla de entrada se queda sin ningun encabezado: quien navega por encabezados no encuentra la pagina y el titulo de la ventana es lo unico que la nombra. | §6.4 regla 2 «Cada estado lleva un encabezado real» + FICHAS | confirmada |
| `58_altas_como_modal` | La pagina pierde su titulo: no hay encabezado de nivel 1 ni nombre visible, y el subtitulo que reconocia que el modal ya solo gobierna cuatro altas desaparece. | §6.4 regla 2 | confirmada |

### 5.4 Arreglos de accesibilidad que el propio cliente documentó y que v2 deshace

`FICHAS_TECNICAS.md` («Defectos reales de accesibilidad encontrados y corregidos», verificados con axe-core) lista arreglos ya hechos en v1. Se comprobó cada uno en el ZIP: **9 de 9 se han perdido** (el patrón de v1 ya no está). Parece que la actualización se aplicó sobre copias anteriores a esos arreglos.

| Pantalla | Arreglo documentado | v1 | v2 | ¿Perdido? |
|---|---|---:|---:|:-:|
| `26_estados_de_pantalla` | `<header class="p4">` duplicaba role="banner" → `<div class="p4">` | 0 | 1 | **sí** |
| `33_cfe_detalle` | `<header class="p4">` duplicaba role="banner" → `<div class="p4">` | 0 | 1 | **sí** |
| `42_alta_tramite_gestoria` | `<header class="p4">` duplicaba role="banner" → `<div class="p4">` | 0 | 1 | **sí** |
| `43_alta_tramite_vehicular` | `<header class="p4">` duplicaba role="banner" → `<div class="p4">` | 0 | 1 | **sí** |
| `44_alta_tramite_cfe` | `<header class="p4">` duplicaba role="banner" → `<div class="p4">` | 0 | 1 | **sí** |
| `24_tickets` | `--text-3-fuerte` en textos que no pasaban 4,5:1 | 6 | 0 | **sí** |
| `33_cfe_detalle` | `--text-3-fuerte` en textos que no pasaban 4,5:1 | 5 | 0 | **sí** |
| `01_login` | `--text-3-fuerte` en textos que no pasaban 4,5:1 | 2 | 0 | **sí** |
| `57_menu_cuenta` | sin `role="menu"` mal aplicado (aria-required-children) | 0 | 2 | **sí** |

(Ocurrencias = veces que aparece la construcción en el archivo; para el arreglo de `header` y `role="menu"`, 0 es lo correcto; para `--text-3-fuerte`, lo correcto es >0.) Además, en `24`, `33` y `01` el `--text-3` sigue en `#66717F` (4,21:1 sobre `--surface-2`), así que esos textos quedan sin ninguno de los dos arreglos: ni `--text-3-fuerte` ni el `#5C6675` nuevo. Esto amplía las 7 regresiones de §5.3, que solo cubrían las pantallas auditadas a fondo.

## 6 · Lo que se adopta del cliente y se documenta en nuestro sistema

De los 268 hallazgos de F1: **128 se adoptan** (el cliente decide), **58 se le exigen**, **58 piden ajustar nuestro sistema**, 22 son decisiones de diseño abiertas y 2 no requieren acción. Estado frente a v1: 198 persisten, 63 son nuevos, 7 son regresiones.

Patrones que el cliente usa y nuestro sistema no documenta (propuestas de regla en cada ficha, campo `cobertura`):

| Pantalla | Patrón sin regla |
|---|---|
| `01_login` | Escena de fondo del acceso con ~20 hex sin token (azules y teal de la ilustración) |
| `05_app_cliente` | Par de botones de acción hermanos en tarjeta móvil (`.abtn`): rótulos de distinta longitud, uno envuelve y el icono queda apartado |
| `05_app_cliente` | Google Fonts por <link> en una pantalla móvil (línea 10) |
| `05_app_cliente` | Tamaños < 12 px en móvil: `.abtn`, `.stbtn`, `.tile` a 11,5 px y etiquetas de la barra de pestañas a 10 px (línea 264) |
| `05_app_cliente` | Marco de teléfono y barra de estado simulados dentro del DOM |
| `05_app_cliente` | Tokens del antecesor en pantalla de cliente (--text-3 #66717F, 14 más) |
| `13_panel_asistencia_rhl` | Selector descendiente de elemento (`.componente span`, `.componente b`) dentro de un componente cuyas filas contienen <span> con otro rol (acciones, texto en línea). Medido en la bandeja de Asistencia RHL: el span genérico anuló display, gap y margin-top de la |
| `13_panel_asistencia_rhl` | Escala de interlineado: el sistema no la define (§2 y §3 solo tienen tamaños y espaciados). En esta pantalla conviven `normal` (≈1,25), 1, 1,05, 1,3, 1,35 y 1,55, y los bloques de texto multilínea del sistema usan 1,4, 1,5, 1,55 y 1,6 sin nombre (§6.7, §6.9, § |
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
| `47_asistente` | Contradiccion entre 10_dprimi_asistente (identico a v1) y 47_asistente |
| `48_asistencia_rhl` | Interlineado de interfaz: el sistema no tiene escala ni valor por omisión. Hay `line-height` solo dentro de cinco componentes (1,4; 1,5; 1,55; 1,6) y las pantallas fijan además 1,25, 1,3 y 1,35 por su cuenta; lo demás computa `normal`. El brief I5 cuenta 4–5 i |
| `51_acceso` | Entrada de tarjeta unica sin columna de marca (`.acceso > .caja-acc`) |
| `51_acceso` | Estado de error de autenticacion con variantes |
| `54_bitacora_descargas` | Marca de sensibilidad del dato (dato personal, confidencial) en un registro o una fila. El sistema tiene el semáforo (§1.3, juicios de estado) y las series (§1.4 y `.p-type`, clasificaciones sin connotación), pero nada para decir «esto tocó dato personal» sin  |
| `55_verificacion_pedido` | Etiqueta de «siguiente paso» sobre el renglón activo de una lista de verificación (`.ren.siguiente::before` con `translateY(-32px)`). El sistema no tiene un patrón para señalar cuál es el próximo elemento a atender dentro de una lista; el cliente lo resolvió c |
| `58_altas_como_modal` | Cuerpo de dialogo con secciones que desplaza (`.modal .cuerpo > .seccion`) |
| `58_altas_como_modal` | Marco de dialogo ilustrado en una pagina de referencia (sin <dialog>) |
| `58_altas_como_modal` | Seccion de registro historico dentro de una maqueta de decision (D1: 41 ya no es dialogo) |
| `58_altas_como_modal` | Tabla de medidas con columnas numericas (`.medida`) |
| `59_editar_cliente` | Hoja de especímenes de un diálogo (varios estados del mismo diálogo en una página) |
| `59_editar_cliente` | Campo de solo lectura con motivo |
| `59_editar_cliente` | Nombre del botón que abre un diálogo parcial |

Contradicciones internas de nuestro sistema que los auditores encontraron (a resolver al subir versión): §2.1 (10,5 px solo en mayúsculas) frente a §7.2 (`.grp` a 10,5 px sin mayúsculas); §6.5 (Material Symbols por `<link>`) frente a D116 (sin Google Fonts); §1.4 frente a §12.5 en la antigüedad de saldo por tramos.

## 7 · Conformidad con el aviso del ingeniero (28-sep) y rediseños

### 7.1 Aviso del padrón, 12 ítems

| # | Decisión | `27` | `21` | `41` | `58` | `59` |
|---:|---|:-:|:-:|:-:|:-:|:-:|
| 1 | D6: «Reenviar liga de registro» retirada (no se construye; dictamen 2894 punto 15). | ✓ | ✓ | ✓ | ✓ | · |
| 2 | D5: Sección «Unidades» (VIN, placas, descripción) en la ficha del cliente. | · | ✓ | · | · | · |
| 3 | D9: «Datos fiscales» (CP, régimen, domicilio) editables en línea en la ficha; `editar-cliente` se queda en dos renglones (razón social + RFC solo lectura). | · | ✓ | · | · | ✓ |
| 4 | D3: Grupo automotriz y Marca pertenecen a «Sucursal» (no a la razón social); en la ficha el grupo se deriva de las sucursales. | · | ? | ✓ | ✗ | · |
| 5 | D2: Sucursal opcional en el alta, con el aviso «Sin sucursal no se le puede programar una orden; se puede añadir después desde la ficha». | · | · | ✗ | ✗ | · |
| 6 | D1: El alta de cliente es una página (ruta /clientes/nuevo), no un diálogo. `58_altas_como_modal` existe: ¿sigue vigente o quedó obsoleta? | ? | · | ✓ | ✗ | · |
| 7 | D10: «Último movimiento» en el listado, ocultable desde «Columnas». | ✓ | · | · | · | · |
| 8 | D13: Contacto «De la empresa» (sin sucursal) en la ficha y en el alta; la sucursal del alta es todo o nada. | · | ✓ | ✓ | ✗ | · |
| 9 | D15: Ficha de cliente inactivo en solo lectura, con banda «Cliente inactivo» y botón «Reactivar». | · | ✓ | · | · | · |
| 10 | D7: D7 (vigencia por documento) AUSENTE: sin columna de vigencia ni chip «con un documento por vencer». | ✗ | ✓ | ✓ | ✓ | · |
| 11 | D8: D8 (duplicados) AUSENTE: sin banner de duplicados ni «Comparar y decidir». | ✗ | ✓ | ✓ | ✓ | · |
| 12 | D4: Exportar la ficha como PDF de una hoja (identidad, estado, expediente, contacto principal, sucursales, contactos; sin historial). Sin cambios. | · | ? | · | · | · |

Las ✗ de `58` se refieren al diálogo «Nuevo cliente» de esa página, obsoleto para el alta de cliente según FICHAS (`58` ya no gobierna `41`, pero sigue gobernando las otras cuatro altas).

✓ cumple · ✗ no cumple · ? no verificable · · no aplica. Desajustes extra y críticos: D7 se pospone, pero 27 dibuja en el estado por defecto el chip «7 con un documento por vencer», la pastilla «Por vencer» con fecha de vencimiento y aviso de 30 días, y «revisadas y vigentes» (FICHAS reconoce que 27 lo dibuja).; D8 se pospone, pero 27 dibuja la tarjeta «Dos pares de razones sociales se parecen demasiado» con dos botones «Comparar y decidir» y la nota de fusión, visible por defecto.; D1: 58 sigue dibujando «Nuevo cliente» como diálogo (con aritmética que lo declara «el único que pasa de dos») y propone «modal en escritorio y página en el teléfono», sin ninguna marca en el HTML de que quedó superada para el alta de cliente; la supersesión solo está en FICHAS_TECNICAS.md. Arrastra los ítems 4, 5 y 8 (Grupo y marca como sección propia, sin Sucursal).; D2: la sucursal es opcional, pero falta el aviso literal «Sin sucursal no se le puede programar una orden; se puede añadir después desde la ficha» (la sección dice solo el todo-o-nada y el estado vacío omite la consecuencia). Omisión de texto, no contradicción de fondo.

### 7.2 Briefs de diseño (Fase 4)

Cada brief parte de lo que dibujó el cliente, evalúa al menos dos opciones (la primera siempre «mínimo cambio sobre lo del cliente»), trae un prototipo medido a 1440/1280/1024/390 px y termina con un veredicto de viabilidad. Los archivos completos están en `audit/v2/briefs-diseno/`.

| Brief | Observación | Veredicto de viabilidad | Recomendación |
|---|---|---|---|
| [`24-tickets-zona-superior.md`](briefs-diseno/24-tickets-zona-superior.md) | 9 y 10 · Tickets TI, zona superior | **viable con condiciones** | Un solo bloque ámbar (el plazo) a ancho declarado junto a los datos; la regla de cierre en una banda neutra de una frase; el resto a toggletip; `padding-bottom` en la cabecera. |
| [`27-acordeon-sucursales.md`](briefs-diseno/27-acordeon-sucursales.md) | 12 · acordeón de sucursales | **viable** | Cinco filas hijas que abren; lista de 560 px sin tarjeta; estado solo si la sucursal no puede recibir órdenes; «Ver órdenes» junto a cada una. Botones fuera de vista a 1280: de 4 a 0. |
| [`27-etiquetas-de-estado.md`](briefs-diseno/27-etiquetas-de-estado.md) | 3 · etiquetas de estado del padrón | **viable con condiciones** | Un estado por eje (Completos · Pendientes · Sin calcular; Activo · Inactivo); el documento que falta es una línea, no un estado; sin «Por vencer» hasta D7. |
| [`28-mi-dia.md`](briefs-diseno/28-mi-dia.md) | 13 · Mi día | **B viable; C viable con condiciones** | `.p4{padding-bottom:var(--sp-3)}`, declarar `--sp-5`, aire al final de la lista y resumen oculto en vacío/error. La opción C recupera los 12 px de pliegue subiendo la fecha a la cabecera, pero requiere decisión de producto. |
| [`34-agenda.md`](briefs-diseno/34-agenda.md) | 14 · agenda de instaladores | **viable con condiciones** | No cambiarla: ningún fallo crítico depende de ella. Cambio mínimo: texto ≥12 px, fila «Sin asignar», domingo visible a 1280, cabecera fija, `--text-3`. La «agenda del sistema» no existe en 2.15.0. |
| [`47-asistente.md`](briefs-diseno/47-asistente.md) | 17 · Asistente | **viable con condiciones** | «Chat» no merece sección propia. La franja se conserva. Quitar `margin-top:-12px` de `.fuentes`; cuerpo y pie como zonas hermanas; 24 px a los 5 destinos pequeños. Condición: decidir si el asistente solo consulta (47) o ejecuta con confirmación (10). |
| [`54-panel-con-que-filtros.md`](briefs-diseno/54-panel-con-que-filtros.md) | 18 · panel «CON QUÉ FILTROS» | **viable con condiciones** | Dos grupos en la misma celda; marca «Dato personal» con escudo sin color de estado; valores literales («Querétaro y Celaya», no «2 de 5»). Incluye la regla de sistema para la marca de sensibilidad. |

**Dos hechos que cambian la lectura de la observación 3:** las etiquetas «Falta documento» e «Incompleto» no existen en `27_padron_clientes` del ZIP (`grep` = 0); «Incompleto» solo aparece en `06_padron_clientes`, un prototipo anterior. Probablemente tu captura es de otra versión. Y los briefs de `24` y `27` parten de la copia que trae el ZIP (Anexo A).

## 8 · Qué tan fiable es esta auditoría

- **Validadores deterministas** (no son agentes): 23 de 23 fichas con 0 errores (JSON, § existentes en la 2.15.0, clases y ids presentes en el HTML, citas literales en su línea, `pp-NNN` reales, hashes). Una ficha de prueba rota a propósito dispara los 8 errores inyectados.
- **Citas del sistema de diseño:** todo lo citado se contrastó con el md de la **v2.15.0** (`docs/sistema-diseno-sio-dproma.md`; es el último disponible: las 4 ramas que traen la 2.15.0 tienen el mismo archivo, hash `a4b43d7a3f3e`; la rama de trabajo, en 2.13.3, no se usó como fuente). De 280 fragmentos entrecomillados, **255 son literales en la 2.15.0** (91 %). Los 25 restantes son citas de `FICHAS_TECNICAS.md` (15) o paráfrasis; **ninguno coincide con la 2.13.3** (0), así que no hay arrastre de la versión anterior. Detalle en `mediciones/v2/citas.json`.
- **Verificación adversarial:** 119 afirmaciones: 110 confirmadas, 9 exageradas, 0 refutadas, 0 no concluyentes. Las exageradas se corrigieron en este informe (p. ej. el recorte de acciones a 1366 px es de 11 px, no «fuera»; el hueco del acordeón mide 578–654 px). **Cero refutaciones no prueba que no haya errores:** la réplica lo muestra.
- **Réplica ciega** (2 pantallas, sin ver el original): mismo veredicto de observación 2 de 2; coincidencia de § citados **43 %**, por debajo del 80 % que nos fijamos. De los hallazgos altos del original, la réplica reprodujo 5 de 10; encontró otros que el original no tenía. Lo que ambas pasadas encuentran es sólido; la lista no es exhaustiva.
- **Instrumentos validados antes de usarse** con HTML sintético de respuesta conocida (contraste con alfa y `color-mix`, táctil, menú, I1–I9, C2, C11, `--sp-5`): 15 de 15 aciertos. Aun así los auditores hallaron seis fallos de mi instrumental (capturas de 800 px, I6, I9, C1 sin estilos en línea, I3 e I7 con falsos positivos, `lib.cjs` inyecta las fuentes y no sirve para probar fuentes). Están corregidos o documentados.
- **Recall frente a tus 19 observaciones:** 16 de 19 reproducidas con evidencia por un auditor (más la 14, respondida por el brief de agenda: 17 de 19 con respuesta); 2 (4 y 15) no se pueden probar porque `49_alta_orden` no viene en el ZIP; **No es un recall ciego:** los auditores sabían qué buscar.
- **Límites.** Las otras 27 pantallas solo tienen medición mecánica. Los hallazgos se refieren al archivo recibido, no a lo que el cliente tenga en otra carpeta. `FICHAS_TECNICAS.md` se usó como fuente de decisiones del cliente; se contradice a sí misma en un punto (plazo de tickets, tanda 3 frente a tanda 4). F3 sale entre 2 y 4 en las pantallas auditadas: 2: 10, 3: 12, 4: 1 pantallas.
- **F5 contra investigación** (solo nivel A y 54): cubre 36, ignora 10.

## 9 · Pendientes

1. **Opcional:** si más adelante se consigue la carpeta `sistema/` del cliente, re-medir esas pantallas; este informe se limita al ZIP recibido.
2. **Confirmar identidades inferidas**: la hoja 1 es `22` o `32` (ambas tienen el defecto); la hoja 2 es `05_app_cliente` (coincide el nombre «Laura Núñez»); la hoja 5 es `13_panel_asistencia_rhl`, no `48`.
3. **Decidir** las preguntas de diseño abiertas (§7.2). Para documentar divergencias en el sistema, el contenido de la 2.15.0 es el mismo en las 4 ramas que la traen; solo falta elegir en cuál se commitea.
4. **Corregir en nuestro sistema** las contradicciones de §6 antes de subir versión.

## Anexo A · Contraste informativo con el PDF del cliente

La columna «Carpeta» sale del propio PDF (`html_v2/` o `sistema/`). El análisis sale de `claims.py` (lectura estática de cada código C1–C18 del PDF contra su archivo) y de comparar hashes con v1. C11, C13, C14, C15 y C18 no se pueden verificar mecánicamente; C2 se mide en navegador.

| Grupo | N | Pantallas |
|---|---:|---|
| Listadas en el PDF y **ausentes del ZIP** | 10 | 31_orden_detalle, 49_alta_orden, 52_vehicular_bandeja, 53_tramite_detalle, facturacion, viaticos-adeudos-nomina, viaticos-alta-solicitud, viaticos-discrepancia-cfdi, viaticos-reembolso, viaticos-remanente |
| Listadas, presentes, **sin los cambios declarados** | 19 | 01_login, 08_detalle_tramite, 22_gestoria, 24_tickets, 26_estados_de_pantalla, 30_ordenes_listado, 32_cfe_bandeja, 33_cfe_detalle, 34_instaladores, 36_recetas_despacho, 42_alta_tramite_gestoria, 43_alta_tramite_vehicular, 44_alta_tramite_cfe, 45_autorizacion_compra, 46_cuentas_por_cobrar, 51_acceso, 56_frontera_error, 57_menu_cuenta, 58_altas_como_modal |
| Listadas, presentes, **cambios confirmados** | 21 | 07_orden_instalacion, 09_app_checklist_instalacion, 20_tablero, 21_ficha_cliente, 23_viaticos, 25_consumo_de_material, 27_padron_clientes, 28_instalador_mi_dia, 29_instalador_orden, 35_incidencias, 37_concluidos, 38_vehicular_detalle, 39_viatico_detalle, 40_usuarios, 41_alta_cliente, 47_asistente, 48_asistencia_rhl, 50_compras_almacen, 54_bitacora_descargas, 55_verificacion_pedido, 59_editar_cliente |
| En el ZIP y nuevas respecto a v1 | 8 | 02_dashboard, 03_kanban_gestoria, 04_app_personal, 05_app_cliente, 06_padron_clientes, 07_orden_instalacion, 38_vehicular_detalle, 48_asistencia_rhl |
| Idénticas byte a byte a v1 | 6 | 10_dprimi_asistente, 11_app_login_2fa_offline, 12_app_checado_asistencia, 13_panel_asistencia_rhl, 14_app_checado_oficina, 56_frontera_error |

Nota sobre C1 (nada menor de 12 px): se midió en las hojas `<style>`. Además, 8 pantallas tienen `font-size` menor de 12 px en atributos `style=""` (23_viaticos, 33_cfe_detalle, 36_recetas_despacho, 37_concluidos, 38_vehicular_detalle, 39_viatico_detalle, 45_autorizacion_compra, 46_cuentas_por_cobrar); no es claro si el PDF contaba esos atributos, así que no se usa para clasificar.

**Lectura.** Las observaciones 4 y 15 (`49_alta_orden`, que vive en `sistema/icev/`) no se pueden auditar sobre v2. Tickets TI, Acceso, Altas como modal, Cuentas por cobrar y Agenda de instaladores son pantallas de `sistema/`: lo que se auditó de ellas es la copia que trae el ZIP, que puede no ser la que viste en tus capturas.

## Anexo B · Cómo reproducir

`audit/v2/instrumentos/` (medidores, `verificar-fixtures.sh`, `validar.py`, `concordancia.py`, `consolidar.py`), `audit/v2/mediciones/` (JSON de v1 y v2), `audit/v2/raw/` (una ficha por pantalla), `audit/v2/verif/` y `audit/v2/replica/`. Todas las cifras de este documento salen de esos archivos.
