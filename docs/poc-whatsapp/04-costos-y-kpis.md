# 04 · Costos estimados y KPIs de la PoC

> Borrador v0.2 · 31/10/2026. Montos en **USD, sin IVA**. Tarifas de fuentes públicas
> consultadas el 31/10/2026 (lista al final). **Hay que verificarlas en las páginas oficiales
> de Meta, Make y n8n antes de presupuestar.** Los volúmenes son supuestos que se corrigen con
> los números de Bernardo (relevamiento B). Alcance: solo el primer contacto; la cotización es
> de otra iniciativa.

## 1. Cómo cobra hoy WhatsApp (corrige el supuesto inicial)

El contexto de arranque hablaba de un "modelo por conversación". **Eso ya no aplica:**

- Desde el **1/07/2025** Meta cobra **por mensaje entregado**, no por conversación.
- Desde el **1/10/2026** también cobra los **mensajes de servicio** (las respuestas dentro de la
  ventana de 24 h): cada número tiene **1,000 gratis al mes** y del 1,001 en adelante se cobran
  a la tarifa de utilidad.
- La tarifa depende del país del **destinatario** (México).

| Tipo de mensaje (México, tarifa desde 1/10/2026) | USD por mensaje | ¿Lo usa la PoC? |
|---|---|---|
| Servicio (respuestas del bot dentro de 24 h) | 1,000 gratis/mes por número; después ≈ 0.0085 | **Sí, es el único** |
| Utilidad (plantillas transaccionales) | ≈ 0.0085 | No |
| Marketing (plantillas promocionales) | ≈ 0.0397 *(una fuente reporta 0.0456)* | No |

El bot siempre contesta dentro de la ventana de 24 h, así que la PoC no necesita plantillas.
Cloud API directa = estas tarifas sin recargo. Un BSP suma su suscripción o margen.

## 2. Supuestos por lead

| Supuesto | Valor | De dónde sale |
|---|---|---|
| Mensajes que manda el bot por lead | ~9 | Guion de `02-flujo-conversacional.md` (bienvenida, 5 preguntas, pedido de fotos, cierre) |
| Mensajes que manda el cliente por lead | ~8 | 6 respuestas + 2 fotos |
| Avisos de estado que manda Meta | ~3 por cada mensaje del bot (enviado, entregado, leído) | Así funciona el webhook |
| Aviso a Bernardo | 1 por lead | Si va por WhatsApp desde el número del bot, también es un mensaje de servicio 🟡 |

**Ojo con los avisos de estado:** cada uno dispara el webhook. En Make consume créditos y en n8n
Cloud cuenta como ejecución, aunque el flujo lo ignore. Por eso se recomienda un **filtro
ligero delante** (una función serverless gratuita que reenvía solo los mensajes y los
`failed`), o usar n8n *self-hosted*, donde las ejecuciones no se cobran.

## 3. Tres escenarios

| | **A · PoC** (1 agencia + directo) | **B · 3 agencias** | **C · Escala** (~10 agencias + campañas) |
|---|---|---|---|
| Leads por mes | 100 | 300 | 1,000 |
| Mensajes de servicio (bot) | ~900 → **gratis** | ~2,700 → 1,700 cobrados | ~9,000 → 8,000 cobrados |
| **Meta total / mes** | **$0** | **≈ $15** | **≈ $68** |
| Webhooks que llegan (con avisos de estado) | ~3,500 | ~10,500 | ~35,000 |
| Webhooks útiles (con filtro) | ~800 | ~2,400 | ~8,000 |
| **n8n self-hosted** (servidor) | $5–20 | $5–20 | $20–40 |
| **n8n Cloud** con filtro | Starter ≈ €24 | Pro ≈ €60 | Pro ≈ €60 (al límite) |
| **n8n Cloud** sin filtro | Pro ≈ €60 | Business ≈ €800 ⚠️ | Business ≈ €800 ⚠️ |
| **Make** (≈ 100 créditos/lead sin filtro) | ~10k créditos → Core al límite (~$11) | ~30k créditos | ~100k créditos |
| **Costo por lead** (Meta + n8n self-hosted) | **≈ $0.05–0.20** | **≈ $0.07–0.12** | **≈ $0.09–0.11** |

