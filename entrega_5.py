"""
Script principal de prueba y demostración del agente de razonamiento cíclico con memoria persistente.
Genera la traza de ejecución en 'log/ejecucion.json'.
"""

import asyncio
import json
import os
from typing import Any, Dict, List
import aiosqlite
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from agent import crear_grafo_agente


def serializar_mensaje(msg: Any) -> Dict[str, Any]:
    """
    Convierte un objeto de mensaje de LangChain en un diccionario JSON-serializable para el log.
    """
    data: Dict[str, Any] = {
        "tipo": msg.__class__.__name__,
        "contenido": msg.content
    }
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        data["tool_calls"] = msg.tool_calls
    if isinstance(msg, ToolMessage):
        data["tool_call_id"] = msg.tool_call_id
        data["name"] = getattr(msg, "name", "")
    return data


async def main() -> None:
    db_path = "checkpoints.db"
    log_dir = "log"
    log_path = os.path.join(log_dir, "ejecucion.json")

    os.makedirs(log_dir, exist_ok=True)

    thread_id = "session_demostracion_001"
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 10
    }

    trace_log: List[Dict[str, Any]] = []

    print("=== Iniciando Demostración del Agente (Pre-entrega 5) ===")

    async with aiosqlite.connect(db_path) as conn:
        checkpointer = AsyncSqliteSaver(conn)
        # Asegurar que las tablas del checkpointer estén creadas
        await checkpointer.setup()

        app = crear_grafo_agente(checkpointer)

        # TURNO 1: Consulta que requiere razonamiento multi-paso (invocando la herramienta >= 2 veces)
        pregunta_turno_1 = (
            "Hola! Quisiera saber el clima en Buenos Aires y Córdoba para decidir qué empacar. "
            "¿Cuál tiene mayor temperatura máxima y en cuál de las dos necesito llevar paraguas?"
        )
        print(f"\n[Turno 1 - Usuario]: {pregunta_turno_1}")

        input_state_1 = {"messages": [HumanMessage(content=pregunta_turno_1)]}

        # Ejecutar e inspeccionar estados intermedios
        trace_turno_1: List[Dict[str, Any]] = []
        async for event in app.astream(input_state_1, config=config, stream_mode="values"):
            mensajes = event.get("messages", [])
            if mensajes:
                ultimo_msg = mensajes[-1]
                msg_dict = serializar_mensaje(ultimo_msg)
                trace_turno_1.append(msg_dict)
                print(f"  └─ [{msg_dict['tipo']}]: {str(msg_dict['contenido'])[:120]}...")
                if "tool_calls" in msg_dict:
                    for tc in msg_dict["tool_calls"]:
                        print(f"      ↳ Llama herramienta: {tc['name']}({tc['args']})")

        trace_log.append({
            "turno": 1,
            "thread_id": thread_id,
            "prompt_usuario": pregunta_turno_1,
            "traza": trace_turno_1
        })

        # TURNO 2: Consulta contextual usando el mismo thread_id (demuestra resiliencia de estado)
        pregunta_turno_2 = "¿Y qué me aconsejás llevar si viajo a Mendoza en vez de esas dos?"
        print(f"\n[Turno 2 - Usuario (mismo thread_id)]: {pregunta_turno_2}")

        input_state_2 = {"messages": [HumanMessage(content=pregunta_turno_2)]}

        trace_turno_2: List[Dict[str, Any]] = []
        async for event in app.astream(input_state_2, config=config, stream_mode="values"):
            mensajes = event.get("messages", [])
            if mensajes:
                ultimo_msg = mensajes[-1]
                msg_dict = serializar_mensaje(ultimo_msg)
                trace_turno_2.append(msg_dict)
                print(f"  └─ [{msg_dict['tipo']}]: {str(msg_dict['contenido'])[:120]}...")
                if "tool_calls" in msg_dict:
                    for tc in msg_dict["tool_calls"]:
                        print(f"      ↳ Llama herramienta: {tc['name']}({tc['args']})")

        trace_log.append({
            "turno": 2,
            "thread_id": thread_id,
            "prompt_usuario": pregunta_turno_2,
            "traza": trace_turno_2
        })

    # Guardar traza en log/ejecucion.json
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(trace_log, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Traza de ejecución guardada exitosamente en '{log_path}'.")


if __name__ == "__main__":
    asyncio.run(main())
