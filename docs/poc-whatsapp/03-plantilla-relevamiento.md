# 03 · Relevamiento

> Para completar con Félix y Bernardo. El Cotizador está fuera de alcance, así que aquí no se
> pregunta nada de precios, SKUs ni visitas técnicas. Se puede contestar en este archivo, en una copia de Google
> Docs o en una llamada de 30 min por bloque. Lo que se responda cierra los 🟡 de
> `01-arquitectura-integracion.md`.

**Fecha:** ____ · **Entrevistó:** ____ · **Respondió:** ____

---

## A · Panel (Félix)

> Ya sabemos, por una revisión de solo lectura del panel, que es Supabase + Netlify, que los
> leads viven en `contactos_comerciales` y que las fotos van a Drive con
> `drive-comercial-upload-auth` + `comercial_evidencias` (ver
> `01-arquitectura-integracion.md` §1). Aquí solo queda lo que el código no responde.

### A.1 Entrada
- [ ] ¿De acuerdo con crear un **usuario de servicio** `bot-whatsapp@dproma.com` con un rol propio, sin acceso al panel? ¿O prefieres otra forma (Edge Function con llave)? ____
- [ ] ¿De acuerdo con una RPC `whatsapp_registrar_lead` (SECURITY DEFINER) que cree o actualice la ficha, deduplique por `telefono_norm`, asigne responsable y cree la actividad en Agenda? ¿La escribes tú o te mandamos un borrador SQL? ____
- [ ] ¿A quién se asignan los leads del bot? ☐ siempre Bernardo ☐ por regla (agencia, zona) ____
- [ ] ¿Qué pasa si el teléfono ya existe en una ficha **perdida** o en un prospecto de ICEV? ☐ reactivar ☐ ficha nueva ☐ solo avisar ____

### A.2 Campos nuevos
- [ ] ¿Se pueden agregar estas columnas? ☐ `canal` ☐ `agencia` ☐ `tipo_inmueble` ☐ `metros_aprox` ☐ `medidor_independiente` — o, como plan B, ¿todo en `observaciones_texto`? ____
- [ ] ¿`origen` = `oem` es correcto para un cliente que llega por el enlace de una agencia? ____
- [ ] ¿Dónde guardamos la bitácora del bot (eventos, `wamid`)? ☐ tabla `whatsapp_eventos` en Supabase ☐ solo en n8n ____

### A.3 Fotos
- [ ] ¿`drive-comercial-upload-auth` acepta el token del usuario de servicio? ¿Hay que darle permiso al rol? ____
- [ ] ¿El registro en `comercial_evidencias` se hace con insert directo (RLS) o con una RPC? ____

### A.4 Ambientes
- [ ] ¿Hay un proyecto Supabase de pruebas, o probamos en producción con fichas marcadas como prueba? ____
- [ ] ¿El filtro de webhooks puede vivir como otra Netlify Function del sitio, o lo hospedamos aparte? ____
- [ ] ¿Cómo se versionan los cambios de base de datos (migraciones numeradas tipo 218–223)? ____

### A.5 Seguridad
- [ ] ¿Experiencia previa con n8n? Si se escala a *self-hosted*, ¿dónde viviría? ____
- [ ] ¿Políticas sobre datos de clientes en servicios de terceros (n8n Cloud, Meta)? ____
- [ ] ¿Quién debe aprobar una integración nueva? ____

---

## B · Comercial (Bernardo)

- [ ] **Capturas de 5–10 conversaciones reales** (tapar datos personales), idealmente: 2 de agencia, 2 de particular, 1 de flotilla, 1 que no se cerró.
- [ ] ¿Qué es lo primero que escriben los clientes? ¿Qué preguntan más? ____
- [ ] ¿Qué datos les pides hoy y en qué orden? ____
- [ ] ¿Qué fotos pides? ¿Cuáles son indispensables? ____
- [ ] ¿Cuántos prospectos nuevos por semana? ¿Cuántos por canal (agencia / web / directo / flotilla)? ____
- [ ] ¿Cuánto tardas hoy, en promedio, en contestar el primer mensaje de un prospecto nuevo? ____ *(línea base del KPI)*
- [ ] ¿Cuántos mensajes de ida y vuelta te toma hoy juntar los datos y fotos de un cliente? ____ *(línea base)*
- [ ] Además de la actividad en tu Agenda del panel, ¿quieres el aviso por WhatsApp? ☐ sí ☐ no ☐ correo ____
- [ ] En el cotizador, ¿«Residencial» significa condominio/edificio? ____
- [ ] Lista de agencias aliadas activas y su contacto: ____
- [ ] Marcas y modelos de auto más frecuentes: ____
- [ ] ¿Quién más contesta mensajes de clientes? ____
- [ ] Horario de atención real: ____

## C · Cuentas

- [ ] ¿DPROMA tiene cuenta de **Meta Business**? ¿Verificada? ¿Quién es administrador? ____
- [ ] Número para el bot: ☐ nuevo dedicado ☐ el de Bernardo (coexistencia) ☐ otro ____
- [ ] Nombre visible del perfil de WhatsApp: ____
- [ ] Método de pago para Meta (tarjeta en Billing Hub) y para el orquestador: ____
- [ ] Aviso de privacidad publicado en: ____ (¿quién lo redacta y aprueba?)
- [ ] ¿Quién da el visto bueno para arrancar la PoC? ____
