# Code review profesional

## Objetivo

Aplicar una revisión técnica sistemática sobre la versión refactorizada del Sistema de Gestión de Solicitudes Académicas para verificar legibilidad, mantenibilidad, separación de responsabilidades, manejo de errores, testabilidad y coherencia con los principios SOLID y Clean Code trabajados en la asignatura.

La revisión se realiza sobre la versión final del código y se contrasta con el diagnóstico de deuda técnica y code smells documentado en `docs/diagnostico-code-smells.md`.

## Escala utilizada

- **Cumple:** el criterio se encuentra resuelto en la versión revisada.
- **Parcial:** existe una mejora concreta, pero todavía queda margen de corrección.
- **Pendiente:** el criterio requiere una acción antes del cierre definitivo.

## Checklist técnico

| N.º | Categoría | Criterio revisado | Evidencia / observación | Resultado |
|---|---|---|---|---|
| 1 | Nombres | Variables, métodos y clases poseen nombres descriptivos | Se reemplazaron identificadores como `n`, `l`, `s` y `res` por nombres vinculados al dominio | Cumple |
| 2 | Funciones | Las funciones mantienen una responsabilidad acotada | `ServicioSolicitudes.registrar()` delega validación y obtención/creación del estudiante en métodos específicos | Cumple |
| 3 | Duplicación | No existe duplicación relevante de lógica | La búsqueda utiliza `CRITERIOS` y el formato de las solicitudes se concentra en métodos de `Solicitud` | Cumple |
| 4 | Constantes y valores | Se redujeron magic strings | Estados, prioridades y tipos se modelaron mediante `Enum` | Cumple |
| 5 | SRP | Las responsabilidades están separadas | Modelos, reglas de negocio, persistencia y consola se encuentran en módulos distintos | Cumple |
| 6 | OCP | Las extensiones requieren menor modificación del código existente | Los tipos y estados están centralizados y los filtros usan una tabla de criterios; los textos de opciones de consola aún deben actualizarse manualmente si se agregan valores | Parcial |
| 7 | DIP | La lógica de negocio depende de una abstracción de repositorio | `ServicioSolicitudes` recibe el repositorio por constructor | Cumple |
| 8 | ISP / LSP | La interfaz del repositorio es pequeña y sustituible | `RepositorioSolicitudes` expone `agregar`, `obtener` y `listar`; `RepositorioEnMemoria` implementa ese contrato | Cumple |
| 9 | Estado global | La lógica evita variables globales mutables | El estado se encapsula en instancias del servicio y del repositorio | Cumple |
| 10 | Manejo de errores | Se utilizan errores específicos del dominio | Existen `DatoInvalidoError`, `NoEncontradoError` y una excepción base del sistema | Cumple |
| 11 | Separación UI / negocio | La entrada y salida por consola no está mezclada con las reglas de negocio | `consola.py` concentra `input()` y `print()`; el servicio devuelve datos o lanza excepciones | Cumple |
| 12 | Pruebas | Existe verificación automatizada del comportamiento | `test_servicio.py` y `test_consola.py` reúnen 16 pruebas automatizadas; además se documentan 15 casos manuales | Cumple |
| 13 | Documentación | README y documentación técnica reflejan la estructura final | El README describe estructura, ejecución y pruebas; se corrige la sección de clonación para eliminar placeholders | Cumple |
| 14 | Encapsulamiento | Las entidades controlan adecuadamente sus cambios | El cambio de estado y la asignación de responsable se realizan mediante métodos de `Solicitud`; el servicio valida la referencia antes de delegar la mutación | Cumple |
| 15 | Validación e higiene | Entradas y repositorio se mantienen consistentes | Se validan campos obligatorios y email; el legajo no posee validación de formato específica. `.gitignore` excluye `__pycache__/` y `*.pyc`; los binarios previamente versionados se retiran del repositorio | Parcial |

## Observaciones y acciones correctivas

1. **Documentación:** se reemplazan los placeholders del README por la URL y el directorio reales del repositorio.
2. **Higiene del repositorio:** se eliminan del control de versiones los archivos `.pyc` existentes. La regla de `.gitignore` ya evita su incorporación futura.
3. **Encapsulamiento:** se trasladó la asignación del responsable a `Solicitud.asignar_responsable()`. La validación de existencia permanece en el servicio porque allí se administra el catálogo de responsables; la entidad concentra la modificación de su estado interno.
4. **Validación:** queda como mejora futura definir una regla explícita para el formato de legajo y, si el dominio lo requiere, ampliar la validación de descripción.
5. **Cobertura:** se agregaron dos pruebas básicas de consola con `unittest.mock` para verificar una entrada numérica inválida y el flujo mínimo de registro. La mayor parte de la cobertura continúa concentrada en la lógica de negocio, por tratarse del componente con más reglas y riesgo de regresión.

## Criterios de aceptación técnica

Se considera que la versión refactorizada satisface los criterios técnicos centrales del trabajo porque:

- mantiene las operaciones funcionales del sistema base;
- elimina las variables globales de la lógica de negocio;
- separa presentación, dominio, servicio y almacenamiento;
- aplica excepciones específicas en lugar de errores genéricos;
- dispone de 16 pruebas automatizadas sobre el servicio y la integración básica de consola;
- conserva trazabilidad entre code smells, refactorings y verificaciones;
- documenta explícitamente los aspectos que permanecen parciales, evitando presentar como resueltos puntos que todavía admiten mejora.

## Conclusión

La revisión confirma una mejora sustancial de la calidad interna respecto de `estado-inicial`. Los principales code smells que motivaron el refactoring fueron corregidos o reducidos de manera verificable. Los puntos parciales restantes no impiden el funcionamiento del sistema, pero se registran como deuda técnica residual y como oportunidades concretas de evolución futura.
