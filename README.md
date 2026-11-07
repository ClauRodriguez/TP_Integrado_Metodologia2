# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador - Metodología de Sistemas II
Tecnicatura Universitaria en Programación a Distancia

**Integrantes:** Claudio Rodriguez - Gaston Cejas - Diego Velardez

## Descripción

Aplicación de consola que permite registrar solicitudes de estudiantes (certificados, equivalencias, bajas, etc.), clasificarlas por tipo, prioridad y estado, asignarles un responsable, buscarlas y generar un reporte.

Este repositorio es la base de un trabajo de evolución de calidad de software. La versión inicial (`estado-inicial`) funciona correctamente desde la mirada del usuario, pero tiene problemas de diseño intencionales que se diagnostican y corrigen mediante refactoring en la versión final (`estado-refactorizado`).

## Funcionalidades

| N.º | Opción del menú | Descripción |
|---|---|---|
| 1 | Registrar | Crea una solicitud con sus datos y valida la información |
| 2 | Cambiar estado | Actualiza el estado (pendiente, en proceso, resuelta, rechazada) |
| 3 | Asignar | Asigna un responsable (Bedelía, Secretaría Académica o Tutoría) |
| 4 | Buscar | Filtra por estado, tipo, prioridad o legajo |
| 5 | Reporte | Muestra el listado y los totales por estado (la generación es simulada por consola) |
| 0 | Salir | Cierra la aplicación |

## Tecnologías

- Python 
- Ejecución por consola
- Sin librerías externas
- Datos almacenados en memoria (se pierden al cerrar el programa)

## Requisitos e instalación

1. Tener Python 3 instalado (se puede verificar con `python --version`).
2. Clonar el repositorio:

```bash
git clone https://github.com/ClauRodriguez/TP_Integrado_Metodologia2.git
cd TP_Integrado_Metodologia2
```

## Uso

```bash
python main.py
```

Se muestra un menú numérico. Ingresar el número de la opción deseada y seguir las indicaciones por pantalla.

## Estructura del repositorio

```
├── main.py              # Punto de entrada: arma el servicio y lanza el menú
├── modelos.py           # Enums y clases: Estado, Prioridad, TipoSolicitud, Estudiante, Responsable, Solicitud
├── excepciones.py       # Errores propios del sistema
├── repositorio.py       # Interfaz y almacenamiento en memoria
├── servicio.py          # Reglas de negocio
├── consola.py           # Menú, entrada y salida por consola
├── test_servicio.py     # Pruebas automatizadas
├── .gitignore
├── README.md
└── docs/                # Diagnóstico, refactorings, pruebas, code review y evidencias
```

## Pruebas

```bash
python -m unittest test_servicio.py -v
```

## Tags del repositorio

| Tag | Hito |
|---|---|
| `estado-inicial` | Sistema base con problemas de diseño |
| `etapa-diagnostico` | Diagnóstico de deuda técnica y code smells |
| `etapa-refactoring` | Refactorings aplicados |
| `etapa-pruebas` | Casos de prueba y evidencias |
| `etapa-docs` | Code review y documentación final |
| `estado-refactorizado` | Versión final mejorada |

## Nota

Los datos utilizados son sintéticos. No se emplean datos personales reales.