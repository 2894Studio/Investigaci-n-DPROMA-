# Auditoría de diseño — SIO-DPROMA

**Paquete auditado:** `maquetas-SIO-por-funcionalidad-2026-09-30` · 52 maquetas vigentes  
**Medido contra:** `docs/sistema-diseno-sio-dproma.md` v2.13.3 y `web/design-tokens.json` (81 tokens)  
**Fecha:** 5 de octubre de 2026 · 2894 Studio

> Las maquetas son de un equipo externo. Este informe es material de conversación, no un cambio
> que hayamos hecho nosotros. No se ha modificado ninguna maqueta ni ningún documento del sistema.

---

## 1. Resumen ejecutivo

Se auditaron **las 52 maquetas** contra el sistema de diseño. Ninguna cumple por completo: **42 no cumplen** y **10 cumplen parcialmente**. Se registran **762 hallazgos** (291 de severidad alta) y **158 propuestas de regla nueva** para huecos de nuestra propia documentación.

**El paquete no está mal construido: está construido sobre una versión anterior del sistema.** De los 35 tokens que divergen del canónico, 34 son el semáforo de la etapa previa —menos contrastado que el actual, pero por encima de 4,5:1—. Solo uno es un fallo real de accesibilidad.

### Los cinco problemas que mandan

**1. Un token obsoleto, en 51 de 52 maquetas.** `--text-3: #66717F` donde el canónico es `#5C6675`. Sobre `--surface-2` cae a **4,21:1**, bajo el mínimo AA. No es teórico: la regla `tbody tr:hover td{background:var(--surface-2)}` existe en 45 maquetas, y **203 nodos de texto en 18 de ellas caen a 4,21:1 cada vez que alguien sobrevuela una fila**. Es la interacción más frecuente de una bandeja. Una línea de corrección en cada archivo.

**2. El menú lateral pierde su nombre a 1000px, en 42 de 46 maquetas.** Medido: `innerText` vacío, `title` nulo, `aria-label` nulo — **630 enlaces anónimos**. §7.2 dice que el rótulo «se convierte en etiqueta emergente; **no desaparece**». La franja afectada es la del portátil de oficina. El patrón correcto ya existe en el paquete: `08_detalle_tramite`, `22_gestoria`, `13_panel_asistencia_rhl` y `10_dprimi_asistente` lo resuelven bien.

**3. Una pantalla queda en blanco.** `10_dprimi_asistente` con `prefers-reduced-motion` activado: los cuatro mensajes computan `opacity: 0`. La media query está escrita **antes** de `.enter{opacity:0}`, misma especificidad, y el `!important` solo cubre `animation`. Quien tenga esa preferencia del sistema abre el asistente y ve el hilo vacío, sin aviso. Verificado con Playwright en los dos modos.

![El mismo asistente con y sin la preferencia de movimiento reducido. A la izquierda, la conversación. A la derecha, el mismo hilo con `prefers-reduced-motion: reduce`.](img/VERIF-dprimi-reduce.png)

*Captura real de `10_dprimi_asistente` con `prefers-reduced-motion: reduce`. Los cuatro mensajes
siguen en el DOM, con `opacity: 0`. No hay aviso ni alternativa.*

**4. Decisiones con dinero sin protección.** `45_autorizacion_compra` aprueba **$48.528 en una pulsación**: cero `<dialog>`, cero `[role=dialog]`, sobre una acción que la propia pantalla declara irreversible. El comentario que ella misma dice que bloquea la decisión no tiene `required`: es un asterisco decorativo. `40_usuarios` tiene el mismo problema con «Dar de baja».

**5. El sistema no se lee igual en dos pantallas seguidas.** «Aprobado» es pastilla verde en `23_viaticos` y gris en `viaticos-reembolso`. En `24_tickets` el rojo significa a la vez prioridad y plazo. Y los dos asistentes del producto se contradicen en lo único que importa: `47_asistente` dice «no modifica nada» y `10_dprimi_asistente` ofrece enviar un PDF por correo — ambos abiertos desde el mismo `.fab`. Es también lo que dice Nielsen: **«Consistencia y estándares» es la heurística peor puntuada** (media 2,75 sobre 4).

### Lo que el paquete hace bien

