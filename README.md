# Pre-entrega 5: Agente de Razonamiento Cíclico con Memoria Persistente

Agente conversacional de razonamiento cíclico (patrón ReAct) desarrollado con **LangGraph**, **LangChain** y **Python 3.12+**, utilizando **`uv`** como gestor de entorno e historia persistente a través de **`AsyncSqliteSaver`**.

## 📌 Características Principales

- **Autonomía (ReAct)**: El agente analiza el prompt del usuario y decide de forma autónoma cuándo llamar a las herramientas asociadas (`llm.bind_tools()`), sin reglas manuales `if/else`.
- **Ciclo de Retorno**: Conexión entre el nodo de agente y las herramientas vía `tools_condition` y arista de retorno (`tools -> agent`).
- **Razonamiento Multi-paso**: Permite la ejecución iterativa/secuencial de múltiples herramientas en un mismo turno de conversación.
- **Resiliencia de Estado (Persistencia)**: Utiliza `AsyncSqliteSaver` junto a `thread_id` para recordar el contexto de conversaciones anteriores.
- **Tipado Estático y Async**: Implementado completamente con `asyncio`, Type Hints y Python 3.12+.

---

## 📁 Estructura del Proyecto

```text
├── AGENTS.md             # Especificaciones y criterios de aceptación del proyecto
├── clima_argentina.py    # Datos climáticos simulados de provincias de Argentina
├── agent.py              # Definición de herramientas, StateGraph (MessagesState) y checkpointer
├── entrega_5.py          # Script principal de prueba y generación de trazas
├── test_local.py         # Tests unitarios para las herramientas locales
├── pyproject.toml        # Configuración del proyecto y dependencias (uv)
├── uv.lock               # Archivo de bloqueo de dependencias de uv
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados en el control de versiones
└── log/
    └── ejecucion.json    # Ejemplo de traza de ejecución (log de razonamiento multi-paso)
```

---

## 🛠️ Requisitos Previos e Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/diegofziegler/entrega_5.git
cd entrega_5
```

### 2. Instalar `uv` (si no lo tienes instalado)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Configurar el Entorno y Variables de Entorno
Copia el archivo `.env.example` a `.env` y configura tu API Key de OpenAI:

```bash
cp .env.example .env
```

Edita `.env`:
```env
OPENAI_API_KEY=tu_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

---

## 🚀 Ejecución del Proyecto

### Ejecutar el Script de Demostración
El script `entrega_5.py` ejecuta dos turnos de conversación con el mismo `thread_id`:
1. **Turno 1**: Realiza una pregunta comparativa sobre dos provincias (provocando múltiples llamadas a herramientas en ciclo ReAct).
2. **Turno 2**: Realiza una pregunta de seguimiento que depende del contexto previo guardado en SQLite.

Para ejecutarlo con `uv`:
```bash
uv run python entrega_5.py
```

Al finalizar, la traza completa de razonamiento se guardará automáticamente en:
`log/ejecucion.json`

---

## 🧪 Pruebas Unitarias Locales

Para verificar el correcto funcionamiento de los módulos y herramientas sin consumir la API de OpenAI:
```bash
uv run python test_local.py
```

---

## 📋 Checklist de Criterios de Aceptación Cumplidos

- [x] Repositorio público configurado con variables de entorno (`.env`).
- [x] Gestión de dependencias y proyecto con `uv` y Python 3.12+.
- [x] `StateGraph` hereda de `MessagesState` con nodo de modelo, herramientas y arista condicional (`tools_condition`).
- [x] Herramientas personalizadas decoradas con `@tool` y docstrings descriptivos.
- [x] Persistencia con `AsyncSqliteSaver` utilizando `thread_id`.
- [x] Prueba de razonamiento multi-paso con límite de recursión (`recursion_limit=10`).
- [x] Ejemplo de traza de ejecución guardado en `log/ejecucion.json`.