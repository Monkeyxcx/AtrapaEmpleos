"""Configuración simple para la primera versión del buscador."""

import json
from pathlib import Path

CONFIG_USUARIO = Path(__file__).resolve().parent.parent / "config_usuario.json"

PALABRAS_CLAVE = ["software", "php"]

CIUDADES = ["Medellin", "Bogota", "Cali", "Barranquilla"]

# Se consideran alrededores habituales de Medellín para ofertas no remotas.
UBICACIONES_MEDELLIN = [
    "medellin", "envigado", "sabaneta", "itagui", "itaguei", "bello",
    "la estrella", "caldas", "copacabana", "girardota", "barbosa",
    "rionegro", "oriente antioqueno", "antioquia",
]

SALARIO_MINIMO_REMOTO = 3_000_000
SALARIO_MINIMO_NO_REMOTO = 3_500_000
DIAS_MAX_DESDE_PUBLICACION = 7
MEJORES_MAX_RESULTADOS = 10

# Si no hay evidencia de modalidad remota, se evalúa como no remoto.
MODALIDAD_REMOTA = ["remoto", "remota", "teletrabajo", "home office", "work from home"]
MODALIDAD_HIBRIDA = ["hibrido", "híbrido", "hybrid"]
MODALIDAD_PRESENCIAL = ["presencial", "onsite", "on-site"]


def _cargar_configuracion_usuario():
    if not CONFIG_USUARIO.exists():
        return {}
    try:
        with CONFIG_USUARIO.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos if isinstance(datos, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


_usuario = _cargar_configuracion_usuario()
PALABRAS_CLAVE = _usuario.get("palabras_clave", PALABRAS_CLAVE)
CIUDADES = _usuario.get("ciudades", CIUDADES)
SALARIO_MINIMO_REMOTO = int(_usuario.get("salario_minimo_remoto", SALARIO_MINIMO_REMOTO))
SALARIO_MINIMO_NO_REMOTO = int(_usuario.get("salario_minimo_no_remoto", SALARIO_MINIMO_NO_REMOTO))
DIAS_MAX_DESDE_PUBLICACION = int(_usuario.get("dias_max_desde_publicacion", DIAS_MAX_DESDE_PUBLICACION))
MEJORES_MAX_RESULTADOS = int(_usuario.get("mejores_max_resultados", MEJORES_MAX_RESULTADOS))
