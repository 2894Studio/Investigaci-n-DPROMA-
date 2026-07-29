---
name: dproma-interview-analyzer
description: Orquesta el análisis completo de una transcripción de entrevista de investigación DPROMA (formato "Notas de Gemini" u otro), lanzando los 6 subagentes especializados en el orden correcto y escribiendo el resultado validado a data/insights/. Úsalo cuando el usuario pida analizar, procesar, o extraer hallazgos de una entrevista/guion/transcripción de DPROMA. Dispara con: "analiza esta entrevista de Dproma", "procesa este guion de entrevista", "saca los hallazgos de esta transcripción", o cuando aparezca un archivo nuevo en data/raw/.
---

# Analizador de entrevistas DPROMA

## Cuándo se activa
- El usuario pide analizar/procesar una transcripción o guion de entrevista de DPROMA.
- El usuario menciona un archivo con formato reconocible de "Notas de Gemini" (Resumen / Próximos pasos / Detalles con timestamps) en el contexto de DPROMA.
- El usuario dice "corre el pipeline" o "actualiza los hallazgos" refiriéndose a entrevistas de DPROMA.

## Qué NO hace esta skill
- No reconstruye la web (eso es `dproma-web-narrative`).
- No decide sola cuándo publicar algo — el checkpoint de anonimización siempre requiere `"passed"` explícito del `narrative-synthesizer`.

## Procedimiento

### 1. Preparación
- Localiza el archivo de la transcripción (docx, pdf, o texto ya extraído). Si es docx/pdf, extrae el texto primero (`extract-text` para docx; para pdf ver skill `pdf-reading`).
- Genera `entrevista_id`: `<fecha-ISO>_<rol-anonimizado-en-kebab-case>`. Nunca usar el nombre real de la persona en el id, ni siquiera abreviado (ej. usar `coordinacion-seguimiento-proveedor-tech`, no `n-cruz` ni `ncruz`).
- Confirma con el usuario en una línea qué se va a procesar antes de lanzar los subagentes, si el archivo no fue explícito en su mensaje.

### 2. Primera capa — 5 subagentes en paralelo
Lanza en un solo turno (Task tool, llamadas concurrentes) pasando a cada uno: el texto completo de la transcripción + `entrevista_id` + el fragmento relevante del brief de DPROMA como contexto compartido:
- `flow-extractor`
- `pain-point-detector`
- `tool-inventory-analyst`
- `ai-adoption-analyst`

(`opportunity-mapper` NO va en esta capa — depende del output de `pain-point-detector`.)

### 3. Validación
Valida cada JSON recibido contra `schema/interview-insight.schema.json`. Si algo no valida:
- No lo "arregles" silenciosamente reescribiendo el output del subagente.
- Reporta al usuario exactamente qué campo falló y de qué subagente vino, y vuelve a lanzar solo ese subagente con una instrucción correctiva.

### 4. Segunda capa — opportunity-mapper
Lanza `opportunity-mapper` pasándole el `pain_points` ya validado + los 6 objetivos específicos del brief (no la transcripción cruda otra vez — ya cumplió su función en `pain-point-detector`).

### 5. Tercera capa — narrative-synthesizer
Lanza `narrative-synthesizer` pasándole los 5 JSON completos (workflows, pain_points, tools_inventory, ai_adoption, opportunities). Este es el único paso que produce texto destinado a ser público (la web); revisa que cada viñeta tenga `anonymization_check: "passed"` antes de continuar. Si alguna viñeta viene `"needs_review"`, exclúyela del registro final y avisa al usuario en una línea, sin bloquear el resto del pipeline.

### 6. Persistencia
- Escribe el registro completo en `data/insights/<entrevista_id>.json` (fusión de las 6 secciones).
- Haz append a `data/aggregate.json` (lista de todas las entrevistas procesadas) — no reescribas entrevistas previas al hacerlo.

### 7. Cierre
Resume al usuario en 3-5 líneas: cuántos pain points/oportunidades/flujos se detectaron y si algo quedó en `needs_review`. No narres el proceso paso a paso — el usuario quiere el resultado, no la mecánica.

## Reglas de negocio fijas (no cambian entre entrevistas)
- Las 6 categorías de pain points son las de la sección "Situación actual" del brief DPROMA — no se inventan categorías nuevas sin que el usuario lo pida explícitamente.
- Los 6 objetivos específicos de `opportunity-mapper` son los del brief DPROMA vigente. Si el brief se actualiza, esta skill debe actualizarse también (vive en `data/brief-context.md`, referenciado, no hardcodeado dos veces).
- Ninguna cita textual de más de 15 palabras sale del sistema hacia la web, en ningún subagente.
