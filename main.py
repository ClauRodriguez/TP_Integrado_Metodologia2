from consola import Consola
from modelos import Responsable
from repositorio import RepositorioEnMemoria
from servicio import ServicioSolicitudes

RESPONSABLES = [
    Responsable(1, "Bedelia"),
    Responsable(2, "Secretaria Academica"),
    Responsable(3, "Tutoria"),
]


def main():
    servicio = ServicioSolicitudes(RepositorioEnMemoria(), RESPONSABLES)
    Consola(servicio).ejecutar()


if __name__ == "__main__":
    main()