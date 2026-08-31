# Sistema de diseño — SIO-DPROMA

Referencia técnica para construir SIO-DPROMA. Empezó siendo el sistema de la pantalla de
acceso; ahora cubre también el arquetipo de dashboard (tabla densa, filtros, formularios,
ficha), que es donde vive el módulo de clientes.

**Fuentes:**

| Pantalla | Archivo | Estado |
|---|---|---|
| Acceso | `web/entregables/propuestas/acceso-sio-dproma.html` | Corregida — 19 puntos de revisión |
| Padrón de clientes | `web/entregables/propuestas/padron-clientes.html` | Corregida |
| Ficha de cliente | `web/entregables/propuestas/ficha-cliente.html` | Corregida |
| Alta de cliente | `web/entregables/propuestas/alta-cliente.html` | Corregida |

Ninguna es un mockup: son las pantallas, con las correcciones ya aplicadas. El detalle de cada
punto y su porqué está en `web/entregables/recomendaciones-login.html#sio` para el acceso, y en
el documento de recomendaciones del padrón para las otras tres. Las decisiones de producto que
tuvimos que tomar nosotros —porque el hallazgo no se arreglaba con CSS— están aparte, en
`docs/decisiones-producto-padron.md`.

**La regla de fondo:** ningún hex literal en un componente. Todo pasa por un token. Cuando algo
no tenga token, se añade aquí siguiendo el patrón de nombres, no se resuelve con un valor suelto
en la hoja de estilos.

---

## 1. Color

Dos temas, claro y oscuro, seleccionados por `prefers-color-scheme` o forzados con
`data-theme="dark"` / `data-theme="light"` en el `<html>`.

### 1.1 Superficies y texto

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--bg` | `#F2F5F7` | `#10161F` | Fondo de página |
| `--surface` | `#FAFCFD` | `#171F2C` | Superficie sólida (tarjetas, tablas, botones) |
| `--surface-2` | `#E7EDF3` | `#1D2735` | Superficie secundaria (cabeceras, filas al pasar el cursor, filas inactivas, esqueleto) |
| `--border` | `rgba(27,36,48,.14)` | `rgba(231,236,242,.12)` | Borde sutil |
| `--border-2` | `rgba(27,36,48,.26)` | `rgba(231,236,242,.24)` | Borde de control interactivo |
| `--text` | `#1B2430` | `#E7ECF2` | Texto principal |
| `--text-2` | `#4C5A6B` | `#A8B3C2` | Texto secundario |
| `--text-3` | `#5C6675` | `#8B96A6` | Texto auxiliar |

Nunca blanco absoluto como superficie: `--surface` es `#FAFCFD`. Un blanco puro sobre una
pantalla brillante fatiga, y la norma europea de accesibilidad de productos digitales
(EN 301 549) lo desaconseja para interfaces de uso continuado.

**`--text-3` cambió de valor.** Era `#66717F`, medido contra `--bg` y `--surface`, donde cumple
(4,53:1 y 4,82:1). Pero el dashboard tiene una tercera superficie que el acceso no tenía —
`--surface-2`, el fondo de las filas inactivas y del hover— y ahí caía a **4,21:1**, por debajo
del mínimo. `#5C6675` cumple en las tres:

| `--text-3` sobre | Antes `#66717F` | Ahora `#5C6675` |
|---|---|---|
| `--surface` | 4,82:1 | 5,65:1 |
| `--bg` | 4,53:1 | 5,31:1 |
| `--surface-2` | **4,21:1** ❌ | 4,93:1 |

En oscuro `#8B96A6` ya cumplía en las tres (5,53 / 6,06 / 5,03) y no se toca.

`acceso-sio-dproma.html` sigue con `#66717F`. No es un defecto ahí: esa pantalla no usa
`--surface-2`, así que su texto auxiliar nunca cae sobre el fondo que fallaba. Queda pendiente
igualarlo cuando esa pantalla se vuelva a tocar.

### 1.2 Acción y marca

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--accent` | `#3E7A4C` | `#4A8F5A` | Acción principal |
| `--accent-ink` | `#F7FAF9` | `#08120D` | Texto e iconos sobre `--accent` |
| `--accent-soft` | `rgba(62,122,76,.10)` | `rgba(74,143,90,.16)` | Fondo tenue de acento |
| `--link` | `#2F6B3C` | `#7FC08F` | Enlaces de texto |

**`--accent` no es `--ok`, a propósito.** Los dos son verdes y podrían haberse fusionado. No se
fusionan porque son cosas distintas: `--accent` es «esto se puede pulsar» y `--ok` es «esto está
bien». Si comparten color, un botón primario se lee como una etiqueta de estado y una etiqueta
de estado invita a pulsarla.

Un tercer color vive fuera de estos tokens porque es de marca, no de interfaz: `#C7D97B`
(verde lima), en el wordmark y el anillo de foco sobre fondo oscuro. No se usa en controles.

### 1.3 Semáforo — cinco estados, tres variantes cada uno

Cinco estados, no dos. Un cliente no está solo bien o mal: puede estar en espera de un
documento (`warn`), bloqueado por una condición que no depende de quien mira (`block`), o
simplemente inactivo (`pause`), que no es un error.

| Estado | Significa | Claro | Oscuro |
|---|---|---|---|
| `--ok` | Correcto, completo, vigente | `#2F8F6F` | `#4FBF98` |
| `--warn` | Falta algo, o vence pronto | `#B98A1E` | `#E8C24C` |
| `--err` | Falta lo que impide operar | `#C24238` | `#EE6E5F` |
| `--block` | Bloqueado por una condición externa | `#9678CC` | `#C0A9F0` |
| `--pause` | Inactivo, en pausa — no es un fallo | `#4A5560` | `#6B7684` |

Cada uno tiene **tres variantes**, y usarlas bien es lo que hace que el contraste no dependa del
contenedor:

- **base** (`--ok`) — el color puro. Solo para elementos gráficos: un punto, un borde, una
  barra. Nunca para texto sobre fondo claro.
- **`-ink`** (`--ok-ink`) — la versión oscurecida hasta cumplir AA. Es la que va en el texto y
  el icono de una etiqueta. En tema oscuro, `-ink` = base, porque ahí el color ya cumple.
- **`-bg`** (`--ok-bg`) — fondo **opaco**, no una transparencia. Una transparencia hereda lo que
  haya detrás, así que el contraste cambia según dónde caiga la etiqueta; un fondo opaco lo fija.

Existe además `-fill` (`rgba` del color base), reservado para rellenos grandes donde sí se
quiere que se vea la superficie de debajo — franjas, áreas de gráfica. No para etiquetas.

Contraste medido de cada `-ink` sobre su `-bg`, que es la combinación real de una etiqueta:

| | Claro | Oscuro |
|---|---|---|
| ok | 5,04:1 | 5,67:1 |
| warn | 5,25:1 | 7,14:1 |
| err | 5,02:1 | 4,59:1 |
| block | 5,41:1 | 6,10:1 |
| pause | 6,30:1 | 5,25:1 |

### 1.4 Series de gráfica

| Token | Claro | Oscuro |
|---|---|---|
| `--serie-1` | `#2C6CA8` | `#6FA8DC` |
| `--serie-2` | `#7A5FA8` | `#B69BE0` |

**Una serie de gráfica nunca reutiliza un color de estado.** Si la barra de «Agencias» fuera
verde, se leería como «agencias correctas». Estos dos azul-violeta existen justo para eso: para
clasificar sin opinar. Se usan también en las etiquetas de tipo de cliente (§6.10). Medidos
como elemento gráfico (mínimo 3:1): 5,35 / 5,06 en claro, 6,55 / 6,90 en oscuro.

### 1.5 Cromo de aplicación

La barra lateral y la superior tienen su propia paleta, porque son fondo oscuro en los dos
temas. Van aparte para que un cambio en las superficies del contenido no las arrastre.

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--chrome` | `#1E4E79` | `#122740` | Fondo del cromo — **solo estructura, nunca fondo de página** |
| `--chrome-ink` | `#F2F5F7` | `#E7ECF2` | Texto sobre el cromo |
| `--chrome-dim` | `rgba(242,245,247,.72)` | `rgba(231,236,242,.72)` | Texto atenuado del cromo |
| `--chrome-line` | `rgba(242,245,247,.14)` | `rgba(231,236,242,.10)` | Separadores dentro del cromo |
| `--chrome-focus` | `#9FE0AE` | igual | Anillo de foco sobre fondo oscuro |
| `--chrome-hover` / `--chrome-activo` | `rgba(255,255,255,.08)` / `.12` | igual | Estados del ítem de menú |

El anillo de foco cambia de color dentro del cromo. `--accent` sobre `#1E4E79` no llega a 3:1;
`--chrome-focus` sí. Es la única excepción a «el foco es idéntico en los dos temas».

