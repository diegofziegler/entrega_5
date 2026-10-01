"""
Módulo principal del agente de razonamiento cíclico (ReAct) con memoria persistente.
"""

import os
from typing import Any, Dict, List, Literal
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from clima_argentina import obtener_clima_provincia, obtener_todas_las_provincias

load_dotenv()


@tool
def consultar_clima_provincia(provincia: str) -> Dict[str, Any]:
    """
    Consulta los datos climáticos actuales y pronosticados para una provincia específica de Argentina.

    Usa esta herramienta cuando el usuario pregunte por la temperatura, lluvia, viento,
    sol o nubosidad de una provincia específica de Argentina (por ejemplo, 'Buenos Aires',
    'Córdoba', 'Mendoza', 'Tierra del Fuego', 'Salta', 'Santa Fe', 'Chubut').

    Args:
        provincia (str): El nombre de la provincia de Argentina a consultar.

    Returns:
        Dict[str, Any]: Un diccionario con la información del clima (temp_min, temp_max, va_llover, esta_nublado, hay_sol, hay_viento).
                        Si la provincia no se encuentra, retorna un mensaje indicando el error.
    """
    resultado = obtener_clima_provincia(provincia)
    if resultado is None:
        return {
            "error": f"No se encontraron datos climáticos para la provincia '{provincia}'.",
            "provincias_disponibles": [p["provincia"] for p in obtener_todas_las_provincias()]
        }
    return resultado


@tool
def listar_provincias_disponibles() -> List[str]:
    """
    Obtiene la lista de todas las provincias de Argentina disponibles en el sistema de consulta climática.

    Usa esta herramienta cuando el usuario pida saber para qué provincias hay información del clima disponible
    o cuando se requiera comparar o explorar múltiples provincias.

    Returns:
        List[str]: Lista con los nombres de las provincias registradas.
    """
    return [p["provincia"] for p in obtener_todas_las_provincias()]


# Lista de herramientas expuestas al modelo
TOOLS = [consultar_clima_provincia, listar_provincias_disponibles]


class AgentState(MessagesState):
    """
    Esquema del estado del agente. Hereda de MessagesState,
    lo que mantiene la lista de mensajes en la conversación.
    """
    pass


def crear_grafo_agente(checkpointer: AsyncSqliteSaver) -> Any:
    """
    Construye y compila el StateGraph del agente con razonamiento cíclico y persistencia.

    Args:
        checkpointer (AsyncSqliteSaver): Instancia del guardador de estados en SQLite.

    Returns:
        CompiledStateGraph: El grafo compilado listo para invocarse.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.0
    )

    llm_with_tools = llm.bind_tools(TOOLS)

    async def call_model(state: AgentState) -> Dict[str, Any]:
        """
        Nodo que invoca al LLM pasándole el historial de mensajes del estado.
        """
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Construcción del StateGraph
    workflow = StateGraph(AgentState)

    # Definición de Nodos
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(TOOLS))

    # Punto de entrada
    workflow.set_entry_point("agent")

    # Arista condicional: si el modelo decide llamar herramientas -> 'tools', de lo contrario -> END
    workflow.add_conditional_edges("agent", tools_condition)

    # Arista de retorno cíclico desde las herramientas hacia el agente (ciclo ReAct)
    workflow.add_edge("tools", "agent")

    # Compilación con checkpointer para resiliencia de estado / memoria persistente
    app = workflow.compile(checkpointer=checkpointer)
    return app
