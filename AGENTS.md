# AGENTS.md

## Project Requirements & Guidelines for Pre-entrega 5

### Project Overview
Agent with cyclic reasoning (ReAct pattern), custom tools, persistent memory (`AsyncSqliteSaver`), static typing, and async management using Python 3.12+ and `uv`.

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

### Code Quality & Standards
- Python 3.12+
- Type Hints on all function definitions.
- Asynchronous code (`asyncio`, `async/await`).
- Clean code architecture with decoupled components (`clima_argentina.py`, `agent.py`, `entrega_5.py`).