- **37 de 52 maquetas no tienen ningún fallo de contraste** medido con composición alfa real.
- El tema oscuro está resuelto en casi todas, por `prefers-color-scheme` y por `data-theme`, con `theme-color`.
- `41_alta_cliente` es la referencia del paquete: `required` y `aria-required` reales, dos niveles de obligatoriedad, error solo tras `blur`, `aria-invalid` + `aria-describedby`, y §6.17 completa.
- `22_gestoria` y `32_cfe_bandeja` implementan §6.21 con ~190 líneas de lógica real: foco al abrir, `Escape` que devuelve el foco, clic fuera, anuncio por `aria-live`.
- El sprite SVG que sustituye a Material Symbols (§6.5) **es probablemente la decisión correcta**: funciona sin red y sin parpadeo, que es lo que pide la app de campo. El sistema es el que va por detrás.

---

## 2. Matriz pantallas × fases

🔴 crítico · 🟡 atención · 🟢 aceptable · — fuera del subconjunto

| Pantalla | Área | F1 cumplimiento | F2 tokens | F3 boost | F4 Nielsen | F5 investigación |
|---|---|---|---|---|---|---|
| **Principal** | | | | | | |
| `20_tablero` | direccion | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | 🟡 max 3 | 🔴 7 pp · 1 contradice |
| **Padrón** | | | | | | |
| `58_altas_como_modal` | comercial | 🔴 9 altas | 🔴 15 div · 1 s/decl | 🔴 2/5 | 🔴 max 4 | 🔴 5 pp · 1 contradice |
| `27_padron_clientes` | comercial | 🔴 8 altas | 🟢 15 div | 🔴 2/5 | 🟡 max 3 | 🟡 6 pp |
| `21_ficha_cliente` | comercial | 🔴 7 altas | 🟢 15 div | 🟡 3/5 | 🟢 max 2 | 🟡 6 pp |
| `59_editar_cliente` | comercial | 🔴 7 altas | 🔴 15 div · 1 s/decl | 🔴 2/5 | 🔴 max 4 | 🟡 5 pp |
| `41_alta_cliente` | comercial | 🟢 2 altas | 🟢 15 div | 🟢 4/5 | 🟢 max 2 | 🟡 7 pp |
| **ICEV** | | | | | | |
| `34_instaladores` | ICEV | 🔴 9 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `29_instalador_orden` | ICEV / almacén | 🔴 7 altas | 🔴 15 div · 2 s/decl | 🔴 2/5 | — | — |
| `30_ordenes_listado` | ICEV | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `49_alta_orden` | ICEV | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `35_incidencias` | ICEV / almacén | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `28_instalador_mi_dia` | ICEV | 🟡 4 altas | 🔴 15 div · 1 s/decl | 🔴 2/5 | 🟡 max 3 | 🟡 6 pp |
| `55_verificacion_pedido` | ICEV / almacén | 🟡 4 altas | 🔴 15 div · 1 s/decl | 🔴 2/5 | — | — |
| `11_app_login_2fa_offline` | ICEV | 🟢 3 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `14_app_checado_oficina` | ICEV | 🟢 3 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `25_consumo_de_material` | ICEV / almacén | 🟢 3 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `31_orden_detalle` | ICEV/operaciones | 🟢 3 altas | 🔴 15 div · 1 s/decl | 🟡 3/5 | 🟡 max 3 | 🔴 9 pp · 1 contradice |
| `09_app_checklist_instalacion` | ICEV | 🟢 2 altas | 🟡 26 div | 🟡 3/5 | 🔴 max 4 | 🟡 5 pp |
| `12_app_checado_asistencia` | ICEV | 🟢 2 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `36_recetas_despacho` | ICEV / almacén | 🟢 2 altas | 🟢 15 div | 🟡 3/5 | — | — |
| **Trámites** | | | | | | |
| `32_cfe_bandeja` | administracion vehicular | 🔴 10 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `37_concluidos` | administracion vehicular | 🔴 10 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `22_gestoria` | administracion vehicular | 🔴 9 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `44_alta_tramite_cfe` | admin vehicular | 🔴 9 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `08_detalle_tramite` | administracion vehicular | 🔴 8 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `42_alta_tramite_gestoria` | administracion vehicular | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `33_cfe_detalle` | admin vehicular | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `43_alta_tramite_vehicular` | administracion vehicular | 🟡 4 altas | 🟢 15 div | 🔴 2/5 | 🔴 max 4 | 🟡 5 pp |
| `52_vehicular_bandeja` | administracion vehicular | 🟡 4 altas | 🟢 16 div | 🟡 3/5 | 🟡 max 3 | 🟡 5 pp |
| `53_tramite_detalle` | administracion vehicular | 🟢 3 altas | 🟢 16 div | 🟡 3/5 | 🟡 max 3 | 🟡 5 pp |
| **Dirección y Admin.** | | | | | | |
| `45_autorizacion_compra` | almacén | 🔴 8 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `viaticos-remanente` | finanzas | 🔴 8 altas | 🟢 15 div | 🟡 3/5 | — | — |
| `54_bitacora_descargas` | jurídico/legal | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `viaticos-reembolso` | finanzas | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `39_viatico_detalle` | finanzas | 🟡 6 altas | 🟢 15 div | 🟡 3/5 | — | — |
| `40_usuarios` | dirección/sistema | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `46_cuentas_por_cobrar` | finanzas/cobranza | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | 🔴 max 4 | 🔴 9 pp · 1 contradice |
| `50_compras_almacen` | almacén | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `viaticos-discrepancia-cfdi` | finanzas | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `23_viaticos` | finanzas | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | 🔴 max 4 | 🟡 7 pp |
| `facturacion` | finanzas | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `viaticos-adeudos-nomina` | finanzas | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `viaticos-alta-solicitud` | finanzas | 🟡 4 altas | 🟢 15 div | 🔴 2/5 | 🔴 max 4 | 🔴 7 pp · 1 contradice |
| `13_panel_asistencia_rhl` | jurídico/RH | 🟢 3 altas | 🟢 16 div | 🔴 2/5 | — | — |
| **Soporte** | | | | | | |
| `24_tickets` | soporte | 🔴 7 altas | 🟢 15 div | 🔴 2/5 | — | — |
| `47_asistente` | soporte | 🟡 6 altas | 🟢 15 div | 🔴 2/5 | 🟡 max 3 | 🟡 5 pp |
| `10_dprimi_asistente` | soporte | 🟡 5 altas | 🟢 15 div | 🔴 2/5 | — | — |
| **Transversales** | | | | | | |
| `51_acceso` | transversal | 🔴 7 altas | 🔴 15 div · 2 s/decl | 🔴 2/5 | 🔴 max 4 | 🔴 3 pp · 1 contradice |
| `26_estados_de_pantalla` | transversal | 🟡 5 altas | 🟢 15 div | 🟡 3/5 | 🔴 max 4 | 🟡 3 pp |
| `57_menu_cuenta` | transversal | 🟡 5 altas | 🔴 15 div · 1 s/decl | 🔴 2/5 | — | — |
| `56_frontera_error` | transversal | 🟢 3 altas | 🟢 15 div | 🟡 3/5 | 🟡 max 3 | 🟡 3 pp |
| `01_login` | transversal | 🟢 2 altas | 🔴 6 div · 1 s/decl | 🟡 3/5 | 🟡 max 3 | 🟡 2 pp |

