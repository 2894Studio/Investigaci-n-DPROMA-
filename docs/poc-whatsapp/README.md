# PoC — Automatización del primer contacto por WhatsApp → CRM + Cotizador

Prueba de concepto de DPROMA × 2894_ para que un prospecto que escribe por WhatsApp quede
registrado como oportunidad en el sistema interno, con sus fotos guardadas, clasificado como
cotización **estándar** o **no estándar**, y con marcas de tiempo para medir el SLA. Todo sin
captura manual.

> **Estado:** borrador v0.1 · 31/10/2026 · los documentos están listos para discutir con el
> equipo, todavía no se ha construido nada.

## ⚠️ Pendientes abiertos (en orden de prioridad)

| # | Pendiente | Quién | Bloquea |
|---|---|---|---|
| **1** | **Información del sistema de Félix**: stack, si tiene API REST o webhooks, autenticación, entidad oportunidad/lead y sus campos, ambientes (pruebas/producción), si ya hay un tablero comercial. Sin esto los campos del CRM siguen "por confirmar". | Félix → Studio2894 | Mapeo de datos, nodo "Crear lead", esquema final |
| 2 | Muestras de chats reales (capturas): qué escriben los clientes, qué fotos mandan, qué se les pide hoy y en qué orden. | Bernardo | Textos del bot, campos obligatorios |
| 3 | Catálogo de SKUs con precios vigentes y regla de cálculo de la cotización estándar. | Nacho | Cotización automática |
| 4 | Decidir qué número de WhatsApp se usa (uno nuevo o coexistencia con el de Bernardo) y quién administra la cuenta de Meta Business. | Dirección + Félix | Alta en Cloud API |
| 5 | SLAs y diagrama de derivación a ICEP acordados por dirección. | Nicole Calderón / Diana Hernández | Reglas de alerta |
| 6 | Aviso de privacidad (LFPDPPP) publicado en una URL. | Jurídico | Salida a producción del bot |

## Documentos

| Archivo | Para quién | Qué contiene |
|---|---|---|
| [`01-arquitectura-integracion.md`](01-arquitectura-integracion.md) | Félix, Studio2894 | Componentes, webhook de Meta, fotos en Drive, clasificación, errores, modelo de datos, Make vs n8n, riesgos |
| [`02-flujo-conversacional.md`](02-flujo-conversacional.md) | Bernardo, Studio2894 | Guion del bot paso a paso, textos, reglas de paso a una persona, cierres |
| [`03-plantilla-relevamiento.md`](03-plantilla-relevamiento.md) | Todo el equipo | Cuestionario con casillas, dividido por responsable |
| [`04-costos-y-kpis.md`](04-costos-y-kpis.md) | Dirección, Félix | Costos estimados en 3 escenarios, KPIs y cómo se miden |
| [`../../schema/poc-whatsapp-lead.schema.json`](../../schema/poc-whatsapp-lead.schema.json) | Félix | Contrato del lead que el orquestador entrega al CRM |
| [`../../schema/poc-whatsapp-ejemplo.json`](../../schema/poc-whatsapp-ejemplo.json) | Félix | Ejemplo: mensaje real de la API de WhatsApp → lead resultante |
| [`05-borradores-correo.md`](05-borradores-correo.md) | Studio2894 | Correos de seguimiento para Félix y Bernardo |

Página para compartir: `web/entregables/poc-whatsapp-primer-contacto.html`.

## Hoy (as-is) vs. con la PoC (to-be)

**Hoy.** El prospecto escribe al WhatsApp de Bernardo y manda fotos sueltas del tablero
eléctrico, la acometida de CFE y el lugar donde quiere el cargador, más mensajes sin estructura.
Llega por tres canales:

- **Agencias aliadas (B2B2C)**: DPROMA es instalador preferente; por ejemplo, Changan del Valle
  con el Dipal S07 mueve unos 30–40 autos eléctricos o enchufables al mes por agencia.
- **Particulares (B2C)**: llegan por la web o por WhatsApp directo.
- **Flotillas (B2B)**: contacto directo.

Las fotos se quedan en el teléfono y los datos se capturan a mano. La investigación de este
repositorio muestra lo que eso cuesta: más de 400 grupos de WhatsApp, una campaña con más de
200 mensajes que nadie alcanzó a atender, y clientes que se pierden en listas reenviadas
(`data/aggregate.json`, `web/entregables/atencion-al-cliente.html`).

**Con la PoC.**

```
Cliente (enlace wa.me de la agencia, de la web o directo)
   │
   ▼
Bot de WhatsApp: nombre · inmueble · auto · ubicación · distancia · fotos
   │                                   └─ pide asesor, es flotilla o no se entiende ─► Bernardo
   ▼
Orquestador (n8n o Make) ─► crea/actualiza la oportunidad en el CRM ─► carpeta en Drive con las fotos
   │
   ├─ tirada ≤ 10 m → Cotizador (SKUs de Almacén) → Bernardo aprueba → propuesta en < 2 h
   └─ > 10 m / no sé / caso especial → alerta a ICEP → visita técnica → oferta formal
   │
   ▼
Instalación + 15 días → encuesta CSAT/NPS y pedido de referencias por WhatsApp
```

## Responsables

| Persona | Rol en la PoC |
|---|---|
| Bernardo Padilla (Líder Comercial) | Dueño del proceso comercial, valida textos del bot, aprueba cotizaciones, recibe los casos que pasan a una persona |
| Félix Sánchez (Tecnología) | Sistema interno/CRM, API y webhooks, hospedaje del orquestador |
| Mauricio CR / Jhonatan Álvarez (Operaciones/ICEP) | Visitas técnicas de los casos no estándar |
| Nacho (Almacén) | Catálogo de SKUs y precios |
| Nicole Calderón / Diana Hernández (Dirección) | SLAs y diagrama de derivación |
| Studio2894 / Operaciones | Orquestación, diseño conversacional, métricas |

## Fuentes

- Correo de inicio de la iniciativa (Studio2894) y resumen del contexto entregado en la sesión.
- Minutas de referencia (privadas en Drive de dproma.com, **no incorporadas todavía**): Iniciativa
  Cotizador 26/10, Notas de Gemini 26/10, Reunión con Área Comercial 15/10. Si se exportan a
  `data/raw/`, se cruzan con estos documentos.
