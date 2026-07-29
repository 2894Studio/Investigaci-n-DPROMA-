# Investigación DPROMA × 2894_ — Biblia de datos de research

Biblia de datos de investigación y sistema de agentes de Claude Code para el proyecto DPROMA:
procesa entrevistas de research, produce hallazgos estructurados y trazables a evidencia, y los
traduce en una web narrativa de resultados.

**Estado actual:** 6 entrevistas procesadas y anonimizadas · 18 puntos de fricción documentados ·
17 oportunidades priorizadas. Ver la web de hallazgos: se publica como Artifact al pedirlo en esta
sesión de Claude Code, o directamente abriendo `web/index.html` en el navegador (no requiere
servidor ni build).

## Por qué "biblia de datos"

Cada afirmación que aparece en la web tiene que poder trazarse hacia atrás hasta un registro
concreto en `data/insights/`. El dato manda, la narrativa comunica — nunca al revés. Esa disciplina
es la que hace de este repositorio una fuente única de verdad (single source of truth) para el
research de DPROMA, en vez de un conjunto de notas de reunión dispersas.

## Estructura del proyecto

```
.
├── README.md                          ← este archivo
├── 01-ESPECIFICACION-TECNICA.md       ← arquitectura completa del sistema, léela primero
├── .claude/
│   ├── agents/                        ← 6 subagentes especializados (1 lente de análisis c/u)
│   │   ├── flow-extractor.md          ← reconstruye flujos "tal como son hoy"
│   │   ├── pain-point-detector.md     ← clasifica fricciones en las 6 categorías del brief
│   │   ├── tool-inventory-analyst.md  ← cataloga herramientas (manual/digital/IA)
│   │   ├── ai-adoption-analyst.md     ← uso, barreras y actitud frente a IA
│   │   ├── opportunity-mapper.md      ← oportunidades ancladas a dolor + objetivo de negocio
│   │   └── narrative-synthesizer.md   ← viñetas humanas + verificación de anonimización
│   ├── skills/
│   │   ├── dproma-interview-analyzer/SKILL.md   ← orquesta el pipeline de análisis completo
│   │   └── dproma-web-narrative/SKILL.md        ← reconstruye la web a partir del dataset
│   └── commands/
│       └── analizar-entrevista.md     ← /analizar-entrevista <archivo>
├── schema/
│   ├── interview-insight.schema.json  ← contrato de datos único (JSON Schema 2020-12)
│   └── example-output.json            ← referencia de "output correcto" para calibrar agentes
├── data/
│   ├── brief-context.md               ← fuente única de las 6 categorías y 6 objetivos del brief
│   ├── raw/                           ← transcripciones nuevas por procesar (vacío por defecto)
│   ├── insights/                      ← un JSON por entrevista ya procesada (6 hoy)
│   └── aggregate.json                 ← dataset acumulado — la biblia de datos completa
└── web/
    └── index.html                     ← web narrativa, standalone, dataset embebido
```

## Cómo se ve esto por fuera (compartir por link)

- **Vía Artifact de Claude Code (rápido, privado por defecto):** pide en esta conversación
  "publica la web de hallazgos" y se genera un link de `claude.ai/code/artifact/...` que puedes
  compartir desde el menú de share del artifact.
- **Vía GitHub Pages (permanente, con el dominio del repo):** en GitHub, ve a
  *Settings → Pages → Deploy from a branch*, elige la rama de este proyecto y la carpeta `/web` (o
  `/root` sirviendo `web/index.html` como `index.html`). Una vez activado, GitHub publica la web en
  `https://2894studio.github.io/Investigaci-n-DPROMA-/`.
- **Local:** abre `web/index.html` directamente en cualquier navegador — no necesita servidor.

## Cómo se usa (flujo de trabajo)

1. Coloca una transcripción nueva en `data/raw/`.
2. En Claude Code: `/analizar-entrevista data/raw/mi-entrevista.docx`
3. El comando delega a la skill `dproma-interview-analyzer`, que lanza los 6 subagentes en el
   orden correcto (5 en paralelo + `narrative-synthesizer` al final), valida cada salida contra
   `schema/interview-insight.schema.json`, y escribe `data/insights/<entrevista_id>.json` +
   actualiza `data/aggregate.json`.
4. Cuando quieras reflejar las entrevistas nuevas en la web: pide "reconstruye la web de hallazgos
   DPROMA" — se activa la skill `dproma-web-narrative`.

## Principios que se respetan siempre

- **Nunca nombres propios.** Rol + área en vez de nombre, tanto del entrevistado como de terceros
  que mencione (clientes, colegas, agencias) — salvo marcas ya públicas en el brief (ej. BYD,
  Changán).
- **Ninguna cita se publica sin `anonymization_check: "passed"`.** Si un fragmento es demasiado
  específico para anonimizar sin perder sentido, se generaliza o se excluye — nunca se inventa un
  dato falso para camuflarlo.
- **La evidencia manda.** Ningún hallazgo en la web existe sin una cita/evidencia trazable a una
  entrevista concreta en `data/insights/`.
- **Revisión humana antes de publicar.** El pipeline no es 100% automático: cada
  `data/insights/<id>.json` se revisa antes de correr `dproma-web-narrative`.

Ver `01-ESPECIFICACION-TECNICA.md` para la arquitectura completa (por qué subagentes en vez de un
solo prompt, el flujo de ejecución paso a paso, y el detalle de cada lente de análisis) y
`data/brief-context.md` para el contexto de negocio que usan `pain-point-detector` y
`opportunity-mapper`.
