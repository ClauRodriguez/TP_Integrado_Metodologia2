import unittest

from excepciones import DatoInvalidoError, NoEncontradoError
from modelos import DatosSolicitud, Estado, Responsable
from repositorio import RepositorioEnMemoria
from servicio import ServicioSolicitudes


def datos_validos(**cambios):
    base = dict(nombre="Clau Rodriguez", legajo="1001", email="clau@gmail.com",
                tipo="certificado", prioridad="alta", descripcion="Necesito certificado")
    base.update(cambios)
    return DatosSolicitud(**base)


class TestServicioSolicitudes(unittest.TestCase):
    def setUp(self):
        responsables = [Responsable(1, "Bedelia"), Responsable(2, "Tutoria")]
        self.servicio = ServicioSolicitudes(RepositorioEnMemoria(), responsables)

    def test_registrar_valida(self):
        solicitud = self.servicio.registrar(datos_validos())
        self.assertEqual(solicitud.id, 1)
        self.assertEqual(solicitud.estado, Estado.PENDIENTE)

    def test_registrar_email_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.servicio.registrar(datos_validos(email="sin-arroba"))

    def test_registrar_tipo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.servicio.registrar(datos_validos(tipo="xyz"))

    def test_registrar_campo_vacio(self):
        with self.assertRaises(DatoInvalidoError):
            self.servicio.registrar(datos_validos(nombre=""))

    def test_plazo_prioridad_alta(self):
        solicitud = self.servicio.registrar(datos_validos())
        self.assertEqual(solicitud.plazo_dias, 2)

    def test_plazo_prioridad_media(self):
        solicitud = self.servicio.registrar(datos_validos(prioridad="media"))
        self.assertEqual(solicitud.plazo_dias, 3)

    def test_cambiar_estado(self):
        self.servicio.registrar(datos_validos())
        self.servicio.cambiar_estado(1, "en proceso")
        self.assertEqual(self.servicio.buscar("estado", "en proceso")[0].id, 1)

    def test_no_cambia_estado_finalizado(self):
        self.servicio.registrar(datos_validos())
        self.servicio.cambiar_estado(1, "resuelta")
        with self.assertRaises(DatoInvalidoError):
            self.servicio.cambiar_estado(1, "pendiente")

    def test_cambiar_estado_inexistente(self):
        with self.assertRaises(NoEncontradoError):
            self.servicio.cambiar_estado(99, "resuelta")

    def test_asignar_responsable(self):
        self.servicio.registrar(datos_validos())
        self.servicio.asignar_responsable(1, 2)
        self.assertEqual(self.servicio.buscar("legajo", "1001")[0].nombre_responsable, "Tutoria")

    def test_asignar_responsable_invalido(self):
        self.servicio.registrar(datos_validos())
        with self.assertRaises(NoEncontradoError):
            self.servicio.asignar_responsable(1, 9)

    def test_buscar_sin_resultados(self):
        self.servicio.registrar(datos_validos())
        self.assertEqual(self.servicio.buscar("tipo", "baja"), [])

    def test_buscar_campo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.servicio.buscar("color", "rojo")

    def test_contar_por_estado(self):
        self.servicio.registrar(datos_validos())
        self.servicio.registrar(datos_validos(legajo="1002"))
        self.servicio.cambiar_estado(2, "resuelta")
        conteo = self.servicio.contar_por_estado()
        self.assertEqual(conteo[Estado.PENDIENTE], 1)
        self.assertEqual(conteo[Estado.RESUELTA], 1)


if __name__ == "__main__":
    unittest.main()