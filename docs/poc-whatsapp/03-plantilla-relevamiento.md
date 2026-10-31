# 03 · Plantilla de relevamiento — PoC WhatsApp primer contacto

> Para completar con Félix y Bernardo. El Cotizador está fuera de alcance, así que aquí no se
> pregunta nada de precios, SKUs ni visitas técnicas. Se puede contestar en este archivo, en una copia de Google
> Docs o en una llamada de 30 min por bloque. Lo que se responda cierra los 🟡 de
> `01-arquitectura-integracion.md`.

**Fecha:** ____ · **Entrevistó:** ____ · **Respondió:** ____

---

## A · Sistema interno / CRM — Félix Sánchez *(prioridad 1)*

### A.1 Stack
- [ ] ¿En qué está construido el sistema? (lenguaje, framework, base de datos): ____
- [ ] ¿Dónde está hospedado? (nube, servidor propio, proveedor): ____
- [ ] ¿Es el mismo sistema que SIO-DPROMA o uno aparte para comercial? ____

### A.2 API y webhooks
- [ ] ¿Tiene API REST (u otra) para **crear** y **actualizar** registros? ¿Documentación? ____
- [ ] ¿Puede **enviar** webhooks cuando algo cambia (ej. cambio de etapa del lead)? ____
- [ ] ¿Límites de peticiones por minuto o tamaño? ____
- [ ] Si no hay API: ¿se puede escribir directo en la base de datos? ¿Con qué usuario y permisos? ____

### A.3 Autenticación
- [ ] ¿Cómo se autentica una integración? ☐ API key ☐ OAuth ☐ usuario/contraseña ☐ token JWT ☐ otro: ____
- [ ] ¿Se puede crear un usuario o llave exclusivo para el orquestador? ____

### A.4 Entidad oportunidad / lead
- [ ] ¿Existe hoy una entidad "lead", "oportunidad" o "prospecto"? ¿Cómo se llama? ____
- [ ] Lista de campos con tipo y si son obligatorios (adjuntar captura o export): ____
- [ ] ¿Hay un tablero comercial con etapas? ¿Cuáles? ____
- [ ] ¿Cómo se identifica a un cliente que ya existe? (teléfono, correo, RFC): ____
- [ ] ¿Se pueden guardar enlaces a archivos (Drive) o adjuntos? ____
- [ ] ¿Guarda fecha y hora de cada cambio de etapa (para medir el SLA)? ____

### A.5 Ambientes
- [ ] ¿Hay ambiente de pruebas separado de producción? URL: ____
- [ ] ¿Se pueden cargar datos de prueba sin afectar reportes? ____

### A.6 Orquestador
- [ ] ¿Experiencia previa con ☐ Make ☐ n8n ☐ Zapier ☐ otra: ____ ¿En qué proyectos? ____
- [ ] Si se escala con n8n *self-hosted*, ¿dónde podría vivir? (VPS, Docker, nube existente): ____
- [ ] ¿Quién daría mantenimiento? ____

### A.7 Seguridad
- [ ] ¿Políticas sobre dónde pueden guardarse datos de clientes (fuera del país, terceros)? ____
- [ ] ¿Quién debe aprobar una integración nueva? ____

---

## B · Proceso comercial — Bernardo Padilla

- [ ] **Capturas de 5–10 conversaciones reales** (tapar datos personales), idealmente: 2 de agencia, 2 de particular, 1 de flotilla, 1 que no se cerró.
- [ ] ¿Qué es lo primero que escriben los clientes? ¿Qué preguntan más? ____
- [ ] ¿Qué datos les pides hoy y en qué orden? ____
- [ ] ¿Qué fotos pides? ¿Cuáles son indispensables? ____
- [ ] ¿Cuántos prospectos nuevos por semana? ¿Cuántos por canal (agencia / web / directo / flotilla)? ____
- [ ] ¿Cuánto tardas hoy, en promedio, en contestar el primer mensaje de un prospecto nuevo? ____ *(línea base del KPI)*
- [ ] ¿Cuántos mensajes de ida y vuelta te toma hoy juntar los datos y fotos de un cliente? ____ *(línea base)*
- [ ] ¿Cómo quieres recibir el aviso de lead nuevo? ☐ WhatsApp ☐ correo ☐ notificación del CRM ☐ otro ____
- [ ] Lista de agencias aliadas activas y su contacto: ____
- [ ] Marcas y modelos de auto más frecuentes: ____
- [ ] ¿Quién más contesta mensajes de clientes? ____
- [ ] Horario de atención real: ____

## C · Cuentas y accesos (Félix o quien administre las cuentas)

- [ ] ¿DPROMA tiene cuenta de **Meta Business**? ¿Verificada? ¿Quién es administrador? ____
- [ ] Número para el bot: ☐ nuevo dedicado ☐ el de Bernardo (coexistencia) ☐ otro ____
- [ ] Nombre visible del perfil de WhatsApp: ____
- [ ] Cuenta de **Google Drive** donde vivirán las carpetas (compartida, no personal): ____
- [ ] Método de pago para Meta (tarjeta en Billing Hub) y para el orquestador: ____
- [ ] Aviso de privacidad publicado en: ____ (¿quién lo redacta y aprueba?)
- [ ] ¿Quién da el visto bueno para arrancar la PoC? ____
