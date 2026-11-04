from excepciones import DatoInvalidoError, NoEncontradoError
from modelos import Estado, Estudiante, Prioridad, Solicitud, TipoSolicitud

CRITERIOS = {
    "estado": lambda s, valor: s.estado.value == valor,
    "tipo": lambda s, valor: s.tipo.nombre == valor,
    "prioridad": lambda s, valor: s.prioridad.value == valor,
    "legajo": lambda s, valor: s.estudiante.legajo == valor,
}


class ServicioSolicitudes:
    def __init__(self, repositorio, responsables):
        self._repositorio = repositorio
        self._responsables = {r.id: r for r in responsables}
        self._estudiantes = {}
        self._ultimo_id = 0

    def registrar(self, datos):
        self._validar_datos(datos)
        estudiante = self._obtener_o_crear_estudiante(datos)
        self._ultimo_id += 1
        solicitud = Solicitud(
            self._ultimo_id,
            estudiante,
            TipoSolicitud.desde_texto(datos.tipo),
            Prioridad.desde_texto(datos.prioridad),
            datos.descripcion,
        )
        self._repositorio.agregar(solicitud)
        return solicitud

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        self._obtener(id_solicitud).cambiar_estado(nuevo_estado)

    def asignar_responsable(self, id_solicitud, id_responsable):
        solicitud = self._obtener(id_solicitud)
        responsable = self._responsables.get(id_responsable)
        if responsable is None:
            raise NoEncontradoError("Responsable inválido")
        solicitud.responsable = responsable

    def buscar(self, campo, valor):
        criterio = CRITERIOS.get(campo)
        if criterio is None:
            raise DatoInvalidoError("Campo de búsqueda inválido")
        return [s for s in self._repositorio.listar() if criterio(s, valor)]

    def listar(self):
        return self._repositorio.listar()

    def contar_por_estado(self):
        conteo = {estado: 0 for estado in Estado}
        for solicitud in self._repositorio.listar():
            conteo[solicitud.estado] += 1
        return conteo

    def _obtener(self, id_solicitud):
        solicitud = self._repositorio.obtener(id_solicitud)
        if solicitud is None:
            raise NoEncontradoError("La solicitud no existe")
        return solicitud

    @staticmethod
    def _validar_datos(datos):
        if not all([datos.nombre, datos.legajo, datos.email, datos.descripcion]):
            raise DatoInvalidoError("Todos los campos son obligatorios")
        if "@" not in datos.email:
            raise DatoInvalidoError("El email no es válido")
        TipoSolicitud.desde_texto(datos.tipo)
        Prioridad.desde_texto(datos.prioridad)

    def _obtener_o_crear_estudiante(self, datos):
        estudiante = self._estudiantes.get(datos.legajo)
        if estudiante is None:
            estudiante = Estudiante(datos.nombre, datos.legajo, datos.email)
            self._estudiantes[datos.legajo] = estudiante
        return estudiante