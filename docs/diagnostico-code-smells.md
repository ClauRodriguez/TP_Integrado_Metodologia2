# Diagnóstico de deuda técnica y code smells

**Deuda técnica:** es el costo extra de mantenimiento que se acumula cuando se elige una solución rápida en lugar de una bien diseñada. En este sistema, la deuda está en que todo funciona hoy, pero cada cambio futuro (un tipo nuevo, un estado nuevo, un filtro nuevo) cuesta más y tiene más riesgo de romper algo.

Se identificaron **10 code smells**. La prioridad indica qué conviene corregir primero.

| N.º | Code smell | Evidencia | Ubicación | Impacto | Riesgo de mantenimiento | Prioridad |
|---|---|---|---|---|---|---|
| 1 | **Variables globales** | `solicitudes`, `estudiantes`, `contador` se modifican desde las funciones con `global` | Inicio de `main.py`, `registrar()` | Cualquier función puede alterar el estado sin control; difícil de probar | Alto: errores difíciles de rastrear | Alta |
| 2 | **Nombres poco claros** | Variables `n`, `l`, `e`, `t`, `p`, `d`, `s`, `x`, `res` | Todas las funciones y el menú | Hay que deducir qué es cada dato; se lee con esfuerzo | Medio: errores al modificar por malinterpretar variables | Alta |
| 3 | **Long Method / responsabilidades mezcladas** | `registrar()` valida, crea el estudiante, calcula el plazo, guarda e imprime | `registrar()` | Función larga y difícil de entender o reutilizar | Alto: un cambio en una parte afecta a las demás | Alta |
| 4 | **Long Parameter List** | `registrar(n, l, e, t, p, d)` recibe 6 parámetros sueltos | `registrar()` | Fácil confundir el orden de los argumentos | Medio: agregar un campo implica cambiar todas las llamadas | Media |
| 5 | **Código duplicado** | `buscar()` repite el mismo bucle 4 veces; el `print` de una solicitud se repite en `buscar()` y `reporte()` | `buscar()`, `reporte()` | Un cambio de formato o de lógica hay que hacerlo en varios lugares | Alto: se corrige uno y se olvida otro | Alta |
| 6 | **Magic strings (textos fijos repetidos)** | `"pendiente"`, `"alta"`, `"certificado"`, etc. escritos a mano en muchos lugares | `registrar()`, `cambiar_estado()`, `buscar()`, `reporte()` | Un error de tipeo no da aviso y el Estado no existe como entidad | Alto: agregar o renombrar un valor obliga a buscar en todo el código | Alta |
| 7 | **Cadenas largas de if/elif** | Plazo según tipo y validaciones con varios `if/elif` encadenados | `registrar()`, `buscar()`, `cambiar_estado()` | Agregar un tipo obliga a modificar código ya existente (viola OCP) | Alto | Media |
| 8 | **Data Clumps / estructuras sin clase** | Solicitud, Estudiante y Responsable son diccionarios con claves en texto (`s["est"]["legajo"]`) | Todo el archivo | Sin comportamiento propio; un error de clave solo falla al ejecutar | Medio | Media |
| 9 | **Manejo de errores deficiente** | `except:` genérico y mensajes "error" o "no existe" sin detalle | Menú (opciones 2 y 3), `registrar()` | El usuario no sabe qué falló y se ocultan errores reales | Medio | Media |
| 10 | **Mezcla de lógica y presentación** | `print()` e `input()` dentro de las funciones de negocio; cálculos del reporte junto con la impresión | `registrar()`, `cambiar_estado()`, `reporte()` | No se puede probar la lógica sin usar la consola; no se reutiliza en otra interfaz | Alto | Alta |

## Resumen de prioridades

- **Alta (1, 2, 3, 5, 6, 10):** afectan directamente la legibilidad y el costo de cambio. Se corrigen primero.
- **Media (4, 7, 8, 9):** mejoran la calidad pero dependen de las correcciones anteriores (por ejemplo, las clases y el Enum facilitan eliminar los `if/elif`).

## Conclusión

La deuda técnica del sistema no afecta lo que ve el usuario, pero sí la facilidad de cambio. Los smells están conectados entre sí: la falta de clases y del Estado como entidad (8 y 6) explica gran parte de la duplicación y de los `if/elif` (5 y 7), por lo que el refactoring en las próximas etapas parte de ahí.