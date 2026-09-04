# Cambios de UX/UI — Administración Vehicular

Esto no es un informe cerrado. Es más bien la memoria de lo que fuimos encontrando mientras
revisábamos las cuatro pantallas del módulo —Tablero, Trámites vehiculares, Detalle de trámite y
Trámites concluidos— y de lo que cada hallazgo terminó dejando escrito en el sistema de diseño,
que al fin y al cabo es lo que sobrevive cuando el proyecto pase a otras manos.

## De qué partíamos

Nos llegaron cuatro maquetas ya construidas, funcionando. No eran un boceto: eran HTML real, con
su sistema de tokens, su tema claro y oscuro, sus estados de carga. La mirada se puso solo en cómo
se usan y cómo se ven, porque el alcance funcional del área quedó congelado a propósito para
revisarlo más adelante. Eso sí, revisar interfaz sin tocar función tiene una ventaja curiosa: te
obliga a mirar de verdad lo que ya está, en vez de proponer lo que falta.

## Un icono que sencillamente no estaba

El primer hallazgo apareció por una captura. En el estado vacío había un botón verde, sólido, con
un icono dentro que no se veía. Al medirlo salió 1,03:1. Para hacerse una idea: el mínimo
aceptable para un elemento gráfico es 3:1, y el mismo botón fuera de ese bloque daba 4,89:1.

La causa era una sola línea. Una regla escrita para teñir de gris los iconos decorativos de los
bloques de estado alcanzaba, en cascada, a todos los iconos que hubiera dentro —incluidos los que
van dentro de un botón que ya tiene su propio color. El arreglo fue acotar el selector a hijo
directo. Tres caracteres. Pero la regla que sacamos de ahí vale más que el arreglo: una regla que
tiñe por contexto no debe pisar a un elemento que ya declaró el suyo.

## El medallón que se veía apagado

Los estados vacío y de error llevan un medallón redondo con un glifo. La receta original pedía un
fondo del color de acento al diez por ciento de opacidad, con el glifo del mismo color. Sobre el
papel es elegante. En pantalla se lee desvaído, sin la presencia que debería tener el único
elemento gráfico de una pantalla que, por definición, está vacía.

Pasó a relleno sólido con la tinta del par. Y aquí hubo una decisión que no era obvia: no vale
blanco literal. Blanco sobre el verde en tema oscuro da 2,27:1, o sea, peor que el problema que
veníamos a arreglar. La tinta tiene que voltear según el tema. Con eso, los números quedaron entre
4,84 y 6,38:1 medidos en las dos variantes.

## Cincuenta cifras en una pantalla

El tablero era el caso más serio, y no por un error puntual sino porque mezclaba dos preguntas
distintas en el mismo plano visual. Una es qué urge. La otra es dónde está cada expediente. Cuatro
plazas, once cifras cada una, más los chips de arriba y la cabecera: alrededor de cincuenta
números pidiendo atención a la vez, sin que ninguno la consiguiera.

La reducción no salió de recortar a ojo, salió de una partición que ya estaba en la documentación
de Calendario Laboral y nadie había usado como criterio visual. Un trámite o tiene el reloj
corriendo o no lo tiene. Si corre, está en plazo, por vencer o vencido: tres casillas excluyentes,
y eso sí es un semáforo. Si no corre, o es que aún no se admitió o es que ya se cerró, y ninguno
de los dos casos tiene un plazo contra el que medirse, así que salen del semáforo y se explican al
pie. «Observado», que estaba ocupando una cuarta casilla, resultó no ser un estado de plazo sino
una marca: su reloj sigue corriendo, con lo cual ya estaba contado. Pasó a contador secundario.

El eje del estado del expediente, que es de segundo nivel, se fue entero detrás de un botón de
cascada por plaza. Cada tarjeta quedó en reposo con dos a cuatro cifras. Las plazas se ordenan por
urgencia, de modo que el ojo cae en el problema sin buscarlo, y un conteo en cero directamente no
se pinta —con el total declarado y la barra delante, la ausencia se lee como cero sin necesidad de
escribirlo.

Ah, y de paso aparecieron dos ejes de datos que no reconciliaban entre sí. El semáforo decía cuatro
sin reloj donde la lista de estados implicaba cinco. Se recalcularon para que cerraran.

## Gráficas, por fin

Diecinueve componentes documentados y ni uno solo de dato visual. Ni una cifra destacada, ni una
barra, ni una tendencia. Se abrió una capa de dashboard con nueve piezas, Chart.js por CDN con
versión fijada, y cuatro condiciones que son las que hacen que una librería de terceros obedezca al
sistema en vez de imponer su estilo: los colores se leen de las variables CSS en tiempo de
ejecución, los gráficos se repintan al cambiar de tema, no animan bajo movimiento reducido, y el
botón de tema no depende de que la librería cargue.

Esa última salió de un error propio, todo hay que decirlo. Un `return` temprano cortaba el script
entero cuando el CDN fallaba y se llevaba por delante el cambio de tema.

Hay una regla que conviene subrayar porque es la que más se incumple por ahí: el `<canvas>` no es
accesible. Cada gráfico lleva su tabla equivalente, y esa tabla es la fuente de verdad del dato, no
un añadido para cumplir. De ahí se sigue lo demás: si la librería no llega, desaparece el lienzo y
se abre la tabla. Estas maquetas se abrían desde disco sin internet, y al meter una dependencia
externa eso dejó de ser cierto.