---

## 3. Pantallas de revisión URGENTE

Criterio: 7 o más hallazgos de severidad alta, o un fallo que impide operar.

| Pantalla | Altas | Motivo |
|---|---|---|
| `32_cfe_bandeja` | 10 | Estados fuera de §6.4, etiquetas sin icono, isotipo roto; 10 altas. |
| `37_concluidos` | 10 | El trabajo pendiente se distingue solo por el tono del texto a 11px; 10 altas. |
| `22_gestoria` | 9 | Estados con `<b>` por título y §6.12 regla 5 incumplida pese a buena barra de filtros. |
| `34_instaladores` | 9 | **64 nodos bajo 12px** donde se decide quién va a cada visita; pinta un 0 que desmiente. |
| `44_alta_tramite_cfe` | 9 | Formulario sin `required`, sin `aria-required` y **sin `<form>`**. |
| `58_altas_como_modal` | 9 | `--sp-5` sin declarar deja los tres rellenos del diálogo en **0px**; §6.18 en bloque. |
| `08_detalle_tramite` | 8 | Carga Google Fonts que §2 prohíbe y `document.fonts.size = 0`: no cargó. |
| `27_padron_clientes` | 8 | Bandeja inerte con `aria-controls` a ids inexistentes; 7 casillas a 15×15px. |
| `45_autorizacion_compra` | 8 | Aprueba **$48.528 sin confirmación** ni `required` en el campo que la bloquea. |
| `viaticos-remanente` | 8 | Vocabulario de estado incompatible con el resto de la familia de viáticos. |
| `21_ficha_cliente` | 7 | Enlaces primarios de fila a 14-15px — el caso que §7.3 nombra literalmente. |
| `24_tickets` | 7 | El semáforo significa prioridad **y** plazo a la vez en la misma fila. |
| `29_instalador_orden` | 7 | **No puede cerrar una orden**: 0 `input[type=file]`; las fotos son botones inertes. |
| `30_ordenes_listado` | 7 | `[data-density="compact"]` no existe en el CSS; §6.11 regla 6 sin implementar. |
| `42_alta_tramite_gestoria` | 7 | Muestra **dos avisos opuestos a la vez** sobre si el canal arranca el reloj. |
| `49_alta_orden` | 7 | Formulario sin obligatoriedad real; §10 trampa 2 escrita literal. |
| `51_acceso` | 7 | `TypeError` al cargar: sin conmutador de tema, sin menú y sin cierre con Escape. |
| `54_bitacora_descargas` | 7 | Registro legal **sin ningún filtro**; su vista vacía remite a un control inexistente. |
| `59_editar_cliente` | 7 | Enuncia por escrito las 4 reglas de foco de §6.18 y no implementa ninguna. |
| `viaticos-reembolso` | 7 | Cabecera dice «Pendiente» y la tarjeta «Suspendido», en la misma pantalla. |

