# CLAUDE.md — Investigación DPROMA × 2894_

## Qué es este repo

Biblia de datos de research + sistema de agentes. Markdown, JSON y HTML standalone.
**No hay build, no hay `package.json`, no hay servidor**: todo HTML abre desde disco.
Arquitectura completa en `01-ESPECIFICACION-TECNICA.md`; contexto de negocio en
`data/brief-context.md`.

**Todo en español**: copy, documentación, commits y las propuestas que me hagas o te haga.

## Dos sistemas de diseño, no uno

Conviven dos sistemas que **declaran las mismas variables CSS con valores distintos**. No es un
error: AZ es la marca del estudio, SIO-DPROMA es el sistema del producto.

| Variable | AZ / 2894 | SIO-DPROMA |
|---|---|---|
| `--accent` | `#0A46FF` cobalto | `#3E7A4C` verde |
| `--surface` | `#FFFFFF` | `#FAFCFD` — nunca blanco absoluto |
| `--bg` | `#F7F8FA` | `#F2F5F7` |
| `--text` | `#0B0B0D` | `#1B2430` |
| Fuente | DM Sans, única | Inter (interfaz) + Michroma (wordmark) |
| Secundaria | `--surface-alt` | `--surface-2` |

**Qué archivo pertenece a cuál:**

- **AZ** → `web/investigacion-dproma.html`, `roadmap.html`, `plan-transformacion.html`,
  `entregables.html`, `web/areas/*`, decks y diagramas para stakeholder.
- **SIO-DPROMA** → `web/entregables/propuestas/*`, `reglas-de-diseno.html`, toda maqueta de producto.

**Nunca se fusionan ni se deriva uno del otro.** Antes de tocar un color o una fuente, decide cuál
aplica. Fuentes: `web/areas/area.css` y `docs/brand/az-branding-guide.md` para AZ;
`web/entregables/design-rules.md` para SIO-DPROMA.

## Innegociables

Valores completos en `web/entregables/design-rules.md` y `docs/criterios-de-animacion.md`.
**No se citan de memoria: se leen.**

- **Ningún hex literal en un componente.** Todo pasa por token. Un `var()` que no resuelve no cae a
  un valor por omisión: **invalida la declaración entera y falla en silencio** (el caso `--sp-5`:
  tres paddings computando a 0). Al copiar una regla de otra pantalla, comprueba `usados − declarados = ∅`.
- **Tipografía SIO:** `Inter` en interfaz, `Michroma`/`Ethnocentric` solo en el wordmark. El `<link>`
  de Google Fonts no es opcional. Escala `--fs-meta 12` · `--fs-dense 13` · `--fs-base 14` ·
  `--fs-sub 16` · `--fs-title 20` · `--fs-kpi 30`. **El suelo son 12px**; única excepción, 10,5px en
  rótulos de grupo. Un dato que se lee a diario va a 12–13px como mínimo.
- **Espaciado:** escala de 4px, `--sp-1..12`. Radios `--r-ctrl 6` · `--r-card 10` · `--r-modal 16` ·
  `--r-pill 999`. El nombre del token no es el multiplicador.
- **Movimiento:** `--dur-enter: 300ms` es **techo duro**, no sugerencia. `--ease-spring` solo en
  píldora de pestañas y tarjeta de kanban. `prefers-reduced-motion` conserva opacidad y color y
  elimina todo desplazamiento y escala, congelando en el **último** fotograma, nunca en el inicial
  vacío. Toda animación se pausa **pulsando la propia animación** —el contenedor es un `<button>` con
  `aria-pressed`—, jamás con un botón «Pausar» aparte. Nada parpadea más de 3 veces por segundo.
  **Sin librerías de animación: CSS y SVG bastan.**
- **Contraste medido, no estimado.** 4,5:1 texto, 3:1 texto grande y elemento gráfico. Cada color se
  mide contra **todos** los fondos donde puede caer, `--surface-2` incluido — ese fue el error de
  `--text-3` durante toda la v1. Objetivo táctil 24×24px, 44px si es acción principal o uso en campo.
  Un estado se comunica con color **+ icono + texto**, nunca con color solo.
- **`--accent` no es `--ok`, a propósito.** «Se puede pulsar» no es «está bien». Y una serie de
  gráfica nunca reutiliza un color de estado: `--serie-1..4` existen justo para clasificar sin opinar.
- **§8 Voz de producto:** en pantalla va qué puedo hacer y qué no, en una o dos frases accionables.
  El porqué, las alternativas descartadas y las referencias a documentos viven en la documentación.
  La prueba: si el texto explica una decisión, no va en pantalla.
- **Anonimización:** rol + área, jamás nombres propios. Ninguna cita se publica sin
  `anonymization_check: "passed"`. Ningún hallazgo existe sin evidencia trazable a `data/insights/`.

## Quién es dueño de qué

- `docs/sistema-diseno-sio-dproma.md`, `web/entregables/design-rules.md` y
  `web/entregables/reglas-de-diseno.html` son **las tres piezas que solo toca
  `sio-dproma-design-sync`**, y siempre las tres a la vez, con su fila de historial.
- **Nada se escribe en la raíz del repo.**
- **Ninguna skill externa escribe archivos.** Produce material que nosotros aplicamos.

## Skills externas: las tres fases

Precedencia: **skill local del repo > skill de Anthropic ya instalada > skill externa.**

| Fase | Skill | Para qué | Guardarraíl |
|---|---|---|---|
| **Antes** | `ui-ux-pro-max` | Explorar patrones y arquetipos de sector | Prohibido: paletas, pairings, generador de design system, cualquier hex. Salida = referencias, no tokens |
| **Durante** | `taste-skill` | Densidad, ritmo y motion al implementar | GSAP vetado. Ban de em-dash desactivado. Techo de 300ms |
| **Después** | `impeccable` | Tercera opinión crítica | Solo `audit`, `critique`, `distill`. Vetado todo lo que escriba. El veredicto de accesibilidad lo firma `wcag-accessibility` |

Routing completo, desambiguación frente a `dataviz`/`artifact-diagramming`/`pptx`/`code-review`, y
fichas por skill: **`docs/skills-externas-routing.md`**. Diagnóstico: `/estado-skills`.

## Proactividad

Cuando una tarea encaje con una skill del sistema, la propongo **antes de empezar**, en una línea,
con este formato, y **espero tu OK**:

> Propongo `<skill>` en fase `<antes|durante|después>` para `<qué produce>`.
> Guardarraíl: `<qué no va a tocar>`. Si no está, lo hago con `<fallback>`. ¿OK?

Nunca la aplico en silencio y nunca instalo nada. **Una propuesta por tarea, no por turno**: si ya la
propuse para esta tarea y la declinaste, no insisto.

## Degradación

Este contenedor es efímero y arranca sin plugins; una sesión web normalmente no tiene ninguna de las
siete. **La ausencia de una skill nunca bloquea una tarea**: lo digo en una línea, nombro el
sustituto y sigo. Fallbacks en `docs/skills-externas-routing.md` §4.

Y la regla que de verdad importa: **no digo «usando X» si X no está.** El riesgo no es que falte la
skill, es que diga que la usé y produzca la salida a ojo.

## Comprobado en el navegador

Trampas de §10 que más cuestan: el tamaño de fuente se mide con **estilo calculado** —la forma
abreviada `font:` esconde el tamaño—; `[hidden]` gana a cualquier regla de estado y `:last-child` no
distingue lo oculto; `icon_names` del subconjunto de Material Symbols se regenera al añadir un icono
o el navegador pinta el nombre en letras.
