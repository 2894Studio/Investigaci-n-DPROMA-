# Decisiones de producto — módulo de clientes

Nueve hallazgos del documento de recomendaciones del padrón no se arreglaban con CSS: para
resolverlos había que **decidir cómo se comporta el producto**, y esa decisión no estaba tomada
en ninguna parte.

Se implementaron, porque dejar una pantalla a medias por no decidir cuesta más que decidir y
anotarlo. Pero son **decisiones nuestras, no del cliente**. Este documento existe para que se
sepa cuáles son y se puedan revocar sin arqueología.

Cada una lleva: qué pasaba, qué decidimos, por qué, y **qué habría que validar con DPROMA**.

---

## 1. El botón «Columnas» ahora hace algo

**Hallazgo 1.7.** Junto al selector de densidad había un botón «Columnas» que no abría nada.

**Decisión.** Se construye: elegir qué columnas se ven, reordenarlas, y **guardar la preferencia
por persona**. Se descartó retirarlo, que era la otra salida limpia.

**Por qué.** La tabla del padrón tiene siete columnas y ya venía con una apagada de fábrica
(«contacto principal», que se cortaba en casi todas las filas). Es decir, la necesidad de elegir
columnas ya estaba reconocida en el diseño; lo que faltaba era el control. Retirar el botón
habría dejado la decisión congelada en la que tomó quien hizo la maqueta.

**A validar.** Dónde se guarda la preferencia. Si es por persona, necesita una tabla de
preferencias de usuario que hoy no está en el esquema. Mientras tanto queda en el navegador,
que se pierde al cambiar de equipo.

---

## 2. Registros por página elegibles

**Hallazgo 1.9.** El pie fijaba seis registros sobre un padrón de 1.248.

**Decisión.** Selector de 10 / 25 / 50 / 100, con la elección recordada entre sesiones.

**Por qué.** No hay nada que decidir sobre si hace falta: revisar un conjunto grande a seis por
página es inviable. Lo que sí decidimos son los cuatro valores y que 25 sea el de partida.

**A validar.** Si el listado se va a exportar con frecuencia, quizá el tope alto deba ser mayor
que 100. Depende de cuánto aguante la consulta, que es una pregunta de backend.

---

## 3. Desactivar un cliente confirma y se puede deshacer

**Hallazgo 1.8.** «Desactivar» estaba a un clic de «Exportar selección», sin confirmación y sin
explicar qué implica.

**Decisión.** Tres cambios: la acción se separa del grupo, confirma nombrando a cuántos y a
quiénes afecta, y se puede deshacer después.

> Vas a desactivar 2 clientes: Grupo Automotriz ELEKTRA y Flotillas GNP.
> Dejarán de aparecer en el padrón activo; sus órdenes y documentos siguen consultables.

**Por qué.** La pregunta que el hallazgo dejaba abierta —«¿deja de aparecer?, ¿se pueden seguir
consultando sus órdenes?»— hay que responderla en el texto de confirmación, así que hubo que
elegir una respuesta. Elegimos la conservadora: desactivar **oculta del padrón activo pero no
borra ni desvincula nada**.

**A validar con DPROMA.** Es la decisión de más calado de esta lista. Si desactivar debe además
impedir facturar, bloquear órdenes en curso o liberar el RFC para otro registro, el texto de
confirmación miente y hay que rehacerlo.

---

## 4. Se pueden retirar contactos

**Hallazgo 3.1.** Cada correo, teléfono y dirección solo tenía botón de editar. Al llegar al
tope de cuatro, el sistema desactivaba «Añadir» y decía «Retira uno para añadir otro correo» —
y no existía ninguna forma de retirarlo. Callejón sin salida.

**Decisión.** Se añade «Retirar» en cada renglón, con confirmación breve, y el mensaje del tope
enlaza directamente a esa acción.

**Por qué.** Era el único hallazgo que dejaba a la persona sin salida posible. Había que abrir
una.

**A validar.** Si por trazabilidad no se puede borrar un dato de contacto —porque cuelga de él
un acuse de recibo o una notificación enviada—, la acción debe ser «Archivar» o «Marcar como no
vigente» en vez de «Retirar». La interfaz es la misma; cambia el verbo y lo que pasa por debajo.
**Esta es la pregunta que hay que hacer antes de construirlo.**

---

## 5. Los documentos se suben, no se escriben

**Hallazgo 4.2.** «Constancia de situación fiscal» e «Identificación del representante» eran
campos de texto vacíos, aunque la ayuda dijera que se espera un PDF o una foto.

**Decisión.** Control de subida real: arrastrar o examinar, con formatos y peso indicados, el
archivo cargado visible con su nombre y fecha, y opción de reemplazar o quitar.

**Por qué.** No es una decisión de producto discutible: el campo no podía cumplir su función.
Lo que sí decidimos son los límites — **PDF, JPG y PNG, hasta 10 MB**.

