# Especificación técnica — Sistema de agentes de análisis de entrevistas DPROMA

**Proyecto:** 2894_ Studio × DPROMA
**Propósito:** Sistema de agentes y skills para Claude Code que procesa guiones/transcripciones de entrevistas de investigación de usuarios y produce hallazgos estructurados + una web narrativa.
**Autor de la especificación:** Claude, para Juan Carlos Díez Rodríguez (2894_ Studio)

---

## 1. Contexto y principio de diseño

DPROMA está construyendo una herramienta interna (CRM + módulos operativos + app móvil offline para instaladores) para reemplazar una operación hoy gestionada por WhatsApp, Excel y memoria institucional. 2894_ está conduciendo entrevistas de research con los stakeholders (Rocío, Óscar, Alexander, Jhonatan, Mauricio, Héctor, Nayeli, Enrique, Arnulfo, Gabriel, Diana, Nacho…) para alimentar la Fase 1 (priorización) del proyecto.

El problema de diseño no es solo "extraer datos de un PDF". Es que Gemini ya produce actas decentes pero **planas**: resúmenes de reunión, no evidencia estructurada reutilizable ni narrativa que un stakeholder de negocio (Arnulfo, Diana) entienda de un vistazo. El sistema que se especifica aquí cierra esa brecha en dos pasos:

1. **Análisis estructurado** (agentes especializados → JSON validado por esquema).
2. **Traducción narrativa** (skill de síntesis → web editorial, no un dashboard de tablas).

Principio rector: *la evidencia manda, la narrativa comunica*. Ningún hallazgo en la web puede existir sin una cita/evidencia trazable a una entrevista concreta; pero ninguna cita aparece en la web sin pasar por anonimización de rol.

---

## 2. Arquitectura general

```
                         ┌─────────────────────────────┐
                         │   /dproma:analizar-entrevista │  (slash command, orquestador)
                         └───────────────┬──────────────┘
                                          │ 1. lee transcripción (docx/pdf)
                                          │ 2. lanza 5 subagentes EN PARALELO (Task tool)
                    ┌─────────────────────┼─────────────────────┬───────────────────┬─────────────────┐
                    ▼                     ▼                     ▼                   ▼                 ▼
           flow-extractor        pain-point-detector   tool-inventory-analyst  ai-adoption-analyst  opportunity-mapper
           (flujos paso a paso)  (fricción, cuellos     (herramientas: manual/  (uso y barreras IA)  (oportunidades,
                                  de botella)            digital/IA)                                  priorizadas)
                    │                     │                     │                   │                 │
                    └─────────────────────┴─────────────────────┴───────────────────┴─────────────────┘
                                          │  cada subagente devuelve JSON validado contra el esquema
                                          ▼
                         ┌─────────────────────────────┐
                         │   narrative-synthesizer      │  (subagente 6º, corre DESPUÉS, no en paralelo)
                         │   - fusiona los 5 outputs     │
                         │   - anonimiza por rol         │
                         │   - redacta viñetas humanas   │
                         └───────────────┬──────────────┘
                                          ▼
                         data/insights/<entrevista-id>.json   (registro por entrevista)
                         data/aggregate.json                  (dataset acumulado, todas las entrevistas)
                                          │
                                          ▼
                         ┌─────────────────────────────┐
                         │  skill: dproma-web-narrative  │  (se invoca manualmente o al acumular N entrevistas)
                         │  reconstruye web/index.html   │
                         └─────────────────────────────┘
```

### Por qué subagentes y no un solo prompt largo

Un solo agente intentando "extraer flujos + dolor + herramientas + barreras IA + oportunidades" a la vez tiende a homogeneizar categorías (todo dolor se ve una oportunidad, todo flujo se ve un dolor). Separar en subagentes con **una sola lente cada uno** y contexto acotado (solo Read/Grep sobre la transcripción, sin escritura) da:

- Salidas más consistentes por categoría (cada prompt está optimizado para un solo tipo de juicio).
- Paralelización real (los primeros 5 no dependen entre sí → menor latencia).
- Auditoría más fácil: si un hallazgo está mal clasificado, se corrige un prompt, no el sistema entero.

