# Sistema de diseño — Acceso SIO-DPROMA

Referencia técnica para construir SIO-DPROMA reutilizando el diseño del acceso.

**Fuente:** `web/entregables/propuestas/acceso-sio-dproma.html`. No es un mockup — es la
pantalla real, con los 19 puntos de la revisión de UX/UI/accesibilidad ya corregidos: contraste
verificado (4,5:1 texto / 3:1 gráficos), bloqueo de doble envío también por teclado, estados
anunciados a lectores de pantalla, objetivos táctiles ≥24px. Todo lo que hay aquí ya pasó por
esa revisión — ver `web/entregables/recomendaciones-login.html#sio` para el detalle de cada
punto y el porqué.

Estos son los tokens de la **pantalla de acceso**. Si SIO-DPROMA crece a un dashboard completo
(tablas, sidebar, filtros), va a necesitar tokens adicionales que aquí no están —
`--fs-title`/`--fs-kpi` para títulos y cifras grandes, una escala de fila `--row-comfy`/
`--row-compact` para tablas densas, colores de estado `--warn`/`--block` además de `--ok`/
`--err`. No se inventan aquí: se añaden cuando haga falta esa pantalla, siguiendo el mismo
patrón de nombres.

---

## 1. Color

Dos temas, claro y oscuro, seleccionados por `prefers-color-scheme` o forzados con
`data-theme="dark"` / `data-theme="light"` en el `<html>`.

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--bg` | `#F2F5F7` | `#10161F` | Fondo de página |
| `--surface` | `#FAFCFD` | `#171F2C` | Superficie sólida (botones, respaldo de `.glass`) |
| `--surface-2` | `#E7EDF3` | `#1D2735` | Superficie secundaria (esqueleto de carga) |
| `--border` | `rgba(27,36,48,.14)` | `rgba(231,236,242,.12)` | Borde sutil |
| `--border-2` | `rgba(27,36,48,.26)` | `rgba(231,236,242,.24)` | Borde de control interactivo |
| `--text` | `#1B2430` | `#E7ECF2` | Texto principal |
| `--text-2` | `#4C5A6B` | `#A8B3C2` | Texto secundario |
| `--text-3` | `#66717F` | `#8B96A6` | Texto auxiliar, 12px — medido a 4,74:1 sobre `--bg` en claro |
| `--accent` | `#3E7A4C` | `#4A8F5A` | Marca / acción principal |
| `--accent-ink` | `#F7FAF9` | `#08120D` | Texto sobre `--accent` |
| `--accent-soft` | `rgba(62,122,76,.10)` | `rgba(74,143,90,.16)` | Fondo tenue de acento (iconos, avisos) |
| `--ok` / `--ok-ink` | `#2F8F6F` / `#22705A` | `#4FBF98` / `#4FBF98` | Estado positivo |
| `--err` / `--err-ink` | `#C24238` / `#B03A31` | `#EE6E5F` / `#EE6E5F` | Estado de error |
| `--err-soft` | `rgba(194,66,56,.10)` | `rgba(238,110,95,.14)` | Fondo tenue de error (icono del estado) |
| `--link` | `#2F6B3C` | `#7FC08F` | Enlaces de texto |

```css
:root{
  --bg:#F2F5F7; --surface:#FAFCFD; --surface-2:#E7EDF3;
  --border:rgba(27,36,48,.14); --border-2:rgba(27,36,48,.26);
  --text:#1B2430; --text-2:#4C5A6B; --text-3:#66717F;
  --accent:#3E7A4C; --accent-ink:#F7FAF9; --accent-soft:rgba(62,122,76,.10);
  --ok:#2F8F6F; --err:#C24238; --ok-ink:#22705A; --err-ink:#B03A31;
  --err-soft:rgba(194,66,56,.10); --link:#2F6B3C;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){ color-scheme:dark;
  --bg:#10161F; --surface:#171F2C; --surface-2:#1D2735;
  --border:rgba(231,236,242,.12); --border-2:rgba(231,236,242,.24);
  --text:#E7ECF2; --text-2:#A8B3C2; --text-3:#8B96A6;
  --accent:#4A8F5A; --accent-ink:#08120D; --accent-soft:rgba(74,143,90,.16);
  --ok:#4FBF98; --err:#EE6E5F; --ok-ink:#4FBF98; --err-ink:#EE6E5F;
  --err-soft:rgba(238,110,95,.14); --link:#7FC08F;
} }
:root[data-theme="dark"]{ /* mismos valores que el bloque de arriba, para forzar el tema
  sin depender de prefers-color-scheme */ color-scheme:dark; }
```

