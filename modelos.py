from dataclasses import dataclass
from enum import Enum

from excepciones import DatoInvalidoError


def _buscar_por(miembros, atributo, texto, etiqueta):
    for miembro in miembros:
        if getattr(miembro, atributo) == texto:
            return miembro
    raise DatoInvalidoError(f"{etiqueta} inválido: '{texto}'")


class Estado(Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en proceso"
    RESUELTA = "resuelta"
    RECHAZADA = "rechazada"

    @property
    def es_final(self):
        return self in (Estado.RESUELTA, Estado.RECHAZADA)

    @classmethod
    def desde_texto(cls, texto):
        return _buscar_por(cls, "value", texto, "Estado")


class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

    @classmethod
    def desde_texto(cls, texto):
        return _buscar_por(cls, "value", texto, "Prioridad")


class TipoSolicitud(Enum):
    CERTIFICADO = ("certificado", 3)
    EQUIVALENCIA = ("equivalencia", 15)
    BAJA = ("baja", 5)
    OTRO = ("otro", 10)

    def __init__(self, nombre, plazo_dias):
        self.nombre = nombre
        self.plazo_dias = plazo_dias

    @classmethod
    def desde_texto(cls, texto):
        return _buscar_por(cls, "nombre", texto, "Tipo")


@dataclass
class Estudiante:
    nombre: str
    legajo: str
    email: str


@dataclass
class Responsable:
    id: int
    nombre: str


@dataclass
class DatosSolicitud:
    nombre: str
    legajo: str
    email: str
    tipo: str
    prioridad: str
    descripcion: str


class Solicitud:
    def __init__(self, id_solicitud, estudiante, tipo, prioridad, descripcion):
        self.id = id_solicitud
        self.estudiante = estudiante
        self.tipo = tipo
        self.prioridad = prioridad
        self.descripcion = descripcion
        self.estado = Estado.PENDIENTE
        self.responsable = None

    @property
    def plazo_dias(self):
        plazo = self.tipo.plazo_dias
        if self.prioridad == Prioridad.ALTA:
            plazo -= 1
        return plazo

    @property
    def nombre_responsable(self):
        return self.responsable.nombre if self.responsable else None

    def cambiar_estado(self, texto_estado):
        if self.estado.es_final:
            raise DatoInvalidoError("No se puede cambiar el estado de una solicitud resuelta o rechazada")
        self.estado = Estado.desde_texto(texto_estado)

    def _campos_base(self):
        return [str(self.id), self.estudiante.nombre, self.tipo.nombre,
                self.prioridad.value, self.estado.value]

    def resumen(self):
        return " | ".join(self._campos_base() + [str(self.nombre_responsable)])

    def resumen_con_plazo(self):
        return " | ".join(self._campos_base() + [f"plazo: {self.plazo_dias} dias"])