Precios de referencia de los orquestadores (mensual, sin descuento anual):
**Make** Core ≈ $10.59 / 10k créditos, Pro ≈ $18.82 / 10k; **n8n Cloud** Starter ≈ €24 /
2,500 ejecuciones, Pro ≈ €60 / 10,000; **n8n Community *self-hosted*** sin costo de licencia
y sin tope de ejecuciones (solo el servidor).

**Lectura:** los mensajes de WhatsApp cuestan poco en los tres escenarios; en la PoC caben en
el tramo gratuito. Lo que decide el costo es **el orquestador y cómo se cuentan los
webhooks**. Con n8n *self-hosted* (o n8n Cloud con filtro), el costo por lead queda en centavos
de dólar.

**No incluido:** horas de Félix y Studio2894 para construir y mantener, Google Workspace (ya
existente 🟡), el hospedaje del aviso de privacidad y el tiempo de Bernardo.

## 4. KPIs de la PoC

Todos salen de la tabla `lead_evento` (`01-arquitectura-integracion.md` §9). La **línea base**
(hoy) se toma de Bernardo antes de arrancar y, si se puede, de las capturas de chats.

| Dimensión | KPI | Fórmula | Meta | Línea base |
|---|---|---|---|---|
| Tiempo de respuesta | Primera respuesta al cliente | `bot_respuesta − primer_mensaje` | < 1 min, 24/7 | 🟡 (Bernardo) |
| Tiempo de respuesta | Primer contacto humano | `contacto_humano − aviso_bernardo` (mediana) | se fija con la línea base 🟡 | 🟡 |
| Captura | Leads completos | `datos_completos / primer_mensaje` | ≥ 60 % 🟡 | — |
| Captura | Abandono por paso | % que deja de responder en cada estado | encontrar la pregunta que sobra | — |
| Captura | Leads con fotos | leads con ≥ 1 foto / leads completos | se observa | — |
| Calidad de datos | Leads sin corrección manual | `leads sin edición de Bernardo / leads en CRM` | ≥ 80 % | — |
| Integración | Tasa de error | `eventos error_* / mensajes procesados` | < 2 % | — |
| Integración | Leads que llegan al CRM | `lead_creado_crm / (datos_completos + derivado_humano)` | 100 % (con reintentos) | — |
| Paso a persona | Tasa de handoff | `derivado_humano / primer_mensaje` (por motivo) | se observa | — |
| Atribución | Leads por canal | conteo por `origen` | se observa | hoy no se mide |
| Costo | Costo por lead | `(Meta + orquestador + servidor) / leads` | < $0.50 | — |

**Duración sugerida:** 4–6 semanas con 1 agencia y el canal directo, con revisión semanal de
abandono por paso y de errores.

## Fuentes (consultadas el 31/10/2026, no oficiales; verificar)

- Tarifas de WhatsApp en México: [getkanal.com](https://getkanal.com/blog/whatsapp-business-pricing-guide), [goeva.ai](https://www.goeva.ai/en/resources/whatsapp-business-api-pricing-mexico), [ManyChat](https://help.manychat.com/hc/en-us/articles/14281380243740-WhatsApp-pricing-guide)
- Cobro de mensajes de servicio desde 1/10/2026: [respond.io](https://respond.io/blog/whatsapp-pricing-change-2026), [YCloud](https://www.ycloud.com/blog/whatsapp-api-message-pricing-update-effective-october-1-2026)
- Coexistencia app Business + API: [360dialog](https://docs.360dialog.com/docs/hub/embedded-signup/whatsapp-coexistence), [Chakra](https://articles.chakrahq.com/article/whatsapp-coexistence-business-app-register-cloud-api/)
- Make: [Jet Admin](https://www.jetadmin.io/blog/make-pricing/), [Latenode](https://latenode.com/blog/make-com-pricing)
- n8n: [Jet Admin](https://www.jetadmin.io/blog/n8n-pricing/), [Sliplane](https://sliplane.io/blog/n8n-pricing)
- Oficiales para verificar: [Meta — precios de WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/pricing), [make.com/pricing](https://www.make.com/en/pricing), [n8n.io/pricing](https://n8n.io/pricing)