### 1.6 Velos

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--velo-suave` | `rgba(19,29,43,.08)` | `rgba(0,0,0,.32)` | Sombra de barra flotante |
| `--velo-modal` | `rgba(19,29,43,.45)` | `rgba(4,8,14,.62)` | Capa detrás de un diálogo |

### 1.7 Regla de contraste

Texto normal 4,5:1 mínimo; texto grande (≥24px, o ≥18,66px en negrita) y elementos gráficos
3:1. **Cada color nuevo se mide contra los fondos donde va a aparecer**, en los dos temas, antes
de darlo por bueno. No se asume por parecido visual, y no basta con medirlo sobre `--surface`:
si el elemento puede caer sobre `--surface-2`, se mide también ahí. Es exactamente el error que
tuvo `--text-3` durante toda la primera versión de este documento.

---

## 2. Tipografía

- **Interfaz:** `Inter` (400, 500, 600, 700). Todo: texto, botones, tablas, formularios.
- **Marca:** `Michroma` / `Ethnocentric Rg` (`--font-brand`), solo para el wordmark
  «SIO-DPROMA» y el nombre «DPROMA». Nunca en texto de interfaz.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Michroma&display=swap" rel="stylesheet">
```

**Ese `<link>` no es opcional.** Las tres maquetas del padrón declaraban `--font-ui:'Inter'` y no
cargaban ninguna fuente, así que se renderizaban en `system-ui` — el sistema de tipografía
existía solo sobre el papel.

| Token | Tamaño | Uso |
|---|---|---|
| `--fs-meta` | 12px | Metadatos, pies, referencias, etiquetas de campo |
| `--fs-dense` | 13px | Tablas densas, cuerpo compacto, ayuda de campo |
| `--fs-base` | 14px | Cuerpo por defecto |
| `--fs-sub` | 16px | Subtítulo destacado, título de página en el cromo |
| `--fs-title` | 20px | Título de pantalla o de ficha |
| `--fs-kpi` | 30px | Cifra grande de un indicador |

Los títulos de tarjeta de estado no usan token: van a 18–21px fijo según el peso visual que
necesite el estado (21px en el acceso, 18px en los estados de resultado).

### 2.1 El suelo son 12px

`--fs-meta` es el tamaño más pequeño del sistema. **Nada baja de ahí.**

No es una preferencia estética. Las maquetas de origen tenían unas treinta declaraciones por
debajo de 12px, y no en adornos: el RFC a 11px —un dato que se compara carácter a carácter—,
todas las etiquetas de estado a 11px, las cabeceras de tabla a 11px en mayúsculas, las notas al
pie a 11,5px, y las etiquetas libres de contacto a 11px. Es decir, casi todo lo que se consulta
a diario estaba en el tamaño reservado a lo secundario.

La regla práctica: **si un dato se lee todos los días, va a 12–13px como mínimo.** Por debajo de
12px no queda nada; si algo parece necesitarlo, la respuesta es que sobra en esa pantalla, no
que haya que encogerlo.

Se admite una excepción, y solo una: 10,5px en mayúsculas con `letter-spacing` para los
**rótulos de grupo** de la barra lateral y las etiquetas de campo del modo tarjeta. Son cuatro
o cinco palabras que se leen una vez para orientarse, no datos.

---

## 3. Espaciado y radios

Escala base de 4px. El nombre del token **no es el multiplicador** — es un identificador, no una
fórmula a extrapolar sin mirar la tabla.

```css
--sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:20px; --sp-6:24px;
--sp-8:32px; --sp-12:48px;
--r-ctrl:6px; --r-card:10px; --r-modal:16px; --r-pill:999px;
--row-comfy:40px; --row-compact:32px;
```

**`--sp-5` (20px) se añadió porque faltaba y ya se estaba usando.** La maqueta del diálogo lo
referenciaba cuatro veces —el padding de la cabecera, el del cuerpo y el del pie— sin que
existiera en ningún `:root`. Un `var()` que no resuelve no cae a un valor por omisión: invalida
**la declaración entera**, así que los tres paddings computaban a **0** y el contenido quedaba
pegado al borde. El documento de recomendaciones lo describió como «los elementos del diálogo
están muy juntos y sin jerarquía»; la causa era un hueco en la escala.

Lo que enseña, más allá del valor: **un token que no existe falla en silencio**. No hay error en
consola, no hay aviso, y el síntoma se parece a una decisión de diseño desafortunada. Cuando un
espaciado se vea raro, lo primero es comprobar que su token está definido.

| Token | Valor | Uso |
|---|---|---|
| `--sp-1` | 4px | Separación mínima entre elementos muy pegados |
| `--sp-2` | 8px | Icono-texto, gap entre chips |
| `--sp-3` | 12px | Gap interno de fila, celda de tabla |
| `--sp-4` | 16px | Padding de control, gap entre bloques cortos |
| `--sp-5` | 20px | Padding interior de un diálogo |
| `--sp-6` | 24px | Padding de sección, margen entre grupos |
| `--sp-8` | 32px | Padding de tarjeta principal, columnas del layout |
| `--sp-12` | 48px | Separación grande entre secciones |

| Token | Valor | Uso |
|---|---|---|
| `--r-ctrl` | 6px | Botones, chips, campos, etiquetas de estado |
| `--r-card` | 10px | Tarjetas |
| `--r-modal` | 16px | Diálogos y la tarjeta flotante del acceso |
| `--r-pill` | 999px | Buscador, chips de filtro, control segmentado |

`--row-comfy` (40px) y `--row-compact` (32px) son las dos alturas de fila de una tabla densa.
Ver §6.11 para la regla de qué cambia además de la altura.

---

## 4. Sombra y superficie translúcida

```css
--sh-rest:0 1px 2px rgba(19,29,43,.07);   /* reposo */
--sh-float:0 6px 18px rgba(19,29,43,.10); /* hover, barra flotante */
--sh-modal:0 24px 60px rgba(19,29,43,.22);/* diálogo, tarjeta flotante */
--glass:rgba(250,252,253,.66);
--glass-line:rgba(27,36,48,.10);
```

La tarjeta del acceso usa `backdrop-filter: blur(16px)` sobre `--glass`. Como no todos los
navegadores lo soportan, lleva respaldo sólido — sin esto, en un navegador sin soporte el fondo
queda semitransparente y el texto se lee mal sobre lo que haya detrás:

```css
.glass{
  background:var(--glass); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-line); box-shadow:var(--sh-modal); border-radius:var(--r-modal);
}
@supports not (backdrop-filter:blur(1px)){ .glass{ background:var(--surface) } }
```

El translúcido es de la pantalla de entrada. En el dashboard las superficies son opacas: sobre
una tabla densa, un fondo que deja ver lo de detrás resta legibilidad sin aportar nada.

---

## 5. Movimiento

```css
--dur-micro:120ms;  /* hover, press, checkbox */
--dur-base:200ms;   /* dropdowns, cambio de tema, popovers */
--dur-enter:300ms;  /* entrada de vistas — techo duro de la UI */
--ease-out:cubic-bezier(.23,1,.32,1);        /* entradas y respuestas al usuario */
--ease-in-out:cubic-bezier(.77,0,.175,1);    /* movimiento de un punto a otro en pantalla */
--ease-spring:cubic-bezier(.34,1.56,.64,1);  /* solo píldora de pestañas y tarjeta de kanban */
--stagger:40ms;                              /* retardo entre elementos de una lista que entra */
```

`--dur-enter` es un techo, no una sugerencia: ninguna entrada de vista pasa de 300ms.

`--ease-spring` rebasa el valor final y vuelve. Eso está bien en un elemento que el usuario
acaba de mover (una píldora de pestaña, una tarjeta que suelta en otra columna) y mal en
cualquier otro sitio, donde se lee como inestabilidad. Por eso está acotado por escrito.

**Reducción de movimiento.** No es «cero animación»: se conservan opacidad y color, se elimina
todo desplazamiento y escala.

```css
@media (prefers-reduced-motion:reduce){
  :root{ --dur-micro:1ms; --dur-base:120ms; --dur-enter:120ms; --ease-spring:linear; --stagger:0ms }
}
```

**Criterio del proyecto, obligatorio para toda animación nueva:** se pausa pulsando la propia
animación — el contenedor es un `<button>` con `aria-pressed`, nunca un botón «Pausar» aparte.
Detalle completo, incluida la trampa del `prefers-reduced-motion` global del sitio, en
`docs/criterios-de-animacion.md`.

---

## 6. Componentes

### 6.1 Botón primario del acceso (`.gbtn`)

El botón de acción principal de la pantalla de entrada. Se bloquea **en el manejador de JS**, no
solo con CSS: `pointer-events:none` detiene el ratón pero no el teclado, y en la maqueta
original cuatro Intro sobre el botón «ocupado» disparaban cuatro envíos.

```css
.gbtn{width:100%;min-height:48px;display:flex;align-items:center;justify-content:center;gap:11px;
  padding:13px;border-radius:var(--r-ctrl);border:1px solid var(--border-2);
  background:var(--surface);color:var(--text);font:600 var(--fs-base) var(--font-ui);
  cursor:pointer;box-shadow:var(--sh-rest)}
.gbtn:hover{box-shadow:var(--sh-float);border-color:var(--text-3)}
.gbtn[aria-busy="true"]{color:var(--text-2);cursor:progress}
.gbtn .spin{display:none;width:16px;height:16px;border:2px solid var(--border-2);
  border-top-color:var(--accent);border-radius:50%;animation:spin .6s linear infinite}
.gbtn[aria-busy="true"] .spin{display:block}
```

