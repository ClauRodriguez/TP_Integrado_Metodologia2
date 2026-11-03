# Calidad externa e interna

## Calidad externa

Es la que percibe quien usa el sistema: que haga lo que promete, sin fallar y con mensajes comprensibles. En nuestro sistema, la versión inicial cumple bien con esto: permite registrar solicitudes, cambiar su estado, asignar responsables, buscar por distintos campos y generar un reporte. Las validaciones básicas (email con "@", tipos y prioridades válidos, estados permitidos) impiden cargar datos incorrectos, y el menú responde como se espera en cada opción. Para el usuario, el sistema funciona.

## Calidad interna

Es la que percibe quien lee, mantiene o modifica el código: legibilidad, orden, cohesión, bajo acoplamiento y facilidad para cambiar. La versión inicial tiene debilidades importantes que el usuario no ve:

- **Legibilidad:** nombres como `n`, `l`, `e`, `s`, `x` o `res` obligan a deducir qué representa cada variable.
- **Estructura:** todo vive en un único archivo, con variables globales (`solicitudes`, `estudiantes`, `contador`) que cualquier función puede modificar.
- **Responsabilidades mezcladas:** `registrar()` valida, crea el estudiante, calcula el plazo, guarda y muestra mensajes por pantalla, todo en la misma función.
- **Duplicación:** `buscar()` repite el mismo bucle cuatro veces, y los textos "pendiente", "alta" o "certificado" aparecen escritos en varios lugares.
- **Manejo de errores pobre:** mensajes como "error" y bloques `except:` genéricos que ocultan la causa real del problema.

## Relación entre ambas

| Aspecto | Qué se ve desde afuera | Qué pasa por dentro |
|---|---|---|
| Funcionalidad | Todo funciona | Lógica y presentación mezcladas |
| Mantenibilidad | No es visible | Cambiar un tipo de solicitud obliga a tocar varias funciones |
| Legibilidad | No es visible | Nombres de una letra y código repetido |
| Evolución futura | No es visible | Agregar un estado, un tipo o un filtro implica modificar código existente y puede romper otras partes |

## Ejemplo concreto

Si mañana se quiere agregar el tipo de solicitud "constancia" con un plazo de 7 días, hay que modificar la validación en `registrar()`, la cadena de `if/elif` de los plazos y el texto del menú. Si se olvida alguno de esos tres lugares, el sistema falla sin que el usuario haya cambiado nada. Esto muestra que un sistema puede tener buena calidad externa y, al mismo tiempo, un costo de cambio alto por su calidad interna baja.

## Conclusión

El sistema base cumple con lo que el usuario espera, pero su estructura interna dificulta mantenerlo y extenderlo. Esa diferencia se aborda en las etapas siguientes mediante el diagnóstico de deuda técnica y el refactoring.