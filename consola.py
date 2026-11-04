from excepciones import DatoInvalidoError, SolicitudError
from modelos import DatosSolicitud, Estado


class Consola:
    def __init__(self, servicio):
        self._servicio = servicio

    def ejecutar(self):
        acciones = {
            "1": self._registrar,
            "2": self._cambiar_estado,
            "3": self._asignar,
            "4": self._buscar,
            "5": self._reporte,
        }
        while True:
            self._mostrar_menu()
            opcion = input("Opcion: ")
            if opcion == "0":
                break
            accion = acciones.get(opcion)
            if accion is None:
                print("opcion invalida")
                continue
            try:
                accion()
            except SolicitudError as error:
                print(error)

    @staticmethod
    def _mostrar_menu():
        print("\n==============================")
        print("  GESTIÓN DE SOLICITUDES")
        print("==============================")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Generar reporte")
        print("0. Salir")
        print("------------------------------")

    @staticmethod
    def _pedir_entero(mensaje):
        try:
            return int(input(mensaje))
        except ValueError:
            raise DatoInvalidoError("Debe ingresar un número")

    def _registrar(self):
        datos = DatosSolicitud(
            nombre=input("Nombre: "),
            legajo=input("Legajo: "),
            email=input("Email: "),
            tipo=input("Tipo (certificado/equivalencia/baja/otro): "),
            prioridad=input("Prioridad (alta/media/baja): "),
            descripcion=input("Descripcion: "),
        )
        solicitud = self._servicio.registrar(datos)
        print("Solicitud " + str(solicitud.id) + " registrada")

    def _cambiar_estado(self):
        id_solicitud = self._pedir_entero("ID: ")
        nuevo = input("Nuevo estado (pendiente/en proceso/resuelta/rechazada): ")
        self._servicio.cambiar_estado(id_solicitud, nuevo)
        print("Estado actualizado")

    def _asignar(self):
        id_solicitud = self._pedir_entero("ID: ")
        id_responsable = self._pedir_entero("ID responsable (1.Bedelia 2.Secretaria 3.Tutoria): ")
        self._servicio.asignar_responsable(id_solicitud, id_responsable)
        print("Responsable asignado")

    def _buscar(self):
        campo = input("Campo (estado/tipo/prioridad/legajo): ")
        valor = input("Valor: ")
        resultados = self._servicio.buscar(campo, valor)
        if not resultados:
            print("sin resultados")
        for solicitud in resultados:
            print(solicitud.resumen())

    def _reporte(self):
        print("=== REPORTE DE SOLICITUDES ===")
        solicitudes = self._servicio.listar()
        for solicitud in solicitudes:
            print(solicitud.resumen_con_plazo())
        conteo = self._servicio.contar_por_estado()
        print("Total: " + str(len(solicitudes)))
        print("Pendientes: " + str(conteo[Estado.PENDIENTE]) +
              " En proceso: " + str(conteo[Estado.EN_PROCESO]) +
              " Resueltas: " + str(conteo[Estado.RESUELTA]) +
              " Rechazadas: " + str(conteo[Estado.RECHAZADA]))
        print("Su reporte ha sido generado")