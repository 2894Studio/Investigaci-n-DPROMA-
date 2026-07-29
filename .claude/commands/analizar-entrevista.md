---
description: Analiza una transcripción de entrevista DPROMA y produce hallazgos estructurados en data/insights/
argument-hint: <ruta-al-archivo-de-transcripción>
---

Vas a procesar la transcripción de entrevista ubicada en: $ARGUMENTS

Antes de lanzar el análisis:
1. Confirma en una línea qué archivo vas a procesar y, si es identificable, qué rol/área representa el entrevistado (sin asumir su nombre como parte del alcance a comunicar).
2. Verifica que el archivo exista y sea legible; si es docx o pdf, extrae el texto primero.

Luego invoca la skill `dproma-interview-analyzer` para ejecutar el pipeline completo (los 6 subagentes en el orden especificado en esa skill) y escribir el resultado en `data/insights/`.

Al terminar, resume en 3-5 líneas: número de flujos, pain points, oportunidades detectadas, y si algo quedó marcado `needs_review` por el chequeo de anonimización. No repitas el contenido completo del JSON en el chat — el usuario puede abrir el archivo si lo necesita.
