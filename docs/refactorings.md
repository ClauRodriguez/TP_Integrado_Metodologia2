# Refactorings aplicados

Se aplicaron **6 refactorings**. Las operaciones exitosas mantienen los mismos mensajes y formato de salida. Los mensajes de error se mejoraron a propósito para que sean más claros, y el menú de consola se rediseñó como mejora de presentación (misma numeración y mismas funciones).

## Resumen

| N.º | Refactoring | Smell que ataca | Dónde queda |
|---|---|---|---|
| 1 | **Extract Method** | Long Method (3) | `ServicioSolicitudes` |
| 2 | **Move Method** | Lógica fuera de la entidad (8) | `Solicitud` |
| 3 | **Introduce Parameter Object** | Long Parameter List (4) | `DatosSolicitud` |
| 4 | **Replace Magic String with Enum** | Magic strings (6) | `Estado`, `Prioridad`, `TipoSolicitud` |
| 5 | **Replace Conditional with Lookup Table** | `if/elif` y duplicación (5, 7) | `CRITERIOS` en `buscar()` |
| 6 | **Separar lógica de presentación** | Mezcla de lógica y `print` (1, 9, 10) | `consola.py` |

## Refactoring 1: Extract Method

**Antes:** `registrar()` hacía todo junto: validar, crear el estudiante, calcular el plazo, guardar e imprimir.

```python
def registrar(n, l, e, t, p, d):
    global contador
    if n == "" or l == "" or e == "" or d == "":
        print("error")
        return
    # ... más validaciones ...
    est = None
    for x in estudiantes:
        if x["legajo"] == l:
            est = x
    if est == None:
        est = {"nombre": n, "legajo": l, "email": e}
        estudiantes.append(est)
    # ... cálculo de plazo, guardado e impresión ...
```

**Después:** cada tarea es un método corto con un nombre que explica lo que hace.

```python
def registrar(self, datos):
    self._validar_datos(datos)
    estudiante = self._obtener_o_crear_estudiante(datos)
    self._ultimo_id += 1
    solicitud = Solicitud(self._ultimo_id, estudiante,
                          TipoSolicitud.desde_texto(datos.tipo),
                          Prioridad.desde_texto(datos.prioridad),
                          datos.descripcion)
    self._repositorio.agregar(solicitud)
    return solicitud
```

**Resultado:** `registrar()` se lee como una lista de pasos, y la validación y la búsqueda del estudiante se pueden modificar o probar por separado.

## Refactoring 2: Move Method

**Antes:** el plazo se calculaba en `registrar()` y el texto de cada solicitud se armaba en `buscar()` y `reporte()`.

```python
if t == "certificado":
    s["plazo"] = 3
# ...
if p == "alta":
    s["plazo"] = s["plazo"] - 1
```

**Después:** `Solicitud`, que tiene los datos, calcula su plazo y arma su resumen.

```python
@property
def plazo_dias(self):
    plazo = self.tipo.plazo_dias
    if self.prioridad == Prioridad.ALTA:
        plazo -= 1
    return plazo
```

**Resultado:** la regla del plazo vive junto a los datos que usa (mayor cohesión) y el formato de impresión deja de estar duplicado.

## Refactoring 3: Introduce Parameter Object

**Antes:** `registrar(n, l, e, t, p, d)` recibía seis parámetros sueltos.

**Después:** un objeto agrupa los seis datos y se pasa uno solo.

```python
@dataclass
class DatosSolicitud:
    nombre: str
    legajo: str
    email: str
    tipo: str
    prioridad: str
    descripcion: str

servicio.registrar(DatosSolicitud(nombre, legajo, email, tipo, prioridad, descripcion))
```

**Resultado:** ya no se puede confundir el orden de los argumentos, y agregar un campo no obliga a cambiar la firma de los métodos.

## Refactoring 4: Replace Magic String with Enum

**Antes:**

```python
if s["estado"] == "resuelta" or s["estado"] == "rechazada":
```

**Después:**

```python
if self.estado.es_final:
```

**Resultado:** el Estado pasa a ser una entidad real. Un valor inexistente falla de inmediato y cada texto está definido en un solo lugar.

## Refactoring 5: Replace Conditional with Lookup Table

**Antes:** `buscar()` repetía el mismo bucle cuatro veces dentro de un `if/elif`.

**Después:**

```python
def buscar(self, campo, valor):
    criterio = CRITERIOS.get(campo)
    if criterio is None:
        raise DatoInvalidoError("Campo de búsqueda inválido")
    return [s for s in self._repositorio.listar() if criterio(s, valor)]
```

**Resultado:** agregar un filtro nuevo es sumar una línea al diccionario `CRITERIOS`, sin modificar `buscar()`.

## Refactoring 6: Separar lógica de presentación

**Antes:** `registrar()`, `cambiar_estado()` y `reporte()` hacían `print()` e `input()` dentro de la lógica de negocio.

**Después:** el servicio devuelve datos o lanza excepciones propias (`DatoInvalidoError`, `NoEncontradoError`), y solo `consola.py` imprime, pide datos y captura errores.

**Resultado:** la lógica se puede probar sin usar la consola y se podría reutilizar con otra interfaz.

## Cambios intencionales de comportamiento

| Aspecto | Versión inicial | Versión refactorizada | Motivo |
|---|---|---|---|
| Mensajes de error | "error", "no existe" | Mensajes específicos (por ejemplo, "El email no es válido") | Mejor manejo de errores |
| Menú | Una sola línea | Título y opciones en líneas separadas | Mejora de presentación |
| Mensajes de operaciones exitosas | Sin cambios | Sin cambios | Se conserva el comportamiento externo |

## Conclusion

Los seis refactorings atacan las causas de los smells identificados (falta de clases, textos fijos, funciones largas y mezcla de responsabilidades) sin alterar lo que el usuario puede hacer con el sistema. El comportamiento externo se conserva y su verificación se documenta en la etapa de pruebas.