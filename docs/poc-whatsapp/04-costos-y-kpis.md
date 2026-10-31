# 04 · Costos estimados y KPIs de la PoC

> Borrador v0.1 · 31/10/2026. Montos en **USD, sin IVA**. Las tarifas son de fuentes
> públicas consultadas el 31/10/2026 (lista al final). **Hay que verificarlas en las páginas
> oficiales de Meta, Make y n8n antes de presupuestar.** Los volúmenes son supuestos que se
> corrigen con los números de Bernardo (relevamiento B).

## 1. Cómo cobra hoy WhatsApp (corrige el supuesto inicial)

El contexto de arranque hablaba de un "modelo por conversación". **Eso ya no aplica:**

- Desde el **1/07/2025** Meta cobra **por mensaje entregado**, no por conversación.
- Desde el **1/10/2026** también cobra los **mensajes de servicio** (las respuestas dentro de la
  ventana de 24 h): cada número tiene **1,000 gratis al mes** y del 1,001 en adelante se cobran
  a la tarifa de utilidad.
- La tarifa depende del país del **destinatario** (México).

| Tipo de mensaje (México, tarifa desde 1/10/2026) | USD por mensaje |
|---|---|
| Servicio (respuestas del bot dentro de 24 h) | 1,000 gratis/mes por número; después ≈ 0.0085 |
| Utilidad (plantillas: propuesta tardía, visita, encuesta) | ≈ 0.0085 |
| Marketing (plantilla de referidos / recompra) | ≈ 0.0397 *(una fuente reporta 0.0456)* |

Cloud API directa = estas tarifas sin recargo. Un BSP suma su suscripción o margen.

## 2. Supuestos por lead

| Supuesto | Valor | De dónde sale |
|---|---|---|
| Mensajes que manda el bot por lead | ~10 | Guion de `02-flujo-conversacional.md` (bienvenida, 5 preguntas, confirmaciones, cierre, propuesta) |
| Mensajes que manda el cliente por lead | ~8 | 6 respuestas + 2 fotos |
| Avisos de estado que manda Meta | ~3 por cada mensaje del bot (enviado, entregado, leído) | Así funciona el webhook |
| Leads que terminan en instalación | 30 % 🟡 | Supuesto, validar con Bernardo |
| Propuestas que salen fuera de 24 h | 20 % de las instalaciones | Supuesto |
| Clientes que dan 9–10 y reciben plantilla de referidos | ~1 de cada 3 instalaciones | Supuesto |

**Ojo con los avisos de estado:** cada uno dispara el webhook. En Make consume créditos y en n8n
Cloud cuenta como ejecución, aunque el flujo lo ignore. Por eso se recomienda un **filtro
ligero delante** (una función serverless gratuita que reenvía solo los mensajes y los
`failed`), o usar n8n *self-hosted*, donde las ejecuciones no se cobran.

## 3. Tres escenarios

| | **A · PoC** (1 agencia + directo) | **B · 3 agencias** | **C · Escala** (~10 agencias + campañas) |
|---|---|---|---|
| Leads por mes | 100 | 300 | 1,000 |
| Instalaciones (30 %) | 30 | 90 | 300 |
| Mensajes de servicio | 1,000 → **gratis** | 3,000 → 2,000 cobrados | 10,000 → 9,000 cobrados |
| Meta: servicio | $0 | $17.00 | $76.50 |
| Meta: plantillas de utilidad | ~50 → $0.43 | ~150 → $1.28 | ~500 → $4.25 |
| Meta: plantillas de marketing | ~10 → $0.40 | ~30 → $1.19 | ~100 → $3.97 |
| **Meta total / mes** | **≈ $1** | **≈ $20** | **≈ $85** |
| Webhooks que llegan (con avisos de estado) | ~3,800 | ~11,400 | ~38,000 |
| Webhooks útiles (con filtro) | ~900 | ~2,700 | ~9,000 |
| **n8n self-hosted** (VPS) | $5–20 | $5–20 | $20–40 |
| **n8n Cloud** con filtro | Starter ≈ €24 | Pro ≈ €60 | Pro ≈ €60 (al límite) |
| **n8n Cloud** sin filtro | Pro ≈ €60 | Business ≈ €800 ⚠️ | Business ≈ €800 ⚠️ |
| **Make** (≈ 110 créditos/lead sin filtro) | ~11k créditos → plan arriba de Core (~$11–20) | ~33k créditos | ~110k créditos |
| **Costo por lead** (Meta + n8n self-hosted) | **≈ $0.06–0.21** | **≈ $0.08–0.13** | **≈ $0.11–0.13** |