```js
var ocupado = false;
boton.addEventListener('click', function(){
  if (ocupado) return;          // el guardián real: bloquea también el teclado
  ocupado = true;
  boton.setAttribute('aria-busy', 'true');
  // ... al terminar: ocupado = false; boton.setAttribute('aria-busy', 'false');
});
```

### 6.2 Botones (`.btn`, `.btn.p`, `.btn.mini`)

```css
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:36px;
  padding:8px 14px;border-radius:var(--r-ctrl);border:1px solid var(--border-2);
  background:var(--surface);color:var(--text);font:600 var(--fs-dense) var(--font-ui);cursor:pointer}
.btn.p{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.mini{min-height:28px;padding:5px 10px;font-size:var(--fs-meta)}
.btn .msi{font-size:17px}
```

En la pantalla de acceso los botones van a 44px de alto, por encima del mínimo, porque son las
dos o tres acciones de toda la pantalla. En el dashboard el suelo es 36px (28px en `.mini`, que
solo se usa dentro de una fila o una tarjeta, junto a otros destinos).

**Un icono dentro de un botón hereda el color del botón.** Suena obvio y fue un fallo real: una
regla de bloque pintaba de gris todos los iconos dentro de un estado, incluido el del botón
«Reintentar» sobre fondo de acento. El contraste entre el icono gris y el verde era de
**1,03:1**; el mínimo para un elemento gráfico es 3:1. Heredando `currentColor` sube a 4,89:1.

```css
/* MAL: alcanza también al icono del botón que hay dentro */
.estado .msi{ color:var(--text-3) }
/* BIEN: el botón se defiende */
.estado .msi{ color:var(--text-3) }
.estado .btn .msi{ color:inherit }
```

### 6.3 Tarjeta (`.tarjeta`) — una sola receta de superficie

Contenedor de contenido agrupado: superficie, borde, radio y sombra de reposo.

```css
.tarjeta{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-card);box-shadow:var(--sh-rest);overflow:hidden}
.tarjeta > header{display:flex;align-items:center;gap:var(--sp-2);
  padding:var(--sp-3) var(--sp-4);background:var(--surface-2);
  border-bottom:1px solid var(--border)}
.tarjeta > header h2,.tarjeta > header h3,.tarjeta > header h4{
  font-size:var(--fs-base);font-weight:600;margin:0}
.tarjeta > header .n{margin-left:auto;font-size:var(--fs-meta);color:var(--text-2)}
.tarjeta .interior{padding:var(--sp-4)}
```

**Es una clase, no un patrón que cada pantalla reimplementa.** La ficha de cliente llegó con
seis definiciones independientes de la misma receta —`.tarjeta`, `.contacto`, `.identidad`,
`.princ`, `.seccion` y `.sk-caja`— que se veían casi igual y divergían en los detalles. Una
variante se declara como modificador:

```css
.tarjeta--acento{background:var(--accent-soft);border-color:transparent;box-shadow:none}
.tarjeta--marcada{border-color:var(--accent);border-width:2px}
```

Y el selector de encabezado cubre `h2`, `h3` **y** `h4` porque las tarjetas anidan a distinta
profundidad; con solo `h2, h3`, los `h4` de las tarjetas de actividad caían al estilo del
navegador.

### 6.4 Vistas de estado de una pantalla

Toda pantalla que pida datos tiene cuatro formas de presentarse: **con datos, cargando, vacía y
con error**. No son un extra: son la pantalla.

**Un solo contenedor, las vistas dentro como hermanas.** No una tarjeta suelta por estado: la
pantalla no debe cambiar de forma según lo que tenga que decir, y así quien mira no pierde la
referencia visual al pasar de cargando a error.

En la pantalla de entrada, el contenedor es la propia tarjeta:

```html
<div class="glass" id="tarjeta" tabindex="-1">
  <div class="vista" id="v-acceso">…</div>
  <div class="vista" id="v-cargando" role="status" aria-label="Comprobando tu acceso" hidden>…</div>
  <div class="vista estado" id="v-vacio" hidden>…</div>
  <div class="vista estado estado--err" id="v-error" hidden>…</div>
</div>
```

En el dashboard el estado ocupa **la zona de contenido**, no la pantalla: la barra lateral, la
superior y el título siguen ahí, porque siguen siendo verdad. El conmutador es un atributo en
el `<main>`:

```html
<main id="contenido" data-vista="ok" tabindex="-1">
  <div class="vista v-ok">…la tabla…</div>
  <div class="vista v-cargando" role="status" aria-label="Cargando el padrón" hidden>…</div>
  <div class="vista estado v-vacio" hidden>…</div>
  <div class="vista estado estado--err" hidden>…</div>
</main>
```

**El estado va dentro de una tarjeta, no suelto sobre el fondo.** En el acceso la tarjeta ya es
el contenedor de las cuatro vistas. En el dashboard la zona de contenido es enorme, así que un
mensaje centrado sin superficie no se lee como una respuesta del sistema, sino como una pantalla
que no terminó de cargar: el estado vacío del padrón dejaba ~500px de fondo liso alrededor de un
glifo gris. El contenedor centra; la tarjeta de dentro es la que tiene forma.

```css
.state{display:none;align-items:center;justify-content:center;flex:1;
  padding:var(--sp-8) var(--sp-4)}

.tarjeta-estado{max-width:480px;width:100%;padding:var(--sp-8);
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-modal);box-shadow:var(--sh-modal);
  display:flex;flex-direction:column;align-items:center;text-align:center;gap:var(--sp-3)}
.estado-ico{width:52px;height:52px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  background:var(--accent-soft);color:var(--accent)}
.estado-ico .msi{font-size:28px}
.tarjeta-estado.es-err .estado-ico{background:var(--err-fill);color:var(--err-ink)}
.tarjeta-estado p{color:var(--text-2);font-size:var(--fs-dense);line-height:1.6;max-width:36ch}
.tarjeta-estado .ref{color:var(--text-3);font-size:var(--fs-meta);font-variant-numeric:tabular-nums}
.tarjeta-estado .acc{display:flex;gap:var(--sp-2);flex-wrap:wrap;justify-content:center;width:100%}
.tarjeta-estado .acc .btn{flex:1 1 auto}
```

```html
<div class="state state-error">
  <div class="tarjeta-estado es-err">
    <span class="estado-ico"><span class="msi" aria-hidden="true" translate="no">error</span></span>
    <h2>No se pudo cargar el padrón</h2>
    <p>…qué pasó · qué no se perdió · qué hacer…</p>
    <p class="ref" translate="no">Referencia del error: PAD-20260821-1655</p>
    <div class="acc">…</div>
  </div>
</div>
```

**Es `--r-modal` y `--sh-modal`, no los de `.tarjeta`.** La tarjeta del acceso tiene 16px de radio
y sombra elevada; `.tarjeta` tiene 10px y `--sh-rest`. Con la receta de `.tarjeta` el estado sale
plano y de esquinas duras: no es la misma tarjeta. Y va **opaca**: el `.glass` del acceso se
compone sobre fondo plano en algo que difiere de `--surface` en 2/255, así que el aspecto es
idéntico y además se respeta el §4 —el translúcido es de la pantalla de entrada—.
El medallón se tiñe con `--err-fill`, no con el `--err-soft` del acceso, que fuera de esa pantalla
no existe.

**El medallón no es decoración: es lo que da peso al icono.** Sin él, el icono de estado acaba
siendo texto en `--text-3`, el gris más apagado del sistema, a 30px. Las cuatro maquetas del
padrón llegaron así pese a que este apartado ya lo prescribía.

**Cuatro reglas que no son opcionales:**

1. **El cambio se anuncia y mueve el foco.** Sin esto, quien usa lector de pantalla no se entera
   de que la pantalla cambió. Las tres maquetas del padrón llegaron sin un solo `aria-live`, con
   el `<main tabindex="-1">` ya preparado para recibir el foco y nadie enviándoselo.

   ```js
   var VISTAS = {
     ok:       { dice:'Padrón de clientes, 1.248 registros.' },
     cargando: { dice:'Cargando el padrón de clientes.' },
     vacio:    { dice:'Ningún cliente coincide con los filtros activos.' },
     error:    { dice:'No se pudo cargar el padrón de clientes.' }
   };
   function muestra(clave, mueveFoco){
     main.dataset.vista = clave;
     live.textContent = VISTAS[clave].dice;   // <p aria-live="polite" class="sr">
     if (mueveFoco) main.focus();
   }
   ```

2. **Cada estado lleva un encabezado real**, no un `<b>`. Es lo que permite navegar la página
   saltando de encabezado en encabezado.

3. **El error dice tres cosas, en este orden:** qué ha pasado, qué **no** se ha perdido, y qué
   hacer. Más una referencia (`PAD-20260729-0637`) con la que abrir un ticket. Es de lo mejor
   que traían las maquetas de origen y conviene mantenerlo en todo el sistema.

4. **El error no se lleva por delante lo que había.** En el alta de cliente, el estado de error
   ocultaba el formulario entero mientras el mensaje afirmaba que lo capturado seguía en el
   borrador: justo en el momento de más incertidumbre, se retiraba la prueba de que el trabajo
   seguía ahí. Cuando hay trabajo del usuario en pantalla, el error va **encima**, como aviso,
   con los campos visibles y rellenos.

### 6.5 Iconos (`.msi`)

