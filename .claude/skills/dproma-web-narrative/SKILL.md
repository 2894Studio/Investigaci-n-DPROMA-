---
name: dproma-web-narrative
description: Reconstruye la web interactiva de resultados de investigación (web/index.html) a partir de data/aggregate.json. Sabe el sistema de diseño narrativo y las reglas de anonimización de contenido publicable. Úsalo cuando el usuario pida "reconstruir la web", "actualizar el sitio de hallazgos", o después de procesar nuevas entrevistas si el usuario quiere verlas reflejadas.
---

# Web narrativa de hallazgos DPROMA

## Principio rector
Esta no es una skill de "generar un dashboard". Es una skill de **traducir evidencia de investigación a una pieza editorial que un stakeholder no-técnico lea con gusto**. Si el resultado se parece a un panel de administración con tarjetas de KPI, se falló el brief.

## Antes de escribir cualquier HTML
1. Lee `data/aggregate.json` completo — no generes contenido de relleno; toda cifra, cita o historia en la web debe trazarse a un registro real de `data/insights/`.
2. Verifica que ninguna viñeta incluida tenga `anonymization_check` distinto de `"passed"`. Si `data/aggregate.json` trae alguna en `needs_review`, **excluirla silenciosamente de la web** (no es tu trabajo resolverla; ya se reportó en el paso de análisis).
3. Cuenta cuántas entrevistas hay agregadas — la narrativa debe reflejar el estado real del research (si son 5 entrevistas, no simules que es un estudio de 50 personas).

## Sistema de diseño (tokens)

**Paleta** (editorial oscura, no genérica — evita el terracota/crema por defecto de IA):
- Fondo base: `#0E1116` (casi negro, cálido)
- Superficie elevada: `#161B22`
- Texto principal: `#EDEEF0`
- Texto secundario: `#9AA3AE`
- Acento — azul DPROMA (tomado del propio brief/marca del cliente, no genérico): `#3FA9F5`
- Acento secundario, cálido, para "voces humanas": `#F5B34F` (ámbar, evoca la luz de un taller/instalación eléctrica — hay coherencia temática con el sector)

**Tipografía**:
- Display: una serif editorial con carácter (ej. "Fraunces" o "Instrument Serif") para titulares e hitos narrativos — NO la misma sans-serif del cuerpo.
- Cuerpo: sans-serif geométrica de alta legibilidad (ej. "Inter" o "IBM Plex Sans").
- Datos/timestamps/metadata: monoespaciada (ej. "IBM Plex Mono") — refuerza que detrás de la narrativa hay evidencia trazable, un guiño a los timestamps de las transcripciones reales.

**Estructura narrativa (no dashboard):**
1. **Apertura — una escena, no una tabla**: describe un momento operativo real y anónimo (ej. una solicitud que llega por WhatsApp un martes a las 7am) para anclar al lector en el mundo de DPROMA antes de mostrar un solo dato.
2. **Voces** — sección explorable de viñetas anonimizadas por arquetipo de rol (no lista de "entrevistados 1 a 5" con números fríos).
3. **Flujos** — visualización simple de 2-3 flujos reales (el de alta de cliente, el de compra/instalación) mostrando dónde vive cada paso hoy (WhatsApp/Excel/papel/verbal), sin diagramas de caja-y-flecha genéricos — usar una línea de tiempo horizontal con el canal como color.
4. **Fricciones** — agrupadas por las 6 categorías del brief, cada una abre con la viñeta humana correspondiente antes del agregado numérico.
5. **Oportunidades** — mapa simple impacto/esfuerzo (2x2), cada burbuja enlaza a su historia de origen al hacer click/hover (sin necesidad de backend — todo el dataset vive inline en el HTML).
6. **Cierre** — qué preguntas siguen abiertas (honestidad sobre el estado incompleto del research, no un cierre falso de "conclusiones finales").

## Reglas de contenido
- Nunca renderizar nombres propios reales — solo `persona_arquetipo` y viñetas ya anonimizadas del dataset.
- Nunca inventar cifras agregadas que el dataset no sostenga (si solo hay 5 entrevistas, no digas "el 80% de los usuarios..." — di "4 de 5 personas entrevistadas...").
- El copy debe sonar como alguien explicándoselo a un colega, no como un informe de consultoría — frases cortas, sin "leverage", sin "sinergia".

## Entregable técnico
- Archivo único `web/index.html` (CSS y JS inline, sin build step) para que sea trivial de compartir o subir a cualquier hosting estático.
- Todo el dataset anonimizado se embebe como un objeto JS al final del `<body>` (`const DATA = {...}`) para que la página funcione standalone sin fetch a un backend.
- Debe verse bien en mobile (el brief no lo pide explícitamente pero un stakeholder lo va a abrir desde el celular en algún momento).
