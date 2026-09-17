---
title: Skills externas — routing, guardarraíles y fallbacks
version: 1.0.0
last_updated: 2026-09-17
description: Qué skill externa se usa en cada tarea, en qué fase, qué no se le deja hacer, y con qué se sustituye cuando no está instalada. El resumen operativo vive en CLAUDE.md; aquí está el detalle.
---

# Skills externas — routing, guardarraíles y fallbacks

Este proyecto ya tiene un aparato de calidad propio y bastante afilado: un sistema de diseño en
versión 2.2.5 con contrastes medidos uno a uno, seis trampas documentadas, un checklist de
componente nuevo y una sección de voz de producto. Lo que no tiene es **mirada de fuera**. Todas
esas reglas salieron de revisar nuestras propias pantallas, así que el sistema no ve lo que nunca
se le ocurrió mirar.

Las siete skills que se documentan aquí sirven para eso, y solo para eso. Ninguna es autoridad sobre
nada que ya esté decidido y medido en `web/entregables/design-rules.md`. La relación es de consulta,
no de gobierno: **ellas opinan, el sistema decide**.

---

## 0. Cómo se instalan

Instalación **global**, en tu máquina. El repositorio no las vendoriza: aquí solo vive la capa de
reglas. Comandos verificados contra el `.claude-plugin/marketplace.json` de cada repositorio el
**2026-09-17**.