El `opportunity-mapper` sí requiere ver `pain_points` y el brief de objetivos de DPROMA para "enganchar" cada oportunidad a un objetivo estratégico (los 6 objetivos específicos del brief) — se le pasa el output de `pain-point-detector` como contexto adicional, no la transcripción cruda otra vez.

El `narrative-synthesizer` corre en serie al final porque necesita **todos** los outputs para no repetir historias y para aplicar anonimización de forma consistente (un mismo entrevistado no debe quedar re-identificable combinando pistas de varias secciones).

---

## 3. Componentes de Claude Code

### 3.1 Subagentes (`.claude/agents/*.md`)

Cada subagente es un archivo Markdown con frontmatter YAML (`name`, `description`, `tools`, `model`). Se invocan vía el Task tool desde el comando orquestador, o automáticamente si Claude Code detecta que la descripción calza con la petición del usuario.

Herramientas permitidas: **solo `Read`, `Grep`, `Glob`** (nunca `Bash`/`Write`/`Edit`) — los subagentes de análisis son de solo lectura por diseño; esto evita que un prompt-injection dentro de una transcripción (ej. texto pegado por un entrevistado) pueda hacer que un agente escriba o ejecute algo.

Ver `.claude/agents/`:
- `flow-extractor.md`
- `pain-point-detector.md`
- `tool-inventory-analyst.md`
- `ai-adoption-analyst.md`
- `opportunity-mapper.md`
- `narrative-synthesizer.md`

### 3.2 Skills (`.claude/skills/*/SKILL.md`)

Dos skills, con responsabilidades distintas a los agentes: los agentes **analizan una entrevista**; las skills **orquestan el proceso repetible** y **saben las reglas de negocio/estilo** que no cambian entrevista a entrevista.

- `dproma-interview-analyzer/SKILL.md` — orquesta el pipeline completo (lanzar los 6 subagentes en el orden correcto, validar contra el JSON Schema, escribir a `data/`). Se activa con: "analiza esta entrevista de Dproma", "procesa este guion", o al detectar un archivo de entrevista nuevo en `data/raw/`.
- `dproma-web-narrative/SKILL.md` — sabe el sistema de diseño (tono, tipografía, principios narrativos) y las reglas de anonimización para reconstruir `web/index.html` a partir de `data/aggregate.json`.

### 3.3 Slash command (`.claude/commands/analizar-entrevista.md`)

Punto de entrada explícito: `/analizar-entrevista <ruta-al-archivo>`. Es un comando fino — delega toda la lógica a la skill `dproma-interview-analyzer`; su único rol es fijar el argumento de entrada y confirmar al usuario qué se va a procesar antes de lanzar los 6 subagentes (evita que se dispare por error sobre un archivo equivocado).

### 3.4 Esquema de datos (`schema/interview-insight.schema.json`)

Contrato único que los 6 subagentes deben respetar. Ver sección 5.

---

## 4. Flujo de ejecución paso a paso

1. **Usuario:** `/analizar-entrevista data/raw/entrevista-nayeli-cruz.pdf`
2. **Comando** confirma alcance ("Voy a analizar la entrevista de [rol], ~45 min, 5 lentes de análisis") y delega a la skill.
3. **Skill `dproma-interview-analyzer`:**
   a. Extrae texto de la transcripción (usa `extract-text` o lectura de PDF según formato).
   b. Genera un `entrevista_id` anonimizado por rol + fecha (ej. `2026-07-16_seguimiento-proveedor-tech`), **nunca el nombre real**, para que ese identificador pueda circular por el resto del pipeline sin exponer PII.
   c. Lanza los 5 subagentes de primera capa **en paralelo**, pasándoles: el texto completo de la transcripción + el `entrevista_id` + fragmento relevante del brief (objetivos, situación actual) como contexto compartido.
   d. Recibe 5 JSON, valida cada uno contra el esquema (aborta y reporta si algo no valida — no intenta "reparar" datos silenciosamente).
   e. Lanza `opportunity-mapper` con: `pain_points` ya extraídos + los 6 objetivos específicos del brief.
   f. Lanza `narrative-synthesizer` con los 5 JSON completos; su output incluye las viñetas humanas y el veredicto de anonimización.
   g. Escribe `data/insights/<entrevista_id>.json` (registro completo) y actualiza `data/aggregate.json` (append).