Material Symbols Rounded, variante rellena (`FILL@1`). Buscar y elegir el icono en
[fonts.google.com/icons](https://fonts.google.com/icons) — filtrar por estilo **Rounded** (no
Outlined ni Sharp, para que combine con el resto) y copiar el nombre exacto que aparece debajo
del icono (p. ej. `account_circle`), que es el mismo que va en el HTML y en `icon_names`.

Se cargan por subconjunto —solo los nombres que se usan— para no pedir la fuente completa. Al
añadir un icono nuevo, se añade su nombre a la lista `icon_names` del `<link>` existente; no se
crea un `<link>` aparte:

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,1,0&icon_names=add,check_circle,error,schedule&display=block" rel="stylesheet">
```

Los cuatro ejes (`opsz,wght,FILL,GRAD@24,500,1,0`) fijan el aspecto de todos los iconos que
pidas con ese `<link>` — tamaño óptico 24, peso 500, relleno activado, grado neutro. No hace
falta tocarlos por icono; se heredan en `font-variation-settings` de `.msi`.

```css
.msi{font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;
  font-size:20px;line-height:1;display:inline-block;white-space:nowrap;direction:ltr;
  width:1em;height:1em;overflow:hidden;  /* si el icono no está en el subconjunto o la fuente
    no carga, el navegador pinta el nombre en letras — la caja fija de 1em×1em evita que eso
    rompa el layout */
  text-transform:none;letter-spacing:normal;font-feature-settings:'liga';
  font-variation-settings:'FILL' 1,'wght' 500,'GRAD' 0,'opsz' 24}
.msi-sm{font-size:17px} .msi-lg{font-size:24px}
```

**El subconjunto se regenera cada vez que cambia el markup.** Es el fallo más fácil de cometer y
el más difícil de ver: se añade un icono al HTML, se olvida añadirlo a `icon_names`, y el
navegador pinta el nombre en letras. Pasó con `close`, `edit`, `pause_circle` y
`progress_activity` en el diálogo, porque la lista se generó antes de escribir el markup.

La comprobación es exacta y cuesta una línea — todo icono usado tiene que estar en la lista:

```js
const enLista = decodeURIComponent(
  document.querySelector('link[href*="icon_names="]').href.split('icon_names=')[1].split('&')[0]
).split(',');
[...document.querySelectorAll('.msi')].map(e => e.textContent.trim())
  .filter(n => !enLista.includes(n));      // tiene que salir vacío
```

Y al generar la lista, **solo los nombres del markup**, más los que el conmutador de tema
intercambia. Un barrido suelto del JS cuela cualquier cadena en minúsculas —`seleccionado`,
`comfy`, `tr`— y un nombre inválido no degrada: devuelve **400** y se quedan sin cargar todos
los iconos de la página.

**Un glifo se dimensiona con `font-size`, nunca con `width`/`height`.** La caja de `.msi` ya es
`1em × 1em` con `overflow:hidden`, así que fijarle 12px de ancho no encoge el dibujo: lo recorta.
Es el resto típico de cuando el icono era un `<svg>`, y le pasó a la flecha de orden de las
cabeceras de tabla.

**`text-transform:none` y `letter-spacing:normal` no son adorno: son lo que hace que el icono
sea un icono.** El glifo se pide por ligadura —el navegador lee las letras `location_on` y las
sustituye por el dibujo—, así que cualquier ancestro que transforme ese texto rompe la
correspondencia y pinta el nombre en letras. Y los dos ancestros que lo hacen son de los más
comunes del sistema: las cabeceras de tabla (`text-transform:uppercase` + `letter-spacing:.04em`)
y los rótulos en mayúsculas. Pasó de verdad: la flecha de orden de cada columna y el icono del
encabezado de sucursales salían como «ARROW_DOWNWARD» y «LOCATION_ON» recortados a un cuadrado.

Se ve en cuanto se abre la pantalla, pero solo si la fuente carga. Con la fuente bloqueada, el
fallo se confunde con el respaldo de la caja de 1em, que hace exactamente lo mismo. De ahí que
la comprobación de iconos tenga que hacerse con red.

Siempre `aria-hidden="true"` y `translate="no"` (el nombre del icono no se traduce):

```html
<span class="msi" aria-hidden="true" translate="no">refresh</span>Reintentar
```

**Un icono nunca es la única forma de entender un control.** Y no basta con que el icono sea
«claro»: se sostiene solo cuando es universal **y su significado no cambia de contexto**. En el
padrón, la tercera acción de cada fila era un marcador en unas filas, un enlace en otras y una
flecha circular en la fila inactiva — tres significados en la misma posición. Ver §6.14.

Si un icono va sin texto visible, lleva **como mínimo** etiqueta emergente y `aria-label`:

```html
<button class="iconbtn" aria-label="Ver la ficha de Grupo Automotriz Vértice"
        title="Ver ficha">
  <span class="msi" aria-hidden="true" translate="no">visibility</span>
</button>
```

### 6.6 Pasos numerados con icono (`.pasos`)

Icono en círculo + título + descripción, con un conector vertical entre pasos. Sustituye a un
párrafo de instrucciones corrido cuando hay una secuencia de 2-4 acciones que seguir.

```css
.pasos{list-style:none;display:flex;flex-direction:column;gap:2px}
.pasos li{display:flex;align-items:flex-start;gap:var(--sp-3);padding:9px 0;position:relative}
.pasos li:not(:last-child)::after{content:"";position:absolute;left:15px;top:38px;bottom:-2px;
  width:2px;background:var(--border)}
.paso-ico{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;background:var(--accent-soft);color:var(--accent)}
.paso-txt{font-size:var(--fs-dense);line-height:1.5;color:var(--text-2);padding-top:6px}
.paso-txt b{color:var(--text);font-weight:600}
```

### 6.7 Esqueleto de carga (`.skel`)

```css
.skel{display:block;border-radius:var(--r-ctrl);
  background:linear-gradient(90deg,var(--surface-2) 25%,var(--border) 50%,var(--surface-2) 75%);
  background-size:200% 100%;animation:shimmer 1.4s linear infinite}
@keyframes shimmer{to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){.skel{animation:none;background:var(--surface-2)}}
```

**Hay que aplanar el fondo, no solo parar la animación.** `animation:none` a secas no retira el
degradado: lo **congela** en la posición 0, y cada barra se queda con una rampa visible de
`--surface-2` a `--border`. Quien pide menos movimiento no recibe una barra en reposo, recibe una
barra a medio pintar. Esta línea del documento se escribió incompleta y las tres maquetas del
padrón la copiaron tal cual; el acceso era el único sitio donde estaba bien.

**Sin texto real dentro de las barras.** Un `role="status"` con `aria-label` en el contenedor
basta, y evita que un lector de pantalla lea contenido oculto por `color:transparent`, que sigue
en el árbol de accesibilidad aunque no se vea. Las tres maquetas llevaban dentro de los
esqueletos el texto que imitaban («razón social y RFC», «Grupo Automotriz ELEKTRA»): invisible,
pero anunciado.

```html
<div class="sk" role="status" aria-label="Cargando el padrón de clientes">
  <span class="skel" style="width:26%;height:14px"></span>
  <!-- barras siguientes, todas vacías -->
</div>
```

El esqueleto **imita la forma de lo que va a llegar**, no una forma genérica: mismas columnas y
mismos anchos que la tabla real, para que el contenido no salte al aparecer.

### 6.8 Chip / control secundario (`.chip`)

Botón compacto para acciones de cabecera (tema, idioma).

```css
.chip{display:inline-flex;align-items:center;justify-content:center;gap:7px;
  min-width:40px;min-height:34px;border:1px solid var(--border);background:var(--surface);
  color:var(--text-2);border-radius:var(--r-ctrl);padding:8px 12px;
  font:600 var(--fs-dense) var(--font-ui);cursor:pointer}
.chip:hover{background:var(--surface-2);color:var(--text);border-color:var(--border-2)}
```

### 6.9 Avisos: inline (`.note`) y banda (`.banda`)

**`.note`** — icono + texto sobre fondo tenue de acento. Para información tranquilizadora, no de
alerta.

```css
.note{display:flex;gap:9px;align-items:flex-start;padding:10px 12px;
  background:var(--accent-soft);border-radius:var(--r-ctrl);
  font-size:var(--fs-meta);color:var(--text-2);line-height:1.5}
.note .msi{font-size:17px;color:var(--accent)}
```

**`.banda`** — aviso de ancho completo que califica lo que viene debajo. Cuatro variantes.

```css
.banda{display:flex;gap:var(--sp-3);align-items:flex-start;padding:var(--sp-3) var(--sp-4);
  border-radius:var(--r-ctrl);border:1px solid transparent;font-size:var(--fs-dense);
  line-height:1.55}
