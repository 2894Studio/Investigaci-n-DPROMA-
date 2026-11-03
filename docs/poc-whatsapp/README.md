# PoC · Primer contacto por WhatsApp

Prueba de concepto de DPROMA × 2894_. Cuando un prospecto escribe por WhatsApp, el bot captura
sus datos y sus fotos, crea la oportunidad en el sistema interno y avisa a Bernardo con todo
listo. Sin captura manual.

> **Estado:** borrador v0.4 · 02/11/2026 · demo lista, piloto sin construir.
>
> **Empieza aquí:** la página interactiva `web/entregables/poc-whatsapp-primer-contacto.html`
> (simulador de WhatsApp, flujo, cómo aprende el bot, limitaciones, calculadoras de costo e
> impacto). Para mostrarlo funcionando sin WhatsApp: la demo de n8n
> ([`07-demo-n8n.md`](07-demo-n8n.md)). Los documentos 01–06 son el anexo técnico.
>
> v0.2: el Cotizador quedó fuera de alcance. v0.3: destino real = Contactos del panel
> (Supabase); preguntas derivadas del cotizador; orquestador n8n. v0.4: página didáctica con
> simulaciones y demo n8n probada.

## Alcance

| Dentro | Fuera |
|---|---|
| Bot de WhatsApp que recibe al prospecto y captura sus datos | Cálculo y envío de cotizaciones (**iniciativa Cotizador**) |
| Fotos guardadas en Drive, en una carpeta por cliente | Agenda de visitas técnicas (ICEP) |
| Alta o actualización de la ficha `lead` en Contactos del panel | Catálogo de SKUs y precios |
| Aviso a Bernardo con todo lo capturado y paso a una persona | Posventa y encuestas de satisfacción |
| Marcas de tiempo y métricas del primer contacto | Cambios al tablero comercial o al proceso de cierre |

**Dónde termina la PoC:** cuando la oportunidad está en el CRM y Bernardo recibió el aviso. Lo
que sigue (cotizar, visitar, cerrar) se hace igual que hoy.

**Lo que hay en común con el Cotizador:** el cotizador del panel se usó como referencia para
decidir **qué datos pide el bot** (cliente, tipo de inmueble, vehículo, domicilio, metros,
medidor independiente y fotos), así Bernardo cotiza sin volver a preguntar. El bot no crea
cotizaciones y ninguna de las dos iniciativas depende de la otra.

## Pendientes

| # | Pendiente | Quién | Bloquea |
|---|---|---|---|
| **1** | **Validar con Félix la propuesta de entrada al panel**: usuario de servicio del bot, RPC `whatsapp_registrar_lead`, columnas nuevas (`canal`, `agencia`, `tipo_inmueble`, `metros_aprox`, `medidor_independiente`) o plan B en `observaciones_texto`, permiso del bot en la función de Drive, ambiente de pruebas. *El stack y la tabla ya se conocen (Supabase + Netlify, `contactos_comerciales`).* | Félix | Construir el nodo "Registrar lead" |
| 2 | Muestras de chats reales (capturas), qué se pide hoy y en qué orden, tiempo actual de primera respuesta. | Bernardo | Textos del bot, línea base de los KPIs |
| 3 | Número para el bot y acceso a la cuenta de Meta Business. | Félix (o quien administre la cuenta) | Alta en la Cloud API |
| 4 | Aviso de privacidad (LFPDPPP) publicado en una URL. Lo exige la ley para pedir nombre, domicilio y fotos. | Quien lleve lo legal | Salida del bot |

## Documentos