Además, fuera del umbral de 7 altas pero con fallo que impide operar:

- `10_dprimi_asistente` — la pantalla desaparece para quien usa `prefers-reduced-motion`.
- `12_app_checado_asistencia` — sin rama de fallo de ubicación: `startCapture()` siempre triunfa, así que sin permiso queda colgada en «Obteniendo ubicación…».
- `14_app_checado_oficina` — promete «foto en vivo + ubicación exacta» y su manejador no captura nada.
---

## 4. Criterios generales de mejora (Do / Don't)

Estos criterios salen de los patrones que se repiten en muchas pantallas. **Aplicarlos corrige la
mayor parte del informe sin revisar pantalla a pantalla.** Cada uno indica a cuántas afecta.

### C1. Un solo token de color, corregido en origen

*Afecta a 31 de 52 pantallas.*

**Haz:** sustituye `--text-3: #66717F` por `#5C6675` en el `:root` de los 51 archivos. Una línea por archivo.

**No hagas:** inventar un token paralelo. Dos maquetas crearon `--text-3-fuerte: #5D6774` —que es el canónico con otro nombre— en vez de corregir el original. Ahora hay dos tokens para un color y el malo sigue en uso.

*Verifica: `grep -c '#66717F' *.html` debe dar 0.*

### C2. El rótulo colapsado no desaparece, se convierte en etiqueta emergente

*Afecta a 14 de 52 pantallas.*

**Haz:** en el menú lateral colapsado, añade `title` y `aria-label` al enlace con el mismo texto del rótulo. Copia el patrón de `08_detalle_tramite`, que ya está bien en el paquete.

**No hagas:** `display:none` sobre `.it .et` sin reemplazo. Entre 860 y 1100px deja la navegación en iconos anónimos.

*Verifica: a 1000px, ningún `.it` con `innerText`, `title` y `aria-label` vacíos a la vez.*

### C3. El esqueleto imita la forma, no el contenido

*Afecta a 40 de 52 pantallas.*

**Haz:** barras mudas. Y con `prefers-reduced-motion`, **aplana el fondo** a `--surface-2`, no solo `animation:none`.

**No hagas:** texto real dentro de las barras con `color:transparent` —sigue en el árbol de accesibilidad—, ni cifras inventadas («$00,000», «00 ago 2026»). Y no dejes `animation:none` sin reponer el fondo: el degradado se congela en vez de desaparecer.

*Verifica: `document.querySelectorAll('.skel')` sin `textContent`; y con `reducedMotion:'reduce'`, `backgroundImage` = `none`.*

### C4. El estado de pantalla es un componente, no un párrafo suelto

*Afecta a 25 de 52 pantallas.*

**Haz:** `.tarjeta-estado` con medallón `.estado-ico` de 52px y un encabezado real (`<h2>`). Anuncia el cambio con `aria-live` y mueve el foco.

