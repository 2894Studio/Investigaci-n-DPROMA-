---
title: Reglas de diseño — DPROMA × 2894 Studio
version: 1.0.0
last_updated: 2026-08-31
description: Documentación viva del sistema de diseño ya implementado en las páginas de este proyecto (color, tipografía, espaciado, componentes, principios). Fuente combinada de docs/brand/az-branding-guide.md y los valores reales presentes en el CSS de web/entregables.html, web/areas/area.css y web/entregables/atencion-al-cliente.html.
---

# Reglas de diseño

Este documento es la referencia canónica del sistema de diseño usado en todas las páginas del proyecto (informe general, áreas, entregables). Combina la guía de marca (`az-branding-guide.md`) con los valores exactos ya implementados en el CSS, para que cualquier página nueva pueda replicar el sistema sin adivinar cifras.

También existe una versión visual de este documento, con muestras renderizadas de cada regla, en [`/entregables/reglas-de-diseno`](/entregables/reglas-de-diseno).

## Color

### Paleta de marca

| Token | Valor | Rol |
|---|---|---|
| `cloud-white` | `#F7F8FA` | Fondo principal claro |
| `sky-blue` | `#7DB7FF` | Acento secundario |
| `deep-cobalt` | `#0A46FF` | Color de marca — CTAs, acento único por grid |
| `soft-gray` | `#E6E8EC` | Superficie neutra secundaria |
| `ink-black` | `#0B0B0D` | Texto principal, superficie oscura |

### Tokens semánticos (modo claro)

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `var(--cloud-white)` | Fondo de página |
| `--surface` | `#FFFFFF` | Fondo de tarjetas/paneles |
| `--surface-alt` | `var(--soft-gray)` | Cabeceras de tabla, hover de fila |
| `--text` | `var(--ink-black)` | Texto principal |
| `--text-muted` | `#53565f` | Texto secundario |
| `--border` | `#d8dbe2` | Bordes, separadores de sección |
| `--accent` | `var(--deep-cobalt)` | Enlaces, focus, acentos |
| `--accent-soft` | `var(--sky-blue)` | Acento secundario |
| `--shadow` | `0 1px 2px rgba(11,11,13,.04), 0 8px 24px rgba(11,11,13,.06)` | Sombra estándar de tarjeta |

Modo oscuro: se activa automáticamente por `prefers-color-scheme: dark`, y puede forzarse con `data-theme="dark"` / `data-theme="light"` en el elemento raíz. En oscuro, `--bg` pasa a `#0B0B0D`, `--surface` a `#16171c`, `--accent` a `#3D6BFF`.

**Regla de marca**: nunca introducir colores cálidos (naranja, amarillo, rojo, verde). Usar como máximo una tarjeta cobalt por grid de 3.

## Tipografía

**DM Sans** es la única familia tipográfica del sistema (con `system-ui, -apple-system, sans-serif` como fallback). La jerarquía se construye solo con peso y tamaño, nunca mezclando tipografías.

### Pesos

| Peso | Valor | Uso típico |
|---|---|---|
| Light | 300 | Copy largo, descripciones secundarias |
| Regular | 400 | Cuerpo de texto, body por defecto |
| Medium | 500 | Nav, subtítulos |
| Bold | 700 | Wordmark, titulares, `h1`/`h2`/`h3`, eyebrow |

### Escala real (tal como se usa hoy)

| Elemento | Tamaño | Detalle |
|---|---|---|
| `.eyebrow` | `0.75rem` | 700, `letter-spacing: 0.14em`, uppercase |
| `h1` (hero) | `clamp(2rem, 4.4vw, 3.25rem)` | 700, `line-height: 1.08` |
| `h2` (section-head) | `clamp(1.5rem, 3vw, 2rem)` | 700 |
| `.card h3` | `1.0625rem`–`1.25rem` | 700 |
| Cuerpo / lede | `0.9375rem`–`1.0625rem` | 400, `line-height: 1.55` |
| `.footer-meta` | `0.8125rem` | 400 |

## Espaciado y layout

| Elemento | Valor |
|---|---|
| Ancho máximo de contenido (`.wrap`) | `1120px`, padding lateral `clamp(1.25rem, 4vw, 2.5rem)` |
| Padding de sección | `clamp(2.5rem, 6vw, 4rem)` vertical |
| Padding de hero | `clamp(3rem, 8vw, 5.5rem)` arriba |
| Gap de grid de tarjetas | `1.25rem` |
| Padding de `.card` | `1.5rem` |
| Padding de `.deliverable-card` | `1.75rem` |
| Radio de `.card` | `18px` |
| Radio de `.deliverable-card` | `20px` |
| Radio de tabla (`.table-scroll`) | `14px` |
| Radio de badges/pills | `999px` |

Separadores entre secciones: `border-top: 1px solid var(--border)`.

## Componentes

- **`.eyebrow`** — etiqueta uppercase con punto de color delante, en `--accent`.
- **`.card` + `.card-neutral` / `.card-brand` / `.card-dark`** — tarjeta base con 3 variantes de fondo; grid 3-up (`.card-grid`), colapsa a 2 columnas (`≤900px`) y 1 columna (`≤560px`). Regla: máximo una `.card-brand` por grid.
- **`.deliverable-card`** — tarjeta-enlace para listar entregables, con badge, título, descripción y flecha "Ver informe →"; hover eleva `-3px` y resalta el borde con `--accent`.
- **Tabla (`.table-scroll` + `table`)** — cabecera uppercase sobre `--surface-alt`, filas con `border-bottom`, hover de fila.
- **`.resp-list`** — lista sin viñetas nativa, cada ítem con guión `—` en `--accent` delante.
- **Masthead** — wordmark + nav de anclas, idéntico en todas las páginas.
- **Footer / `.footer-nav`** — enlace de retorno en `--accent`, meta info en `--text-muted`.

## Principios (de la guía de marca)

**Hacer**
- Palette restringida a los 5 tokens de marca.
- Wordmark solo en DM Sans Bold, uppercase.
- Un titular poético + una línea funcional en cada hero/card.
- Una sola tarjeta cobalt como "featured" por grid de 3.

**Evitar**
- Colores cálidos en cualquier parte del sistema.
- Una segunda tipografía para dar contraste.
- Botones con forma de píldora (pill) — las esquinas son suavemente redondeadas, no circulares.
- Sobrecargar de texto las imágenes/zonas con mucho whitespace.

## Historial de cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-08-31 | Primera versión: documenta el sistema ya implementado (color, tipografía, espaciado, componentes, principios). |