Un tercer color vive fuera de estos tokens porque es de marca, no de interfaz: `#C7D97B`
(verde lima), usado solo en el wordmark y el anillo de foco sobre la columna oscura de marca.
No se usa en controles de la interfaz.

**Regla de contraste:** texto normal 4,5:1 mínimo, texto grande (≥24px, o ≥18,66px en negrita)
y elementos gráficos 3:1 mínimo. Cada color nuevo que se añada a la paleta se mide contra los
fondos donde va a aparecer antes de darlo por bueno — no se asume por parecido visual.

---

## 2. Tipografía

- **Interfaz:** `Inter` (400, 500, 600, 700). Toda la interfaz — texto, botones, formularios.
- **Marca:** `Michroma` / `Ethnocentric Rg` (`--font-brand`), solo para el wordmark
  «SIO-DPROMA» y el nombre «DPROMA» en la columna de marca. Nunca en texto de interfaz.

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Michroma&display=swap" rel="stylesheet">
```

| Token | Tamaño | Uso |
|---|---|---|
| `--fs-meta` | 12px | Pie, referencias, texto auxiliar |
| `--fs-dense` | 13px | Subtítulos, cuerpo de tarjeta compacto |
| `--fs-base` | 14px | Cuerpo de texto por defecto |
| `--fs-sub` | 16px | Subtítulo destacado |

Los títulos de tarjeta (`.glass h1`) no usan un token de escala — van a 18-21px fijo según el
peso visual que necesite el estado (21px en el acceso, 18px en los estados de resultado). Al
extender el sistema a pantallas con títulos de sección o cifras grandes, retomar
`--fs-title`/`--fs-kpi` de la maqueta original (20px / 30px) en vez de inventar un tamaño nuevo.

---

## 3. Espaciado y radios

Escala base 4px (`--sp-2` = 2×4, `--sp-6` = 6×4...), aunque el nombre del token no es el
multiplicador — es un identificador arbitrario, no una fórmula a extrapolar sin mirar la tabla:

```css
--sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-6:24px; --sp-8:32px;
--r-ctrl:6px; --r-card:10px; --r-modal:16px;
```

| Token | Valor | Uso |
|---|---|---|
| `--sp-2` | 8px | Separación mínima (icono-texto, gap entre chips) |
| `--sp-3` | 12px | Gap interno de fila (paso numerado, botón) |
| `--sp-4` | 16px | Padding de control, gap entre bloques cortos |
| `--sp-6` | 24px | Padding de sección, margen entre grupos |
| `--sp-8` | 32px | Padding de la tarjeta principal, columnas del layout |

La maqueta original define además `--sp-1` (4px) y `--sp-12` (48px) para los extremos —
espaciado mínimo entre elementos muy pegados, y separación grande entre secciones—, que la
propuesta de acceso no llegó a necesitar. Añadirlos si hace falta ese rango, en vez de usar un
valor suelto fuera de la escala.

| Token | Valor | Uso |
|---|---|---|
| `--r-ctrl` | 6px | Botones, chips, campos |
| `--r-card` | 10px | Tarjetas internas menores |
| `--r-modal` | 16px | La tarjeta principal (`.glass`) |

---

## 4. Sombra y superficie translúcida

```css
--sh-rest:0 1px 2px rgba(19,29,43,.07);   /* reposo */
--sh-float:0 6px 18px rgba(19,29,43,.10); /* hover */
--sh-modal:0 24px 60px rgba(19,29,43,.20);/* la tarjeta flotante */
--glass:rgba(250,252,253,.74);
--glass-line:rgba(27,36,48,.10);
```

La tarjeta principal usa `backdrop-filter: blur(16px)` sobre `--glass`. Como no todos los
navegadores lo soportan, lleva respaldo sólido — sin esto, en un navegador sin soporte el fondo
queda semitransparente y el texto se lee mal sobre lo que haya detrás:

```css
.glass{
  background:var(--glass); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--glass-line); box-shadow:var(--sh-modal); border-radius:var(--r-modal);
}
@supports not (backdrop-filter:blur(1px)){ .glass{ background:var(--surface) } }
```

---

## 5. Movimiento

```css
--dur-micro:120ms; --dur-base:200ms; --dur-enter:300ms;
--ease-out:cubic-bezier(.23,1,.32,1);
```

**Criterio del proyecto, obligatorio para toda animación nueva:** se pausa pulsando la propia
animación — el contenedor es un `<button>` con `aria-pressed`, nunca un botón «Pausar» aparte.
Detalle completo, incluida la trampa del `prefers-reduced-motion` global del sitio, en
`docs/criterios-de-animacion.md`.

---

## 6. Componentes

### 6.1 Botón primario (`.gbtn`)

El único botón de acción principal de la pantalla. Se bloquea en el manejador de JS, no solo
con CSS: `pointer-events:none` detiene el ratón pero no el teclado, y en la maqueta original
cuatro Intro sobre el botón «ocupado» disparaban cuatro envíos.

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

### 6.2 Botones de acción (`.btn`, `.btn--p`)

Los de los estados de resultado (Reintentar, Solicitar acceso, Cerrar sesión). Mínimo 44px de
alto — por encima del mínimo de 24px de WCAG 2.5.8, para que sean cómodos también en táctil.

```css
.btn{flex:1 1 auto;min-height:44px;display:inline-flex;align-items:center;justify-content:center;
  gap:8px;padding:11px 16px;border-radius:var(--r-ctrl);border:1px solid var(--border-2);
  background:var(--surface);color:var(--text);font:600 var(--fs-dense) var(--font-ui);cursor:pointer}
