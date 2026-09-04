# Cambios de UX/UI — Administración Vehicular

Documento de trabajo. Recoge las modificaciones de experiencia e interfaz aplicadas a las cuatro
pantallas del módulo (Tablero, Trámites vehiculares, Detalle de trámite, Trámites concluidos) y
las reglas que cada una dejó incorporadas al sistema de diseño de SIO-DPROMA.

## 1. Contexto

Se recibieron cuatro maquetas HTML ya construidas. La revisión se limitó a experiencia de uso,
interfaz y accesibilidad; el alcance funcional del área quedó fuera por decisión expresa.

## 2. Cambios aplicados

### 2.1 Iconos invisibles sobre relleno sólido

Se detectó que la regla `.state .ico{color:var(--text-3)}` teñía en cascada todos los iconos
dentro de un bloque de estado, incluidos los que van dentro de un botón de relleno sólido. El
contraste medido fue de 1,03:1. Se acotó el selector a hijo directo.

### 2.2 Medallón de estado

La receta prescribía un fondo translúcido al 10% con el glifo del mismo color de familia. Se
sustituyó por relleno sólido con tinta que voltea según el tema.

### 2.3 Reducción de la carga visual del tablero

El estado con datos presentaba aproximadamente cincuenta cifras. Se estableció una partición
entre trámites con reloj corriendo y trámites sin reloj, y el eje del estado del expediente pasó
a una cascada por plaza.

### 2.4 Capa de dashboard

Se añadieron nueve piezas de dato visual sobre Chart.js con envoltura propia, más la alternativa
en tabla obligatoria para cada gráfico.

### 2.5 Anillo de foco duplicado

El buscador pintaba dos anillos concéntricos. Se unificó en un solo anillo sobre el envoltorio.

### 2.6 Barra de filtros

Se completó con desplegables que incorporan buscador y selección múltiple, pastillas de lo
aplicado con máximo visible, y un botón de añadir filtro. Las dimensiones con juicio —estatus y
plazo— muestran la pastilla de color del estado en el panel, en el resumen del botón y en la
pastilla aplicada.

### 2.6.1 Relleno de la cabecera con una fila oculta

El relleno inferior declarado sobre el último hijo lo consumía la fila de filtros aplicados, que
nace oculta. Se trasladó al contenedor.

### 2.7 Ficha de detalle

La tarjeta de plazo quedaba comprimida. Se pasó a rejilla con ancho declarado y el contacto del
cliente se reubicó bajo la identidad del expediente.

## 3. Conclusiones

Los cambios quedaron documentados en el sistema de diseño, que pasó de la versión 1.5.1 a la
2.2.1.
