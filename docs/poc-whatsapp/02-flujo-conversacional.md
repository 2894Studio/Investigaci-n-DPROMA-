# 02 · Flujo conversacional del bot (borrador)

> Borrador v0.2 · 31/10/2026. El bot captura datos y avisa a Bernardo; no cotiza (el Cotizador
> es otra iniciativa). Los textos tienen que pasar por Bernardo: él sabe cómo le
> hablan los clientes. Se ajustan con las capturas que mande (relevamiento B).

## Principios

- **Pocas preguntas, de un toque.** Se usan botones (máximo 3 por mensaje) y listas (máximo 10
  opciones). Solo el nombre se escribe.
- **Nunca un callejón sin salida.** Escribir `asesor` en cualquier momento pasa con una persona.
- **No preguntar lo que ya sabemos.** El teléfono viene del propio WhatsApp. La marca del
  auto viene del enlace de la agencia.
- **Tono:** de tú, cordial y breve, sin tecnicismos ("tablero eléctrico", no "centro de
  carga").
- **Se mide el abandono en cada paso** para saber qué pregunta sobra.

## Guion

### 0 · Bienvenida + nombre
> ¡Hola! 👋 Soy el asistente de **DPROMA**. En un par de minutos tomo los datos para preparar la
> cotización de la instalación de tu cargador para auto eléctrico.
>
> Al seguir aceptas nuestro aviso de privacidad: {URL_AVISO}
>
> ¿A nombre de quién hacemos la cotización?

- Espera texto. Guarda `nombre`. Si el texto parece una pregunta ("¿cuánto cuesta?"), contesta
  "Con gusto te digo el precio exacto, solo necesito unos datos 🙂" y repite la pregunta.
- Si viene de agencia: "¡Hola! Vienes de **{Agencia}**, ¡felicidades por tu auto nuevo! …"

### 1 · Tipo de inmueble (botones)
> Gracias, {nombre}. ¿Dónde quieres instalar el cargador?

`[🏠 Casa]` `[🏢 Empresa / flotilla]` `[Otro lugar]`

- **Empresa / flotilla →** "Para flotillas armamos una propuesta a la medida. Te comunico con
  Bernardo, de nuestro equipo comercial." → `HUMANO` (Bernardo recibe todo lo capturado).
- **Otro lugar →** se sigue normal; Bernardo lo ve en el resumen.

### 2 · Auto (lista) — *se salta si vino de una agencia*
> ¿Qué auto tienes o vas a recibir?

Lista: `Changan Dipal S07` · `BYD` · `MG` · `Tesla` · `Otro…` 🟡 (Bernardo confirma las marcas
más comunes)

- `Otro…` → "¿Cuál? Escríbelo, por favor." (texto libre a `modelo_auto`).

### 3 · Ubicación (solicitud de ubicación)
> ¿Dónde está el lugar de instalación? Puedes compartir tu ubicación 📍 o escribir tu código
> postal.

- Mensaje interactivo de *solicitud de ubicación* (botón "Enviar ubicación").
- Acepta un `location` (lat/long) o un texto con CP de 5 dígitos. Cualquier otra cosa → repite
  una vez y luego pasa a una persona.

### 4 · Distancia (botones)
> Última pregunta 🙌 Más o menos, ¿qué distancia hay **del tablero eléctrico al lugar donde
> vas a cargar el auto**?

`[Hasta 10 metros]` `[Más de 10 metros]` `[No sé]`

- Ayuda opcional antes de los botones: "Un auto mide unos 4.5 m; si caben dos autos entre el
  tablero y el lugar, son unos 9–10 m."

### 5 · Fotos (opcionales, de una en una)
> ¿Nos mandas una foto de tu **tablero eléctrico** (la caja con los interruptores)? Así la
> cotización sale más precisa.

`[Enviar después]`

> ¡Perfecto! Ahora una foto del **lugar donde quieres cargar el auto**.

`[Enviar después]`

> Y por último, si la tienes a la mano, una foto de tu **medidor de CFE**.

`[Enviar después]`

- Cada foto se guarda en Drive con su tipo (`tablero`, `sitio`, `acometida`). 🟡 Bernardo
  confirma cuáles fotos le sirven de verdad; si alguna sobra, se quita.
- `Enviar después` → se le manda el enlace del formulario de carga (plan B).

### 6 · Cierre
> ¡Listo, {nombre}! Ya tenemos todo. **Bernardo, de nuestro equipo**, te escribe para darte tu
> cotización. Nuestro horario es lun–vie 9–18 h, sáb 9–14 h 🟡.

→ Se crea el lead en el CRM y Bernardo recibe el resumen:

```
🔌 Nuevo lead · {origen}
{nombre} · {telefono}
{tipo_inmueble} · {marca_auto} {modelo_auto}
📍 {ubicacion}  · Distancia: {distancia}
📷 {n} fotos: {carpeta_drive_url}
CRM: {enlace_al_lead}
```

🟡 El tiempo que se le promete al cliente lo define Bernardo según su capacidad real.

## Pasar con una persona (*handoff*)

| Disparador | Mensaje al cliente | A quién |
|---|---|---|
| Escribe `asesor`, `humano`, `persona`, `llamar` | "Claro, te comunico con alguien del equipo. Te escribe en {tiempo} 🟡." | Bernardo |
| Elige Empresa / flotilla | ver paso 1 | Bernardo |
| 2 respuestas que el bot no entiende seguidas | "Mejor te comunico con alguien del equipo para no hacerte perder tiempo." | Bernardo |
| Manda audio, video o un documento que no es foto | "¡Gracias! Lo guardo para que lo revise el equipo." (sigue el flujo) | Marca para revisión |
| Escribe después de terminar | Se adjunta como nota del lead | Bernardo |
| Sin respuesta 23 h | — (el lead queda `INCOMPLETO`) | Bernardo |

Bernardo recibe el aviso **con todo lo capturado** (nombre, origen, pasos respondidos, enlace a
fotos), así no tiene que volver a preguntar.

## Recordatorio (sin respuesta 30 min)
> ¿Seguimos, {nombre}? Solo me falta {lo que falta} para tu cotización 🙂

Uno solo. No se insiste más.

## Lo que hay que validar con Bernardo

- [ ] ¿Los clientes entienden "tablero eléctrico"? ¿Cómo lo llaman ellos?
- [ ] Marcas y modelos más frecuentes para la lista del paso 2.
- [ ] ¿La pregunta de distancia le sirve para priorizar? ¿Los clientes pueden contestarla sin ir a medir?
- [ ] ¿Qué fotos son realmente indispensables?
- [ ] Horario de atención y tiempo de respuesta que se puede prometer.
- [ ] ¿Hay preguntas frecuentes (precio, tiempo de instalación, garantía, facturación) que el bot
  debería contestar antes de pedir datos?