.btn--p{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
```

### 6.3 Tarjeta de estado única (`.glass` + `.vista`)

Un solo contenedor `.glass`, con las vistas dentro como hermanos que se muestran/ocultan por
`hidden`. **No** una tarjeta suelta por estado: la pantalla no debe cambiar de forma según lo
que tenga que decir, y así el usuario no pierde la referencia visual al pasar de cargando a
error.

```html
<div class="glass" id="tarjeta" tabindex="-1">
  <div class="vista" id="v-acceso">…</div>
  <div class="vista" id="v-cargando" role="status" aria-label="Comprobando tu acceso" hidden>…</div>
  <div class="vista estado" id="v-vacio" hidden>…</div>
  <div class="vista estado estado--err" id="v-error" hidden>…</div>
</div>
```

Cada cambio de vista **anuncia el cambio y mueve el foco** a la tarjeta — sin esto, quien usa
lector de pantalla no se entera de que la pantalla cambió:

```js
function muestra(clave, mueveFoco){
  Object.keys(VISTAS).forEach(function(k){
    document.getElementById(VISTAS[k].el).hidden = (k !== clave);
  });
  regionLive.textContent = VISTAS[clave].dice;   // aria-live="polite" en algún <p class="sr">
  if (mueveFoco) tarjeta.focus();
}
```

Cada estado de resultado (vacío, error) lleva un **encabezado real** (`<h1>`, no negrita
suelta) — es lo que permite navegar la página saltando de encabezado en encabezado con un
lector de pantalla.

### 6.4 Iconos (`.msi`)

Material Symbols Rounded, variante rellena (`FILL@1`). Buscar y elegir el icono en
[fonts.google.com/icons](https://fonts.google.com/icons) — filtrar por estilo **Rounded** (no
Outlined ni Sharp, para que combine con el resto) y copiar el nombre exacto que aparece debajo
del icono (p. ej. `account_circle`), que es el mismo nombre que va en el HTML y en `icon_names`
del `<link>`.

Se cargan por subconjunto —solo los nombres que se usan— para no pedir la fuente completa. Al
añadir un icono nuevo, se añade su nombre a la lista de `icon_names` del `<link>` existente, no
se crea un `<link>` aparte:

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,1,0&icon_names=account_circle,badge,cloud_off,login,lock,logout,refresh,support_agent&display=block" rel="stylesheet">
```

Los cuatro ejes del nombre de familia (`opsz,wght,FILL,GRAD@24,500,1,0`) fijan el aspecto para
todos los iconos que pidas con ese `<link>` — tamaño óptico 24, peso 500, relleno activado,
grado neutro. No hace falta tocarlos por icono; se heredan igual en `font-variation-settings`
de `.msi`.

```css
.msi{font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;
  font-size:20px;line-height:1;display:inline-block;white-space:nowrap;direction:ltr;
  width:1em;height:1em;overflow:hidden;  /* si el icono no está en el subconjunto o la fuente
    no carga, el navegador pinta el nombre en letras — la caja fija de 1em×1em evita que eso
    rompa el layout */
  font-variation-settings:'FILL' 1,'wght' 500,'GRAD' 0,'opsz' 24}
```

Siempre `aria-hidden="true"` y junto a su texto — el icono nunca es la única forma de entender
qué hace un control:

```html
<span class="msi" aria-hidden="true" translate="no">refresh</span>Reintentar
```

### 6.5 Pasos numerados con icono (`.pasos`)

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

### 6.6 Esqueleto de carga (`.skel`)

Sin texto real dentro de las barras — un `role="status"`/`aria-label` en el contenedor basta, y
evita que un lector de pantalla lea contenido oculto por opacidad (que sigue en el árbol de
accesibilidad aunque no se vea).

```css
.skel{display:block;border-radius:var(--r-ctrl);
  background:linear-gradient(90deg,var(--surface-2) 25%,var(--border) 50%,var(--surface-2) 75%);
  background-size:200% 100%;animation:shimmer 1.4s linear infinite}
```

```html
<div role="status" aria-label="Comprobando tu acceso">
  <span class="skel" style="width:52px;height:52px;border-radius:50%"></span>
  <!-- barras siguientes, todas vacías -->
</div>
```

### 6.7 Chip / control secundario (`.chip`)

Botón compacto para acciones de cabecera (tema, idioma).

```css
.chip{display:inline-flex;align-items:center;justify-content:center;gap:7px;
  min-width:40px;min-height:34px;border:1px solid var(--border);background:var(--surface);
  color:var(--text-2);border-radius:var(--r-ctrl);padding:8px 12px;
  font:600 var(--fs-dense) var(--font-ui);cursor:pointer}
.chip:hover{background:var(--surface-2);color:var(--text);border-color:var(--border-2)}
```

### 6.8 Aviso inline (`.note`)

Icono + texto sobre fondo tenue de acento. Para información tranquilizadora, no de alerta.

```css
.note{display:flex;gap:9px;align-items:flex-start;padding:10px 12px;
  background:var(--accent-soft);border-radius:var(--r-ctrl);
  font-size:var(--fs-meta);color:var(--text-2);line-height:1.5}
.note .msi{font-size:17px;color:var(--accent)}
```

---

## 7. Layout base (`.split`)

Columna de marca (fondo oscuro, ilustración) + columna de acceso, lado a lado desde 920px y
apiladas debajo. Reutilizable en cualquier pantalla de entrada al sistema.

```css
.split{display:flex;flex:1;min-height:0}
.brand{flex:1.05;background:#071120;color:#F2F5F7;padding:var(--sp-6) var(--sp-8);min-height:520px}
main.access{flex:1;padding:var(--sp-6) var(--sp-8)}
@media (max-width:920px){
  .split{flex-direction:column}
  .brand{flex:none;min-height:300px}
}
```

---

## 8. Checklist de accesibilidad al añadir un componente nuevo

- ¿El contraste está medido, no supuesto? 4,5:1 texto / 3:1 gráficos, en los dos temas.
- ¿Todo objetivo interactivo mide 24px o más de alto? (44px si es la acción principal).
- ¿Un cambio de estado se anuncia (`aria-live`) y mueve el foco?
- ¿Cada pantalla o vista tiene un encabezado real, no solo texto en negrita?
- ¿Un botón «ocupado» se bloquea en el manejador, no solo con `pointer-events`?
- ¿Toda animación que dure más de 5s se puede pausar pulsándola, sin botón aparte?
- ¿Cada icono va acompañado de texto, y nunca es la única fuente de significado?
