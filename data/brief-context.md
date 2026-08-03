# Contexto de negocio — Brief DPROMA x 2894_ (referenciado por las skills)

Este archivo es la fuente única de verdad para las 6 categorías de dolor y los 6 objetivos
específicos que usan `pain-point-detector` y `opportunity-mapper`. Si el brief de DPROMA
cambia, actualiza este archivo — no los prompts de los subagentes.

> Fuente: `BRIEFING DPROMA x 2894_` (documento oficial del cliente, 2026). La lista de
> stakeholders a entrevistar del documento original incluye nombres reales y se omite aquí
> deliberadamente — este archivo solo registra roles/áreas, nunca identidad.

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

## Visión de crecimiento (marco para priorizar oportunidades)
DPROMA está en expansión activa, no solo resolviendo dolor operativo del presente:
- Creación de una Gerencia de TI & IA y contratación de una consultora externa — la dirección
  declara este proyecto como estratégico para "los próximos años".
- Crecimiento del equipo en el corto-mediano plazo, incorporando nuevos perfiles al CRM.
- Visión de expansión geográfica a otros países de Latinoamérica, horizonte aún no definido.
- La herramienta interna es también la propuesta de valor para posicionar a DPROMA como
  empresa tecnológica, no solo una solución de eficiencia interna.

## Funcionalidades previstas (punto de partida para priorización en Fase 1, no alcance cerrado)
Este inventario proviene del alcance que DPROMA había definido con un proveedor externo previo;
sirve como referencia de qué módulos existen en el radar, no como backlog ya validado.

**Módulos web** (equipo interno de oficina): CRM Comercial · Clientes y sitios (Operaciones) ·
Trámites vehiculares (Gestores) · Instalación de cargadores · Inventario y almacén · Compras
(Administración) · Caja chica y viáticos · Solicitud de recursos · Customer Support (llamadas y
atención a cliente) · Gestión bancaria · Facturación y cobranzas (SAT) · Módulo jurídico + gestor
documental · Dashboard y reportes con IA.

**App móvil de instaladores de campo**: funcionamiento offline con sincronización automática al
recuperar conexión · integración con Google Maps (navegación al sitio) · escaneo de materiales
por código de barras · gestión de evidencias (fotos y videos por etapa de trabajo) · registro de
llegada, estado del sitio, instalación y mantenimientos. La IA en la app móvil se evaluará
después según impacto real vs. costo — no es parte del alcance confirmado todavía.

## Perfiles de usuario de la herramienta (roles, no personas)
- **Administración**: permisos adicionales, ver reportes, dar permisos, aprobar.
- **Operaciones**: tesorería, área comercial y afines.
- **Gestores**: vehículos, legal.
- **Instaladores**: solo tienen acceso a la app móvil.

La lista de stakeholders prioritarios a entrevistar en el brief cubre seis roles (administración
y finanzas, administración vehicular, coordinación técnica de instalaciones, operaciones,
proyectos especiales, jurídico) — coherente con la cobertura de las 10 entrevistas ya realizadas,
que además profundizó en comercial/cobranza y dirección general.

## Preguntas abiertas del brief (a validar con el equipo DPROMA, no asumir respuesta)
- ¿La lista de stakeholders cubre todos los perfiles necesarios para el flujo end-to-end del CRM?
- ¿En qué horizonte de tiempo se proyecta la expansión a otros mercados, y a qué países?
- ¿Cuáles son las áreas y actividades prioritarias en el CRM — el mayor dolor operativo hoy?
- ¿Existe alguna restricción no comentada aún (presupuesto, integraciones obligatorias, etc.)?
- ¿Cómo impacta hoy la operación interna en la experiencia del cliente? ¿Hay algún proceso de
  cara al cliente prioritario de mejorar?
- Al finalizar las tres fases del proyecto, ¿qué tiene que haber cambiado en la operación para
  que se considere exitoso?