**No hagas:** `<b>` como título, ni el estado suelto sobre el fondo. Y **nunca sustituyas un formulario relleno por la vista de error**: tres pantallas lo hacen mientras su propio texto dice «lo que capturaste sigue en el borrador».

*Verifica: cada vista de estado con 1 encabezado real y 1 `.estado-ico`.*

### C5. Un color de estado no se reutiliza para una categoría, ni al revés

*Afecta a 8 de 52 pantallas.*

**Haz:** semáforo (§1.3) para lo que cambia solo y tiene juicio; series (§1.4) para clasificar sin juicio. Una severidad ordinal es un tercer caso y necesita su propia escala.

**No hagas:** pintar prioridad y plazo con el mismo rojo en la misma fila (`24_tickets`), ni teñir una clasificación con el ámbar del semáforo y luego escribir 298 caracteres para desmentir lo que el color afirma (`54_bitacora_descargas`).

*Verifica: ningún elemento usa `--err`/`--warn` para algo que no cambia solo.*

### C6. El asterisco no es obligatoriedad

*Afecta a 16 de 52 pantallas.*

**Haz:** `required` y `aria-required` reales, dentro de un `<form>`, con los dos niveles de obligatoriedad escritos en palabras. `41_alta_cliente` lo tiene resuelto entero.

**No hagas:** `<span class="req">*</span>` sin respaldo. En cinco formularios `grep -c required` da **0** y los asteriscos son adorno; en uno de ellos el campo decorado es el que la pantalla declara que bloquea la decisión.

*Verifica: `required` ≥ número de asteriscos.*

### C7. Una decisión irreversible se confirma

*Afecta a toda decisión irreversible del producto.*

**Haz:** `<dialog>` nativo con `showModal()` y las cuatro reglas de foco de §6.18. Bloquea el cierre mientras la operación está en vuelo.

**No hagas:** aprobar dinero o dar de baja a una persona en una sola pulsación. Y no uses `div[role=dialog]`: §6.18 avisa de que obliga a reimplementar foco, capa y velo, «y en la práctica no se reimplementan» — las dos maquetas con modal lo confirman, con 0 llamadas a `focus()`.

*Verifica: 0 `div[role=dialog]`; toda acción irreversible con un `<dialog>` delante.*

### C8. El destino interactivo mide 24px, y 44 en campo

*Afecta a 23 de 52 pantallas.*

**Haz:** amplía el área sin agrandar el dibujo (`padding` + `margin` negativo). Los enlaces primarios de fila —folio, miga, «Ver en Maps»— llevan padding hasta 24px.

**No hagas:** escribir la regla `data-tacto` sin `:root`. Está así en 42 de 52 archivos; §7.3 documenta ese mismo error y explica que la regla queda sin efecto.

*Verifica: ningún interactivo visible por debajo de 24×24px.*

### C9. El andamiaje se retira con un solo selector

*Afecta a 9 de 52 pantallas.*

**Haz:** marca con `data-andamio` **todo** lo que no va a producción: bandas «pendiente de revisión», etiquetas «No existe todavía», comparativas «ASÍ NO / ASÍ SÍ», notas en primera persona del autor.

**No hagas:** dejar contenido de proyecto dentro de `<main>` sin marcar. Hay rutas de API, `prisma/schema.prisma:1682`, «(doc 31, línea 179)» y nombres de archivos de maqueta viajando como UI de producto. En `facturacion`, **la vista «con datos» entera** es uno de esos avisos.

*Verifica: `[data-andamio]` cubre todo bloque que cite el proyecto.*

### C10. Una frase, no un párrafo

*Afecta a 24 de 52 pantallas.*

**Haz:** el bloque siempre visible va bajo ~140 caracteres y una frase. Lo demás, a toggletip (§6.23).

**No hagas:** explicar por qué se tomó una decisión de producto dentro de la pantalla. Récords medidos: 1.062 caracteres en `51_acceso`, 534 en `35_incidencias`, 422 en `24_tickets`. En `56_frontera_error` el texto además **contradice la pantalla**: dice «tampoco hay menú al que ir» con los 14 enlaces de la barra lateral dibujados.

*Verifica: `innerText.length` ≤ 140 en bloques siempre visibles.*