Precios de referencia de los orquestadores (mensual, sin descuento anual):
**Make** Core ≈ $10.59 / 10k créditos, Pro ≈ $18.82 / 10k; **n8n Cloud** Starter ≈ €24 /
2,500 ejecuciones, Pro ≈ €60 / 10,000; **n8n Community *self-hosted*** sin costo de licencia
y sin tope de ejecuciones (solo el servidor).

**Lectura:** el costo de mensajes de WhatsApp es bajo en los tres escenarios. Lo que decide el
costo es **el orquestador y cómo se cuentan los webhooks**. Con n8n *self-hosted* (o n8n Cloud
con filtro) el costo por lead queda en centavos de dólar. Make y n8n Cloud sin filtro se
encarecen rápido.

**No incluido:** horas de Félix/Studio2894 para construir y mantener, Google Workspace (ya
existente 🟡), el dominio y hospedaje del aviso de privacidad, y el tiempo de Bernardo e ICEP.

## 4. KPIs de la PoC

Todos salen de la tabla `lead_evento` (`01-arquitectura-integracion.md` §11). La **línea base**
(hoy) se toma de Bernardo antes de arrancar y, si se puede, de las capturas de chats.

| Dimensión | KPI | Fórmula | Meta | Línea base |
|---|---|---|---|---|
| Tiempo de respuesta | Primera respuesta | `bot_respuesta − primer_mensaje` | < 1 min | 🟡 |
| SLA estándar | Tiempo a cotización | `cotizacion_enviada − datos_completos` (mediana y % < 2 h) | < 2 h en ≥ 90 % | 🟡 |
| SLA no estándar | Tiempo a visita agendada | `visita_agendada − datos_completos` | SLA de dirección 🟡 | 🟡 |
| Conversión del bot | Leads completos | `datos_completos / primer_mensaje` | ≥ 60 % 🟡 | — |
| Abandono por paso | Dónde se van | % que no responde en cada estado | identificar el peor paso | — |
| Eficiencia | Lead → visita → instalación | `visita_realizada / leads`, `instalacion / leads` | 🟡 | 🟡 |
| Calidad de datos | Leads sin corrección manual | `leads sin edición de Bernardo / leads completos` | ≥ 80 % | — |
| Errores de integración | Tasa de error | `eventos error_* / mensajes procesados` | < 2 % | — |
| Paso a persona | Tasa de handoff | `derivado_humano / primer_mensaje` (por motivo) | se observa | — |
| Posventa | CSAT/NPS a 15 días | promedio y NPS de `encuesta_respondida` | NPS ≥ 50 🟡 | — |
| Costo | Costo por lead / por instalación | `(Meta + orquestador + infra) / leads` | < $0.50 / lead | — |

**Duración sugerida de la PoC:** 4–6 semanas con 1 agencia y el canal directo, con revisión
semanal de abandono por paso y de errores.

## Fuentes (consultadas el 31/10/2026, no oficiales; verificar)

- Tarifas de WhatsApp en México: [getkanal.com](https://getkanal.com/blog/whatsapp-business-pricing-guide), [goeva.ai](https://www.goeva.ai/en/resources/whatsapp-business-api-pricing-mexico), [ManyChat](https://help.manychat.com/hc/en-us/articles/14281380243740-WhatsApp-pricing-guide)
- Cobro de mensajes de servicio desde 1/10/2026: [respond.io](https://respond.io/blog/whatsapp-pricing-change-2026), [YCloud](https://www.ycloud.com/blog/whatsapp-api-message-pricing-update-effective-october-1-2026)
- Coexistencia app Business + API: [360dialog](https://docs.360dialog.com/docs/hub/embedded-signup/whatsapp-coexistence), [Chakra](https://articles.chakrahq.com/article/whatsapp-coexistence-business-app-register-cloud-api/)
- Make: [Jet Admin](https://www.jetadmin.io/blog/make-pricing/), [Latenode](https://latenode.com/blog/make-com-pricing)
- n8n: [Jet Admin](https://www.jetadmin.io/blog/n8n-pricing/), [Sliplane](https://sliplane.io/blog/n8n-pricing)
- Oficiales para verificar: [Meta — precios de WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/pricing), [make.com/pricing](https://www.make.com/en/pricing), [n8n.io/pricing](https://n8n.io/pricing)
