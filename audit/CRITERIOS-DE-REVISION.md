# Criterios de revisión de la persona que dirige el proyecto

Se leen antes de empezar cualquier revisión de pantallas de DPROMA. Salen de las observaciones que la persona que dirige el proyecto marcó en capturas (`Capturas_de_errores_percibidos.pdf`, 14-oct-2026) y de las correcciones que pidió al informe «Revisión de pantallas SIO DPROMA». No sustituyen al sistema de diseño: dicen qué mirar y cómo entregarlo.

## 1 · Dos reglas de trabajo

1. **Prioridad al cliente, salvo que sea crítico.** Lo que DPROMA hizo se adopta y se documenta en el sistema; no se le pide cambiar. Es crítico si cumple al menos una de estas cinco condiciones:
   1. Falla de accesibilidad medida: contraste menor de 4,5:1 en texto o de 3:1 en controles, destino de menos de 24 px, control sin nombre accesible, contenido invisible bajo una preferencia del usuario.
   2. Impide completar la tarea u oculta la acción principal.
   3. Acción irreversible o de dinero sin protección.
   4. Contradice una decisión de DPROMA (aviso del 28-sep, `FICHAS_TECNICAS.md`) o expone datos personales.
   5. Es un rediseño marcado como crítico y viable.
2. **Lo no crítico no se descarta.** «No crítico» solo significa que no se le exige a DPROMA. Un cambio sencillo que mejora la estética de forma global, o que delata una causa raíz en el sistema de diseño, se evalúa con una solución concreta.

## 2 · Qué mirar en una pantalla (lo que la persona vio a ojo)

- **Cortes:** iconos, pastillas, cajas o botones cortados o a medio dibujar. Si pasa en todas las filas de una tabla, es un defecto de ancho de columna.
- **Aire:** siempre debe haber margen entre los controles de una cabecera y la línea que la cierra. Si pasa en una pantalla, se mide en todas.
- **Celdas de tabla:** llevan un dato, no un párrafo. Los estados son cortos y dicen una sola cosa.
- **Estados:** si un texto ya lo confirmó DPROMA, se respeta; si no cabe, se ajusta primero el ancho de la columna.
- **Botón flotante:** no puede tapar la acción principal de la pantalla.
- **Color:** demasiados colores del semáforo sin un juicio de estado detrás es un defecto.
- **Ritmo vertical:** el interlineado y el espaciado que dan sensación de desorden se miden contra la escala `--sp-*`.
- **Gráficas:** el texto no se amontona sobre las marcas y las barras comparten línea base.
- **Etiquetas pegadas al borde de una tarjeta** y botones hermanos que no se parecen (alto, posición del icono).
- **Icono dentro de un botón:** debe verse sobre el relleno del botón en todos los estados, no solo en el principal.

## 3 · Cómo se entrega

- **Evidencia:** cada hallazgo lleva archivo, selector, línea y medición. No se inventa ninguna cifra, selector ni línea.
- **Verificación:** todo hallazgo alto o crítico lo intenta refutar otra persona con medición propia antes de llegar al informe.
- **Primera revisión:** si es la primera vez que se revisa un paquete, no se comparan versiones ni se usan etiquetas v1/v2.
- **Antes del ingeniero:** la persona que dirige el proyecto ve la lista de críticos antes de que nada llegue al ingeniero de DPROMA.
- **El informe del ingeniero:**
  - Cada cambio dice dónde está, qué se ve, por qué pasa y cómo comprobarlo.
  - Cada cambio lleva captura del antes y el después; el «después» se prueba aplicando el arreglo sobre el archivo.
  - Se escribe en lenguaje llano, con titulares que dicen algo y sin el patrón «no es X, es Y».
  - No lleva asuntos internos de Studio ni la diagramación del informe de Finanzas.
  - Se redacta pensando en quien no es ingeniero y debe poder entenderlo.