### C11. Si parece interactivo, interactúa

*Afecta a 14 de 52 pantallas.*

**Haz:** o cableas el control, o lo presentas como cifra de lectura sin `aria-pressed` ni cursor de puntero.

**No hagas:** 113 atributos `aria-pressed` que nunca cambian, `aria-controls` apuntando a ids inexistentes, o un conmutador «Compacta» cuando `[data-density="compact"]` no existe en el CSS.

*Verifica: todo `aria-pressed` cambia al pulsar.*

### C12. El isotipo no se recorta

*Afecta a 43 de 52 pantallas.*

**Haz:** no repitas el `viewBox` del `<symbol>` en el `<svg>`, y da medidas al `<use>`. `08_detalle_tramite` y `01_login` lo escriben bien.

**No hagas:** `<svg width="44" height="42" viewBox="740 0 970 932"><use href="#dproma-mark"/></svg>`. Medido: **−32,5px** de desplazamiento, la marca sale como una astilla. §10 trampa 5 lo documenta con ese mismo número.

*Verifica: `getBoundingClientRect()` del `<use>` alineado con el del `<svg>`.*

---

## 5. Gap del sistema de diseño

Esta sección no es sobre las maquetas: es sobre **nuestra fuente de verdad**.

### 5.1 Por qué un token obsoleto llegó a 51 archivos

No fue descuido. El documento principal **no publica ningún hex** para las variantes `-ink`, `-bg` y
`-fill` del semáforo: solo publica el ratio. El único sitio donde esos valores están escritos es
`docs/sistema-diseno-acceso-sio-dproma.md`, el documento antecesor — que es justo el que arrastra el
`--text-3: #66717F` obsoleto. Quien necesitaba un `-ink` se llevó el `:root` entero de ahí, y el token
malo viajó de paquete. **El hueco de documentación causó el incumplimiento.**

### 5.2 Tokens

- **14 tokens canónicos que ninguna maqueta usa:** `--chrome-alerta`, `--chrome-alerta-ink`, `--marca-1`, `--marca-2`, `--marca-4`, `--marca-5`, `--marca-6`, `--marca-7`, `--marca-lienzo`, `--marca-lienzo-ink`, `--pause`, `--serie-3`, `--serie-4`, `--surface-hover`. Seis de los siete `--marca-*` y las series 3 y 4.
- **20 tokens usados que `design-tokens.json` no publica**, entre ellos **todos los de movimiento** (`--dur-*`, `--ease-*`, `--stagger`), los velos y `--row-*`. No es culpa de las maquetas: el generador los pierde porque se alimenta del `:root` de la página renderizada, y esa página no necesita animar ni dibujar velos.
- **`--focus-w` y `--focus-offset` se usan en §1.7 y nunca se definen** en el documento. Las maquetas los declaran correctamente a `2px`. El sistema debería publicarlos.

### 5.3 Componentes documentados que nadie implementa

| Componente | § | Uso en las 52 | Lectura |
|---|---|---|---|
| `.msi` iconos | 6.5 | **0/52** | Las 52 usan sprite SVG. **La maqueta acierta**: funciona sin red. El sistema va por detrás. |
| `.dash` `.widget` `.cifras` | 12.4 | **0/52** | El tablero reimplementa la rejilla con vocabulario propio (`.card`, `.bloque`, `.pila`). |
| `.vista` | 6.4 | **0/52** | Renombrado a `.estado` / `.state`. |
| `.ambito` | 6.22 | **0/52** | El concepto se usa, pintado con colores de semáforo que lo contradicen. |
| `.infob` toggletip | 6.23 | **0/52** | Sin implementar: por eso el texto largo se queda en pantalla. |
| `.pasos` `.paso-ico` | 6.6 | 1/52 | Sin demo viva en `reglas-de-diseno.html` tampoco. |

### 5.4 Incoherencias dentro del propio sistema

