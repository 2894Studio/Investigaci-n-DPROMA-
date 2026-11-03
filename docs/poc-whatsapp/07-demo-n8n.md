# 07 · Demo n8n

> v0.4 · 02/11/2026. Sirve para **mostrar el bot en una reunión** sin cuenta de Meta, sin número
> de WhatsApp, sin Supabase y sin contraseñas. Usa exactamente el mismo guion que el simulador
> de la página (`web/entregables/poc-whatsapp-primer-contacto.html`).
>
> **Probado** en n8n 2.45.7 local el 02/11/2026: 5 conversaciones completas (agencia, particular
> que escribe libre, flotilla, pregunta de precio y reinicio). Las 43 ejecuciones terminaron
> sin error.

## Qué incluye

| Archivo | Para qué |
|---|---|
| `n8n/demo-bot-whatsapp-dproma.json` | El workflow, listo para importar |
| `n8n/motor-guion.js` | El guion (preguntas, reglas, validaciones). Fuente única para la demo y la página |
| `scripts/build-poc-whatsapp.py` | Después de cambiar el guion, regenera el workflow y la página: `python3 scripts/build-poc-whatsapp.py` |

## Workflow

```
💬 Chat (simula WhatsApp) → ⚙️ Motor del guion → ◇ ¿Terminó la conversación?
                                                    ├─ no → ↩ Responder siguiente pregunta
                                                    └─ sí → 🗂 Simular registro en panel
                                                             → 📣 Simular aviso a Bernardo
                                                             → ↩ Responder al cliente
```

- **Chat (simula WhatsApp):** la ventana de chat que trae n8n. Hace el papel de WhatsApp.
- **Motor del guion:** decide qué preguntar, valida la respuesta y recuerda en qué paso va cada
  conversación.
- **Simular registro en panel:** arma la ficha con los mismos campos que se mandarían a la
  función `whatsapp_registrar_lead` del panel (ver `01-arquitectura-integracion.md` §3).
- **Simular aviso a Bernardo:** el texto que le llegaría por WhatsApp.

En el lienzo hay notas de colores que explican cada bloque.

## Pasos

### 1. n8n
Elige una:
- **n8n Cloud (lo más fácil):** crea una cuenta de prueba gratis en [n8n.io](https://n8n.io).
- **En tu computadora:** con Node.js 24 o superior, ejecuta `npx n8n` y abre
  `http://localhost:5678`.
- **Con Docker:** `docker run -it --rm -p 5678:5678 docker.n8n.io/n8nio/n8n`.

### 2. Importar
- Ya está creado en n8n Cloud de Studio2894: https://studio2894.app.n8n.cloud/workflow/BSGo2SQsDdHyK888
- En otra instancia: en n8n, menú **⋯ → Import from File** y elige `n8n/demo-bot-whatsapp-dproma.json`.

No pide credenciales: ningún nodo se conecta a nada externo.

### 3. Publicar
Botón **Publish**, arriba a la derecha. En versiones anteriores de n8n es el interruptor
**Active**.

> Importante: la memoria de cada conversación solo se guarda con el workflow publicado. Si
> pruebas con el botón **Open chat** del editor sin publicar, el bot olvida tus respuestas y
> vuelve a saludar en cada mensaje.

### 4. Chat
Abre el nodo **Chat (simula WhatsApp)** y copia la **Chat URL**. Ábrela en otra pestaña o
mándala a tu teléfono: se ve como una ventana de chat.

### 5. Conversar
- Empieza con **«Hola, vengo de Changan del Valle»** (detecta la agencia y no pregunta el
  vehículo) o solo con **«Hola»**.
- Las opciones salen numeradas: contesta con el número o con la palabra («casa», «no sé»,
  «depa»…).
- Escribe **«foto»** para simular que mandas una imagen y **«ubicación»** para simular la
  ubicación.
- Escribe **«asesor»** en cualquier momento para pasar a una persona.
- Escribe **«reiniciar»** para empezar de nuevo.

### 6. Ejecuciones
En **Executions** se ve cada mensaje como una ejecución. En la última de una conversación
terminada, el nodo **Simular registro en panel** muestra la ficha completa y **Simular aviso
a Bernardo** el WhatsApp que recibiría.

## Guiones de prueba

| Caso | Escribe, en orden | Qué demuestra |
|---|---|---|
| Cliente de agencia | `Hola, vengo de Changan del Valle` → `Ana López` → `1` → `Av. Coyoacán 1500, Col. Del Valle, CDMX 03100` → `1` → `1` → `foto` → `foto` → `foto` | Caso ideal: 8 respuestas, ficha completa, origen «vía OEM» |
| Particular que escribe | `Hola` → `luis pérez` → `es un depa` → `5` → `MG4` → `Calle Pino 12, Satélite` → `53100` → `3` → `no sé` → `después` → `foto` → `1` | Reconoce palabras («depa», «no sé»), pide el CP si falta, fotos pendientes |
| Flotilla | `Buenas tardes` → `Logística Norte SA` → `3` | Pasa a Bernardo con lo capturado |
| Pregunta el precio | `hola` → `¿cuánto cuesta?` → `¿y el precio?` | Limitación del guion: a la segunda, pasa a una persona |

## Demo vs. piloto

| En la demo | En el piloto |
|---|---|
| Chat de n8n | Webhook de WhatsApp Cloud API (con firma y filtro de avisos) |
| Opciones numeradas | Botones y listas de WhatsApp |
| «foto» simula una imagen | Fotos reales, descargadas de Meta y subidas a Drive |
| Memoria del workflow | Igual, o una tabla en Supabase si Félix lo prefiere |
| «Simular registro en panel» | Función `whatsapp_registrar_lead` en Supabase (ficha + Agenda) |
| «Simular aviso a Bernardo» | Mensaje de WhatsApp a Bernardo |
| Sin recordatorio ni cierre a las 23 h | Workflow programado que revisa conversaciones sin respuesta |

## Edición del guion
1. Edita `n8n/motor-guion.js` (textos en `P`, orden en `ORDEN`, palabras reconocidas en
   `claves`).
2. Ejecuta `python3 scripts/build-poc-whatsapp.py`.
3. Vuelve a importar el JSON en n8n. La página se actualiza sola con el mismo cambio.