4. **Usuario, en otro momento:** "reconstruye la web con las últimas entrevistas" → se activa `dproma-web-narrative`, que lee `data/aggregate.json` y regenera `web/index.html`.

### Puntos de control humano (no es un pipeline 100% automático)

- Después del paso 3.f, el sistema **no publica automáticamente** ninguna cita en la web sin que la skill marque explícitamente `anonymization_check: "passed"`. Si un fragmento es demasiado específico para anonimizar sin perder sentido (ej. "el ingeniero que antes lideraba instalaciones y ahora solo gestoría vehicular" — hay un único rol así en la empresa), el `narrative-synthesizer` debe marcarlo `anonymization_check: "needs_review"` y generalizarlo aún más o excluirlo, nunca inventar un dato falso para camuflarlo.
- Juan Carlos revisa `data/insights/<id>.json` antes de correr `dproma-web-narrative` — el sistema está pensado para acompañar el research, no para reemplazar la lectura del investigador.

---

## 5. Estructura de datos de salida

Ver `schema/interview-insight.schema.json` para el contrato completo (JSON Schema Draft 2020-12) y `schema/example-output.json` para un ejemplo poblado con datos reales anonimizados de las 5 entrevistas ya realizadas (Rocío/Nayeli/Alexander-Jhonatan/Jesus Ignacio/Enrique/Mauricio).

Resumen de las 6 secciones por entrevista:

| Sección | Qué responde | Generado por |
|---|---|---|
| `meta` | ¿Quién (rol, no nombre), cuándo, cuánto duró? | orquestador |
| `workflows` | ¿Cómo se hace hoy, paso a paso? | `flow-extractor` |
| `pain_points` | ¿Dónde duele, y cuánto? | `pain-point-detector` |
| `tools_inventory` | ¿Con qué herramientas (manual/digital/IA)? | `tool-inventory-analyst` |
| `ai_adoption` | ¿Cuánta IA usan hoy y qué lo frena? | `ai-adoption-analyst` |
| `opportunities` | ¿Qué se podría mejorar, y con qué prioridad? | `opportunity-mapper` |
| `narrative` | Viñeta humana anonimizada para la web | `narrative-synthesizer` |

---

## 6. Skills y prompts — resumen de cada lente de análisis

(El texto completo de cada prompt vive en su archivo `.claude/agents/*.md`; aquí el resumen de criterio.)

### `flow-extractor`
Reconstruye el flujo **tal como es hoy** (no como debería ser), en pasos ordenados con actor + acción + herramienta + canal. Regla dura: si la transcripción no deja claro un paso, se marca `"unclear": true` en vez de inferir — evita flujos "bonitos" que no reflejan la realidad operativa (ej. el alta de cliente de Nayeli: WhatsApp → petición de documentos → Excel manual → confirmación — no se "limpia" el paso informal de WhatsApp aunque no sea la versión ideal).

### `pain-point-detector`
Clasifica cada fricción en una de 6 categorías fijas (`proceso_manual`, `falta_centralizacion`, `comunicacion_informal`, `dependencia_externa`, `falta_estandarizacion`, `falta_visibilidad_kpis` — tomadas literalmente de la sección "Situación actual" del brief de DPROMA, para que el vocabulario de research calce con el vocabulario que ya usa el cliente). Cada pain point lleva severidad (baja/media/alta) justificada por impacto operativo declarado, no por percepción del agente.