| Archivo | Para quién | Qué contiene |
|---|---|---|
| [`07-demo-n8n.md`](07-demo-n8n.md) | Todo el equipo | Cómo correr y mostrar la demo en n8n sin WhatsApp ni APIs |
| [`08-auditoria-lenguaje.md`](08-auditoria-lenguaje.md) | Studio2894 | Criterios de lenguaje y cambios aplicados a la página |
| [`../../n8n/`](../../n8n/) | Studio2894 | Workflow importable y motor del guion (fuente única) |
| [`06-hallazgos-panel.md`](06-hallazgos-panel.md) | Félix, Studio2894 | Lo que se encontró en la revisión del panel |
| [`01-arquitectura-integracion.md`](01-arquitectura-integracion.md) | Félix, Studio2894 | Componentes, webhook de Meta, fotos en Drive, errores, modelo de datos, Make vs n8n, riesgos |
| [`02-flujo-conversacional.md`](02-flujo-conversacional.md) | Bernardo, Studio2894 | Guion del bot paso a paso, textos y reglas de paso a una persona |
| [`03-plantilla-relevamiento.md`](03-plantilla-relevamiento.md) | Félix, Bernardo | Cuestionario con casillas |
| [`04-costos-y-kpis.md`](04-costos-y-kpis.md) | Félix, Studio2894 | Costos estimados en 3 escenarios, KPIs y cómo se miden |
| [`05-borradores-correo.md`](05-borradores-correo.md) | Studio2894 | Correos de seguimiento para Félix y Bernardo |
| [`../../schema/poc-whatsapp-lead.schema.json`](../../schema/poc-whatsapp-lead.schema.json) | Félix | Formato del lead que el orquestador entrega al CRM |
| [`../../schema/poc-whatsapp-ejemplo.json`](../../schema/poc-whatsapp-ejemplo.json) | Félix | Ejemplo: mensaje de WhatsApp → lead resultante |

Página para compartir: `web/entregables/poc-whatsapp-primer-contacto.html`.

## Hoy vs. con el bot

**Hoy.** El prospecto escribe al WhatsApp de Bernardo y manda fotos sueltas (tablero eléctrico,
acometida de CFE, lugar de instalación) y mensajes sin estructura. Llega por tres canales:

- **Agencias aliadas (B2B2C)**: DPROMA es instalador preferente; por ejemplo, Changan del Valle
  con el Dipal S07 mueve unos 30–40 autos eléctricos o enchufables al mes por agencia.
- **Particulares (B2C)**: por la web o WhatsApp directo.
- **Flotillas (B2B)**: contacto directo.

Las fotos se quedan en el teléfono y los datos se capturan a mano. La investigación de este
repositorio muestra lo que eso cuesta: más de 400 grupos de WhatsApp, una campaña con más de
200 mensajes que nadie alcanzó a atender y clientes que se pierden en listas reenviadas
(`data/aggregate.json`, `web/entregables/atencion-al-cliente.html`).

**Con la PoC.**

```
Cliente (enlace wa.me de la agencia, de la web o directo)
   │
   ▼
Bot de WhatsApp: nombre · inmueble · vehículo · domicilio · metros · medidor · fotos
   │                          └─ pide asesor, es flotilla o no se entiende ─► Bernardo
   ▼
n8n (Studio2894)
   ├─► RPC whatsapp_registrar_lead → ficha «lead» en Contactos (Supabase) + actividad en la Agenda
   ├─► fotos → Drive «DPROMA — Comercial/{folio}» + comercial_evidencias
   └─► resumen por WhatsApp a Bernardo
                │
                ▼
      Bernardo sigue como hoy (cotiza, coordina visita, cierra)
```

## Responsables

| Persona | Rol en la PoC |
|---|---|
| Bernardo Padilla (Líder Comercial) | Dueño del proceso, valida los textos del bot, recibe los leads y los casos que pasan a una persona |
| Félix Sánchez (Tecnología) | Panel DPROMA (Supabase/Netlify): RPC y usuario de servicio del bot, columnas nuevas, cuenta de Meta |
| Studio2894 / Operaciones | Flujo en n8n, diseño conversacional, métricas |

## Fuentes

- Correo de inicio de la iniciativa (Studio2894) y contexto entregado en la sesión.
- Revisión de solo lectura de `panel.dproma.com` (02/11/2026) y capturas del cotizador.
- Minutas de referencia (privadas en Drive de dproma.com, **no incorporadas todavía**): Reunión
  con Área Comercial 15/10 y las de la iniciativa Cotizador 26/10, que solo sirven de
  referencia por los campos en común.
