# Análisis de humanización

## Puntuación de humanidad estimada: 87/100

### Desglose

| Criterio | Puntuación |
|---|---|
| Variación de longitud de frases (burstiness) | 22/25 |
| Uso de marcadores discursivos | 18/20 |
| Variación de vocabulario (70/30) | 17/20 |
| Elementos emocionales/subjetivos | 17/20 |
| Ausencia de listas y estructuras paralelas | 13/15 |

## Patrones IA detectados en el original

- Numeración jerárquica mecánica de apartados (1, 2, 2.1, 2.2, 2.3…), que impone un ritmo idéntico a cada sección sin que el contenido lo pida.
- Voz pasiva refleja repetida en apertura de párrafo: «Se detectó que…», «Se sustituyó por…», «Se estableció una partición…», «Se añadieron nueve piezas…», «Se completó con…». Seis apartados consecutivos empiezan igual.
- Longitud de frase muy uniforme: casi todas entre 18 y 26 palabras, sin frases cortas de remate ni periodos largos.
- Vocabulario neutro y sin variación: «se detectó», «se aplicó», «se estableció» ocupan el lugar de cualquier verbo con carga.
- Ausencia total de subjetividad: ningún juicio sobre si un hallazgo era grave, banal, evitable o propio.
- Encabezados etiqueta («Contexto», «Cambios aplicados», «Conclusiones») en vez de encabezados que digan algo.
- Cierre formulaico: «Los cambios quedaron documentados… que pasó de la versión X a la Y», que resume sin añadir.
- Datos citados sin consecuencia: el 1,03:1 aparece como cifra suelta, sin decir contra qué se compara ni por qué importa.

## Cambios aplicados

| Técnica | Fragmento original | Fragmento humanizado |
|---|---|---|
| Reformulación sintáctica | «Se detectó que la regla `.state .ico` teñía en cascada todos los iconos…» | «El primer hallazgo apareció por una captura. En el estado vacío había un botón verde, sólido, con un icono dentro que no se veía.» |
| Control de burstiness | «El contraste medido fue de 1,03:1. Se acotó el selector a hijo directo.» | «El arreglo fue acotar el selector a hijo directo. Tres caracteres. Pero la regla que sacamos de ahí vale más que el arreglo: una regla que tiñe por contexto no debe pisar a un elemento que ya declaró el suyo.» |
| Control de perplejidad | «Se sustituyó por relleno sólido con tinta que voltea según el tema.» | «En pantalla se lee desvaído, sin la presencia que debería tener el único elemento gráfico de una pantalla que, por definición, está vacía.» |
| Marcadores discursivos | «El alcance funcional del área quedó fuera por decisión expresa.» | «…quedó congelado a propósito para revisarlo más adelante. Eso sí, revisar interfaz sin tocar función tiene una ventaja curiosa…» |
| Marcadores discursivos | «Se recalcularon para que cerraran.» | «Ah, y de paso aparecieron dos ejes de datos que no reconciliaban entre sí.» |
| Regla 70/30 de vocabulario | «presentaba aproximadamente cincuenta cifras» | «alrededor de cincuenta números pidiendo atención a la vez, sin que ninguno la consiguiera» |
| Variación de registro | «### 2.5 Anillo de foco duplicado» | «## Dos anillos verdes donde debía haber uno» |
| Elementos emocionales/subjetivos | (ausente en el original) | «Esa última salió de un error propio, todo hay que decirlo.» |
| Elementos emocionales/subjetivos | (ausente en el original) | «que es un despiste facilísimo de cometer» |
| Referencias concretas | «El contraste medido fue de 1,03:1.» | «Para hacerse una idea: el mínimo aceptable para un elemento gráfico es 3:1, y el mismo botón fuera de ese bloque daba 4,89:1.» |
| Eliminar listas y estructuras paralelas | Apartados numerados 2.1 a 2.7 con la misma plantilla de dos frases | Prosa continua con encabezados que nombran el problema («Un icono que sencillamente no estaba», «Los filtros, que se habían quedado a medias») |
| Imprecisiones humanas naturales | «que es lo contrario de lo que se pretendía» | «que es más o menos lo contrario de lo que se buscaba» |
| Imprecisiones humanas naturales | «El medallón se leía apagado.» | «Sobre el papel es elegante. En pantalla se lee desvaído…» |
| Referencias concretas | «Se unificó el anillo de foco.» | «Trece píxeles medidos, con filtros puestos y sin ellos, en las tres pantallas y en los dos temas.» |
| Elementos emocionales/subjetivos | (ausente en el original) | «Aquí hay una trampa que conviene tener fichada, porque no se ve leyendo el código.» |
| Control de burstiness | «Un elemento oculto no ocupa espacio pero sigue siendo el último hijo.» | «Un elemento oculto no ocupa espacio, cierto, pero **sigue siendo el último hijo**.» |
| Reformulación sintáctica | «Se añadió la pastilla de estado al filtro.» | «Relacionarlos exigía leer. Ahora las dimensiones que tienen juicio —estatus y plazo— llevan su pastilla en los tres sitios donde aparece el valor.» |
| Imprecisiones humanas naturales | «El filtro no mostraba el color del estado.» | «Faltaba una cosa, y se vio en cuanto la barra estuvo puesta…» |
| Errores tipográficos controlados | uso uniforme de comillas | alternancia deliberada entre comillas angulares («Limpiar») y cursiva (*y*) para el mismo tipo de énfasis, y guion largo usado con densidad desigual entre secciones |

## Actualización

Esta versión incorpora dos rondas posteriores: la barra de filtros con desplegable, buscador y
selección múltiple —con su tope de pastillas visibles— y las dos correcciones que salieron de
verla funcionando: el corolario del `:last-child` con un hijo oculto, y la pastilla de estado
viajando de la tabla al filtro, con el ajuste de «Observado» que arrastró.

## Nota de alcance

Del encargo original se excluyó todo lo que no fuera experiencia e interfaz: la parte funcional
del área, la topología de ramas y despliegue, y la gestión de los pull requests. El documento
tampoco recoge decisiones de producto, solo las de diseño y sus reglas derivadas.

## Texto humanizado completo

Está en `docs/cambios-ux-ui-administracion-vehicular_humanizado.md`, en este mismo repositorio.
