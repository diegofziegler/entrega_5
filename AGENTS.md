# Pre-entrega 5: Agente de razonamiento cíclico con memoria persistente

## Resumen de lo que vamos a construir

Agent with cyclic reasoning (ReAct pattern), custom tools, persistent memory (`AsyncSqliteSaver`), static typing, and async management using Python 3.12+ and `uv`.


### Criterios de Aceptación

Para que este trabajo se considere aprobado, el entregable debe cumplir con lo siguiente:

- **Autonomía**: El agente debe ser capaz de determinar por sí mismo cuándo llamar a una herramienta basándose en el prompt del usuario (sin rutas manuales `if/else`).
- **Ciclo de Retorno**: Si una herramienta devuelve un error o información incompleta, el agente debe ser capaz de realizar un segundo intento o pedir aclaraciones.
- **Resiliencia de Estado**: Al proporcionar un `thread_id`, el agente debe ser capaz de recordar interacciones previas dentro de una misma sesión de razonamiento.
- **Código Limpio**: Uso de Python 3.12 o mayor, tipado estático (Type Hints) y gestión asíncrona (`asyncio`).

## Guía de Implementación Sugerida

### Fase 1: El Contrato de Herramientas

Define tus funciones utilizando el decorador `@tool` de LangChain. Asegúrate de incluir docstrings extremadamente descriptivos; recuerda que el LLM decide qué herramienta usar basándose únicamente en esa descripción.

### Fase 2: Definición del Estado y el Grafo

Crea el esquema de tu estado. En LangGraph, el estado es inmutable y se actualiza mediante reducers (usualmente `operator.add` para la lista de mensajes). Configura el `StateGraph` conectando el nodo del modelo con el nodo de ejecución de herramientas mediante una arista condicional (`tools_condition`).

### Fase 3: Persistencia

Configura un Checkpointer. Esto es lo que permite que el agente sea "arquitectónicamente escalable". Sin persistencia, tu agente es efímero; con ella, es capaz de manejar flujos de trabajo largos que requieren intervención humana o esperar procesos externos.

## Errores a evitar

- **Descripciones Insuficientes o vagas**: Si el agente no usa la herramienta que esperas, el error suele estar en el docstring de la función, no en la lógica del grafo.
- **Bucles Infinitos**: No establecer un límite de recursión (`recursion_limit`) al invocar el grafo. Define siempre un techo (ej. 10 pasos) para evitar costos inesperados en la API.
- **Estado Sucio**: Olvidar que el estado se acumula. Asegúrate de limpiar o resumir mensajes si el contexto se vuelve demasiado grande.

## Detalles de la entrega

- **Repositorio** el código en un repositorio público de GitHub. El repositorio para el código fuente es   `https://github.com/diegofziegler/entrega_5.git`
- **Artefacto concreto:** repo con el `StateGraph`, al menos una herramienta propia, persistencia (`SqliteSaver`), la traza ReAct como log o `.json`, y un `README.md`.
- **Qué NO hace falta:** no entregás documento aparte; la traza del razonamiento se entrega como log/JSON dentro del repo.

Repositorio de GitHub que contenga el código del agente en un entorno asíncrono, incluyendo la definición del grafo, las herramientas y la configuración del checkpointer. Debe incluir un archivo README explicando cómo levantar el entorno y un ejemplo de traza de ejecución (.json o log).

### Instrucciones

1. Proyecto debe correr con `uv`, python 3.12+.
2. Define un `StateGraph` que herede de `MessagesState`.
3. Crea al menos una herramienta personalizada que simule una operación de base de datos o búsqueda técnica.
4. Configura un LLM (OpenAI) vinculado a las herramientas (`llm.bind_tools()`).
5. Implementa la lógica de persistencia usando `SqliteSaver` (para desarrollo local).
6. Realiza una prueba de ejecución donde el agente deba llamar a la herramienta al menos dos veces para llegar a la conclusión (razonamiento multi-paso).
7. Sube el código a un repositorio público y asegúrate de no incluir las API Keys (usa variables de entorno).
8. Te dejare creados `.env.example` y `.env` en el directorio de trabajo.
9. Type Hints on all function definitions.
10. Asynchronous code (`asyncio`, `async/await`).
11. Clean code architecture with decoupled components (`clima_argentina.py`, `agent.py`, `entrega_5.py`).


### Specific Requirements
1. **Domain & Custom Tool (`clima_argentina.py`)**:
   - Simulates current weather data for provinces in Argentina (fields: `provincia`, `temp_min`, `temp_max`, `va_llover`, `esta_nublado`, `hay_sol`, `hay_viento`).
   - The agent uses custom tool(s) with clear `@tool` docstrings to query weather data and provide recommendations (e.g., whether to bring a jacket or umbrella).

2. **Test Script (`entrega_5.py`)**:
   - Main async execution entrypoint.
   - Demonstrates multi-step reasoning where the agent invokes tools at least twice (`recursion_limit` set, e.g. 10).
   - Demonstrates persistent memory across queries using `thread_id`.

3. **Execution Trace**:
   - Saved in directory `log/` in `ejecucion.json` (`log/ejecucion.json`).

4. **Persistence**:
   - Uses `AsyncSqliteSaver` from `langgraph.checkpoint.sqlite.aio` with local database (e.g., `checkpoints.db`).

5. **Environment & Variables**:
   - Uses `.env` and `.env.example` with `OPENAI_API_KEY` and `OPENAI_MODEL`.
   - Never commit sensitive API keys to git.

6. **Environment & Package Management**:
   - Uses `uv` with Python 3.12+ in root directory.



#### Ejemplo de la traza esperada (razonamiento cíclico)

El agente desarrollado debe mostrar un ciclo ReAct como este (incluilo como log o .json en el repo):

```text
Usuario: "¿Cuántos pedidos tuvo el cliente 102 y cuál fue el total?"    
→ El agente decide usar la herramienta: buscar_pedidos(cliente_id=102)    
→ La herramienta devuelve: { "pedidos": 3, "total": 14500 }    
→ El agente razona: ya tiene los datos → responde.    
Respuesta: "El cliente 102 tuvo 3 pedidos por un total de $14.500."    
  
(Con el mismo thread_id, si después preguntás "¿y el último?", el agente recuerda el contexto.)    
```

 
#### Checklist de entrega

- Repo público (sin API keys; variables de entorno) con README de cómo levantar el entorno.
- `StateGraph` (hereda de `MessagesState`) con nodo de modelo + nodo de herramientas y arista condicional (`tools_condition`).
- Al menos 1 herramienta con `@tool` y docstring descriptivo.
- Persistencia con `SqliteSaver` + `thread_id` (recuerda la sesión).
- Prueba con razonamiento multi-paso (la herramienta se invoca ≥2 veces) y `recursion_limit` definido.
- Ejemplo de traza de ejecución (.json o log) incluido.
