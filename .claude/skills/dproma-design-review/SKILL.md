---
name: dproma-design-review
description: Ejecuta el ciclo de calidad de una entrega visual del proyecto DPROMA en sus tres fases — explorar antes, implementar durante, auditar después — encadenando las skills externas de diseño con los guardarraíles del sistema SIO-DPROMA o AZ según corresponda. Úsalo cuando el usuario pida "revisa esta pantalla", "audita esta maqueta", "está lista para enseñar", "revisión de diseño", "monta la pantalla de X", o antes de entregar cualquier HTML del repositorio. Funciona aunque las skills externas no estén instaladas.
---

# Ciclo de calidad de una entrega visual

Este proyecto ya tiene checklist propio (§11), corpus de trampas comprobadas (§10) y contrastes
medidos. Lo que las skills externas añaden es mirada de fuera. Esta skill ordena las dos cosas para
que la externa sea **tercera opinión** y no autoridad, que es el modo en que se pierde un sistema de
diseño sin darse cuenta.

## Antes de nada: qué sistema aplica

No hay un sistema de diseño en este repositorio, hay dos, y **declaran las mismas variables CSS con
valores distintos**. Decide esto primero y déjalo dicho en una línea:

- **AZ / 2894** — `web/investigacion-dproma.html`, `roadmap.html`, `plan-transformacion.html`,
  `entregables.html`, `web/areas/*`, decks. DM Sans, `--accent: #0A46FF`, `--surface: #FFFFFF`.
  Fuente: `web/areas/area.css` y `docs/brand/az-branding-guide.md`.
- **SIO-DPROMA** — `web/entregables/propuestas/*`, `reglas-de-diseno.html`, toda maqueta de producto.
  Inter, `--accent: #3E7A4C`, `--surface: #FAFCFD`. Fuente: `web/entregables/design-rules.md`.

Si la pantalla mezcla los dos, es un bug, no una decisión de estilo.

## Fase ANTES — solo si el arquetipo es nuevo

Sáltatela si la pantalla ya tiene precedente en §6 o en §12.6: copiar el arquetipo existente es
mejor que explorar uno nuevo, y esa es justamente la disciplina que sostiene el sistema.

Si de verdad es nueva, propón `ui-ux-pro-max` con el formato de propuesta de `CLAUDE.md` y espera OK.
Pídele patrones y arquetipos de layout. **Si la respuesta trae hexes o pairings tipográficos, está
fuera de su fase**: se descarta esa parte y se sigue con los tokens del sistema que toque.

Sin la skill: `WebSearch` acotado al sector, más los arquetipos ya documentados.

## Fase DURANTE — al implementar

Propón `taste-skill` con los diales fijados: variance bajo, motion bajo, densidad alta. Los tres
salen de decisiones ya tomadas, no de preferencia.

Manda el sistema, en concreto:

- Escala de 4px y tokens `--sp-*`; radios `--r-*`. Ningún hex literal.
- Suelo tipográfico de 12px. Nada baja de ahí salvo rótulos de grupo a 10,5px.
- `--dur-enter: 300ms` es techo duro. Nada de GSAP ni de ninguna librería de animación.
- Toda animación se pausa pulsando la propia animación, con `<button>` y `aria-pressed`.
- Su ban de em-dash **no se aplica**.

## Fase DESPUÉS — el orden importa

Este es el orden, y es fijo. Cambiarlo es lo que convierte a impeccable en la autoridad.

1. **Checklist §11 del sistema de diseño.** Local, siempre, no negociable. Está en
   `web/entregables/design-rules.md` §11 — léelo, no lo cites de memoria.
2. **`wcag-accessibility`** para el veredicto de accesibilidad. Es la autoridad: 4,5:1 texto, 3:1
   gráfico, táctil 24×24, y cada color medido contra todos los fondos donde puede caer,
   `--surface-2` incluido.
3. **`impeccable`** si está, en modo lectura: `audit`, `critique`, `distill`. Nada que escriba.
   Sus 61 reglas son opinión estética. Contrástalas con §10 antes de aceptar ninguna: varias
   decisiones de este sistema son correctas y una heurística las marcará como error —`--surface` no
   es blanco puro a propósito, hay cinco colores de estado y no dos, `--serie-4` se acepta en 2,62:1
   porque la capa de dashboard exige siempre tabla equivalente—.
4. **Tokens usados menos declarados.** Sobre el archivo tocado, comprueba que no queda ningún `var()`
   sin declarar. Un `var()` que no resuelve invalida la declaración entera y **no da error en
   consola**: es la trampa de §10 que más caro sale.
5. **`git status --short`.** Confirma que no apareció nada nuevo en la raíz. Si aparecieron
   `PRODUCT.md`, `DESIGN.md`, `.impeccable/` o `style-guide.md`, no se commitean: están en
   `.gitignore` por esto.

## Al cerrar

Si el ciclo produjo una regla nueva —no una corrección puntual, una regla—, encadena con
`sio-dproma-design-sync`, que sincroniza las tres piezas del sistema y anota la fila de historial.
Es lo que hace que lo aprendido de fuera entre en el sistema en vez de quedarse en el chat.

Si no produjo regla, dilo y no fuerces una: la mayoría de las revisiones no producen ninguna.

## Si no hay ninguna skill externa instalada

El ciclo sigue funcionando: pasos 1, 2, 4 y 5 son locales, y el 1 son treinta comprobaciones. Dilo en
una línea, nombra lo que falta, y ejecuta. **No digas que usaste una skill que no estaba.**