**A validar.** El peso máximo y si se admiten fotos de móvil sin procesar, que superan los 10 MB
con facilidad. Y dónde se guardan: el plan del padrón menciona expediente en Drive.

---

## 6. Guardado automático, sin botón de guardar

**Hallazgo 4.6.** La barra inferior decía «Borrador guardado hace 1 min» y a la vez ofrecía un
botón «Guardar borrador».

**Decisión.** Se elige el guardado automático. El botón desaparece; queda el indicador de estado.

**Por qué.** De las dos salidas, ésta es la que no pierde trabajo. Y el resto del formulario ya
está escrito asumiendo que el borrador existe: el estado de error dice «lo que capturaste sigue
en el borrador de esta pantalla».

**A validar.** Cada cuánto guarda, y qué pasa con un borrador que nadie retoma. Si un alta a
medias bloquea el RFC para otra persona, hace falta una regla de caducidad.

---

## 7. Dos niveles de obligatoriedad, con nombres distintos

**Hallazgo 4.3.** El aviso de entrada decía que para dar de alta bastaban razón social y RFC.
Al mismo tiempo, tres campos llevaban asterisco de obligatorio y el domicilio fiscal mostraba
error en rojo antes de que nadie escribiera nada.

**Decisión.** No es un error de copy, son dos conceptos que compartían marca:

| Nivel | Significa | Campos |
|---|---|---|
| **Obligatorio para dar de alta** | Sin esto no hay registro | Razón social, RFC |
| **Necesario para facturar o programar** | El registro existe, pero no opera | Domicilio fiscal, código postal, régimen fiscal, los dos documentos |

Se marcan distinto y se nombran distinto. El aviso de entrada se reescribe para decir lo mismo
que marcan los campos.

**Por qué.** Coincide con la regla de negocio que el propio padrón ya declaraba en otra pantalla
—«no se puede programar una instalación para una sucursal con datos fiscales incompletos»—, así
que el segundo nivel no lo inventamos: lo nombramos.

**A validar.** El reparto exacto de campos entre los dos niveles. Lo de arriba es nuestra
lectura de las notas de las maquetas, no una lista que nos hayan dado.

---

## 8. El aviso de duplicados llega plegado

**Hallazgo 2.1.** La tarjeta de razones sociales parecidas ocupaba la parte alta del contenido,
antes de la tabla. Aparecía siempre, aunque nadie fuera a resolver duplicados ese día.

**Decisión.** Se convierte en un aviso de una línea, plegado por omisión —«2 posibles duplicados
— revisar»— que se despliega al pulsarlo.

**Por qué.** Es información valiosa pero puntual, y desplazaba hacia abajo lo que sí se consulta
a diario. Plegar conserva el aviso y devuelve la pantalla.

**A validar.** Si resolver duplicados resulta ser una tarea frecuente y no puntual, el sitio
correcto es una sección propia dentro del padrón, no un aviso plegado. Es una pregunta de
frecuencia real, que sabremos cuando el padrón esté cargado.

---

## 9. El control de densidad se retira

**Hallazgo 1.3.** «Cómoda» y «Compacta» reducían el espaciado sin reducir contenido, así que la
vista compacta se leía peor sin mostrar más.

**Decisión.** Se retira el control. La tabla se queda en densidad cómoda.

**Por qué.** El hallazgo admitía dos salidas: hacer que compacta redujera también contenido, o
quitarla. Se implementó la primera y después se optó por la segunda. Dos botones permanentes en
la barra de filtros, para una preferencia que casi nadie cambia, compiten por atención con los
controles que sí se usan a diario — y la barra ya tiene cuatro filtros, el aviso de columnas
ocultas y, cuando hay selección, su propia barra de acciones.

**A validar.** Si al cargar el padrón real las filas resultan más altas de lo previsto y hay
quien pide ver más de un vistazo, la salida no es devolver los dos botones: es que la densidad
sea una preferencia de la persona, guardada junto a la de columnas, y no un control en pantalla.

---

## Lo que no decidimos

Dos cosas del documento de recomendaciones quedan fuera a propósito.

**El flujo del padrón** (sección 7 del documento): de la entrada del cliente al inicio del
trámite, con los tres orígenes —ICEV, Gestoría, Comercial— y los dos puntos donde el criterio
humano es imprescindible (decidir si dos registros son el mismo cliente, y aprobar el alta). Es
diseño de proceso, no de interfaz. Explica **por qué** existen ciertos estados en estas
pantallas —el registro incompleto, el recordatorio automático, el aviso a las áreas
interesadas— pero no se maqueta aquí.

**El diálogo de edición** (`59_editar_cliente.html`, sección 5): el archivo no llegó. De sus
ocho hallazgos solo se llevó al sistema el patrón de foco, que estaba bien resuelto y merece
generalizarse, y la separación entre maqueta y especificación. Los seis restantes siguen
pendientes.
