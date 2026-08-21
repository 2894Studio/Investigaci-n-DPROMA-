# Criterios de animación

Norma del proyecto para cualquier animación que se añada al sitio, de aquí en adelante.

## 1. Se pausa pulsando la propia animación

**Nada de botón «Pausar» al lado.** El control es la animación misma: se pulsa encima y se
detiene; se vuelve a pulsar y sigue. Un botón aparte ensucia la página y compite con el
contenido, sobre todo cuando la animación es pequeña o decorativa.

Cómo se implementa, para que no sea un control escondido:

- El contenedor de la animación es un `<button>`, no un `<div>`. Así funciona con el ratón y
  también con el teclado (Tab para llegar, Intro o Espacio para activar), gratis y sin JS
  extra.
- Lleva `aria-label` que diga qué es y que se puede pausar, y `aria-pressed` que refleje el
  estado. Los dos se actualizan al pausar.
- `cursor: pointer` para que se note que responde.
- Una pista de texto —«Pausar» / «Reanudar»— que aparece al apuntar con el ratón o al
  recibir el foco, y **desaparece al salir, también si está en pausa**. El control existe
  siempre, pero no se queda encendido llamando la atención sobre sí mismo: el estado de
  pausa ya lo cuenta `aria-pressed` a quien lo necesita, y quien pausó sabe que pausó.
  Nunca en color de acento: la pista es una ayuda, no un aviso.
- El anillo de foco tiene que verse. No quitar el `:focus-visible`.

## 2. Con `prefers-reduced-motion`, quieta y completa

La animación no se esconde: se congela en un fotograma que siga explicando lo que enseñaba
en movimiento. Si el contenido aparece por fases, se congela con todo visible, nunca en el
fotograma inicial vacío.

Ojo con la regla global de las hojas de estilo de este sitio:

```css
@media (prefers-reduced-motion: reduce){
  *{ animation-duration: 0.001ms !important; }
}
```

Deja cualquier animación en su **último** fotograma. Si ahí el contenido está oculto, hay que
restituir la duración dentro de la propia media query y dejarla en pausa con un
`animation-delay` negativo, o quitar la animación y describir el estado final a mano.

Con movimiento reducido tampoco hace falta el control de pausa: se oculta la pista y se
quita el `cursor: pointer`, porque ya no hay nada que parar.

## 3. Por qué hay que poder pararla

No es un capricho: el criterio [WCAG 2.2.2 «Pausar, detener, ocultar»][1] pide que todo
movimiento que arranque solo, dure más de cinco segundos y conviva con otro contenido pueda
detenerse. Cualquier bucle decorativo entra ahí.

[1]: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html

## 4. Sutileza por defecto

- Ciclos largos y lentos antes que rápidos y llamativos.
- Contraste bajo en el elemento en reposo; el color de acento solo en la parte que se mueve.
- Nada que parpadee más de tres veces por segundo (riesgo de crisis fotosensibles).
- Sin librerías: CSS y SVG bastan para todo lo que hay en este sitio.

## Dónde está aplicado

| Dónde | Qué |
|---|---|
| `web/plan-transformacion.html` | Electrocardiograma del Diagnóstico. Sigue este criterio. |
| `web/entregables/recomendaciones-login.html` | Cinco simulaciones de la pantalla de acceso. **Todavía usan botón «Pausar» aparte**, de antes de esta norma. Pendiente de convertir. |
