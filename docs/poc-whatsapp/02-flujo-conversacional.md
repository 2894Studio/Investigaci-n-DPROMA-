# 02 · Flujo conversacional del bot (borrador)

> Borrador v0.3 · 02/11/2026. El bot captura datos, crea la ficha en Contactos del panel y
> avisa a Bernardo; **no cotiza** (el Cotizador es otra iniciativa). Las preguntas se
> derivaron de lo que pide el cotizador del panel, para que Bernardo cotice sin volver a
> preguntar (ver la tabla al final). Los textos los revisa Bernardo con las capturas reales
> (relevamiento B).

## Principios

- **Pocas preguntas, casi todas de un toque.** Botones (máximo 3 por mensaje) y listas (máximo
  10 opciones). Solo el nombre y el domicilio se escriben.
- **Nunca un callejón sin salida.** Escribir `asesor` en cualquier momento pasa con una persona.
- **No preguntar lo que ya sabemos.** El teléfono viene del propio WhatsApp. La marca del
  auto viene del enlace de la agencia.
- **Tono:** de tú, cordial y breve, sin tecnicismos ("tablero eléctrico", no "centro de
  carga").
- **Se mide el abandono en cada paso.** Son 6 preguntas: si una pierde mucha gente, se quita
  o se pasa a la llamada de Bernardo.

## Guion

### 0 · Bienvenida + nombre
> ¡Hola! 👋 Soy el asistente de **DPROMA**. En un par de minutos tomo los datos para preparar la
> cotización de la instalación de tu cargador para auto eléctrico.
>
> Al seguir aceptas nuestro aviso de privacidad: {URL_AVISO}
>
> ¿A nombre de quién hacemos la cotización? (persona o empresa)

- Espera texto → `nombre`. Si el texto parece una pregunta ("¿cuánto cuesta?"), contesta
  "Con gusto te damos el precio exacto, solo necesito unos datos 🙂" y repite la pregunta.
- Si viene de agencia: "¡Hola! Vienes de **{Agencia}**, ¡felicidades por tu auto nuevo! …"

### 1 · Tipo de inmueble (botones) → cotizador: «Tipo de inmueble»
> Gracias, {nombre}. ¿Dónde quieres instalar el cargador?

`[🏠 Casa]` `[🏢 Condominio / edificio]` `[Empresa / flotilla]`

- Casa → `Casa particular`. Condominio/edificio → `Residencial`. 🟡 Bernardo confirma que
  "Residencial" significa eso en el cotizador.
- **Empresa / flotilla →** "Para empresas y flotillas armamos una propuesta a la medida. Te
  comunico con Bernardo, de nuestro equipo comercial." → `HUMANO`. La ficha se crea con lo
  que haya.
- Condominio: añadir al cierre "Si tu condominio pide permiso de la administración, ten a la
  mano el reglamento" 🟡 (Bernardo decide si aplica).

### 2 · Vehículo (lista) → cotizador: «Vehículo» — *se salta si vino de una agencia*
> ¿Qué auto tienes o vas a recibir?

Lista: `Changan Dipal S07` · `BYD` · `MG` · `Tesla` · `Otro…` 🟡 (Bernardo confirma las marcas
más comunes)

- `Otro…` → "¿Cuál? Escríbelo, por favor." (texto libre).

### 3 · Domicilio → cotizador: «Domicilio»
> ¿Cuál es el domicilio de la instalación? Calle, número, colonia y código postal.
>
> Si te queda más fácil, también puedes mandar tu ubicación 📍

- Texto → `domicilio`. Se exige un CP de 5 dígitos dentro del texto; con él, n8n obtiene el
  estado (`estado_id`). Si no viene, se pide una vez: "¿Y el código postal?".
- Si manda un `location`, se guarda el enlace de mapa en la observación y se pide igualmente
  el CP. El cotizador necesita el domicilio en texto.

### 4 · Metros aproximados (lista) → cotizador: concepto 1 (incluye 10 m) y concepto 3 (metro desde el 11)
> Más o menos, ¿qué distancia hay **del tablero eléctrico al lugar donde vas a cargar el
> auto**? 📏 Un auto mide unos 4.5 m.

Lista: `Hasta 10 m` · `De 11 a 20 m` · `De 21 a 30 m` · `Más de 30 m` · `No sé`

- Se guarda como `metros_aprox`. No se le dice al cliente si su caso es "estándar": eso lo
  decide Bernardo al cotizar.

### 5 · Medidor (botones) → cotizador: concepto 2 (trámite CFE) y concepto 5 (mufa)
> ¿Quieres un **medidor de CFE independiente** solo para el cargador, o conectarlo a tu luz de
> siempre?

`[Medidor nuevo]` `[Mi luz actual]` `[No sé]`

- Se guarda como `medidor_independiente` (`si` / `no` / `no_se`).
- Ayuda opcional, si el cliente pregunta: "Un medidor aparte permite una tarifa especial para
  autos eléctricos; Bernardo te explica si te conviene."

### 6 · Fotos (opcionales, de una en una) → cotizador: tierra física, mufa, consideraciones
> ¿Nos mandas una foto de tu **tablero eléctrico** (la caja con los interruptores)? Así la
> cotización sale más precisa.

`[Enviar después]`

> Ahora una foto del **lugar donde quieres cargar el auto**, y si se puede, del camino por donde
> iría el cable.

`[Enviar después]`

> Y por último, una foto de tu **medidor de CFE**.

`[Enviar después]`

- Las fotos se suben a la carpeta de la ficha en Drive (`DPROMA — Comercial/{folio}`) y se
  registran en `comercial_evidencias`, igual que si Bernardo las subiera desde el panel.
- Con estas fotos Bernardo puede revisar tierra física, mufa, muro disponible y si hace falta
  andamio (consideraciones del cotizador). 🟡 Él confirma cuáles le sirven; si alguna sobra,
  se quita.
- `Enviar después` → se le manda el enlace del formulario de carga (plan B).

### 7 · Cierre
> ¡Listo, {nombre}! Ya tenemos todo. **Bernardo, de nuestro equipo**, te escribe para darte tu
> cotización. Nuestro horario es lun–vie 9–18 h, sáb 9–14 h 🟡.

→ n8n llama a `whatsapp_registrar_lead`: se crea o actualiza la ficha `lead` en Contactos, se
suben las fotos y queda una actividad en la Agenda de Bernardo. Además le llega este resumen
por WhatsApp:

```
🔌 Nuevo lead WhatsApp · {origen}
Ficha {folio} · {nombre} · {telefono}
🏠 {tipo_inmueble} · 🚗 {vehiculo}
📍 {domicilio}
📏 {metros_aprox} · ⚡ Medidor: {medidor_independiente}
📷 {n} fotos
Abrir ficha: https://panel.dproma.com/#contactos ({folio})
```

🟡 El tiempo que se le promete al cliente lo define Bernardo según su capacidad real.

## Pasar con una persona (*handoff*)

| Disparador | Mensaje al cliente | Qué pasa |
|---|---|---|
| Escribe `asesor`, `humano`, `persona`, `llamar` | "Claro, te comunico con alguien del equipo. Te escribe en {tiempo} 🟡." | Ficha con lo capturado + aviso a Bernardo |
| Elige Empresa / flotilla | ver paso 1 | Igual |
| 2 respuestas que el bot no entiende seguidas | "Mejor te comunico con alguien del equipo para no hacerte perder tiempo." | Igual |
| Manda audio, video o un documento | "¡Gracias! Lo guardo para que lo revise el equipo." (sigue el flujo) | Se adjunta a la ficha |
| Escribe después de terminar | — | Observación en la ficha + aviso |
| Sin respuesta 23 h | — | Ficha con lo que haya y observación "datos incompletos" |

## Recordatorio (sin respuesta 30 min)
> ¿Seguimos, {nombre}? Solo me falta {lo que falta} para tu cotización 🙂

Uno solo. No se insiste más.

## De dónde sale cada pregunta

| Pregunta | Campo o concepto del cotizador | Por qué |
|---|---|---|
| Nombre | Cliente (nombre o razón social) | Encabezado de la cotización |
| Tipo de inmueble | Tipo de inmueble (`Casa particular` / `Residencial`) | Campo del cotizador |
| Vehículo | Vehículo (marca / modelo) | Campo del cotizador |
| Domicilio | Domicilio (calle, número, colonia, CP, ciudad) | Campo del cotizador + zona |
| Metros | 1 · Instalación estándar (10 m incluidos) · 3 · Metro excedente desde el 11 | Define cuántos metros extra cotizar |
| Medidor | 2 · Trámite CFE · 5 · Mufa | Define si entran estos dos conceptos |
| Fotos | 4 · Tierra física · consideraciones (tablero, muro, andamio) | Bernardo valida sin visita |

## Lo que hay que validar con Bernardo

- [ ] ¿"Residencial" en el cotizador es condominio/edificio? ¿Hace falta otra opción?
- [ ] ¿Los clientes entienden "tablero eléctrico" y "medidor independiente"? ¿Cómo lo dicen ellos?
- [ ] Marcas y modelos más frecuentes para la lista del paso 2.
- [ ] ¿Los rangos de metros le sirven? ¿Los clientes pueden estimarlos sin ir a medir?
- [ ] ¿Qué fotos son realmente indispensables?
- [ ] Horario de atención y tiempo de respuesta que se puede prometer.
- [ ] ¿Hay preguntas frecuentes (precio, tiempo de instalación, garantía, facturación) que el bot
  debería contestar antes de pedir datos?