| Skill | Comandos | Licencia |
|---|---|---|
| ui-ux-pro-max | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`<br>`/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` | MIT |
| impeccable | `/plugin marketplace add pbakaus/impeccable`<br>`/plugin install impeccable@impeccable` | Apache 2.0 |
| taste-skill | `/plugin marketplace add Leonxlnx/taste-skill`<br>`/plugin install taste-skill@taste-skill` | MIT |
| frontend-slides | `/plugin marketplace add zarazhangrui/frontend-slides`<br>`/plugin install frontend-slides@frontend-slides` | MIT |
| diagram-design | `/plugin marketplace add cathrynlavery/diagram-design`<br>`/plugin install diagram-design@diagram-design` | MIT |
| understand-anything | `/plugin marketplace add Egonex-AI/Understand-Anything`<br>`/plugin install understand-anything@understand-anything` | MIT |

**stop-slop no tiene marketplace.** Es una carpeta de skill plana —`SKILL.md` más
`references/{phrases,structures,examples}.md`—. Dos formas de instalarla:

```bash
git clone https://github.com/hardikpandya/stop-slop /tmp/stop-slop
cp -r /tmp/stop-slop ~/.claude/skills/stop-slop
```

O subirla como skill de cuenta en claude.ai (Ajustes → Capacidades → Skills), que además la
sincroniza a las sesiones web. Licencia MIT.

### Qué NO se instala, y por qué

- **`npx impeccable install`.** Compila un CLI en Rust, instala hooks propios y escribe en carpetas
  de una docena de proveedores. Nos quedamos con la capa markdown del plugin: es la que aporta el
  criterio, y el resto mete dependencias y automatismos de terceros dentro del flujo.
- **El dashboard y el grafo de Understand-Anything.** Necesita Node, tree-sitter y llamadas a una
  API de LLM para construir el índice. Este repositorio no tiene código de aplicación que indexar.

### El alcance real de «global»

Un `/plugin marketplace add` persiste en la máquina donde lo ejecutas. Las sesiones remotas —Claude
Code en web o móvil— corren en un contenedor efímero que arranca vacío, así que **ahí no estará
ninguna**. Es el caso normal, no el caso límite, y por eso la sección 4 existe.

Si en algún momento quieres cobertura también en web sin vendorizar nada, el canal es subir las
skills a tu cuenta de claude.ai: eso sí se sincroniza a cada sesión. Funciona bien con las que son
carpeta plana (stop-slop, y el `SKILL.md` de taste-skill y diagram-design) y peor con las que
dependen de comandos de plugin.

---

## 1. Tabla de routing

Precedencia, siempre: **skill local del repo > skill de Anthropic ya instalada > skill externa.**

| Tarea | Skill | Fase | Guardarraíl |
|---|---|---|---|
| Analizar transcripción de entrevista | `dproma-interview-analyzer` (local) | — | Ninguna externa participa en el pipeline de research |
| Diseñar un guion de entrevista | `ux-interview-guide` | — | Contexto desde `data/brief-context.md`, en español |
| Journey map | `ux-user-journey` | — | Trazable a `data/insights/` |
| Test A/B o de usabilidad | `ab-test-generator` | — | Entrevista al usuario antes de generar |
| Pantalla nueva: explorar | `ui-ux-pro-max` | **antes** | Solo patrones, arquetipos de layout y referencias |
| Pantalla nueva: implementar | `taste-skill` | **durante** | Diales fijados, GSAP vetado, techo de 300ms |
| Pantalla nueva: auditar | `impeccable` + `wcag-accessibility` | **después** | Vía `dproma-design-review`. impeccable en lectura |
| Revisión de código, bugs | `code-review` | — | No `impeccable:critique` |
| Simplificar código | `simplify` | — | No `impeccable:distill` |
| Gráfico, dashboard, KPI | `dataviz` + §12 | durante | Paleta `--serie-1..4` del proyecto. Tabla equivalente obligatoria |
| Esquema de flujo o arquitectura | `diagram-design` | durante | Recibe explícitamente qué sistema aplica |
| Presentación para stakeholder | `frontend-slides` | durante | Tokens AZ, nunca SIO |
| Redactar o humanizar un documento | `stop-slop` vía `dproma-texto-humano` | después | Método sí, listas inglesas no |
| Copy de pantalla de producto | Prueba de §8, local | durante | Aquí stop-slop sobra |
| Entender el repo o el impacto de un cambio | `understand-anything` | antes | Sin grafo, sin tree-sitter, sin API |
| Cambiar el sistema de diseño | `sio-dproma-design-sync` (local) | — | Ninguna externa, jamás |

### Desambiguación

Conviven unas veinte skills y varias dicen «design» en su descripción. Sin estas reglas escritas, la
elección la decide el parecido del texto, que es la peor forma de decidirla.

- **`dataviz` es dueña de cualquier gráfico de datos.** Gobierna la capa de dashboard de §12 con
  Chart.js. Ni `ui-ux-pro-max` ni `diagram-design` entran ahí. Y su paleta por defecto
  (`references/palette.md`) se sustituye por `--serie-1..4`, que están validadas contra daltonismo
  en los dos temas.
- **`diagram-design` es para esquemas conceptuales sin datos**: flujos, arquitecturas, secuencias.
- **`artifact-diagramming` sigue siendo dueña cuando el entregable es un artifact de chat**, no un
  HTML del repositorio.
- **`wcag-accessibility` es la autoridad en accesibilidad.** Las 61 reglas de impeccable son opinión
  estética; el veredicto de accesibilidad lo firma wcag, y las cifras de contraste de nuestro sistema
  están medidas y no las sobreescribe una heurística.
- **`frontend-slides` por defecto para presentaciones.** `anthropic-skills:pptx` solo si pides
  literalmente un `.pptx`.
- **El pipeline de entrevistas no se toca.** `ux-interview-guide` diseña guiones,
  `dproma-interview-analyzer` los analiza. Ninguna skill nueva entra ahí.

---

## 2. Las tres de diseño, en detalle

Las tres prometen lo mismo —«que el frontend no parezca hecho por IA»— y las tres se activarían con
la frase «diseña esta pantalla». Por eso el criterio que las separa es **la fase**, escrita como
regla, y no la descripción de cada una.

### ui-ux-pro-max — fase ANTES

**Qué se toma:** las 192 reglas de razonamiento por industria y los arquetipos de layout. Sirve
cuando hay que construir un arquetipo que §6 todavía no cubre y conviene ver cómo lo resuelven otros
antes de decidir.

**Qué se descarta:** sus 192 paletas, sus 74 pairings tipográficos y su generador de design system.
No porque sean malos, sino porque aquí ya hay uno, medido, y un segundo sistema que se le parezca es
peor que no tener ninguno.

**Salida esperada:** una lista de referencias y decisiones de layout. Si la respuesta trae hexes,
está fuera de su fase.

### taste-skill — fase DURANTE

**Diales fijados**, no negociables por la skill:

| Dial | Valor | Por qué |
|---|---|---|
| `DESIGN_VARIANCE` | bajo | El sistema existe para que dos pantallas se parezcan |
| `MOTION_INTENSITY` | bajo | §5 fija 300ms de techo y sutileza por defecto |
| `VISUAL_DENSITY` | alto | El arquetipo dominante es tabla densa de trabajo diario |

**Vetos:** sus esqueletos canónicos de GSAP —`criterios-de-animacion.md` §4 dice literalmente «sin
librerías: CSS y SVG bastan para todo lo que hay en este sitio»— y su ban duro de em-dash, por lo
que explica la sección 3.

Sus curvas de easing se traducen a `--ease-out`, `--ease-in-out` o `--ease-spring`, o se descartan.

### impeccable — fase DESPUÉS

**Comandos permitidos:** `audit`, `critique`, `distill`. Los tres leen y devuelven informe.

**Comandos vetados:** `polish`, `craft`, `shape`, `animate` y cualquier otro que escriba en el
repositorio. También su registro de contexto en `PRODUCT.md` y `DESIGN.md`, que ya están en
`.gitignore` como cinturón de seguridad.

El motivo es concreto, no una precaución genérica: un `DESIGN.md` en la raíz se leería como la
fuente de verdad del diseño y competiría con `docs/sistema-diseno-sio-dproma.md`, que sí lo es y que
además tiene dos copias sincronizadas. `sio-dproma-design-sync` no sabría de su existencia, así que
la desincronización sería invisible hasta que alguien construyera una pantalla con el documento
equivocado.

---

## 3. Lo que ninguna skill externa puede hacer

Lista cerrada. Si una sugerencia cae aquí, no se discute: se descarta y se sigue.

1. **Redefinir un token o proponer una paleta.** Los valores están en `design-rules.md` §1 y en
   `area.css`, y están medidos.
2. **Fusionar los dos sistemas de diseño**, o derivar uno del otro. Son dos, deliberadamente.
3. **Generar un design system.** Ya hay uno, en versión 2.2.5.
4. **Escribir cualquier archivo del repositorio**, y en particular en la raíz o en las tres piezas
   que sincroniza `sio-dproma-design-sync`.
5. **Aplicar un ban de em-dash a la documentación.** Ver abajo.
6. **Sustituir una cifra de contraste medida por una estimación heurística.**
7. **Introducir una librería de animación.**
8. **Escribir en inglés.**

Sobre la quinta: el repositorio tiene 1.055 em-dash, 138 solo en `design-rules.md` y 115 en
`sistema-diseno-sio-dproma.md`. `cambios-ux-ui-administracion-vehicular_analisis.md` lo cataloga como
técnica deliberada de humanización. Y a la vez, la entrada 2.2.5 del historial celebra haber sacado
la última raya de la página renderizada. No es una contradicción: es **una regla por superficie, ya
tomada y medida** — sí en prosa y documentación, donde es ortografía española correcta; minimizada
en copy de producto, donde §8 quiere frases secas. Un ban global la rompería en las dos direcciones
y produciría un diff de cientos de líneas que nadie pidió.

Sobre la sexta, con casos concretos que una heurística marcará como error siendo correctos:
`--surface` no es blanco puro a propósito; hay cinco colores de estado y no dos; `--serie-4` queda
en 2,62:1 sobre superficie clara y se acepta **porque** la capa de dashboard exige siempre etiqueta
visible o tabla equivalente; `--text-3` vale `#5C6675` y no `#66717F` por una medición contra
`--surface-2`.

