# Contexto de negocio — Brief DPROMA x 2894_ (referenciado por las skills)

Este archivo es la fuente única de verdad para las 6 categorías de dolor y los 6 objetivos
específicos que usan `pain-point-detector` y `opportunity-mapper`. Si el brief de DPROMA
cambia, actualiza este archivo — no los prompts de los subagentes.

## Objetivo general
Implementar la estrategia de transformación digital de DPROMA, acompañando al equipo interno
en la identificación de oportunidades, optimización de procesos, automatización de tareas y
desarrollo de soluciones tecnológicas que fortalezcan la operación y preparen a la empresa
para el crecimiento proyectado.

## Objetivos específicos (usados por `opportunity-mapper`)
1. Centralizar toda la información operativa, comercial, financiera y jurídica en una sola herramienta (CRM).
2. Conocer a profundidad cómo opera cada área para identificar cuellos de botella y qué flujos tienen mayor impacto y viabilidad para ser transformados con tecnología e IA.
3. Integrar la IA en los procesos de forma efectiva y responsable.
4. Estandarizar procesos y formatos entre áreas para garantizar consistencia y trazabilidad.
5. Formar al equipo en las posibilidades que ofrece la IA de Gemini, para que la transformación sea adoptada y no solo implementada.
6. Dotar a los instaladores de campo de una app móvil que funcione también sin conexión.

## Categorías de "situación actual" (usadas por `pain-point-detector`)
- **falta_centralizacion**: no existe una herramienta centralizada; la información se registra en Excel, sin formatos comunes entre áreas.
- **falta_formatos_comunes**: no hay estándares para el registro de operaciones.
- **gestion_por_whatsapp**: coordinaciones críticas se realizan por mensajería, sin historial estructurado ni trazabilidad.
- **trabajo_manual**: todo depende de procesos manuales sin automatización.
- **falta_governance_ia**: no hay políticas, criterios ni lineamientos definidos sobre cómo el equipo adopta, usa o evalúa herramientas tecnológicas e IA.
- **falta_visibilidad_kpis**: no existe un panel de control que permita a la dirección tomar decisiones basadas en datos en tiempo real.

## Restricciones y decisiones ya tomadas (a respetar en cualquier propuesta de `opportunity-mapper`)
- La herramienta se construye con el equipo interno de DPROMA, sin proveedor externo de desarrollo.
- Plataforma: Web + App móvil.
- Base de datos por definir (Supabase o Amazon).
- IA: herramientas de Google (Gemini).
- Integraciones API previstas: SAT (timbrado), APIs bancarias, Google Maps, API CRM.
- El diseño de experiencia de usuario (UX) y la arquitectura de información **no** están contemplados en el alcance actual del proyecto — los flujos definidos en esta investigación sientan las bases para una etapa posterior si DPROMA decide profundizar en ello.
- Principio de usabilidad ya validado con el cliente: la herramienta debe comunicar en todo momento el estado de los procesos (ej. si una transferencia bancaria fue procesada o no).
