# Pruebas y verificación del comportamiento

**Estrategia:** se definen casos de prueba que se ejecutan contra ambas versiones (`estado-inicial` y `estado-refactorizado`). Para cada caso se registra la entrada, el resultado esperado y el resultado obtenido en cada versión. Así se verifica que el comportamiento externo se mantiene y que las únicas diferencias son las intencionales (mensajes de error y menú).

## Casos de prueba manuales

| N.º | Caso | Entrada | Resultado esperado | Versión inicial | Versión refactorizada |
|---|---|---|---|---|---|
| 1 | Registrar solicitud válida | Ana Pérez, 1001, ana@mail.com, certificado, alta, "Necesito certificado" | "Solicitud 1 registrada" | ✔ Igual | ✔ Igual |
| 2 | Registrar con email inválido | Email sin "@" | Se rechaza el registro | "error" | "El email no es válido" |
| 3 | Registrar con tipo inválido | Tipo "xyz" | Se rechaza el registro | "tipo invalido" | "Tipo inválido: 'xyz'" |
| 4 | Registrar con campo vacío | Nombre vacío | Se rechaza el registro | "error" | "Todos los campos son obligatorios" |
| 5 | Cambiar estado válido | ID 1, "en proceso" | "Estado actualizado" | ✔ Igual | ✔ Igual |
| 6 | Cambiar estado de solicitud finalizada | Resolver la 1 y volver a cambiarla | Se rechaza el cambio | "no se puede cambiar" | "No se puede cambiar el estado de una solicitud resuelta o rechazada" |
| 7 | Cambiar estado de solicitud inexistente | ID 99 | Se informa que no existe | "no existe" | "La solicitud no existe" |
| 8 | Asignar responsable válido | ID 1, responsable 2 | "Responsable asignado" | ✔ Igual | ✔ Igual |
| 9 | Asignar responsable inválido | ID 1, responsable 9 | Se rechaza la asignación | "responsable invalido" | "Responsable inválido" |
| 10 | Buscar por estado | Campo "estado", valor "en proceso" | Lista la solicitud 1 | ✔ Igual | ✔ Igual |
| 11 | Buscar sin resultados | Campo "tipo", valor "baja" | "sin resultados" | ✔ Igual | ✔ Igual |
| 12 | Buscar por campo inválido | Campo "color" | Se rechaza la búsqueda | "campo invalido" | "Campo de búsqueda inválido" |
| 13 | Generar reporte | Opción 5 | Listado con plazos, totales y "Su reporte ha sido generado" | ✔ Igual | ✔ Igual |
| 14 | Plazo con prioridad alta | Certificado + alta | Plazo de 2 días en el reporte | 2 días | 2 días |
| 15 | Entrada no numérica en un ID | Letras en lugar de número | Se rechaza sin cerrar el programa | "error" | "Debe ingresar un número" |

**Resultado:** las operaciones exitosas (casos 1, 5, 8, 10, 11, 13 y 14) producen la misma salida en ambas versiones. En los casos de error, las dos versiones rechazan la operación y la refactorizada lo informa con un mensaje más claro.

## Pruebas automatizadas (versión refactorizada)

Como la lógica ya no depende de la consola, se puede probar directamente. Las pruebas están en `test_servicio.py` y se ejecutan con:

```bash
python -m unittest test_servicio.py -v
```

| Área | Pruebas incluidas |
|---|---|
| Registrar | Solicitud válida, email inválido, tipo inválido, campo vacío |
| Plazos | Prioridad alta (2 días), prioridad media (3 días) |
| Cambiar estado | Cambio válido, solicitud finalizada, solicitud inexistente |
| Asignar responsable | Asignación válida, responsable inválido |
| Buscar | Sin resultados, campo inválido |
| Reporte | Conteo de solicitudes por estado |

**Resultado:** 14 pruebas ejecutadas, todas exitosas (`Ran 14 tests ... OK`).

## Cómo se verificó que no hubo regresiones

1. Se ejecutaron manualmente los 15 casos en la versión inicial (tag `estado-inicial`).
2. Se repitieron los mismos casos en la versión refactorizada y se compararon las salidas.
3. Se ejecutaron las pruebas automatizadas, que quedan como red de seguridad para futuros cambios.

## Diferencias intencionales

| Aspecto | Versión inicial | Versión refactorizada | Motivo |
|---|---|---|---|
| Mensajes de error | Genéricos ("error", "no existe") | Específicos para cada caso | Mejor manejo de errores |
| Menú | Una sola línea | Título y opciones en líneas separadas | Mejora de presentación |
| Operaciones exitosas | Sin cambios | Sin cambios | Se conserva el comportamiento externo |

## Evidencias

Las capturas de pantalla se encuentran en `docs/evidencias/`:

- Ejecución de los casos en la versión inicial.
- Ejecución de los casos en la versión refactorizada.
- Resultado de `python -m unittest test_servicio.py -v`.

## Conclusión

El comportamiento externo se mantiene en todas las operaciones exitosas, y las diferencias detectadas corresponden a las mejoras intencionales documentadas en `docs/refactorings.md`. Las pruebas automatizadas quedan como respaldo para detectar regresiones en cambios futuros.