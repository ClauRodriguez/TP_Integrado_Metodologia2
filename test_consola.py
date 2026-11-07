import unittest
from unittest.mock import patch

from consola import Consola
from excepciones import DatoInvalidoError
from modelos import Responsable
from repositorio import RepositorioEnMemoria
from servicio import ServicioSolicitudes


class TestConsola(unittest.TestCase):
    def setUp(self):
        responsables = [Responsable(1, "Bedelia"), Responsable(2, "Tutoria")]
        self.servicio = ServicioSolicitudes(RepositorioEnMemoria(), responsables)
        self.consola = Consola(self.servicio)

    @patch("builtins.input", return_value="abc")
    def test_pedir_entero_rechaza_texto(self, _):
        """Verifica que la interfaz convierta una entrada no numérica en un error controlado."""
        with self.assertRaises(DatoInvalidoError):
            self.consola._pedir_entero("ID: ")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=[
        "Ana", "2001", "ana@mail.com", "certificado", "alta", "Certificado"
    ])
    def test_registrar_desde_consola(self, _, mock_print):
        """Comprueba la integración mínima consola-servicio sin interacción manual."""
        self.consola._registrar()

        self.assertEqual(len(self.servicio.listar()), 1)
        mock_print.assert_called_with("Solicitud 1 registrada")


if __name__ == "__main__":
    unittest.main()