.banda .msi{flex-shrink:0}
.banda-info{background:var(--surface-2);color:var(--text-2);border-color:var(--border)}
.banda-warn{background:var(--warn-bg);color:var(--warn-ink)}
.banda-err {background:var(--err-bg); color:var(--err-ink)}
.banda-ok  {background:var(--ok-bg);  color:var(--ok-ink)}
```

**El icono tiene que coincidir con la variante.** El alta de cliente abría con un triángulo de
advertencia sobre una banda neutra: señal mixta, el lector no sabe si preocuparse.

**Un aviso que cambia cómo se interpreta lo de abajo va antes del título de esa sección**, no
después ni al pie. En la ficha, la advertencia de que las listas están recortadas por alcance
—que cambia el significado de todos los ceros que vienen después— se presentaba como una nota
más, al mismo nivel visual que el resto. Va con `role="status"`, icono y contraste propio, antes
del encabezado.

### 6.10 Etiqueta de estado (`.pill`) y de clasificación (`.p-type`)

Dos familias que se parecen y **no son lo mismo**. Confundirlas es el problema transversal más
extendido de las maquetas de origen: bajo el nombre del cliente había cuatro etiquetas en fila
—tipo, estado comercial, estado de expediente y grupo automotriz— todas con la misma forma y
tamaño, así que parecían cuatro valores del mismo campo.

**`.pill` = estado.** Algo que puede cambiar solo: vigente, falta un documento, inactivo.
Lleva color + **icono + texto**, nunca color a secas.

```css
.pill{display:inline-flex;align-items:center;gap:5px;border-radius:var(--r-ctrl);
  padding:3px 9px;font-size:var(--fs-meta);font-weight:700;white-space:nowrap}
.pill .msi{font-size:15px}
.p-ok{background:var(--ok-bg);color:var(--ok-ink)}
.p-warn{background:var(--warn-bg);color:var(--warn-ink)}
.p-err{background:var(--err-bg);color:var(--err-ink)}
.p-block{background:var(--block-bg);color:var(--block-ink)}
.p-pause{background:var(--pause-bg);color:var(--pause-ink)}
```

**`.p-type` = clasificación.** Lo que la cosa **es**: empresa, agencia, persona física, grupo al
que pertenece. No cambia solo y no tiene connotación de bueno ni malo, así que usa las series de
gráfica (§1.4), no el semáforo. Punto de color y peso visual más bajo.

```css
.p-type{display:inline-flex;align-items:center;gap:6px;border-radius:var(--r-ctrl);
  padding:3px 9px;font-size:var(--fs-meta);font-weight:600;color:var(--text-2)}
.p-type::before{content:"";width:7px;height:7px;border-radius:999px;flex-shrink:0;
  background:var(--text-3)}                      /* neutro por omisión */
.p-s1{background:color-mix(in srgb,var(--serie-1) 16%,var(--surface))}
.p-s1::before{background:var(--serie-1)}
.p-s2{background:color-mix(in srgb,var(--serie-2) 16%,var(--surface))}
.p-s2::before{background:var(--serie-2)}
.p-s0{background:var(--surface-2)}               /* conserva el punto neutro */
```

**Todas las de una familia se ven como una familia.** «Persona física» llegó sin punto de color
pero conservando el hueco donde debía ir, así que su texto quedaba desalineado respecto a
«Agencia» y «Empresa». O las tres llevan punto, o ninguna: aquí lleva punto gris neutro, que
distingue sin inventarle una tercera serie.

Cuando haya que poner varias etiquetas seguidas, **se agrupan por significado y se separan
visualmente**: primero clasificación, después estado, con una separación clara entre ambos
grupos y, si el sitio lo permite, un rótulo por grupo.

### 6.11 Tabla densa

El arquetipo del padrón. Es la pantalla más usada del módulo, así que cada gramo de carga visual
se multiplica.

```html
<div class="tabla-caja">
  <table>
    <caption class="sr">Padrón de clientes con RFC, tipo, sucursales, documentos fiscales,
      último movimiento y estado comercial</caption>
    <colgroup><col style="width:26%"><!-- … --></colgroup>
    <thead>
      <tr>
        <th scope="col" aria-sort="none">
          <button data-col="razon">Razón social / RFC
            <span class="msi sort" aria-hidden="true" translate="no">arrow_downward</span></button>
        </th>
        <th scope="col">Tipo</th>
      </tr>
    </thead>
    <tbody>
      <tr><th scope="row">…</th><td data-et="Tipo">…</td></tr>
    </tbody>
  </table>
</div>
<div class="tfoot">…</div>
```

```css
.tabla-caja{overflow-x:auto;position:relative}
table{width:100%;border-collapse:collapse;font-size:var(--fs-dense)}
thead th{text-align:left;color:var(--text-2);font-size:var(--fs-meta);font-weight:700;
  letter-spacing:.04em;text-transform:uppercase;padding:var(--sp-2) var(--sp-3);
  border-bottom:1px solid var(--border);background:var(--surface);
  white-space:nowrap;position:sticky;top:0;z-index:5}
tbody th,td{padding:0 var(--sp-3);height:var(--row-comfy);border-bottom:1px solid var(--border);
  vertical-align:middle;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
tbody th{text-align:left;font-weight:400}
tbody tr:hover td{background:var(--surface-2)}
tbody tr[aria-selected="true"] td{background:var(--accent-soft)}
/* Primera columna congelada al desplazar en horizontal */
thead th:first-child,tbody th:first-child{position:sticky;left:0;background:var(--surface);z-index:6}
thead th:first-child{z-index:7}
```

**Nueve reglas.**

1. **`<caption>` siempre**, aunque vaya oculto con `.sr`. Es lo que dice de qué es la tabla a
   quien no la ve.
2. **`<th scope="row">` en la primera celda** de cada fila: es la que identifica al registro.
3. **`aria-sort` en todas las columnas ordenables**, incluidas las que aún no ordenan
   (`aria-sort="none"`). Si solo lo lleva la columna activa, las demás no se anuncian como
   ordenables.
4. **La cabecera no se corta.** Si «ÚLTIMA O…» no cabe, sobran columnas: se reduce el número de
   columnas visibles de forma explícita, no truncando el rótulo.
5. **Ninguna columna desaparece en silencio.** Ocultar por `@media` sin avisar deja a quien
   trabaja en un portátil pequeño con menos datos sin saber que faltan. O hay desplazamiento
   horizontal, o hay un aviso de cuántas columnas están ocultas con forma de recuperarlas.
6. **Si se ofrece densidad, la compacta reduce contenido, no solo espacio.** Bajar la fila de 40
   a 32px y dejar la misma información produce una pantalla más apretada que se lee peor, sin
   ganar nada. Compacta significa: fila de `--row-compact`, la segunda línea de la celda
   principal pasa a etiqueta emergente, y las listas largas dentro de celda se acortan.

   ```css
   [data-density="compact"] tbody th,[data-density="compact"] td{height:var(--row-compact)}
   [data-density="compact"] .rz small{display:none}
   ```

   **Y la primera pregunta es si hace falta ofrecerla.** El padrón la retiró: dos botones
   permanentes en la barra de filtros, para una preferencia que casi nadie cambia, compiten por
   atención con los controles que sí se usan a diario. Los tokens `--row-comfy`/`--row-compact`
   siguen en el sistema para cuando una pantalla la necesite de verdad.

7. **Una celda no lleva un párrafo.** Una tabla se escanea en vertical; con dos o tres líneas de
   prosa distintas por fila deja de poder escanearse y obliga a leerlo todo. En la celda va la
   etiqueta; el matiz va a etiqueta emergente o a la ficha.
8. **Las dos líneas de la celda principal se distinguen.** El dato principal (razón social) a
   `--fs-dense` en `--text`; el secundario (RFC) a `--fs-meta` en `--text-3`, con aire entre
   ambos. Y el nombre completo accesible al pasar el cursor, porque se corta con puntos
   suspensivos.
9. **Registros por página elegibles.** Un pie que fija seis registros sobre un padrón de 1.248
   obliga a pasar páginas para cualquier revisión. Selector de 10 / 25 / 50 / 100, recordado
   entre sesiones.

**Modo tarjeta por debajo de 860px.** La tabla pasa a lista de tarjetas; cada celda muestra su
rótulo desde `data-et`:

```css
@media (max-width:860px){
  thead{display:none}
  tbody tr{display:block;border:1px solid var(--border);border-radius:var(--r-card);
    margin-bottom:var(--sp-3);background:var(--surface)}
  tbody td{display:grid;grid-template-columns:minmax(88px,34%) 1fr;height:auto;
    white-space:normal;padding:var(--sp-2) var(--sp-3)}
  tbody td::before{content:attr(data-et);font-size:10.5px;font-weight:700;
    letter-spacing:.06em;text-transform:uppercase;color:var(--text-2)}
}
```

### 6.12 Resumen de estatus y barra de filtros

Son **dos zonas distintas**, no una fila. Llegaron mezclados en la misma línea y con la misma
forma de pastilla: tres contadores de estado y cuatro desplegables de filtro, indistinguibles.
No se veía qué era resumen y qué era control.

```
┌ Resumen ───────────────────────────────────────────┐
│  ✓ 1.189 activos   ⏱ 42 incompletos   ⏸ 17 inactivos│   ← lectura (y atajo)
└────────────────────────────────────────────────────┘
┌ Filtros ───────────────────────────────────────────┐
│  Tipo ▾   Estado: Activos ▾   Origen ▾   Quitar todos│  ← control
└────────────────────────────────────────────────────┘
```

**Cinco reglas.**

1. **Un filtro se resalta solo si su valor difiere del predeterminado.** «Tipo: Todos» aparecía
   con borde y fondo de filtro aplicado, y «Todos» no filtra nada. El resalte debe significar
   «aquí hay algo puesto»; si adorna un valor por omisión, deja de significarlo.
2. **Un filtro, un sitio.** El contador «1.189 activos» y el desplegable «Estado: Activos»
   llevaban al mismo resultado sin reflejarse el uno en el otro: pulsar el contador no cambiaba
   el desplegable, y al revés. Si el contador se mantiene como atajo, **al pulsarlo actualiza el
   desplegable**, para que el estado del filtro sea visible en un único lugar.
3. **Los contadores agrupados por criterio.** Cuatro cifras que responden a preguntas distintas
   —dos sobre el expediente documental, una sobre actividad comercial, otra sobre el estado del
   cliente— presentadas iguales parecen cuatro valores del mismo campo e invitan a compararlos.
   Van agrupadas con un rótulo por grupo («Expediente», «Actividad»), o se queda en la barra un
   solo criterio y el resto pasa a filtros.
4. **Los filtros aplicados se ven y se quitan uno a uno**, como etiquetas con «×», más un enlace
   «Quitar todos los filtros».
5. **Los desplegables se ven desplegables**: rótulo + valor + flecha.

```css
.resumen{display:flex;gap:var(--sp-2);flex-wrap:wrap;align-items:center;
  padding:var(--sp-3) var(--sp-6)}
.schip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--border);
  background:var(--surface);border-radius:var(--r-pill);padding:6px 13px;cursor:pointer;
  font:600 var(--fs-meta) var(--font-ui);box-shadow:var(--sh-rest)}
