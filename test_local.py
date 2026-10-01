"""
Test de simulación local para verificar la lógica del flujo del agente sin necesidad de API key de OpenAI.
"""

import asyncio
import json
import os
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from clima_argentina import obtener_clima_provincia
from agent import consultar_clima_provincia, listar_provincias_disponibles


def test_clima_provincia_data():
    bsas = obtener_clima_provincia("Buenos Aires")
    assert bsas is not None
    assert bsas["provincia"] == "Buenos Aires"
    assert bsas["temp_max"] == 24.7

    coba = obtener_clima_provincia("Córdoba")
    assert coba is not None
    assert coba["va_llover"] is True

    inexistente = obtener_clima_provincia("ProvinciaInexistente")
    assert inexistente is None


def test_tools():
    res_bsas = consultar_clima_provincia.invoke({"provincia": "Buenos Aires"})
    assert res_bsas["provincia"] == "Buenos Aires"

    provincias = listar_provincias_disponibles.invoke({})
    assert "Buenos Aires" in provincias
    assert "Cordoba" in provincias


if __name__ == "__main__":
    test_clima_provincia_data()
    test_tools()
    print("✓ Todos los tests unitarios locales pasaron exitosamente.")