1. **Dos fuentes de verdad declaradas.** `scripts/gen-design-tokens.py:4` dice que la fuente es `reglas-de-diseno.html`; `sio-dproma-design-sync/SKILL.md:27` dice que es `docs/sistema-diseno-sio-dproma.md`. Y la skill de sync **no incluye** el paso de regenerar el JSON que el script le atribuye.
2. **La fuente canónica no tiene número de versión.** `design-rules.md` y `reglas-de-diseno.html` van por 2.13.3; `docs/sistema-diseno-sio-dproma.md` no lleva ninguno, así que no es verificable.
3. **`web/llms.txt:17` publica «Versión vigente: 2.6.0»** cuando el sistema va por 2.13.3.
4. **El doc de acceso no está marcado como obsoleto** y la skill de auditoría manda leerlo para logins. Choques de valor verificados: `--text-3`, `--sh-modal` (.20 vs .22) y `--glass` (.74 vs .66).
5. **El historial está desordenado:** 2.13.0 → 2.13.2 → **2.11.1** → 2.13.3, y faltan 2.9.x–2.12.x.
6. **Contradicción interna:** §1.2 asigna el verde lima `#C7D97B` al «anillo de foco sobre fondo oscuro», y §1.5 asigna **la misma descripción literal** a `--chrome-focus #9FE0AE`.

### 5.5 Las 158 propuestas de regla

Los subagentes redactaron **158 propuestas** en el tono del sistema, listas para aprobar o ajustar. Las familias con más peso:

- **Formato móvil / campo (≈25):** no existe especificación de teléfono. §1.8 tema de exterior, §3.2 radios en teléfono, §7.3.1 token `--touch:48px`, §7.4 barra fija con `env(safe-area-inset-bottom)`, §6.17.1 evidencia fotográfica, §14 comportamiento sin conexión.
- **Asistente conversacional (≈11):** el patrón no está documentado en absoluto. §6.25 conversación, §6.25.2 «un solo asistente, un solo contrato», §6.26 procedencia de la respuesta.
- **Permisos de dispositivo (≈4):** §6.25 extiende §6.4 a cinco estados, incluido «denegado», que hoy no existe y deja pantallas colgadas.
- **Visualización sin librería (≈6):** §12.1 bis admite gráfica en CSS/SVG manteniendo obligatoria la tabla equivalente de §12.3.

Se entregan dentro de cada JSON, en el array `cobertura`. Incorporarlas es trabajo de `sio-dproma-design-sync`, no de esta auditoría.

---

## 6. Anexos

| Archivo | Contenido |
|---|---|
| `audit/raw/*.json` | **52 fichas**, una por maqueta, con las cinco fases y su evidencia. |
| `audit/F2-gap-sistema-diseno.json` | Gap global de tokens: canónicos sin uso, usados fuera del canon, divergencias. |
| `audit/mediciones-contraste.json` | Contraste con composición alfa real, claro y oscuro. |
| `audit/medidor-contraste.cjs` | El medidor, versionado para que las cifras sean reproducibles. |
| `audit/mediciones-tactil.json` | Destinos interactivos bajo 24px, con selector y medida. |
| `audit/mediciones-menu-lateral.json` | Enlaces sin nombre accesible a 1000px. |
| `audit/mediciones-hover.json` | Nodos que caen a 4,21:1 al sobrevolar una fila. |
| `audit/pain-points-por-area.md` | Puente área ↔ pantalla: 106 pain points mapeados. |

### Nota de método

Las mediciones se hicieron con Playwright sobre las 52 maquetas servidas por HTTP local, nunca por `file://`. El andamiaje de demo se ocultó para no contaminar ni capturas ni cifras.

**El medidor de contraste se corrigió dos veces durante la auditoría**, y conviene decirlo porque cambia las cifras: la primera versión trataba los fondos `rgba()` como opacos, y la segunda no entendía `color(srgb …)`, que es lo que devuelve `color-mix()`. Las dos inflaban los fallos. Los totales pasaron de 119 a **17 fallos reales en 11 maquetas**. Cuatro lotes detectaron esos artefactos por separado rehaciendo la aritmética, y por eso no llegaron al informe.

Por el mismo motivo se **descartaron dos hallazgos** que no resistieron verificación: que la receta de `.p-type` de §6.10 no pasara contraste (calculada sobre las cuatro series da 5,26:1 a 5,91:1, cumple), y que el esqueleto de `13_panel_asistencia_rhl` filtrara nombres de personas a un lector de pantalla (su vista de carga es inalcanzable y el contenedor va en `display:none` y `aria-hidden="true"`).

Donde no hubo evidencia, la ficha dice `sin_datos` con el motivo. Ningún hallazgo de F1 entra sin citar su §; ningún hallazgo de F5 entra sin citar su `pp-NNN` y su documento.