También hubo que tocar la paleta. Los dos colores de serie que había fallaban medidos uno contra
otro: 1,1 de ΔE en protanopia, 10,0 en visión normal, cuando el suelo razonable son 15. El sistema
los había medido solo contra el fondo, que es un despiste facilísimo de cometer. Se sustituyeron
por cuatro validados en los dos temas.

## Dos anillos verdes donde debía haber uno

El buscador de la lista es un contenedor con borde de pastilla que envuelve a un campo sin borde.
Para quien lo mira es un control. Estaba pintando dos anillos concéntricos al recibir el foco,
porque el contenedor dibujaba el suyo y el campo de dentro añadía el estándar. Se ve raro, aunque
al principio cuesta identificar por qué.

Ahora el anillo va una vez, en el elemento que la persona percibe como el control. La regla general
quedó así: si un contenedor reacciona al foco dibujando algo, ningún descendiente suyo dibuja
además.

## Los filtros, que se habían quedado a medias

En la pantalla de trámites convivían cuatro contadores de estatus arriba y un desplegable
«Estatus: Todos» diez píxeles más abajo. Dos controles del mismo campo, uno al lado del otro, sin
reflejarse. El sistema ya tenía escrita la regla —un filtro, un sitio— y solo faltaba el
corolario: cuando la barra ya cubre esa dimensión, la fila de contadores sobra y se retira.

Después vino la parte grande. Los desplegables eran botones sin panel, con un valor por dimensión y
sin posibilidad de pedir Querétaro Centro *y* Celaya a la vez, que es exactamente lo que hace
falta en un listado real. Ahora cada dimensión abre un panel con buscador y casillas, con el
conteo de cada opción a la derecha —esto importa más de lo que parece: permite decidir sin aplicar
el filtro para ver qué pasa— y un «Limpiar» acotado a esa dimensión.

Son cinco dimensiones: plaza, trámite, responsable, plazo y estatus. Ponerlas todas a la vista
llenaba la barra de controles que casi nadie toca, así que tres van visibles y las demás entran
por un «+ Añadir filtro». El que se añade aparece con su panel ya abierto, porque quien lo pidió
lo pidió para usarlo ahora, no para mirarlo.

Lo que se selecciona baja a una fila propia de pastillas, cada una con su dimensión, su valor y su
equis. Con un tope de cuatro visibles y un «+N más» que despliega el resto: sin ese tope, seis
filtros cruzados empujan la tabla fuera de la pantalla, que es más o menos lo contrario de lo que
se buscaba. Al final, «Quitar todos los filtros», y la fila entera desaparece cuando no hay nada
puesto.

Del teclado no se negoció nada. El botón declara si está abierto, el foco entra en el buscador, la
tecla de escape cierra y devuelve el foco al botón —no al principio de la página, que es el fallo
clásico— y cada equis dice qué quita en concreto. En una fila de seis, seis botones «×» idénticos
son indistinguibles al tabular.

La misma barra se llevó tal cual a Trámites concluidos, que no tenía ninguna. Que dos pantallas
hermanas filtren distinto es una fuente de fricción gratuita.

## La ficha de detalle

Tres cosas, y las tres venían de lo mismo: el bloque de cabecera estaba montado como caja flexible
donde la tarjeta del reloj recibía lo que sobrara. Y lo que sobraba eran doscientos cincuenta
píxeles para meter una cifra grande, un párrafo y tres filas de fechas. Se veía apretado porque lo
estaba.

Pasó a rejilla, donde el ancho es una decisión y no un residuo. La tarjeta respira con el
espaciado del sistema, las dos columnas se equilibran verticalmente y por debajo del punto de
ruptura vuelven a apilarse.

Faltaba aire bajo el título de la pantalla, y resultó no ser un despiste sino un defecto del
componente: el relleno inferior de la cabecera lo aportaba una fila de chips que es opcional. En
cuanto se quitaron los chips, el título quedó a cinco píxeles de su propio borde. El relleno pasó
al contenedor.

Y el contacto del cliente estaba al final de la columna derecha, debajo de los documentos. Para
llamar a la persona del trámite había que recorrer la pantalla entera. Subió justo bajo la
identidad del expediente, a ancho completo y con los datos en fila. Ese orden es también el del
recorrido con teclado, que es la otra razón por la que importa.

## Qué queda escrito

El sistema de diseño pasó de 1.5.1 a 2.2.0 a lo largo de estas rondas. Lo relevante no es el
número sino que cada corrección dejó una regla en su sitio, con el caso medido al lado, en los tres
archivos que tienen que decir lo mismo: la fuente técnica, la copia descargable con su historial y
la página renderizada.

Hubo incluso que resolver una contradicción que el propio documento arrastraba. Un apartado seguía
prescribiendo el medallón apagado mientras otro, más nuevo, nombraba ese mismo medallón como caso
de la regla contraria. Dos respuestas distintas a la misma pregunta, las dos escritas. Se reescribió
el apartado viejo en vez de añadir una nota encima: una nota deja el conflicto donde estaba, solo
que tapado.

Queda pendiente una cosa que conviene no olvidar. Tres pantallas del módulo de clientes —padrón,
ficha y alta— siguen con la receta antigua del medallón. Son de otro módulo y quedaron fuera de
este encargo, pero hoy están divergentes de lo que dice el sistema. Son tres líneas por archivo.
