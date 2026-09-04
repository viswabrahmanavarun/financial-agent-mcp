# AI Financial Analyst

A persona-configurable AI financial analyst agent that queries a local SQLite database containing sector-specific data via the Model Context Protocol (MCP).

## Architecture

This project consists of 4 main components:
1. **Data Layer**: An SQLite database (`financial.db`) containing mocked data for 3 sectors (Tech, Retail, Logistics).
2. **MCP Server** (`src/mcp_server.py`): A FastMCP server exposing database query functions as tools.
3. **Agent Logic** (`src/agent.py`): The core intelligence. It establishes a `stdio` connection to the MCP server, fetches the tools dynamically, maps them to Gemini Function Declarations, and handles the chat loop.
4. **Interfaces**:
   - **Streamlit UI** (`src/ui.py`): A human-facing chat interface.
   - **FastAPI** (`src/api.py`): A machine-facing REST endpoint returning structured JSON.

## Setup Instructions

> **Note:** The `mcp` SDK requires Python 3.10+. Ensure you are using an up-to-date Python environment.

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. Build the sample database:
   ```bash
   python data/build_db.py
   ```

## Running the Interfaces

**Run the API:**
```bash
uvicorn src.api:app --reload
```
*You can then test the API via `curl` or by visiting `http://localhost:8000/docs`.*

**Run the UI:**
```bash
streamlit run src/ui.py
```

## Schema Decisions

The database is built using SQLite for simplicity and portability. The schema is normalized into three tables:
1. `companies`: Core information (ticker, name, sector) and recent hiring signals (for testing data-grounding).
2. `financials`: Hard numerical metrics (growth, margins, PE ratio, leverage).
3. `operational_metrics`: Qualitative/operational data like specific levers for PE, or benchmark comparisons for MF analysts.

This structure allows the MCP tools to query specific aspects of a company without pulling unnecessary data, while also allowing a full sector sweep if needed.

## MCP Design

The MCP Server is implemented using the `FastMCP` class from the official `mcp` Python SDK. It is exposed via `stdio`. 
In `agent.py`, the agent establishes a subprocess connection to the server, calls `session.list_tools()`, and dynamically parses the JSON schema provided by MCP into Gemini-compatible `FunctionDeclaration` objects. When the LLM requests a tool call, the agent forwards it to the MCP session and passes the text result back. This maintains a strict boundary between the LLM and the database, fulfilling the MCP requirement.

## Future Improvements

If I had more time, I would:
1. **Tool Error Handling:** Add more robust schema validation when dynamically converting MCP JSON Schema to Gemini Schema (currently it assumes all inputs are strings for simplicity).
2. **SSE vs Stdio:** For a production deployment, I would separate the MCP server into a standalone process using HTTP/SSE instead of `stdio` to allow multiple agents to query the same server without spawning new subprocesses per request.
3. **Advanced Memory:** Implement LangChain or similar for persisting chat history across complex multi-turn analysis.
