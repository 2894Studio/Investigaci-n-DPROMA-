---
name: dproma-texto-humano
description: Humaniza y revisa textos del proyecto DPROMA — informes, documentación, entregables — combinando el método de stop-slop con la rúbrica propia del proyecto y la regla de voz de producto §8. Sabe qué se aplica a prosa y qué a copy de pantalla, que son cosas distintas. Úsalo cuando el usuario pida "humaniza este texto", "esto suena a IA", "revisa la redacción", "pásale el humanizer", o al redactar cualquier documento largo del repositorio. Funciona sin stop-slop instalado.
---

# Humanización de textos DPROMA

El proyecto ya humaniza a mano: `docs/cambios-ux-ui-administracion-vehicular.md` tiene su
`_humanizado.md` y su `_analisis.md` al lado, y ese análisis puntuó 87/100 con una rúbrica propia.
Esta skill ordena ese trabajo y le añade el método de stop-slop **como método, no como autoridad**.

## Primero: qué superficie es

Las dos reglas siguientes son opuestas y las dos son correctas. Elegir mal es el error más común.

**Prosa y documentación** —informes, `docs/*.md`, análisis, README—. Aquí manda la rúbrica de
humanización. La raya (—) se conserva: es ortografía española correcta y el propio `_analisis.md` la
cataloga como técnica deliberada.

**Copy de pantalla de producto** —botones, avisos, estados vacíos, ayuda de campo—. Aquí manda §8
Voz de producto, y la rúbrica de humanización **no aplica**: el problema de un copy de pantalla no es
sonar a IA, es sonar a conversación interna. La prueba de §8: si el texto explica una decisión, no va
en pantalla; si explica una consecuencia para quien está mirando, sí, y en una frase. Ahí la raya se
minimiza, como ya hizo la versión 2.2.5 del sistema de diseño.

## La rúbrica del proyecto

De `docs/cambios-ux-ui-administracion-vehicular_analisis.md`. Cinco criterios sobre 100, con pesos
desiguales a propósito:

| Criterio | Peso |
|---|---|
| Variación de longitud de frases (burstiness) | 25 |
| Uso de marcadores discursivos | 20 |
| Variación de vocabulario (70/30) | 20 |
| Elementos emocionales y subjetivos | 20 |
| Ausencia de listas y estructuras paralelas | 15 |

Se puntúa contra esta, no contra las cinco dimensiones sobre 50 de stop-slop. No son comparables:
pesos distintos, escala distinta, idioma distinto.

## Los tells de este corpus

Están catalogados de una revisión real, así que valen más que una lista genérica. Búscalos primero:

- **Pasiva refleja repetida en apertura de párrafo.** «Se detectó que», «Se sustituyó por», «Se
  estableció», «Se añadieron». En el original había seis apartados consecutivos empezando igual.
- **Numeración jerárquica mecánica** (1, 2, 2.1, 2.2, 2.3…) que impone el mismo ritmo a cada sección
  sin que el contenido lo pida.
- **Longitud de frase uniforme**, casi todas entre 18 y 26 palabras, sin frases cortas de remate ni
  periodos largos.
- **Vocabulario neutro sin variación**: «se aplicó», «se estableció» ocupando el lugar de cualquier
  verbo con carga.
- **Ausencia total de subjetividad**: ningún juicio sobre si un hallazgo era grave, banal o evitable.
- **Encabezados etiqueta** —«Contexto», «Cambios aplicados», «Conclusiones»— en vez de encabezados
  que digan algo.
- **Cierre formulaico** que resume sin añadir.
- **Datos citados sin consecuencia**: una cifra suelta sin decir contra qué se compara ni por qué
  importa.

## Cómo entra stop-slop

Si está instalada, propónla con el formato de `CLAUDE.md` y espera OK. De ella se toma **el método**:
detectar muletillas, romper la cadencia plana, subir la densidad, su marco de directness y ritmo.

De ella **no** se toman las listas de `references/phrases.md` y `references/structures.md`: están
escritas para prosa en inglés y sus frases no traducen. Tampoco su ban de em-dash, por lo que dice
la sección de superficie. Tampoco su umbral de 35/50, que se sustituye por la rúbrica de arriba.

Si algún día se traducen sus listas al castellano, se hace una vez, se guarda en `docs/` y se
versiona. No se traduce al vuelo en cada uso.

## Qué no se toca

`docs/sistema-diseno-sio-dproma.md` y `web/entregables/design-rules.md` están secos a propósito: son
referencia técnica, se consultan por índice y §8 quiere exactamente eso. No se les pasa el humanizer.

## Salida

Devuelve el texto revisado y, debajo, la puntuación contra los cinco criterios con una línea por
criterio diciendo qué falló. Si no llega a 80/100, dilo y propón una segunda pasada en vez de
entregarlo.

Sin stop-slop instalado, el ciclo funciona igual con la rúbrica y la lista de tells: es lo que ya se
usó para llegar a 87/100. Dilo en una línea y sigue. **No digas que usaste stop-slop si no estaba.**