.schip b{font-size:var(--fs-dense);font-weight:800;font-variant-numeric:tabular-nums}
.schip[aria-pressed="true"]{box-shadow:inset 0 0 0 1.5px currentColor,var(--sh-rest)}
.c-ok{color:var(--ok-ink)}     .c-ok[aria-pressed="true"]{background:var(--ok-bg)}
.c-warn{color:var(--warn-ink)} .c-warn[aria-pressed="true"]{background:var(--warn-bg)}
.c-pause{color:var(--pause-ink)}.c-pause[aria-pressed="true"]{background:var(--pause-bg)}

.filtros{display:flex;gap:var(--sp-2);flex-wrap:wrap;align-items:center;
  padding:var(--sp-2) var(--sp-6);border-bottom:1px solid var(--border)}
.f{display:inline-flex;align-items:center;gap:6px;min-height:32px;background:var(--surface);
  border:1px solid var(--border);border-radius:var(--r-pill);padding:6px 12px;
  font-size:var(--fs-meta);color:var(--text-2);cursor:pointer}
.f b{color:var(--text)}
.f[data-activo="true"]{border-color:var(--accent);background:var(--accent-soft);color:var(--text)}
```

### 6.13 Barra de selección

Aparece **solo cuando hay selección**, y se nota que ha aparecido.

```css
.barra-sel{display:none;align-items:center;gap:var(--sp-3);flex-wrap:wrap;
  padding:var(--sp-3) var(--sp-6);background:var(--accent-soft);
  border-block:1px solid var(--border);position:sticky;top:0;z-index:8}
.barra-sel[data-hay="true"]{display:flex}
.barra-sel .destructiva{margin-left:auto}
```

**Cuatro reglas.**

1. **Botones, no enlaces.** «Exportar selección», «Desactivar» y compañía llegaron como `<a>`.
   Un lector de pantalla los anuncia como enlaces, lo que hace esperar que lleven a otra página,
   y con teclado no responden igual. Enlace es lo que navega; botón es lo que ejecuta.
2. **La acción destructiva se separa del grupo**, a la derecha y con espacio de por medio.
   «Desactivar» estaba a un clic de «Exportar selección», que no cambia nada.
3. **Confirma diciendo a cuántos y a quiénes afecta**, con la consecuencia en una línea:
   «Vas a desactivar 2 clientes: Grupo Automotriz ELEKTRA y Flotillas GNP. Dejarán de aparecer
   en el padrón activo; sus órdenes siguen consultables.»
4. **Y se puede deshacer** después.

La barra queda fija mientras haya selección, y siempre muestra cuántos elementos hay
seleccionados y cómo deshacer la selección.

### 6.14 Menú de acciones por fila

Con **una o dos** acciones estables en todas las filas: botones de icono con `aria-label` y
etiqueta emergente. Si el ancho lo permite, texto junto al icono en la acción principal.

Con **más de dos**, o si cambian según la fila: menú `⋯` con las opciones **escritas**.

```html
<button class="iconbtn" aria-haspopup="menu" aria-expanded="false" aria-controls="m-gav"
        aria-label="Más acciones para Grupo Automotriz Vértice">
  <span class="msi" aria-hidden="true" translate="no">more_horiz</span>
</button>
<div class="menu" id="m-gav" role="menu" hidden>
  <button role="menuitem">Ver órdenes</button>
  <button role="menuitem">Reenviar liga de registro</button>
  <button role="menuitem" class="destructiva">Desactivar</button>
</div>
```

Cierra con Escape y devuelve el foco al botón que lo abrió.

### 6.15 Fila desplegable

Detalle que se abre **dentro de la propia fila**, sin sacar a nadie de la lista. Funciona bien y
conviene extenderlo a otros datos que hoy obligan a abrir la ficha.

```html
<tr>
  <th scope="row">
    <button class="suc-btn" aria-expanded="false" aria-controls="suc-gav">
      <span class="msi msi-sm" aria-hidden="true" translate="no">location_on</span>
      <span class="tnum">4</span>
      <span class="msi msi-sm chev" aria-hidden="true" translate="no">expand_more</span>
    </button>
  </th>
</tr>
<tr class="hijas" id="suc-gav" hidden><td colspan="7">…</td></tr>
```

`aria-expanded` y `aria-controls` **tienen que apuntar a algo que exista**. Cuatro de los cinco
botones de sucursales del padrón apuntaban a identificadores inexistentes y anunciaban
«contraído» sobre un control que no hacía nada.

Cierra con Escape, y al cerrar el foco vuelve al botón que lo abrió.

### 6.16 Formulario

```css
.seccion{}                                   /* usa .tarjeta (§6.3) */
.seccion .rejilla{display:grid;gap:var(--sp-4);
  grid-template-columns:repeat(auto-fit,minmax(230px,1fr));padding:var(--sp-4)}
.ctrl{display:flex;flex-direction:column;gap:5px;min-width:0}
.ctrl.ancho{grid-column:1/-1}
.ctrl > label{font-size:var(--fs-meta);font-weight:600;color:var(--text-2)}
.ctrl input,.ctrl select,.ctrl textarea{min-height:38px;padding:9px 11px;
  border:1px solid var(--border-2);border-radius:var(--r-ctrl);
  background:var(--bg);color:var(--text);font:400 var(--fs-dense) var(--font-ui)}
.ctrl .ayuda{font-size:var(--fs-meta);color:var(--text-2);line-height:1.5}
.ctrl .mal{font-size:var(--fs-meta);color:var(--err-ink);font-weight:600;
  display:flex;gap:5px;align-items:flex-start}