### `tool-inventory-analyst`
Cataloga cada herramienta mencionada con su tipo (`manual`, `digital`, `ia`) y su nivel de adopción (`ninguna`, `básica`, `intermedia`, `avanzada`). Debe distinguir explícitamente entre herramienta usada **por decisión personal** del entrevistado (ej. el Excel "chafita" de Jesus Ignacio) y herramienta **impuesta por la organización** — esa distinción es oro para priorizar qué digitalizar primero (lo personal-informal es más fácil de reemplazar sin resistencia).

### `ai-adoption-analyst`
No pregunta "¿usan IA?" en abstracto — busca 3 señales: (1) casos de uso reales ya en marcha, (2) barreras explícitas nombradas por el entrevistado (ej. desconfianza de Enrique tras recibir datos falsos de agencias), (3) tono/actitud (resistente / cauteloso / curioso / campeón). Un entrevistado puede tener uso alto y actitud cautelosa a la vez (Mauricio: usa IA para renders y redacción, pero "paso a paso para asegurar la calidad") — el esquema permite ambos valores simultáneamente sin forzar una sola etiqueta.

### `opportunity-mapper`
Cada oportunidad debe enlazar a ≥1 `pain_point_id` y a ≥1 de los 6 objetivos específicos del brief DPROMA (centralizar en CRM, conocer a profundidad cada área, integrar IA responsablemente, estandarizar procesos/formatos, formar al equipo en Gemini, dotar a instaladores de app offline). Una oportunidad sin dolor de origen ni objetivo de negocio asociado se descarta — evita que el sistema "invente" mejoras cosméticas.

### `narrative-synthesizer`
Convierte lo anterior en 1–3 viñetas humanas por entrevista para la web. Reglas de anonimización:
- Nunca nombre propio, ni de la persona ni de terceros que mencione (clientes, agencias, colegas) salvo que sea una marca ya pública en el brief (ej. "BYD", "Changán" como marcas de auto, que son contexto público del sector, no dato personal).
- Rol + área en vez de nombre ("la persona que gestiona el alta de clientes ante Enteratec", no "Nayeli").
- Si un dato temporal o numérico hace identificable a una sola persona en la organización (ej. "la única persona que factura para 4 agencias"), se generaliza ("quien concentra la facturación de varias agencias bajo una sola razón social").

---

## 7. Web interactiva — principios de diseño narrativo

Ver `.claude/skills/dproma-web-narrative/SKILL.md` para el detalle de tokens visuales. Resumen de intención:

- **No es un dashboard.** Es una pieza editorial: la home abre con una escena (un día cualquiera en DPROMA — WhatsApp, Excel, un cargador a medio instalar), no con una tabla de KPIs.
- **Las citas mandan, las cifras acompañan.** Cada sección de hallazgos abre con una viñeta humana anonimizada y cierra con el dato agregado que la sostiene (ej. "más de 200 mensajes de WhatsApp perdidos en una campaña" es el remate de una historia, no el titular).
- **Explorable, no lineal.** El lector puede entrar por "flujos", por "voces" (casos anónimos) o por "oportunidades" — no se le obliga a leer de arriba a abajo un informe de 40 páginas.
- **Tono:** investigación rigurosa (cada afirmación es trazable) + cercanía (lenguaje llano, sin jerga de consultoría). Alineado con el marco de 2894_ ("Diseño aumentado", "IA práctica") pero sin sobre-usar el eslogan — la evidencia de DPROMA es la protagonista, no la marca de 2894_.

---

## 8. Extensibilidad

- Nuevas entrevistas se procesan sin tocar el esquema: se agregan a `data/aggregate.json` por append.
- Si DPROMA quiere trackear evolución en el tiempo (¿bajó la dependencia de WhatsApp tras el CRM?), el esquema ya soporta reprocesar la misma persona en una fecha distinta (`meta.entrevista_id` incluye fecha) y la web puede eventualmente comparar "antes/después" sin cambio estructural.
- El pipeline es agnóstico al idioma de la transcripción (las entrevistas de DPROMA están en español mexicano; el esquema y los campos internos están en español para que Juan Carlos y el equipo de DPROMA puedan auditar `data/*.json` directamente sin traducir mentalmente).
