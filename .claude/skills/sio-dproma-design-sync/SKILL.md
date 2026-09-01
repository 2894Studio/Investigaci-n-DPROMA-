---
name: sio-dproma-design-sync
description: Sincroniza una regla o componente nuevo del sistema de diseño SIO-DPROMA en las tres piezas que deben quedar coherentes — la fuente técnica, la copia descargable y la página renderizada — y anota el cambio en el historial de versiones. Úsalo cuando el usuario pida "actualiza el sistema de diseño", "documenta este componente en design-rules", "sube de versión el sistema de diseño", "añade esta regla a SIO-DPROMA", o pida reflejar un hallazgo/corrección de diseño (color, tipografía, espaciado, accesibilidad) en la documentación del sistema.
---

# Sincronización del sistema de diseño SIO-DPROMA

## Principio rector
El sistema de diseño de SIO-DPROMA no vive en un solo archivo. Un cambio que solo toca uno de
los tres deja a las otras dos desincronizadas — un token que cambió en el `.md` pero sigue
literal en el HTML, o una versión subida sin fila en el historial. Esta skill existe para que
un cambio de diseño se propague siempre completo, en el mismo orden, o se declare explícitamente
qué parte no aplica.

## Las tres piezas y su rol

| Archivo | Rol |
|---|---|
| `docs/sistema-diseno-sio-dproma.md` | Fuente técnica real. Aquí se decide y redacta la regla primero. |
| `web/entregables/design-rules.md` | Copia descargable del mismo sistema, con su propio front matter (`version`, `last_updated`) y su propia sección `## Historial de cambios` al final. |
| `web/entregables/reglas-de-diseno.html` | Página renderizada de las mismas reglas — los tokens de color/espaciado/tipografía están repetidos ahí como variables CSS en `:root`. |

No existe `CHANGELOG.md` independiente ni carpeta `docs/components`: el historial y la
documentación de componentes viven embebidos en `design-rules.md` / `reglas-de-diseno.html`.

## Orden de propagación (no saltarse pasos)

1. **Aplica el cambio primero en `docs/sistema-diseno-sio-dproma.md`.** Es la fuente. Redacta la
   regla con el mismo tono técnico y estructura por sección (§) que ya usa el archivo.
2. **Propaga el mismo contenido a `web/entregables/design-rules.md`**, en la sección con el mismo
   número (§) que en el paso 1. El texto puede variar levemente si `design-rules.md` ya lo
   contextualiza distinto (es "copia descargable", no un espejo byte a byte), pero el valor del
   token, la regla o el racional deben ser idénticos.
3. **Actualiza `web/entregables/reglas-de-diseno.html`** si el cambio toca:
   - una variable CSS en `:root` (color, espaciado, radio, sombra, tipografía) → cambia el valor
     ahí también, nunca lo dejes solo en el `.md`;
   - un componente documentado visualmente en la página → refleja el cambio en su marcado/estilo.
   Si el cambio es puramente de redacción o racional sin ningún impacto visual (p. ej. "por qué"
   se eligió un valor, sin cambiar el valor), **no toques el HTML** — pero dilo explícitamente en
   el resumen final al usuario, no lo omitas en silencio.
4. **Añade una fila a "Historial de cambios"** en `web/entregables/design-rules.md` (tabla al
   final del archivo, columnas `Versión | Fecha | Cambios`):
   - Sube versión con semver: **patch** (x.x.N) para aclaraciones o correcciones menores sin
     cambiar comportamiento; **minor** (x.N.0) para una regla o componente nuevo documentado;
     **major** (N.0.0) para un cambio que rompe un token o valor que ya se usaba en pantallas
     existentes.
   - Fecha: la fecha real de hoy.
   - Descripción: concreta, referencia la sección (§) afectada, explica el **motivo** del cambio
     (qué hallazgo o revisión lo dispara), no solo repite "qué" cambió — sigue el estilo de las
     entradas ya existentes (1.0.0 → 1.5.0) como referencia de tono y nivel de detalle.
5. **Actualiza el front matter de `design-rules.md`** (`version:` y `last_updated:`) para que
   coincidan exactamente con la versión y fecha que acabas de añadir al historial.

## Verificación antes de terminar

- El número de versión y la fecha del front matter de `design-rules.md` coinciden con la última
  fila de su tabla de historial.
- Ningún hex literal quedó fuera de un token en ningún componente tocado — la regla de fondo que
  el propio `design-rules.md` declara al inicio ("ningún hex literal en un componente, todo pasa
  por un token; cuando algo no tenga token, se añade siguiendo el patrón de nombres").
- Si el cambio tocó una variable CSS, el mismo valor aparece igual en `docs/sistema-diseno-sio-dproma.md`,
  `web/entregables/design-rules.md` y `web/entregables/reglas-de-diseno.html` — sin divergencias.
- El resumen final al usuario dice qué se tocó en cada uno de los tres archivos, y explícitamente
  si alguno se dejó sin cambios y por qué.