.ctrl[data-error="true"] input{border-color:var(--err);box-shadow:0 0 0 1px var(--err)}
/* Dato calculado: no es un campo */
.dato-calc{display:flex;flex-direction:column;gap:3px}
.dato-calc .valor{font-size:var(--fs-base);font-weight:600;color:var(--text)}
@media (pointer:coarse){ .ctrl input,.ctrl select,.ctrl textarea{font-size:max(16px,var(--fs-dense))} }
```

**Ocho reglas.**

1. **Un dato calculado se muestra como dato, no como campo.** «Tipo de cliente» era un
   `<input type="text">` **editable** con el valor `"Se calcula solo"` — se podía borrar y
   escribir cualquier cosa, y esa frase se habría enviado como dato. Etiqueta y valor en texto,
   con el valor real («Empresa»), no la frase que describe el mecanismo, y una nota corta o un
   icono que indique de dónde se deduce.
2. **Dos niveles de obligatoriedad, con palabras distintas.** El aviso de entrada decía que
   bastaban razón social y RFC, y a la vez tres campos llevaban asterisco. No es una
   contradicción de copy: son dos conceptos. **Obligatorio para dar de alta** (sin esto no hay
   registro) y **necesario para facturar o programar** (el registro existe, pero no opera). Se
   nombran distinto y se marcan distinto.
3. **`required` y `aria-required` de verdad.** Los asteriscos eran `<span>` decorativos sin
   `required`, sin `aria-required` y sin leyenda, así que un lector leía «Razón social
   asterisco».
4. **No hay error antes de la interacción.** El domicilio fiscal se pintaba en rojo con el campo
   vacío, antes de que nadie escribiera nada. El error aparece cuando la persona ha pasado por
   el campo.
5. **El error se vincula, no se coloca al lado.** `aria-invalid="true"` en el control y
   `aria-describedby` apuntando al `id` del mensaje. Las tres maquetas tenían cero de ambos: el
   mensaje era texto adyacente, invisible programáticamente.

   ```html
   <div class="ctrl ancho" data-error="true">
     <label for="dom">Domicilio fiscal <span class="req" aria-hidden="true">*</span></label>
     <input type="text" id="dom" aria-required="true" aria-invalid="true" aria-describedby="e-dom">
     <span class="mal" id="e-dom">
       <span class="msi msi-sm" aria-hidden="true" translate="no">error</span>
       Falta el domicilio fiscal. Sin él no se puede timbrar una factura a este cliente.</span>
   </div>
   ```

6. **El tipo de campo es el tipo del dato.** `type="email"`, `type="tel"`, `inputmode="numeric"`
   en el código postal. Todo era `type="text"`, así que en móvil salía el teclado equivocado.
   Y `autocomplete` donde corresponda.
7. **El contador de sección habla en español, no en aritmética.** «2 de 3 obligatorios · 0 de 2
   documentos» obliga a traducir mentalmente qué falta. «Falta el domicilio fiscal» lo dice. Y
   si cuenta, cuenta bien: dos de los contadores de origen no cuadraban con los campos de su
   sección.
8. **Guardado automático o botón de guardar, no los dos.** La barra decía «Borrador guardado
   hace 1 min» y al lado ofrecía «Guardar borrador». Si guarda solo, el botón sobra; si no,
   el mensaje engaña.

**Un botón deshabilitado no recibe el foco**, así que quien navega con teclado pasa de largo y
nunca llega a la explicación de por qué no puede seguir. Se mantiene activable con
`aria-disabled="true"` y al pulsarlo se explica el motivo:

```html
<button class="btn mini" aria-disabled="true" aria-describedby="tope-correo-34">Añadir</button>
<span class="motivo" id="tope-correo-34">Tope: 4 de 4. Retira uno para añadir otro correo.</span>
```

Ese `id` **tiene que ser único**. Con dos contactos en pantalla, los mensajes de tope de correos,
teléfonos y direcciones compartían identificador, así que `aria-describedby` resolvía siempre al
primero: el único mensaje que explicaba el bloqueo nunca llegaba a un lector de pantalla.

**Y si la interfaz dice «retira uno», tiene que existir la forma de retirarlo.** Las listas de
contacto solo tenían botón de editar. Al llegar al tope, el mensaje pedía una acción que no
existía en ninguna parte: un callejón sin salida. Si por trazabilidad no se quiere borrar de
verdad, la salida puede ser «Archivar» o «Marcar como no vigente» — pero tiene que haber salida.

### 6.17 Subida de archivo

Un documento no se pide en una caja de texto. «Constancia de situación fiscal» e «Identificación
del representante» eran `<input type="text">` vacíos, con una ayuda que decía «PDF o foto» y
ningún modo de adjuntar nada.

```html
<div class="ctrl ancho">
  <label for="csf">Constancia de situación fiscal</label>
  <div class="subida" data-estado="vacio">
    <input type="file" id="csf" accept=".pdf,.jpg,.jpeg,.png" aria-describedby="a-csf">
    <p class="ayuda" id="a-csf">PDF o imagen, hasta 10 MB. Arrastra el archivo o pulsa para elegirlo.</p>
    <!-- con archivo: nombre, fecha, y acciones Reemplazar / Quitar -->
  </div>
</div>
```

Indica formatos y peso admitidos, muestra el archivo cargado con su nombre y fecha, y permite
reemplazarlo o quitarlo.

### 6.18 Diálogo modal

**Se usa `<dialog>` nativo con `showModal()`.** El navegador da el velo, la capa superior y la
trampa de foco; lo que sigue siendo trabajo nuestro es a dónde entra el foco al abrir y a dónde
vuelve al cerrar. La alternativa —un `<div role="dialog" aria-modal="true">` en el flujo del
documento— obliga a reimplementar las tres cosas, y en la práctica no se reimplementan.

```css
dialog.modal{border:0;padding:0;margin:auto;   /* margin:auto es el centrado nativo:
    un margin propio lo anula y el diálogo se pega a la esquina */
  max-width:520px;width:calc(100% - 32px);max-height:calc(100dvh - 64px);
  background:var(--surface);color:var(--text);
  border-radius:var(--r-modal);box-shadow:var(--sh-modal)}
dialog.modal[open]{display:flex;flex-direction:column}
dialog.modal::backdrop{background:var(--velo-modal)}
dialog.modal > header{display:flex;align-items:center;gap:var(--sp-3);
  padding:var(--sp-4) var(--sp-5);border-bottom:1px solid var(--border)}
dialog.modal .cuerpo{padding:var(--sp-6) var(--sp-5);display:flex;
  flex-direction:column;gap:var(--sp-5)}
dialog.modal > footer{display:flex;align-items:center;gap:var(--sp-3);
  padding:var(--sp-4) var(--sp-5);border-top:1px solid var(--border)}
