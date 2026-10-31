# 03 · Plantilla de relevamiento — PoC WhatsApp primer contacto

> Para completar con cada responsable. Se puede contestar en este archivo, en una copia de Google
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
- [ ] ¿Puede **enviar** webhooks cuando algo cambia (ej. lead pasa a "cotizado")? ____
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

### A.6 Cotizador
- [ ] ¿El cotizador vive dentro del sistema o es aparte (Excel, otra app)? ____
- [ ] ¿Se puede llamar desde fuera con los datos de la tirada y que devuelva total y PDF? ____

### A.7 Orquestador
- [ ] ¿Experiencia previa con ☐ Make ☐ n8n ☐ Zapier ☐ otra: ____ ¿En qué proyectos? ____
- [ ] Si se escala con n8n *self-hosted*, ¿dónde podría vivir? (VPS, Docker, nube existente): ____
- [ ] ¿Quién daría mantenimiento? ____

### A.8 Seguridad
- [ ] ¿Políticas sobre dónde pueden guardarse datos de clientes (fuera del país, terceros)? ____
- [ ] ¿Quién debe aprobar una integración nueva? ____

---

## B · Proceso comercial — Bernardo Padilla

- [ ] **Capturas de 5–10 conversaciones reales** (tapar datos personales), idealmente: 2 de agencia, 2 de particular, 1 de flotilla, 1 que no se cerró.
- [ ] ¿Qué es lo primero que escriben los clientes? ¿Qué preguntan más? ____
- [ ] ¿Qué datos les pides hoy y en qué orden? ____
- [ ] ¿Qué fotos pides? ¿Cuáles son indispensables para cotizar? ____
- [ ] ¿Cuántos prospectos nuevos por semana? ¿Cuántos por canal (agencia / web / directo / flotilla)? ____
- [ ] ¿Cuánto tardas hoy, en promedio, desde el primer mensaje hasta mandar la cotización? ____ *(línea base del KPI)*
- [ ] ¿Qué porcentaje es estándar (≤ 10 m) vs. no estándar? ____
- [ ] Lista de agencias aliadas activas y su contacto: ____
- [ ] Marcas y modelos de auto más frecuentes: ____
- [ ] ¿Quién más contesta mensajes de clientes? ____
- [ ] Horario de atención real: ____

## C · Catálogo y precios — Nacho (Almacén)

- [ ] ¿Dónde vive el catálogo de SKUs? (Excel, sistema, Google Sheets): ____
- [ ] Partidas de una instalación estándar con cantidades: cable THW cal. 6, centro de carga 2 polos, interruptor termomagnético, tubería, caja NEMA, mano de obra, cargador: ____
- [ ] ¿Cada cuánto cambian los precios? ¿Quién los actualiza y cómo? ____
- [ ] ¿Hay margen o descuento distinto para clientes de agencia? ____
- [ ] ¿Cuántos días puede tener un precio antes de considerarse viejo? ____

## D · Visitas técnicas — ICEP (Mauricio CR / Jhonatan Álvarez)

- [ ] ¿Cómo se agenda hoy una visita? ¿Dónde se anota? ____
- [ ] ¿Cuántas visitas por semana pueden hacer? ¿Qué zonas cubren? ____
- [ ] ¿Qué información necesitan antes de ir (fotos, ubicación, datos del medidor)? ____
- [ ] ¿Cómo prefieren recibir la alerta? ☐ WhatsApp ☐ correo ☐ tablero ☐ otro ____
- [ ] ¿Cuánto tarda en salir la oferta formal después de la visita? ____

## E · Dirección — Nicole Calderón / Diana Hernández

- [ ] SLA acordado por etapa (cotización estándar, agendar visita, oferta no estándar): ____
- [ ] Diagrama de derivación vigente (adjuntar): ____
- [ ] ¿Qué decisiones necesitan tomar con los resultados de la PoC? ____
- [ ] Presupuesto mensual aceptable para la PoC: ____
- [ ] Duración de la PoC y criterio de éxito para escalar: ____

## F · Cuentas y accesos

- [ ] ¿DPROMA tiene cuenta de **Meta Business**? ¿Verificada? ¿Quién es administrador? ____
- [ ] Número para el bot: ☐ nuevo dedicado ☐ el de Bernardo (coexistencia) ☐ otro ____
- [ ] Nombre visible del perfil de WhatsApp: ____
- [ ] Cuenta de **Google Drive** donde vivirán las carpetas (compartida, no personal): ____
- [ ] Método de pago para Meta (tarjeta en Billing Hub) y para el orquestador: ____
- [ ] Aviso de privacidad publicado en: ____ (Jurídico)
