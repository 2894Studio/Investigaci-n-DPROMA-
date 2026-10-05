# Pain points por area, con su pantalla candidata

Fuente canonica: `data/insights/*.json` — 11 entrevistas. El campo `area` NO existe en el
pain point; se infiere por `meta.entrevista_id`. Este puente no existia en el repo.

Al citar en F5 usa SIEMPRE el `pp-NNN` y el documento. Nunca `schema/example-output.json`,
que reusa `pp-001..010` para otros dolores.


## soporte administrativo transversal
`data/insights/2026-07-16_soporte-administrativo-transversal.json` · 10 pain points · 9 oportunidades
**Pantallas:** 06-soporte/* (24_tickets, 10_dprimi_asistente, 47_asistente)

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-100` | **alta** | falta_centralizacion, falta_formatos_comunes | No existe repositorio centralizado de contratos comerciales; cada área guarda su copia de forma aislada, generando cobros inconsistentes con lo pactado, reclamos y riesgo | `op-089` alto/medio |
| `pp-106` | **alta** | gestion_por_whatsapp, falta_centralizacion | Una campaña de marketing generó contactos por un número de WhatsApp de uso interno de instalaciones, que no consideraba que le correspondía atender gestoría; se perdió ca | `op-094` alto/medio |
| `pp-097` | **media** | falta_centralizacion, falta_formatos_comunes, gestion_por_whatsapp, trabajo_manual | El alta de clientes se inicia en WhatsApp, sigue por correo y se captura manualmente en Excel; no existen formularios digitales automatizados, y el tiempo de respuesta de | `op-086` alto/medio |
| `pp-098` | **media** | trabajo_manual | Cuando una razón social factura para varias agencias, se identifica manualmente qué sucursal generó el servicio para asociarlo correctamente. | `op-087` medio/bajo |
| `pp-099` | **media** | trabajo_manual | La aprobación de pagos a proveedores externos depende de recibir el comprobante de transferencia; cuando se retrasa, el pedido urgente se demora un día hábil adicional. | `op-088` medio/medio |
| `pp-101` | **media** | falta_centralizacion, trabajo_manual, falta_formatos_comunes | El inventario de EPP, uniformes y materiales de instalación se registra manualmente en Excel, sin integración con el sistema de inventario general de compras. | `op-090` medio/medio |
| `pp-102` | **media** | gestion_por_whatsapp, trabajo_manual | Las cotizaciones de proveedores se envían a Dirección General por WhatsApp para autorización, sin flujo formal con trazabilidad. | `op-091` medio/bajo |
| `pp-104` | **media** | falta_formatos_comunes | La certificación ISO 9001 en curso exige crear procedimientos normalizados y formatos de registro que hoy no existen de forma estandarizada entre departamentos. | `op-093` medio/alto |
| `pp-103` | **baja** | falta_governance_ia | El nivel de uso de IA (Gemini) en la organización es aún muy básico; las consultas de soporte solo abordan configuración de cuentas, sin estrategia de uso más avanzada. | `op-092` bajo/medio |
| `pp-105` | **baja** | falta_centralizacion | Un proyecto previo con un proveedor tecnológico externo se detuvo en la fase de maquetado visual sin avanzar a desarrollo funcional, obligando a revalidar el punto de par | — huerfano |

## almacen e inventario
`data/insights/2026-07-20_gestion-almacen-inventario.json` · 9 pain points · 8 oportunidades
**Pantallas:** 05-.../50_compras_almacen, 45_autorizacion_compra · 03-.../25_consumo_de_material, 36_recetas_despacho, 55_verificacion_pedido

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-032` | **alta** | trabajo_manual, falta_visibilidad_kpis | La ausencia previa de niveles de stock mínimo/máximo definidos provocaba desabastecimientos, obligando a compras de emergencia con sobrecosto de 5%-10%. | `op-032` alto/alto |
| `pp-031` | **media** | falta_formatos_comunes, trabajo_manual | Antes de la llegada del responsable de almacén no existían formatos de registro de entrada/salida de material; las decisiones de despacho se tomaban sin sustento document | `op-031` medio/bajo |
| `pp-033` | **media** | falta_centralizacion, falta_visibilidad_kpis, trabajo_manual | El control de inventario se lleva en un Excel individual operado por una sola persona; los reportes se generan solo bajo solicitud puntual, sin panel periódico automatiza | `op-032` alto/alto |
| `pp-034` | **media** | trabajo_manual | El conteo físico de inventario, identificado como la tarea que más tiempo consume, requiere revisar producto por producto de forma manual. | `op-033` medio/alto |
| `pp-035` | **media** | gestion_por_whatsapp | La coordinación operativa diaria entre almacén, operaciones e instaladores ocurre principalmente por WhatsApp, sin historial estructurado ni trazabilidad. | `op-034` alto/alto |
| `pp-036` | **media** | falta_formatos_comunes, falta_visibilidad_kpis | No existe una definición validada de la cantidad exacta de piezas requerida por tipo de instalación; las cifras han cambiado informalmente sin estudio de campo formal. | `op-035` medio/bajo |
| `pp-037` | **media** | trabajo_manual, falta_visibilidad_kpis | El control de la flota vehicular es completamente manual: no hay GPS instalado; las rutas se reconstruyen a posteriori en Google Maps y el kilometraje se valida con fotos | `op-036` medio/alto |
| `pp-038` | **media** | falta_governance_ia | El responsable de almacén utiliza IA generativa de forma personal y no reglamentada, sin lineamientos ni supervisión definidos por la empresa. | `op-037` medio/bajo |
| `pp-039` | **baja** | falta_visibilidad_kpis, falta_formatos_comunes | No se ha definido el plan logístico ni las políticas de stock mínimo/máximo para los futuros almacenes foráneos (Tijuana y Monterrey). | `op-038` bajo/medio |

## ICEV / operaciones de campo
`data/insights/2026-07-22_coordinacion-tecnica-instalaciones.json` · 11 pain points · 7 oportunidades
**Pantallas:** 03-icev-instalacion-de-cargadores/* (14 maquetas)

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-028` | **alta** | trabajo_manual, gestion_por_whatsapp | La ejecución de instalaciones depende de aprobaciones y recursos de áreas externas; cuando esos vistos buenos se retrasan, la operación queda completamente detenida hasta | `op-025` alto/medio |
| `pp-020` | **media** | gestion_por_whatsapp, falta_centralizacion, trabajo_manual | Las solicitudes de instalación ingresan casi exclusivamente por grupos de WhatsApp de agencias o directamente de clientes; no existe un formulario o canal centralizado de | `op-020` alto/alto |
| `pp-021` | **media** | falta_centralizacion, falta_formatos_comunes, trabajo_manual | La información de clientes de distintas marcas se gestiona en archivos Excel separados; una plataforma piloto fue abandonada y se regresó a Excel. | `op-020` alto/alto |
| `pp-022` | **media** | falta_formatos_comunes, falta_centralizacion, trabajo_manual | La programación y las rutas de instalación se elaboran en un Word manejado aparte, desconectado de la base de datos de clientes en Excel. | `op-020` alto/alto |
| `pp-023` | **media** | falta_governance_ia, trabajo_manual | El uso de IA en el área (optimización de rutas) es puntual, no estandarizado y depende del diseño y mantenimiento personal de un solo integrante del equipo. | `op-021` medio/bajo |
| `pp-024` | **media** | trabajo_manual, falta_formatos_comunes | La validación y despacho de materiales depende de la disponibilidad simultánea de dos personas; cuando alguna no está disponible, los materiales salen sin las firmas de c | `op-022` medio/bajo |
| `pp-025` | **media** | gestion_por_whatsapp, falta_formatos_comunes, trabajo_manual | No existe un proceso formal de devolución o registro de materiales sobrantes al almacén; el ajuste se comunica por WhatsApp y se descuenta manualmente del siguiente pedid | `op-023` alto/alto |
| `pp-026` | **media** | trabajo_manual, falta_centralizacion, falta_visibilidad_kpis | Las hojas de servicio se registran en papel; la conciliación de materiales entre estas hojas y los totales de almacén se realiza como un cruce manual posterior. | `op-023` alto/alto |
| `pp-027` | **media** | gestion_por_whatsapp, trabajo_manual | La solicitud y aprobación de viáticos y recursos financieros para desplazamientos se gestiona a través de un grupo de WhatsApp, sin un flujo estructurado de solicitud-rev | `op-024` medio/medio |
| `pp-029` | **media** | trabajo_manual, falta_formatos_comunes | La cotización de materiales para venta al cliente recae exclusivamente en el mismo rol técnico que supervisa instalaciones; el equipo comercial copia manualmente esos núm | `op-026` medio/bajo |
| `pp-030` | **media** | falta_centralizacion, falta_formatos_comunes | Las herramientas de trabajo diarias del equipo de operaciones se limitan a WhatsApp, Excel y correo electrónico, sin una plataforma centralizada que unifique la gestión d | `op-020` alto/alto |

## comercial + admin vehicular
`data/insights/2026-07-23_comercial-administracion-vehicular.json` · 13 pain points · 8 oportunidades
**Pantallas:** 02-padron-de-clientes/* · 04-tramites-vehiculares-y-cfe/*

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-046` | **alta** | trabajo_manual, falta_visibilidad_kpis | La emisión de facturas depende de una contadora externa que a su vez debe solicitarlas a un tercero, con retrasos de hasta dos meses. | `op-043` alto/alto |
| `pp-040` | **media** | falta_centralizacion, trabajo_manual | El área comercial no cuenta con una herramienta de CRM; el seguimiento de más de 20 clientes activos depende de la memoria del vendedor, sin registro estructurado. | `op-040` alto/alto |
| `pp-041` | **media** | falta_formatos_comunes, falta_centralizacion | Al cerrar un cliente, no existe un formato o procedimiento estándar para transferir la información y responsabilidad del caso hacia operaciones. | `op-040` alto/alto |
| `pp-043` | **media** | gestion_por_whatsapp | Los canales oficiales de coordinación interna se limitan prácticamente a WhatsApp, sin herramienta estructurada. | `op-041` medio/medio |
| `pp-044` | **media** | falta_centralizacion, gestion_por_whatsapp | La documentación de clientes se envía por WhatsApp o se guarda en Drive personal, sin estructura de carpetas compartidas por cliente. | `op-042` medio/medio |
| `pp-045` | **media** | trabajo_manual, falta_formatos_comunes | Las bases de datos de clientes se comparten como Excel adjuntos por correo; los cambios de una parte no se reflejan para la otra. | `op-040` alto/alto |
| `pp-047` | **media** | falta_formatos_comunes, falta_centralizacion | Ante retrasos de facturación o trámites, los clientes contactan directamente al vendedor en lugar del área responsable. | `op-044` medio/bajo |
| `pp-048` | **media** | falta_formatos_comunes, trabajo_manual | El área jurídica es de reciente creación y no se ha definido si la firma de contratos será digital o autógrafa. | `op-045` medio/medio |
| `pp-049` | **media** | falta_formatos_comunes, trabajo_manual | Al no existir procesos ni catálogo de productos establecido, comercial promovió servicios que no existían, obligando a improvisar alianzas con terceros. | — huerfano |
| `pp-050` | **media** | falta_governance_ia | Un colaborador externo del área comercial utiliza IA de forma intensiva para generar listados de agencias, pero la herramienta ha entregado información inexistente sin pr | `op-046` medio/bajo |
| `pp-052` | **media** | falta_centralizacion, falta_formatos_comunes | No existe un área de marketing ni proceso definido para canalizar los contactos comerciales que no cierran venta de forma inmediata. | `op-047` medio/medio |
| `pp-042` | **baja** | falta_formatos_comunes | No existe un cuestionario o formato digital para perfilar a un cliente potencial antes de una visita comercial. | — huerfano |
| `pp-051` | **baja** | falta_governance_ia | El entrevistado reconoce uso mínimo e informal de IA en su trabajo diario, sin haberla incorporado de forma establecida por desconocimiento. | — huerfano |

## direccion / proyectos especiales
`data/insights/2026-07-23_direccion-proyectos-especiales.json` · 10 pain points · 7 oportunidades
**Pantallas:** 01-principal/20_tablero

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-053` | **media** | falta_formatos_comunes, falta_centralizacion | No existen formatos ni flujos de trabajo documentados para los proyectos de expansión, ni etapas definidas. | `op-050` alto/medio |
| `pp-054` | **media** | falta_formatos_comunes | No existe un formato estandarizado de información mínima de viabilidad que deba entregarse al iniciar un proyecto. | `op-051` alto/medio |
| `pp-055` | **media** | gestion_por_whatsapp, falta_formatos_comunes | La solicitud de requerimientos entre comercial y proyectos especiales se realiza de manera informal, principalmente por WhatsApp o correo. | `op-051` alto/medio |
| `pp-056` | **media** | falta_formatos_comunes, trabajo_manual | La información inicial que llega de comercial suele ser incompleta, obligando a saltar el canal habitual y contactar directamente a terceros. | `op-051` alto/medio |
| `pp-057` | **media** | falta_formatos_comunes | No existe un área legal dedicada ni un proceso definido para la gestión de permisos de construcción y usos de suelo. | `op-052` medio/alto |
| `pp-058` | **media** | falta_visibilidad_kpis, falta_centralizacion | No existe una base de datos ni panel de seguimiento visible del estado de los proyectos. | `op-053` alto/alto |
| `pp-060` | **media** | trabajo_manual, falta_centralizacion | La búsqueda y evaluación de proveedores se realiza de forma completamente manual, sin base de datos centralizada de proveedores. | `op-054` medio/medio |
| `pp-061` | **media** | falta_formatos_comunes, trabajo_manual | Las responsabilidades críticas del flujo de un proyecto se concentran casi en su totalidad en una sola persona, sin proceso documentado de respaldo. | `op-055` medio/bajo |
| `pp-059` | **baja** | falta_centralizacion, falta_formatos_comunes | El trabajo se apoya en múltiples herramientas dispersas (AutoCAD, Google Earth, Office) sin ningún estándar que defina en qué herramienta debe elaborarse cada tipo de doc | — huerfano |
| `pp-062` | **baja** | falta_governance_ia | El uso de IA (redacción de correos, renders) se realiza de manera individual y discrecional, sin políticas ni procesos formales. | `op-056` bajo/bajo |

## juridico y RH
`data/insights/2026-07-28_juridico-recursos-humanos.json` · 8 pain points · 8 oportunidades
**Pantallas:** 05-.../54_bitacora_descargas, 13_panel_asistencia_rhl

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-011` | **alta** | trabajo_manual, falta_formatos_comunes | La elaboración de contratos para casos no estandarizados ('de bomberazo') se realiza manualmente desde cero: se busca inspiración en contratos similares en internet y se  | `op-010` alto/medio |
| `pp-012` | **media** | gestion_por_whatsapp, falta_centralizacion, falta_formatos_comunes | La negociación de cláusulas entre legal, comercial y la contraparte se realiza mediante múltiples canales sin un estándar único: Google Docs, correo y WhatsApp, perdiendo | `op-011` medio/alto |
| `pp-013` | **media** | falta_centralizacion, trabajo_manual | No existe un repositorio documental centralizado para documentos corporativos ni para los expedientes de clientes ('padrón'); se maneja como un archivo disperso sin contr | `op-012` alto/medio |
| `pp-014` | **media** | trabajo_manual, falta_centralizacion | Los documentos de cada colaborador se gestionan de forma manual en carpetas individuales de Drive, sin firma digital ni portal de autoservicio donde el empleado consulte  | `op-013` medio/alto |
| `pp-015` | **media** | trabajo_manual, falta_formatos_comunes, falta_centralizacion | El proceso de solicitud de viáticos depende de formatos que los colaboradores llenan y reenvían manualmente por correo; se identifica como cuello de botella, agravado por | `op-014` medio/medio |
| `pp-016` | **media** | falta_governance_ia | El uso de IA para generar borradores de contratos de obra en proyectos nuevos se realiza de manera ad hoc, según criterio individual, sin política formal sobre qué datos  | `op-015` medio/bajo |
| `pp-017` | **baja** | falta_visibilidad_kpis | No existe un panel o reporte de indicadores sobre la gestión legal/RH; el responsable aprende por iniciativa propia SQL y Python para generar estadísticas básicas. | `op-016` bajo/medio |
| `pp-018` | **baja** | falta_formatos_comunes, falta_centralizacion | Existe ambigüedad terminológica entre áreas sobre conceptos operativos clave (ej. qué es el 'padrón' de clientes), por falta de documentación compartida de procesos entre | `op-017` bajo/bajo |

## direccion comercial / cobranza
`data/insights/2026-07-30_direccion-comercial-cobranza.json` · 7 pain points · 6 oportunidades
**Pantallas:** 05-.../46_cuentas_por_cobrar, facturacion · 02-padron-de-clientes/*

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-077` | **alta** | falta_formatos_comunes, falta_centralizacion, trabajo_manual | Cada grupo automotriz exige campos de validación distintos (TOT, VIN) no estandarizados para facturar, generando un cuello de botella financiero de casi 2 millones de pes | `op-069` alto/medio |
| `pp-078` | **alta** | falta_centralizacion, gestion_por_whatsapp | Sin canal oficial trazable para autorizar clientes finales, vendedores comparten directamente el teléfono del equipo; las agencias luego no reconocen esos casos y no paga | `op-070` alto/medio |
| `pp-074` | **media** | falta_centralizacion, falta_visibilidad_kpis | No existe un espacio donde el cliente pueda consultar por sí mismo el estatus de sus trámites (placas), generando disputas sobre a quién corresponde la responsabilidad de | `op-066` medio/alto |
| `pp-075` | **media** | trabajo_manual | El envío de reportes semanales a clientes B2B se realiza de forma manual y sin horario fijo, provocando que se envíen cada vez más tarde. | `op-067` medio/medio |
| `pp-076` | **media** | gestion_por_whatsapp, falta_centralizacion, falta_formatos_comunes | La recepción de datos de clientes finales para instalaciones se realiza de forma informal por WhatsApp o correo, sin formato estandarizado, y algunos registros se pierden | `op-068` medio/medio |
| `pp-079` | **media** | trabajo_manual, falta_formatos_comunes | Los reportes de estatus e instalación se elaboran a mano sin plantilla automatizada. | `op-067` medio/medio |
| `pp-080` | **media** | falta_centralizacion, trabajo_manual | La gestión de cobranzas ha recaído informalmente en Dirección comercial, ante la ausencia de un proceso o sistema definido de seguimiento de pagos. | `op-071` medio/bajo |

## administracion vehicular
`data/insights/2026-07-31_administracion-vehicular-equipo.json` · 9 pain points · 7 oportunidades
**Pantallas:** 04-tramites-vehiculares-y-cfe/* (10 maquetas)

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-084` | **alta** | falta_centralizacion, falta_formatos_comunes, gestion_por_whatsapp | Los clientes asignan trámites por canales distintos sin alerta centralizada; si no se comparte a tiempo, se pierde al menos un día completo antes de iniciar trámites de g | `op-074` alto/alto |
| `pp-081` | **media** | trabajo_manual, falta_centralizacion | La operación (300-900 trámites mensuales) se gestiona en hojas de Excel con macros y semáforos, compartidas de forma colaborativa entre múltiples usuarios internos y del  | `op-072` alto/alto |
| `pp-082` | **media** | gestion_por_whatsapp | La comunicación interna y con clientes depende en gran medida de grupos de WhatsApp, restando formalidad y generando ambigüedad sobre quién responde. | `op-073` alto/alto |
| `pp-083` | **media** | gestion_por_whatsapp, falta_centralizacion | Clientes contactan de manera directa e informal a integrantes específicos del equipo por WhatsApp, evadiendo un canal único. | `op-073` alto/alto |
| `pp-085` | **media** | falta_visibilidad_kpis, gestion_por_whatsapp | No existe un panel para que el cliente consulte en tiempo real el estatus de sus trámites, generando esperas de hasta una hora sin respuesta. | `op-075` medio/medio |
| `pp-086` | **media** | gestion_por_whatsapp, falta_centralizacion | El equipo maneja más de 400 grupos de WhatsApp, dificultando el control y aumentando el riesgo de que una solicitud pase desapercibida. | `op-073` alto/alto |
| `pp-087` | **media** | trabajo_manual | El proceso de liberación de viáticos pasa secuencialmente por 4 niveles de aprobación, sin política de montos exentos ni tiempos máximos de respuesta. | `op-076` medio/bajo |
| `pp-089` | **media** | trabajo_manual | No existe un criterio único para asignar la responsabilidad de trámites de alto volumen; los dos responsables del área tienen visiones distintas (por persona vs. por loca | `op-078` medio/bajo |
| `pp-088` | **baja** | trabajo_manual, falta_governance_ia | El reporteo interno de movimientos se elabora manualmente, sin criterios definidos sobre uso de IA, aun reconociendo el área como poco desarrollada. | `op-077` bajo/medio |

## direccion general / supervision
`data/insights/2026-07-31_direccion-general-supervision-operativa.json` · 11 pain points · 9 oportunidades
**Pantallas:** 01-principal/20_tablero · 05-.../40_usuarios

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-063` | **alta** | falta_centralizacion, falta_visibilidad_kpis, trabajo_manual | La dirección general no cuenta con un tablero de control único que consolide en tiempo real información financiera, de facturación, cuentas por cobrar, inventario y estad | `op-057` alto/alto |
| `pp-065` | **alta** | trabajo_manual, falta_formatos_comunes, falta_visibilidad_kpis | La falta de un control sistemático de inventario permitió un faltante significativo de material que no fue detectado a tiempo, obligando a investigar manualmente y contra | `op-059` alto/medio |
| `pp-068` | **alta** | falta_formatos_comunes, falta_visibilidad_kpis, falta_centralizacion | El seguimiento comercial con agencias carece de rigor y registro estructurado, lo que ha provocado pérdida explícita de oportunidades de negocio. | `op-062` alto/medio |
| `pp-069` | **alta** | falta_visibilidad_kpis, trabajo_manual | No existen alertas automáticas que señalen cuando un cliente no ha sido contactado dentro de las primeras 24 horas o cuando no se cumple una visita técnica. | `op-062` alto/medio |
| `pp-064` | **media** | gestion_por_whatsapp, falta_centralizacion | La coordinación diaria con todas las áreas se realiza a través de más de 70 grupos de WhatsApp sin historial estructurado, lo que puede provocar pérdida de información re | `op-058` medio/alto |
| `pp-066` | **media** | trabajo_manual, gestion_por_whatsapp | La aprobación de fondos para operaciones depende de un flujo manual por chat con validación de visto bueno de dos personas, sin un sistema formal de aprobación. | `op-060` medio/medio |
| `pp-067` | **media** | falta_centralizacion, trabajo_manual, falta_visibilidad_kpis | Para revisar reportes y evidencias fotográficas fuera de lo que circula en los chats, la dirección general debe solicitarlos manualmente, generando demoras para revisione | `op-061` medio/medio |
| `pp-070` | **media** | falta_governance_ia | No hay criterios definidos ni un proceso maduro para el uso de inteligencia artificial en la operación; se reconoce el riesgo de que fallas del asistente virtual queden s | `op-063` medio/bajo |
| `pp-071` | **media** | falta_visibilidad_kpis | Los reportes actuales no son visuales ni gráficos, lo que dificulta identificar rápidamente problemas operativos antes de que escalen. | `op-057` alto/alto |
| `pp-072` | **baja** | trabajo_manual | La falta de espacio físico adecuado para reunir a varias áreas obliga a resolver pendientes llamando a cada persona de forma individual. | `op-064` bajo/bajo |
| `pp-073` | **baja** | falta_centralizacion, trabajo_manual | El software actual usado para los cargadores eléctricos presenta limitaciones funcionales, quedando corto para diferenciarse ante el cliente final y conectarse con otras  | `op-065` bajo/alto |

## finanzas, cobranza y almacen
`data/insights/2026-07-31_finanzas-cobranza-almacen.json` · 7 pain points · 7 oportunidades
**Pantallas:** 05-direccion-y-administracion/* (14 maquetas)

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-090` | **alta** | trabajo_manual | El proceso de facturación requiere validación manual exhaustiva de números de serie (VIN) contra las plataformas de cada cliente y corrección manual de errores en las pre | `op-079` alto/alto |
| `pp-091` | **media** | falta_formatos_comunes, falta_centralizacion | Otras áreas no envían información previa ni utilizan formatos específicos y estandarizados al solicitar aprobaciones, generando situaciones imprevistas al gestionar autor | `op-080` medio/bajo |
| `pp-092` | **media** | trabajo_manual | El proceso de compras es completamente manual: requisición, evaluación de costo/tiempo/calidad, autorización, transferencia de fondos, pago y entrega de comprobante, todo | `op-081` medio/alto |
| `pp-094` | **media** | trabajo_manual, falta_centralizacion | Para confirmar que un servicio fue ejecutado, especialmente ante reclamos de clientes, finanzas debe revisar manualmente múltiples fuentes dispersas sin un repositorio ún | `op-083` medio/alto |
| `pp-096` | **media** | trabajo_manual | La comprobación fiscal de viáticos depende de un seguimiento manual de plazos estrictos; si el colaborador no cumple el plazo, debe cubrir el costo de su bolsillo. | `op-085` medio/medio |
| `pp-093` | **baja** | trabajo_manual | La gestión de caja chica y la validación de gastos de transporte público se realizan de forma manual, exigiendo comprobante fiscal caso por caso. | `op-082` bajo/bajo |
| `pp-095` | **baja** | falta_governance_ia | Se utilizan herramientas de inteligencia artificial de forma informal, sin que exista una política o criterio formal que regule su uso. | `op-084` bajo/bajo |

## administracion y finanzas
`data/insights/2026-09-10_administracion-finanzas.json` · 11 pain points · 8 oportunidades
**Pantallas:** 05-direccion-y-administracion/* (14 maquetas)

| pp | sev | categorias | descripcion | oportunidad (impacto/esfuerzo) |
|---|---|---|---|---|
| `pp-107` | **alta** | falta_formatos_comunes, trabajo_manual | La solicitud de viáticos no recoge los datos mínimos del viaje: no dice quién viaja, qué necesita ni cuánto tiempo estará fuera. Sin esos campos no se puede presupuestar  | `op-095` alto/bajo |
| `pp-108` | **alta** | falta_formatos_comunes, falta_visibilidad_kpis | Las áreas operativas piden dinero a cualquier hora y sin planificación previa, lo que convierte cada solicitud en una urgencia y deja a dirección gestionando el flujo de  | `op-095` alto/bajo |
| `pp-109` | **alta** | trabajo_manual, falta_centralizacion | Los datos fiscales del cliente se transcriben a mano de una hoja a otra. Un error en la razón social o el RFC provoca el rechazo fiscal de la factura y obliga a rehacer e | `op-097` alto/medio |
| `pp-110` | **alta** | trabajo_manual | La revisión manual de facturas para detectar datos mal capturados consume más de 16 horas semanales de una sola persona del área. | `op-097` alto/medio |
| `pp-111` | **alta** | falta_centralizacion, falta_formatos_comunes, trabajo_manual | Los trámites vehiculares y la facturación dependen del número de serie del vehículo (VIN) y de la razón social, que hoy se copian a mano entre áreas. Los datos llegan err | `op-097` alto/medio |
| `pp-112` | **alta** | falta_formatos_comunes | Se contrata a instaladores y proveedores sin verificar que puedan emitir factura, de modo que el gasto operativo no es deducible. No hay catálogo depurado ni tope de cost | `op-099` alto/medio |
| `pp-113` | **alta** | trabajo_manual, falta_formatos_comunes | La comprobación de viáticos llega tarde o no llega, y los recursos sobrantes no siempre se devuelven. No hay mecanismo que avise del plazo ni que escale el incumplimiento | `op-096` alto/bajo |
| `pp-117` | **alta** | falta_visibilidad_kpis, falta_formatos_comunes | Ninguna área tiene presupuesto mensual ni semanal asignado, de modo que no hay techo de gasto contra el que contrastar una solicitud ni forma de estimar cuánto cuesta pre | `op-101` alto/medio |
| `pp-114` | **media** | falta_formatos_comunes, trabajo_manual | La evidencia de gasto llega como fotografía de un recibo o nota simple, que no es fiscalizable. La deducción exige el par completo de archivos del comprobante fiscal: el  | `op-096` alto/bajo |
| `pp-115` | **media** | trabajo_manual, falta_centralizacion | Cuadrar lo que administración registró con lo que finanzas facturó y cobró es un proceso lento, porque cada mitad vive en su propia hoja y no hay identificador común que  | `op-100` alto/medio |
| `pp-116` | **media** | falta_formatos_comunes, falta_visibilidad_kpis | Se manejan estados de factura —pendiente, por cobrar, por pagar, vencida, anulada— sin una definición común ni un flujo documentado que diga quién los cambia, cuándo y co | `op-100` alto/medio |

---

**Totales: 106 pain points · 84 oportunidades · 11 entrevistas.**
(El README dice 95/76/10 — esta obsoleto.)
