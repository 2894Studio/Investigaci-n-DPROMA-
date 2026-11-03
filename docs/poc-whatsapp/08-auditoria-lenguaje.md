# 08 · Auditoría de lenguaje

> 03/11/2026 · Página `web/entregables/poc-whatsapp-primer-contacto.html` (v0.5).
> Lectores: equipo comercial y dirección de DPROMA, sin formación técnica.

## Criterios

1. Títulos de sección con sustantivos, sin frases.
2. Una idea por oración. Intros de una o dos líneas.
3. Nombrar las cosas como las nombra el usuario, no como las nombra el sistema.
4. Términos técnicos solo en el anexo (`docs/poc-whatsapp/01–07`).

## Hallazgos y cambios

| Antes | Problema | Ahora |
|---|---|---|
| "Un bot que atiende el primer WhatsApp y deja la ficha lista para Bernardo" | Título con frase | "Bot de primer contacto" |
| "Simulador: lo que ve el cliente y lo que pasa por dentro" | Título con frase | "Simulador" |
| "Del primer 'Hola' a la ficha lista, en cuatro tramos" | Título con frase | "Flujo" |
| "¿Cómo 'aprende' el bot?" | Pregunta como título | "Aprendizaje" |
| "Limitaciones y qué hacemos con cada una" | Título largo | "Limitaciones" |
| "Calculadora de costos mensuales" / "Impacto: el mismo cliente…" | Títulos largos | "Costos" / "Impacto" |
| Etiquetas "n8n", "panel", "aviso" en el paso a paso | Jerga y nombres de herramienta | "Bot", "Panel", "Bernardo", "Atención", "WhatsApp" |
| "WhatsApp lo entrega a n8n (webhook)" | Jerga técnica | "Escribe el cliente · Toca un botón" |
| "Mensaje de servicio dentro de la ventana de 24 h" | Concepto de facturación de Meta | "Al instante y sin costo dentro del mismo día" |
| "Llama a la función del panel `whatsapp_registrar_lead`" | Nombre interno | "Arma la ficha · Con todo lo que contestó el cliente" |
| "Etapa 'Lead'", "Nuevo lead", "leads" | Anglicismo | "Ficha creada", "Nueva ficha", "clientes" |
| "Vía OEM" | Sigla interna | "Agencia · Changan del Valle" |
| "campo nuevo propuesto" | Lenguaje de especificación | "campo por agregar" |
| "Starter · 2,500 ejecuciones" | Jerga de n8n | "plan básico · 2,500 usos" |
| "Filtro de avisos de 'entregado/leído'" | Largo | "Filtro de avisos de lectura" |
| "El bot de esta prueba no usa inteligencia artificial… como se ajusta un formulario después de ver cómo lo llena la gente…" | 3 oraciones para 1 idea | "No usa IA: sigue un guion. No se entrena; se ajusta cada semana." |

## Estructura

- Se quitaron los rótulos sobre cada título ("Míralo funcionar", "Pregunta 1"…). Repetían el título.
- Se quitó la sección "Demo en n8n" de la página. La guía sigue en `07-demo-n8n.md`.
- Simulador: teléfono a la izquierda; casos, controles y paso a paso a la derecha.
  - Los casos son tarjetas del mismo tamaño en una rejilla de 3 columnas (2 en celular).
  - En celular el orden es: casos, teléfono, paso a paso.

## Pendiente

- Validar el tono de los mensajes del bot con Bernardo y con chats reales.
- Mantener la jerga técnica fuera de la página: va en el anexo para Félix.
