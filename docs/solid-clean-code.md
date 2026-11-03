# Aplicación de SOLID y Clean Code

En esta etapa se define el diseño de la versión refactorizada y se muestran los fragmentos clave. El código completo, con el antes/después de cada técnica, se documenta en la etapa de refactoring.

## Estructura propuesta

```
├── main.py              # Solo arranca el menú
├── modelos.py           # Enums y clases: Estado, Tipo, Prioridad, Estudiante, Responsable, Solicitud
├── excepciones.py       # Errores propios del sistema
├── repositorio.py       # Interfaz y almacenamiento en memoria
├── servicio.py          # Reglas de negocio
└── consola.py           # Menú, input y print
```

## Principios SOLID

| Principio | Problema en la versión inicial | Mejora aplicada |
|---|---|---|
| **SRP** (una sola responsabilidad) | `registrar()` valida, crea, calcula plazos, guarda e imprime | Cada pieza tiene un único motivo de cambio: `Solicitud` guarda sus datos y calcula su plazo, `ServicioSolicitudes` aplica las reglas, el repositorio guarda y `consola.py` muestra |
| **OCP** (abierto a extensión, cerrado a modificación) | Agregar un tipo obliga a tocar validaciones y cadenas de `if/elif` | Los tipos y sus plazos viven en un `Enum`; los filtros de búsqueda en un diccionario de criterios. Agregar uno es sumar una línea |
| **LSP** (sustitución) | No aplicaba: no había jerarquías | Cualquier repositorio que cumpla la interfaz (memoria o uno falso para pruebas) puede reemplazar a otro sin que el servicio note la diferencia |
| **ISP** (interfaces pequeñas) | No aplicaba: no había interfaces | La interfaz del repositorio tiene solo tres métodos (`agregar`, `obtener`, `listar`); nadie depende de métodos que no usa |
| **DIP** (depender de abstracciones) | Las funciones usaban listas globales directamente | `ServicioSolicitudes` recibe el repositorio por constructor y depende de la interfaz, no de una lista concreta |

## Fragmentos clave

### Estado, tipo y prioridad como entidades (OCP)

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en proceso"
    RESUELTA = "resuelta"
    RECHAZADA = "rechazada"

class TipoSolicitud(Enum):
    CERTIFICADO = ("certificado", 3)
    EQUIVALENCIA = ("equivalencia", 15)
    BAJA = ("baja", 5)
    OTRO = ("otro", 10)

    def __init__(self, nombre, plazo_dias):
        self.nombre = nombre
        self.plazo_dias = plazo_dias
```

Para agregar "constancia" alcanza con una línea en `TipoSolicitud`; la validación, el menú y el plazo se actualizan solos.

### Errores propios (manejo de errores)

```python
class SolicitudError(Exception):
    """Error base del sistema."""

class DatoInvalidoError(SolicitudError):
    pass

class NoEncontradoError(SolicitudError):
    pass
```

### Repositorio con interfaz (DIP, ISP, LSP)

```python
from abc import ABC, abstractmethod

class RepositorioSolicitudes(ABC):
    @abstractmethod
    def agregar(self, solicitud): ...
    @abstractmethod
    def obtener(self, id_solicitud): ...
    @abstractmethod
    def listar(self): ...

class RepositorioEnMemoria(RepositorioSolicitudes):
    def __init__(self):
        self._solicitudes = {}

    def agregar(self, solicitud):
        self._solicitudes[solicitud.id] = solicitud

    def obtener(self, id_solicitud):
        return self._solicitudes.get(id_solicitud)

    def listar(self):
        return list(self._solicitudes.values())
```

### Servicio que depende de la abstracción (DIP, SRP)

```python
class ServicioSolicitudes:
    def __init__(self, repositorio):
        self._repositorio = repositorio
```

### Filtros sin if/elif (OCP)

```python
CRITERIOS = {
    "estado": lambda s, valor: s.estado.value == valor,
    "tipo": lambda s, valor: s.tipo.nombre == valor,
    "prioridad": lambda s, valor: s.prioridad.value == valor,
    "legajo": lambda s, valor: s.estudiante.legajo == valor,
}
```

## Clean Code

| Aspecto | Antes | Después |
|---|---|---|
| **Nombres** | `n`, `l`, `e`, `s`, `x`, `res` | `nombre`, `legajo`, `email`, `solicitud`, `resultados` |
| **Funciones** | `registrar()` hace 5 cosas | Funciones cortas de una sola tarea (`validar_datos`, `obtener_o_crear_estudiante`, `crear_solicitud`) |
| **Manejo de errores** | `print("error")` y `except:` | Excepciones propias con mensajes claros, capturadas solo en `consola.py` |
| **Cohesión** | Datos y reglas separados | El plazo se calcula dentro de `Solicitud`, que es quien tiene los datos |
| **Acoplamiento** | Todo depende de listas globales | Dependencias inyectadas, sin variables globales |
| **Límites entre componentes** | Un archivo con todo | Capas separadas: modelos, reglas, almacenamiento y presentación |
| **Constantes** | Textos repetidos | Enums, un único lugar para cada valor |

## Conclusión

El diseño nuevo ataca las causas de los smells (clases, Enums, repositorio y separación en capas), no solo los síntomas. Con esto, agregar un tipo, un estado o un filtro deja de requerir cambios en varios lugares.