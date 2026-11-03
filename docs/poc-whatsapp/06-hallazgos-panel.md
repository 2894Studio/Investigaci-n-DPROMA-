# 06 · Hallazgos del panel

> 02/11/2026 · Studio2894. Revisión **de solo lectura** de `panel.dproma.com`: inicio de sesión
> con la cuenta de prueba de Comercial, navegación sin guardar y lectura del JavaScript que el
> panel entrega al navegador. No se creó, editó ni borró ningún registro. Las credenciales no
> se guardan en este repositorio. **Se recomienda cambiar la contraseña de la cuenta de
> prueba**, porque se compartió por chat.

## Stack

| Capa | Qué usa | Evidencia |
|---|---|---|
| Interfaz | HTML + JavaScript sin framework (módulos ES), Tailwind por CDN, fuente Barlow Semi Condensed | `src/js/app.js`, `router.js`, `src/views/*.html` |
| Hospedaje | Netlify; funciones en `/.netlify/functions/*` | `config.js` → `functionsBase` |
| Backend | Supabase: Auth, PostgREST, RPCs en Postgres, RLS por rol | `supabase-client.js`, llamadas a `/rest/v1` y `/rpc/*` |
| Archivos | Google Drive, a través de una función que entrega token y carpeta | `contactos-imagenes.js` → `drive-comercial-upload-auth` |
| Roles | Comercial, ICEV y otros; menú y permisos por rol | `permissions.js` |

## Módulo Comercial

**Contactos** (`contactos_comerciales`): son las fichas de Comercial.
- Al registrar un "Nuevo lead" se guardan `nombre`, `telefono`, `correo`, `vehiculo`,
  `domicilio`, `estado_id`, `observaciones_texto` e imágenes opcionales.
- Antes de guardar se buscan duplicados por `telefono_norm` y con la RPC
  `prospecto_duplicados`.
- La etapa `lead → prospecto → cliente` la calcula la base de datos; el estado es `activo` o
  `perdido`.
- Origen: `directa` (venta directa) u `oem` (vía OEM).
- La ficha tiene línea de tiempo (`contacto_timeline`), observaciones para ICEV
  (`contacto_observar`), actividades de Agenda y cotizaciones ligadas.

**Agenda** (`comercial_actividades`): pendientes del vendedor. Es el lugar natural para el
aviso de "lead nuevo de WhatsApp".

**Cotizaciones** (`cotizaciones`, ligadas por `contacto_id`):
- Estados: borrador, enviada, aceptada, rechazada, cancelada.
- Campos de cliente: `cliente_nombre`, `cliente_domicilio`, `tipo_inmueble`
  (`Residencial` / `Casa particular`), `vehiculo`.
- Conceptos por defecto:

| # | Concepto | Unidad | Precio |
|---|---|---|---|
| 1 | Instalación estándar de cargador EV (incluye hasta 10 m de canalización) | Servicio | $12,000 |
| 2 | Gestión y trámite ante CFE, medidor independiente con tarifa EV (opcional) | Trámite | $5,500 |
| 3 | Metro excedente de canalización y cableado (a partir del metro 11) | Metro | $450 |
| 4 | Sistema de tierra física dedicada (si se requiere) | Pieza | $2,800 |
| 5 | Mufa (acometida del nuevo medidor) | Pieza | $4,500 |

Las consideraciones del documento mencionan obra civil, tablero existente, muro disponible y
gestoría ante CFE. El desglose de materiales incluye renta de andamio "según la altura de la
trayectoria indicada por el cliente".

**Lo que pasa después:**
- Con una cotización aceptada, `comercial_formalizar` crea el prospecto para ICEV.
- `comercial_pasar_a_icev` acepta un motivo de no estándar (ej. "Más de 10 m de
  canalización").
- ICEV trabaja `prospectos` (nuevo, datos incompletos, localizado, confirmado, convertido…),
  visitas técnicas y órdenes de instalación.

## Implicaciones

1. **No hay que crear un CRM ni una bóveda de fotos.** El bot crea una ficha `lead` en
   Contactos y sube las fotos a la carpeta de esa ficha, igual que "Nuevo lead".
2. **Las preguntas del bot salen del cotizador**, para que Bernardo cotice sin volver a
   preguntar (ver `02-flujo-conversacional.md`, "Origen de las preguntas").
3. **Lo que falta en el panel** (y se le propone a Félix):
   - un usuario de servicio para el bot;
   - una RPC de entrada;
   - columnas para canal, agencia, tipo de inmueble, metros y medidor (o, como plan B, el
     resumen en `observaciones_texto`);
   - una bitácora de eventos para los KPIs.
4. **El flujo de ICEV no cambia.** La PoC termina en la ficha y el aviso.

## Observaciones

- El panel carga Tailwind desde el CDN de desarrollo (`cdn.tailwindcss.com`), que el propio
  Tailwind no recomienda para producción: es más pesado y depende de un tercero. Conviene
  compilarlo cuando haya oportunidad.
- `supabase-js` se carga como `@supabase/supabase-js@2`, sin versión exacta: una versión nueva
  puede cambiar el comportamiento sin aviso. Conviene fijarla.
- La llave pública (*anon*) de Supabase visible en el navegador es normal. La seguridad
  depende de que el RLS esté bien en todas las tablas; por eso la propuesta usa una RPC con
  permisos acotados para el bot.
