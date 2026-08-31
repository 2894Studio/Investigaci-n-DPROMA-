# Patrón de diálogo — SIO-DPROMA

Especificación del diálogo modal: cuándo se usa, cómo se comporta el foco, y por qué cinco de
los seis diálogos del sistema no caben en un teléfono.

Acompaña a la maqueta navegable en `web/entregables/propuestas/editar-cliente.html`. Son dos
documentos a propósito: quien revise el diseño abre la pantalla, quien lo construya lee esto.
Mezclarlos —que es como llegó la entrega original— hace imposible saber qué es producto y qué
es razonamiento.

El componente y sus tokens están en `docs/sistema-diseno-sio-dproma.md` §6.18.

---

## 1. Comportamiento del foco

Es la regla que nadie escribe y todo el mundo incumple: quien navega con teclado abre un
diálogo, lo cierra, y aparece al principio del documento teniendo que recorrer la pantalla
entera para volver donde estaba.

| Momento | Qué pasa |
|---|---|
| **Al abrir** | El foco va al **primer control que se puede rellenar** —no al diálogo, no al aspa de cerrar. Quien pulsa «Editar» viene a escribir. Lo de detrás deja de ser alcanzable con `Tab`: el velo tapa a la vista **y** al teclado. |
| **Mientras está abierto** | `Tab` desde el último control vuelve al primero. Es la única trampa de foco legítima que existe. |
| **Al cerrar sin guardar** | El foco vuelve **al botón desde el que se abrió**, no al principio de la página. |
| **Al cerrar guardando** | El foco va **a la fila que se acaba de cambiar**, que es a donde miraría cualquiera. Si esa fila ya no existe —se filtró y se fue de la lista—, al contenedor más cercano que siga existiendo. Nunca al `body`. |

**Mientras guarda no cierra nada.** Ni Escape, ni el aspa, ni el clic en el velo. Cerrar a medio
guardar deja a alguien sin saber si se guardó. Y «Guardando» **se dice**, no solo se pinta: un
botón que cambia de color no llega a quien no lo ve.

Con `<dialog>` nativo, la trampa de foco y el velo los da el navegador con `showModal()`. Lo que
sigue siendo trabajo nuestro es a dónde entra el foco al abrir y a dónde vuelve al cerrar.

```js
function abre(disparador){
  origen = disparador;
  dlg.showModal();
  dlg.querySelector('input:not([readonly]), select, textarea')?.focus();
}
dlg.addEventListener('close', function(){
  var destino = dlg.returnValue === 'guardado' ? filaCambiada() : origen;
  (destino || document.getElementById('contenido')).focus();
});
```

---

## 2. Qué va en un diálogo y qué en una página

La regla se elige **por formulario, no por sistema**: no «los diálogos son para X», sino «este
formulario cabe o no cabe».

La ventana útil de un teléfono de 390×844 son unos **700 px** una vez descontadas la barra del
navegador y las zonas seguras. La cabecera del diálogo se lleva 64 y el pie 76: quedan
**≈560 px de cuerpo**.

Cada renglón ocupa lo suyo: un campo 77 px (etiqueta 16, hueco 5, control 44, separación 12),
un encabezado de sección 56, una casilla 44, un área de texto 109.

| Diálogo | Renglones | Alto del cuerpo | Pantallas | ¿Cabe como diálogo? |
|---|---:|---:|---:|---|
| `41_alta_cliente` | 14 | 1302 px | 2,3 | **No** — el único que pasa de dos |
| `44_alta_tramite_cfe` | 13 | 1024 px | 1,8 | Sí, desplazando |
| `43_alta_tramite_vehicular` | 10 | 970 px | 1,7 | Sí, desplazando |
| `42_alta_tramite_gestoria` | 11 | 902 px | 1,6 | Sí, desplazando |
| `49_alta_orden` | 7 | 763 px | 1,4 | Sí, y es la más holgada de las altas |
| `59_editar_cliente` | 2 | 218 px | 0,4 | Cabe entero, sin desplazar |

**Uno de seis no cabe, y es el alta de cliente.** Ninguna de las cinco altas cabe sin desplazar
—la más corta pide 1,4 pantallas—, pero lo que separa al alta de cliente es que **pasa de dos**:
a partir de ahí quien rellena ya no recuerda qué diálogo abrió ni ve el botón que lo cierra, y
el modal ha dejado de comportarse como un modal aunque siga siéndolo.

Para ése, y solo para ése: **modal en escritorio y página en el teléfono**. Es la razón de que
el alta de cliente exista como pantalla propia (`propuestas/alta-cliente.html`) y no como
diálogo.

---

## 3. Tres reglas de contenido

**El nombre del botón y el contenido del diálogo coinciden.** «Editar cliente» que solo deja
cambiar la razón social se llama **«Cambiar razón social»**. La distancia entre lo que se espera
y lo que se encuentra es lo que hace que alguien abra el diálogo tres veces buscando un campo
que no está.

**Un campo de solo lectura se muestra como dato, no como campo.** Si el RFC no se puede cambiar,
no lleva caja de campo: etiqueta y valor, en tamaño menor, como contexto. En la entrega original
el campo bloqueado ocupaba más espacio que el editable, con dos líneas explicando por qué no se
podía tocar: la mitad del diálogo dedicada a algo que no se puede tocar.

Lo que sí hay que conservar es **el motivo**. Un campo en gris sin explicación se lee como una
carencia del formulario; con el motivo al lado se lee como lo que es, una decisión. El RFC es la
identidad fiscal y la clave única del cliente: cambiarlo no es editar un cliente, es decir que
era otro, y eso necesita su propio circuito con su rastro.

**Detrás del diálogo va la pantalla real atenuada**, no un esqueleto de carga. Las barras grises
que la entrega original dibujaba detrás son idénticas a las que el sistema usa para decir
«cargando»: quien lo vea puede pensar que la pantalla de atrás se está recargando o que ha
perdido su sitio en la lista. Ver el contexto propio tranquiliza; ver barras grises inquieta.

---

## 4. Lo que este documento no dirime

No se decide aquí si el padrón debería poder editar más cosas de un cliente. Se especifica lo
que hoy se puede editar y cómo debe comportarse mientras se hace. Ampliar el alcance de la
edición es una decisión de producto, y va en `docs/decisiones-producto-padron.md` cuando se
tome.
