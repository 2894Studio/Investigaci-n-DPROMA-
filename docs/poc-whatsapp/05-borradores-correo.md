# 05 · Correos (borradores)

## Félix

**Asunto:** PoC WhatsApp → panel: propuesta para registrar los leads en Contactos

¡Hola, Félix!

Revisamos el panel en modo de solo lectura, con la cuenta de prueba de Comercial, y vimos que
el lugar natural para los leads del bot es `contactos_comerciales`, con las fotos en la carpeta
de Drive de cada ficha (`drive-comercial-upload-auth` + `comercial_evidencias`). El bot no
cotiza; solo pide los datos que el cotizador necesita y deja la ficha lista para Bernardo.

Para conectarlo sin usar cuentas de personas ni la llave de servicio, te proponemos:

1. Un usuario de servicio `bot-whatsapp@dproma.com` con un rol propio, sin acceso al panel.
2. Una RPC `whatsapp_registrar_lead` (SECURITY DEFINER) que cree o actualice la ficha,
   deduplique por `telefono_norm`, asigne a Bernardo y cree la actividad en su Agenda.
3. Columnas nuevas en `contactos_comerciales`: `canal`, `agencia`, `tipo_inmueble`,
   `metros_aprox`, `medidor_independiente`. Si prefieres no tocar el esquema todavía, como
   plan B lo resumimos en `observaciones_texto`.
4. Permiso para que ese usuario use la función de Drive y registre las fotos.

La lógica del bot vive en n8n y la operamos nosotros; de tu lado solo quedarían la RPC y el
usuario. ¿Lo vemos en una llamada de 30 minutos? También nos sirve saber si hay un proyecto
Supabase de pruebas.

Te adjunto la propuesta completa (`01-arquitectura-integracion.md`, §3 y §9), los hallazgos
(`06-hallazgos-panel.md`) y el formato del lead.

¡Gracias!
Studio2894

---

## Bernardo

**Asunto:** PoC WhatsApp: ¿nos compartes 5–10 conversaciones de ejemplo?

¡Hola, Bernardo!

Ya tenemos un primer guion del bot. Pregunta nombre, tipo de inmueble, auto, ubicación y
distancia del tablero, pide fotos y te pasa a ti los casos de flotilla o los que pidan hablar
con alguien. Antes de afinarlo necesitamos ver cómo te escriben de verdad los clientes:

- 5–10 capturas de conversaciones (tapando datos personales): 2 de agencia, 2 de particulares,
  1 de flotilla y 1 que no se cerró, si es posible.
- Qué datos y qué fotos pides hoy, y en qué orden.
- Cuánto tardas hoy en promedio en contestar a un prospecto nuevo. Es nuestra línea base para
  medir la mejora.
- Cómo prefieres recibir el aviso de cada lead nuevo (WhatsApp, correo, CRM).
- Marcas y modelos de auto más frecuentes.

Te adjunto el guion para que lo revises (sobre todo cómo suena) y la sección B de la plantilla.

¡Gracias!
Studio2894
