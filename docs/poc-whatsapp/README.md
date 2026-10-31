# PoC — Automatización del primer contacto por WhatsApp → CRM

Prueba de concepto de DPROMA × 2894_. Cuando un prospecto escribe por WhatsApp, el bot captura
sus datos y sus fotos, crea la oportunidad en el sistema interno y avisa a Bernardo con todo
listo. Sin captura manual.

> **Estado:** borrador v0.2 · 31/10/2026 · todavía no se construye nada.
> v0.2: el Cotizador quedó fuera de alcance (es otra iniciativa y va en paralelo).

## Alcance

| Dentro | Fuera |
|---|---|
| Bot de WhatsApp que recibe al prospecto y captura sus datos | Cálculo y envío de cotizaciones (**iniciativa Cotizador**) |
| Fotos guardadas en Drive, en una carpeta por cliente | Agenda de visitas técnicas (ICEP) |
| Alta o actualización de la oportunidad en el CRM de Félix | Catálogo de SKUs y precios |
| Aviso a Bernardo con todo lo capturado y paso a una persona | Posventa y encuestas de satisfacción |
| Marcas de tiempo y métricas del primer contacto | Cambios al tablero comercial o al proceso de cierre |

**Dónde termina la PoC:** cuando la oportunidad está en el CRM y Bernardo recibió el aviso. Lo
que sigue (cotizar, visitar, cerrar) se hace igual que hoy.

**Lo que hay en común con el Cotizador:** los datos que captura el bot (tipo de inmueble, auto,
ubicación, distancia del tablero, fotos) son los mismos que el Cotizador va a necesitar. Por
eso se usan nombres de campo estables (`schema/poc-whatsapp-lead.schema.json`), pero ninguna de
las dos iniciativas depende de la otra.

## ⚠️ Pendientes abiertos

| # | Pendiente | Quién | Bloquea |
|---|---|---|---|
| **1** | **Información del sistema de Félix**: stack, si tiene API REST o webhooks, autenticación, entidad oportunidad/lead y sus campos, ambientes, si ya hay un tablero comercial. Sin esto los campos del CRM siguen "por confirmar". | Félix → Studio2894 | Mapeo de datos, nodo "Crear lead" |
| 2 | Muestras de chats reales (capturas), qué se pide hoy y en qué orden, tiempo actual de primera respuesta. | Bernardo | Textos del bot, línea base de los KPIs |
| 3 | Número para el bot y acceso a la cuenta de Meta Business. | Félix (o quien administre la cuenta) | Alta en la Cloud API |
| 4 | Aviso de privacidad (LFPDPPP) publicado en una URL. Lo exige la ley para pedir nombre, domicilio y fotos. | Quien lleve lo legal | Salida del bot |

## Documentos

| Archivo | Para quién | Qué contiene |
|---|---|---|
| [`01-arquitectura-integracion.md`](01-arquitectura-integracion.md) | Félix, Studio2894 | Componentes, webhook de Meta, fotos en Drive, errores, modelo de datos, Make vs n8n, riesgos |
| [`02-flujo-conversacional.md`](02-flujo-conversacional.md) | Bernardo, Studio2894 | Guion del bot paso a paso, textos y reglas de paso a una persona |
| [`03-plantilla-relevamiento.md`](03-plantilla-relevamiento.md) | Félix, Bernardo | Cuestionario con casillas |
| [`04-costos-y-kpis.md`](04-costos-y-kpis.md) | Félix, Studio2894 | Costos estimados en 3 escenarios, KPIs y cómo se miden |
| [`05-borradores-correo.md`](05-borradores-correo.md) | Studio2894 | Correos de seguimiento para Félix y Bernardo |
| [`../../schema/poc-whatsapp-lead.schema.json`](../../schema/poc-whatsapp-lead.schema.json) | Félix | Formato del lead que el orquestador entrega al CRM |
| [`../../schema/poc-whatsapp-ejemplo.json`](../../schema/poc-whatsapp-ejemplo.json) | Félix | Ejemplo: mensaje de WhatsApp → lead resultante |

Página para compartir: `web/entregables/poc-whatsapp-primer-contacto.html`.

## Hoy (as-is) vs. con la PoC (to-be)

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
Bot de WhatsApp: nombre · inmueble · auto · ubicación · distancia · fotos
   │                          └─ pide asesor, es flotilla o no se entiende ─► Bernardo
   ▼
Orquestador (n8n o Make)
   ├─► crea/actualiza la oportunidad en el CRM de Félix
   ├─► guarda las fotos en una carpeta de Drive del cliente
   └─► avisa a Bernardo con el resumen y los enlaces
                │
                ▼
      Bernardo sigue como hoy (cotiza, coordina visita, cierra)
```

## Responsables

| Persona | Rol en la PoC |
|---|---|
| Bernardo Padilla (Líder Comercial) | Dueño del proceso, valida los textos del bot, recibe los leads y los casos que pasan a una persona |
| Félix Sánchez (Tecnología) | Sistema interno/CRM, API y webhooks, cuenta de Meta, hospedaje del orquestador |
| Studio2894 / Operaciones | Orquestación, diseño conversacional, métricas |

## Fuentes

- Correo de inicio de la iniciativa (Studio2894) y contexto entregado en la sesión.
- Minutas de referencia (privadas en Drive de dproma.com, **no incorporadas todavía**): Reunión
  con Área Comercial 15/10 y las de la iniciativa Cotizador 26/10, que solo sirven de
  referencia por los campos en común.
