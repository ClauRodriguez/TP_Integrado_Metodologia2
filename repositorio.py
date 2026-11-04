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