---

## 4. Fallbacks

Qué se hace con cada tarea cuando la skill no está. Diagnóstico rápido: `/estado-skills`.

| Ausente | Sustituto | Qué se pierde |
|---|---|---|
| ui-ux-pro-max | `WebSearch` acotado al sector + los arquetipos de §6 y §12.6 | El catálogo de 79 estilos. La fase se mantiene |
| taste-skill | §5 Movimiento, `criterios-de-animacion.md` y §3 Espaciado | Poco: los diales ya estaban fijados a valores del proyecto |
| impeccable | Checklist §11 completo + `wcag-accessibility` | La mirada de fuera. §11 son 30 comprobaciones y para este repo cubre más que sus 61 reglas |
| stop-slop | La rúbrica de `_analisis.md`, 5 criterios sobre 100 | El corpus de patrones. La rúbrica propia ya dio 87/100 |
| frontend-slides | HTML standalone con tokens AZ a mano | Los 12 presets. Es lo que ya son `plan-transformacion.html` y `areas/*` |
| diagram-design | SVG inline siguiendo `artifact-diagramming` | Los 39 tipos y el export a PNG |
| understand-anything | `Grep`, `Glob` y `git log` | Nada apreciable en este repositorio |

**La ausencia de una skill nunca bloquea una tarea.** Se dice en una línea qué falta y con qué se
sustituye, y se sigue. No se propone instalar salvo que lo preguntes.

Y una regla de honestidad, que cubre el fallo más sutil de todos: **no se dice «usando X» si X no
está**. El riesgo real no es que falte la skill; es que se diga que se usó y la salida se produzca a
ojo con el mismo aplomo.

---

## 5. Dependencias que aquí no existen

`ui-ux-pro-max` trae scripts de Python. `frontend-slides` necesita `python-pptx` para convertir PPT
y Playwright para exportar a PDF. `diagram-design` necesita Playwright para exportar a SVG y PNG.

No hay `package.json` ni entorno de Python del proyecto, y el contenedor remoto es efímero. Los
exports se tratan como opcionales: **la salida primaria es siempre HTML o SVG autocontenido**, que
además es exactamente lo que el repositorio ya produce.

---

## 6. Deuda anotada

`--focus-w`, `--focus-offset` y `--grid` se usan en `docs/sistema-diseno-sio-dproma.md` sin estar
declarados en sus tablas de tokens; solo existen en los HTML. Es un verdadero positivo, y es
literalmente la trampa que §10 describe. Cuando una auditoría externa lo saque, **no se arregla en
caliente**: entra por `sio-dproma-design-sync` con subida de versión y fila de historial, como
cualquier otro cambio del sistema.

---

## Historial de cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-09-17 | Documento inicial. Incorpora siete skills externas (ui-ux-pro-max, impeccable, taste-skill, stop-slop, frontend-slides, diagram-design, understand-anything) con instalación global, routing por fases, y fallback por skill. El criterio que separa las tres de diseño es la fase, no la descripción, porque las tres se activan con la misma frase. Deja por escrito la colisión entre los dos sistemas de tokens —`--accent`, `--surface`, `--bg` y `--text` tienen valores distintos en AZ y en SIO-DPROMA— que era el riesgo mayor de incorporar herramientas que generan paletas. Y fija la política de em-dash por superficie, que el proyecto ya practicaba sin tenerla escrita. |