```

**Cuatro reglas de foco**, que son las que nadie escribe y todo el mundo incumple:

1. Al abrir, el foco va al **primer control que se puede rellenar** — no al diálogo, no al aspa.
2. Mientras está abierto, `Tab` cicla dentro. Lo da `showModal()`.
3. Al cerrar sin guardar, el foco vuelve **al control desde el que se abrió**.
4. Al cerrar guardando, va **a la fila o el elemento que se acaba de cambiar**; si ya no existe,
   al contenedor más cercano. Nunca al `body`. Ojo: una `<tr>` no recibe foco sin `tabindex="-1"`.

**Mientras una operación está en vuelo, nada cierra el diálogo:** ni Escape, ni el aspa, ni el
clic en el velo. Cerrar a medio guardar deja a alguien sin saber si se guardó.

```js
dlg.addEventListener('cancel', function(e){          // Escape
  if (dlg.dataset.momento === 'guardando') e.preventDefault();
});
```

Tres reglas de contenido, con su detalle y la aritmética de qué formularios caben en un diálogo,
en `docs/patron-dialogo-sio-dproma.md`:

- **El nombre del botón y el contenido coinciden.** «Editar cliente» que solo deja cambiar la
  razón social se llama «Cambiar razón social».
- **Un campo de solo lectura se muestra como dato**, no como campo — pero conservando el motivo.
  Un campo en gris sin explicación se lee como una carencia del formulario; con el motivo al
  lado, como la decisión que es.
- **Detrás va la pantalla real atenuada**, no un esqueleto de carga. Las barras grises se
  confunden con «cargando» y hacen pensar que se ha perdido el sitio en la lista.

**El andamiaje de maqueta no puede vivir fuera del diálogo.** Un modal bloquea todo lo que hay
fuera de la capa superior, así que el panel de estados deja de ser pulsable en cuanto el diálogo
abre. Mientras está abierto, el panel se traslada dentro del `<dialog>`. Es código de maqueta —
en el producto no existe— pero sin él la maqueta no se puede recorrer.

## 7. Layout

### 7.1 Entrada al sistema (`.split`)

Columna de marca (fondo oscuro, ilustración) + columna de acceso, lado a lado desde 920px y
apiladas debajo. Reutilizable en cualquier pantalla de entrada.

```css
.split{display:flex;flex:1;min-height:0}
.brand{flex:1.05;background:#071120;color:#F2F5F7;padding:var(--sp-6) var(--sp-8);min-height:520px}
main.access{flex:1;padding:var(--sp-6) var(--sp-8)}
@media (max-width:920px){ .split{flex-direction:column} .brand{flex:none;min-height:300px} }
```

### 7.2 Cromo de aplicación

Barra lateral de navegación + barra superior + zona de contenido.

```css
.app{display:flex;min-height:100vh}
.side{width:236px;background:var(--chrome);color:var(--chrome-ink);flex-shrink:0}
.side :focus-visible{outline-color:var(--chrome-focus)}
.grp{margin:14px 8px 4px;font-size:10.5px;font-weight:700;letter-spacing:.1em;color:var(--chrome-dim)}
.it{display:flex;align-items:center;gap:10px;min-height:38px;padding:9px 10px;border-radius:7px;
  color:var(--chrome-dim);font-size:var(--fs-dense);text-decoration:none;
  border-left:3px solid transparent}
.it:hover{background:var(--chrome-hover);color:var(--chrome-ink)}
.it[aria-current="page"]{background:var(--chrome-activo);color:var(--chrome-ink);
  font-weight:600;border-left-color:var(--ok)}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
```

Tres anchos: completa (≥1100px), colapsada a solo iconos (860–1100px) y cajón con velo
(<860px). En modo colapsado el rótulo se convierte en etiqueta emergente; no desaparece.

### 7.3 Objetivos táctiles

Todo destino interactivo mide **24×24px como mínimo** (WCAG 2.2, 2.5.8), y 44px si es la acción
principal de la pantalla o el uso es en campo o tableta.

```css
:root[data-tacto="dedo"] .it,
:root[data-tacto="dedo"] .iconbtn,
:root[data-tacto="dedo"] .btn{min-height:46px}
```

Ese bloque existía en las tres maquetas y **nunca se activaba**: el atributo `data-tacto` no
aparecía ni en el markup ni en el JS. Y aunque se hubiera activado, dejaba fuera justo los dos
casos que fallaban:

- **Casillas de selección de 15×15px.** Se amplía el área pulsable sin agrandar el dibujo, o se
  hace pulsable toda la celda:

  ```css
  .selfila{display:flex;align-items:center;min-height:24px;padding:4px;margin:-4px}
  input[type="checkbox"]{width:16px;height:16px;accent-color:var(--accent)}
  ```

- **Botones de orden de cabecera**, a ~19px de alto por un `margin` negativo que compensaba el
  espaciado visual sin agrandar el área. Se les da `min-height:24px` real.

Y los enlaces que son el elemento primario de su fila (un folio, una miga, «Ver en Maps») no
son texto en prosa: llevan padding hasta llegar a 24px.

---

## 8. Voz de producto

Seis de las pantallas revisadas tenían el mismo problema, y no es de diseño visual: **hablaban
en voz de conversación interna**. Párrafos que explican por qué se tomó una decisión, referencias
a documentos del proyecto («Plan §3.4»), códigos internos, y descripciones de la estructura del
formulario («1 campo editable · 1 de solo lectura»).

La separación:

| En pantalla | En la documentación |
|---|---|
| Qué puedo hacer y qué no | Por qué se decidió así |
| «No se puede programar una instalación si faltan datos fiscales» | La regla de negocio completa y su origen |
| Una o dos frases, accionables | El razonamiento, las alternativas descartadas |
| — | Referencias a documentos y códigos de proyecto |

Casos concretos que había que reducir: el alta abría con un solo `<p>` de 554 caracteres antes
del primer campo; el padrón cerraba con tres notas al pie que ocupaban más alto que varias filas
de la tabla; la ficha empezaba la sección de contactos con cinco líneas de explicación, que es
lo primero que se encuentra quien viene a consultar un teléfono.

La prueba: **si el texto explica una decisión, no va en pantalla.** Si explica una consecuencia
para quien está mirando, sí — y en una frase.

---

## 9. Andamiaje de maqueta

Las pantallas llevan un conmutador flotante con «Con datos · Cargando · Vacío · Error». **No es
una función del producto**: son las cuatro formas en que la pantalla puede presentarse según lo
que responda el sistema, no algo que la persona elige. Leído como parte del producto, parece un
filtro más.

Se marca siempre con `data-andamio`, va visualmente separado del producto y **rotulado**:

```html
<aside class="demo" data-andamio role="group"
       aria-label="Controles de la maqueta: ver la pantalla en sus distintos estados">
  <span class="et-g">Vista de maqueta</span>
  <button data-vista="ok" aria-pressed="true">Con datos</button>
  …
</aside>
```

Todo lo que lleve `data-andamio` se retira en la versión real. Un solo selector lo encuentra.

---

## 10. Seis trampas comprobadas

No son teoría: las seis aparecieron aplicando este documento al módulo de clientes, y las
seis se ven solo si se comprueba en el navegador, no leyendo la hoja de estilos.

**El tamaño se mide en el navegador, no en el CSS.** La regla de los 12px se puede burlar sin
querer con la forma abreviada `font:`, donde el tamaño no aparece como `font-size`. Los avatares
del cromo llevaban `font:700 11px var(--font-ui)` y sobrevivieron a una revisión completa de
todos los `font-size` del archivo. Se comprueba con el estilo calculado de cada elemento que
tenga texto.

**Selectores por exclusión, no por enumeración.** El tamaño de los campos estaba definido como
`.ctrl input[type="text"], .ctrl input[type="date"], .ctrl input[type="number"]`. Al cambiar dos
campos a `type="email"` y `type="tel"` —que es lo correcto— se quedaron fuera y colapsaron a
19px de alto. Lo que aplica a todos los campos se escribe
`.ctrl input:not([type="file"]):not([type="checkbox"]):not([type="radio"])`.

**`[hidden]` gana a cualquier regla de estado.** La base del sistema declara
`[hidden]{display:none !important}`. Una vista que se muestre según el estado de la pantalla no
puede llevar `hidden` en el HTML: su visibilidad la gobierna el estado. Con las dos cosas a la
vez, el estado no puede mostrarla nunca y el fallo es silencioso.

**El destino táctil es la región que acepta la pulsación, no el elemento.** Una casilla de 16px
dentro de una `<label>` de 24×24 cumple, porque la etiqueta es el destino. Y al revés: un campo
de búsqueda dentro de un `<div>` con forma de pastilla **no** cumple, porque pulsar la pastilla
no hace nada. El contenedor tiene que ser una `<label for="…">`.

**Un `<symbol>` ya trae su `viewBox`; repetirlo en el `<svg>` que lo invoca descoloca la marca.**
El isotipo se escribe así, con las medidas en el `<use>` y **sin** `viewBox` en el envoltorio:

```html
<svg width="44" height="42" aria-hidden="true">
  <use href="#dproma-mark" width="44" height="42"/>
</svg>
```

Escrito al revés —`viewBox="740 0 970 932"` en el `<svg>` y un `<use>` sin medidas— el `<use>`
toma su tamaño por omisión, el 100% del lienzo, que en ese sistema de coordenadas son 970×932
unidades **empezando en x=0**, mientras que la marca vive a partir de x=740. Resultado: se pinta
32,5px a la izquierda de su caja y se recorta casi entera. No da error, no avisa, y el atributo
sobrante parece lo correcto. Se comprueba midiendo la caja del `<use>` contra la del `<svg>`:
si el desplazamiento no es ~0, está mal.

**Una regla copiada del acceso puede traerse un token que allí existe y aquí no.** El medallón de
error del acceso usa `--err-soft`; su tarjeta usa `--glass-line`. Ninguno de los dos está declarado
en las maquetas del padrón, que tienen `--err-fill` en su lugar. Copiada tal cual, la declaración
entera se invalida en silencio: mismo desenlace que `--sp-5`, pero más traicionero, porque el
archivo de origen se ve perfectamente y la regla parece probada. Cada archivo declara sus propios
tokens en su `:root`, así que el copiar-pegar entre pantallas hay que comprobarlo:

```
usados    = {var(--x) en el <style> y en los style=""}
declarados = {--x: en el <style>}
usados - declarados  →  tiene que ser vacío
```

---

## 11. Checklist al añadir un componente nuevo

**Color y tipografía**
- ¿El contraste está **medido**, no supuesto? 4,5:1 texto / 3:1 gráficos, en los dos temas.
- ¿Se midió también sobre `--surface-2`, y no solo sobre `--surface`?
- ¿Ningún texto baja de 12px?
- ¿Los iconos dentro de un botón heredan el color del botón?

**Estados y jerarquía**
- ¿Un estado se comunica con color **+ icono + texto**, nunca con color solo?
- ¿Las etiquetas de estado y las de clasificación se distinguen a simple vista?
- ¿Un filtro se resalta solo cuando su valor difiere del predeterminado?
- ¿Cada filtro tiene una sola vía de entrada y un solo sitio donde se ve su estado?

**Interacción**
- ¿Todo objetivo interactivo mide 24px o más? (44px si es la acción principal.)
- ¿Un cambio de estado se anuncia (`aria-live`) y mueve el foco?
- ¿Toda acción destructiva confirma, dice a cuántos afecta y se puede deshacer?
- ¿Un botón «ocupado» se bloquea en el manejador, no solo con `pointer-events`?
- ¿Lo que ejecuta es un `<button>` y lo que navega un `<a>`?
- ¿Si la interfaz dice «retira uno», existe la forma de retirarlo?
- ¿El nombre del botón coincide con lo que hace el diálogo que abre?

**Estructura**
- ¿Cada pantalla o vista tiene un encabezado real, no solo texto en negrita?
- ¿Los estados de vacío y error van en tarjeta, con su medallón, y no sueltos sobre el fondo?
- ¿Todos los `id` son únicos, y cada `aria-describedby` / `aria-controls` apunta a algo que
  existe?
- ¿Toda columna ordenable declara `aria-sort`, incluidas las que aún no ordenan?
- ¿Cada icono va acompañado de texto o, como mínimo, de etiqueta emergente y `aria-label`?
- ¿El error deja a la vista el trabajo que la persona ya había hecho?

**Movimiento y voz**
- ¿Toda animación que dure más de 5s se puede pausar pulsándola, sin botón aparte?
- ¿El texto en pantalla dice qué se puede hacer, y no por qué se decidió así?
- ¿Lo que es andamiaje de maqueta lleva `data-andamio` y está rotulado?

**Comprobado en el navegador, no solo leído** (§10)
- ¿El tamaño se midió con el estilo calculado, y no buscando `font-size` en la hoja?
- ¿El selector cubre por exclusión, de modo que no deje fuera un tipo que se añada después?
- ¿Ninguna vista de estado lleva `hidden` en el HTML, que anularía la regla del estado?
- ¿El destino de 24px es el contenedor que acepta la pulsación, y ese contenedor es pulsable?
- ¿Los iconos se vieron con la fuente cargada? Sin red, un glifo roto y el respaldo de la caja
  de 1em se ven igual.
- ¿Se regeneró `icon_names` después del último cambio de markup, y todo icono usado está dentro?
- ¿Ningún icono se dimensiona con `width`/`height` en vez de con `font-size`?
- ¿El isotipo lleva sus medidas en el `<use>` y ningún `viewBox` repetido en el `<svg>`?
  Se comprueba midiendo: la caja del `<use>` debe empezar donde empieza la del `<svg>`.
- ¿Todo token `var(--x)` que usa el archivo está declarado **en ese mismo archivo**? Copiar una
  regla de otra pantalla es la vía habitual de colar uno que no existe aquí.
