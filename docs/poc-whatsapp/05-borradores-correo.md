# 05 · Borradores de correo (no enviados)

## Para Félix Sánchez — relevamiento técnico

**Asunto:** PoC WhatsApp → CRM: lo que necesitamos de tu sistema para arrancar

¡Hola, Félix!

Para avanzar con la PoC del primer contacto por WhatsApp ya tenemos un borrador de
arquitectura: el bot recibe al cliente, un orquestador (proponemos n8n) crea la oportunidad
en tu sistema, guarda las fotos en Drive y separa los casos estándar (≤ 10 m, cotización en
< 2 h) de los que necesitan visita de ICEP.

Lo que falta para cerrar el diseño depende de tu sistema. ¿Nos ayudas con estos puntos?
Pueden ser respuestas cortas o una llamada de 30 minutos:

1. Stack y dónde está hospedado.
2. Si tiene API REST o webhooks para crear y actualizar oportunidades, y cómo se autentica.
3. La entidad de lead/oportunidad: campos, etapas del tablero comercial y cómo se identifica
   a un cliente que ya existe.
4. Si hay ambiente de pruebas.
5. Dónde vive el cotizador y si se puede llamar desde fuera.
6. Tu experiencia con Make, n8n o similares, y dónde podría vivir n8n si escalamos.

Te adjunto la plantilla completa (sección A) y el contrato JSON del lead que proponemos.

¡Gracias!
Studio2894

---

## Para Bernardo Padilla — muestras de chats

**Asunto:** PoC WhatsApp: ¿nos compartes 5–10 conversaciones de ejemplo?

¡Hola, Bernardo!

Ya tenemos un primer guion del bot. Pregunta nombre, tipo de inmueble, auto, ubicación y
distancia del tablero, pide fotos y te pasa a ti los casos de flotilla o los que pidan hablar
con alguien. Antes de afinarlo necesitamos ver cómo te escriben de verdad los clientes:

- 5–10 capturas de conversaciones (tapando datos personales): 2 de agencia, 2 de particulares,
  1 de flotilla y 1 que no se cerró, si es posible.
- Qué datos y qué fotos pides hoy, y en qué orden.
- Cuánto tardas hoy en promedio en mandar una cotización. Es nuestra línea base para medir la
  mejora.
- Marcas y modelos de auto más frecuentes.

Te adjunto el guion para que lo revises (sobre todo cómo suena) y la sección B de la plantilla.

¡Gracias!
Studio2894
