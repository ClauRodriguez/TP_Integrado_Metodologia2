class SolicitudError(Exception):
    """Error base del sistema."""


class DatoInvalidoError(SolicitudError):
    """Un dato ingresado no es válido."""


class NoEncontradoError(SolicitudError):
    """No existe el elemento buscado."""