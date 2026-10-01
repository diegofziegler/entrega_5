"""
Módulo para simular la obtención de datos del clima de las provincias de Argentina.
"""

from typing import Any, Dict, List, Optional


WEATHER_DATA: List[Dict[str, Any]] = [
    {
        "provincia": "Buenos Aires",
        "temp_min": 12.3,
        "temp_max": 24.7,
        "va_llover": False,
        "esta_nublado": True,
        "hay_sol": True,
        "hay_viento": False,
    },
    {
        "provincia": "Cordoba",
        "temp_min": 8.0,
        "temp_max": 18.5,
        "va_llover": True,
        "esta_nublado": True,
        "hay_sol": False,
        "hay_viento": True,
    },
    {
        "provincia": "Mendoza",
        "temp_min": 5.2,
        "temp_max": 15.0,
        "va_llover": False,
        "esta_nublado": False,
        "hay_sol": True,
        "hay_viento": True,
    },
    {
        "provincia": "Santa Fe",
        "temp_min": 14.0,
        "temp_max": 27.2,
        "va_llover": False,
        "esta_nublado": False,
        "hay_sol": True,
        "hay_viento": False,
    },
    {
        "provincia": "Tierra del Fuego",
        "temp_min": -2.0,
        "temp_max": 6.0,
        "va_llover": True,
        "esta_nublado": True,
        "hay_sol": False,
        "hay_viento": True,
    },
    {
        "provincia": "Salta",
        "temp_min": 11.0,
        "temp_max": 22.0,
        "va_llover": False,
        "esta_nublado": True,
        "hay_sol": True,
        "hay_viento": False,
    },
    {
        "provincia": "Chubut",
        "temp_min": 3.0,
        "temp_max": 12.0,
        "va_llover": False,
        "esta_nublado": False,
        "hay_sol": True,
        "hay_viento": True,
    },
]


def obtener_clima_provincia(provincia: str) -> Optional[Dict[str, Any]]:
    """
    Busca los datos climáticos simulados de una provincia de Argentina.
    Realiza una búsqueda case-insensitive e ignora acentos básicos.

    Args:
        provincia (str): Nombre de la provincia.

    Returns:
        Optional[Dict[str, Any]]: Diccionario con los datos del clima o None si no existe.
    """
    def normalizar(texto: str) -> str:
        remplazos = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        s = texto.lower().strip()
        for a, b in remplazos:
            s = s.replace(a, b)
        return s

    prov_norm = normalizar(provincia)
    for data in WEATHER_DATA:
        if normalizar(data["provincia"]) == prov_norm:
            return data
    return None


def obtener_todas_las_provincias() -> List[Dict[str, Any]]:
    """
    Devuelve la lista completa con los datos climáticos de todas las provincias disponibles.

    Returns:
        List[Dict[str, Any]]: Lista de información climática.
    """
    return WEATHER_DATA
