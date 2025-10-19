# FastMCP Todo Application

A complete example of FastMCP integration with a FastAPI Todo application, demonstrating MCP (Model Context Protocol) server-client architecture.

## Architecture

```
┌──────────────┐     HTTP/SSE      ┌──────────────┐     HTTP      ┌──────────────┐
│  MCP Client  │ ◄───────────────► │  MCP Server  │ ◄──────────► │  FastAPI     │
│              │                    │  Port 8001   │               │  Port 8000   │
└──────────────┘                    └──────────────┘               └──────────────┘
                                           │                              │
                                           │                              ▼
                                           │                        ┌──────────┐
                                           └───────────────────────►│  SQLite  │
                                                                    │    DB    │
                                                                    └──────────┘
```

## Components

1. **FastAPI Todo App** (`main.py`) - REST API with full CRUD operations
2. **MCP Server** (`mcp_server.py`) - FastMCP server exposing Todo tools
3. **MCP Client** (`mcp_client_fixed.py`) - Client to interact with MCP server
4. **Database** (`database.py`) - SQLAlchemy models and configuration
5. **Schemas** (`schemas.py`) - Pydantic validation schemas

## Setup Instructions

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Seed the database with sample todos
python seed_data.py
```

### 3. Start the Servers

#### Option A: Use the Run Script (Recommended for macOS)

```bash
chmod +x run_servers.sh
./run_servers.sh
```

#### Option B: Manual Start (Multiple Terminals)

**Terminal 1 - FastAPI Server:**
```bash
source .venv/bin/activate
python main.py
# OR
uvicorn main:app --reload
```

**Terminal 2 - MCP Server (HTTP mode):**
```bash
source .venv/bin/activate
fastmcp run mcp_server.py:mcp --transport http --port 8001
```

### 4. Test the Setup

**Terminal 3 - Run MCP Client:**
```bash
source .venv/bin/activate

# Test connection
python test_mcp_connection.py

# Run the fixed client (recommended)
python mcp_client_fixed.py
```

## Available MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `greet` | Simple greeting | `name: str` |
| `get_todos` | Retrieve todos with filters | `completed?: bool, priority?: str, limit?: int` |
| `create_todo` | Create new todo | `title: str, description?: str, priority?: str` |
| `update_todo` | Update existing todo | `todo_id: int, title?: str, description?: str, completed?: bool, priority?: str` |
| `delete_todo` | Delete a todo | `todo_id: int` |
| `complete_todo` | Mark todo as complete | `todo_id: int` |
| `get_todo_stats` | Get statistics | None |
| `calculate_completion_rate` | Calculate completion metrics | `total: int, completed: int` |

## URLs & Endpoints

- **FastAPI Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **MCP Server**: http://localhost:8001
- **MCP Endpoint**: http://localhost:8001/mcp

## Client Usage Examples

### Using the Fixed MCP Client

```python
# Interactive mode
python mcp_client_fixed.py
# Choose option 2 for interactive mode

# Example interaction:
# Enter tool name: greet
# Enter parameters as JSON: {"name": "World"}
# Result: Hello, World! Welcome to the Todo MCP Server.
```

### Programmatic Usage

```python
from mcp import ClientSession
import asyncio

async def example():
    async with ClientSession(
        uri="http://localhost:8001/mcp",
        transport="http"
    ) as session:
        await session.initialize()

        # Call a tool
        result = await session.call_tool(
            "create_todo",
            {
                "title": "My New Todo",
                "description": "Created via MCP",
                "priority": "high"
            }
        )
        print(result.content)

asyncio.run(example())
```

## Troubleshooting

### Error: "Not Acceptable: Client must accept text/event-stream"

This means the client isn't sending the correct headers for SSE. Use `mcp_client_fixed.py` which properly handles HTTP/SSE transport.

### Connection Refused

1. Make sure FastAPI server is running on port 8000
2. Make sure MCP server is running on port 8001 with HTTP transport
3. Check firewall settings

### Tools Not Working

1. Ensure FastAPI server is running and accessible
2. Verify database is initialized: `python seed_data.py`
3. Check MCP server logs for errors

## FastMCP CLI Commands

```bash
# Check version
fastmcp version

# Run server (stdio mode - for CLI integration)
fastmcp run mcp_server.py:mcp

# Run server (HTTP mode - for network access)
fastmcp run mcp_server.py:mcp --transport http --port 8001

# Get help
fastmcp --help
```

## Development Tips

1. **Adding New Tools**: Add methods with `@mcp.tool` decorator in `mcp_server.py`
2. **Testing Tools**: Use `mcp_client_fixed.py` in interactive mode
3. **Debugging**: Check server logs in both terminal windows
4. **API Testing**: Use FastAPI's built-in docs at http://localhost:8000/docs

## Project Structure

```
week_12/
├── .venv/                  # Virtual environment
├── main.py                 # FastAPI application
├── database.py            # Database models
├── schemas.py             # Pydantic schemas
├── seed_data.py           # Database seeder
├── mcp_server.py          # FastMCP server
├── mcp_client.py          # Original client (may have issues)
├── mcp_client_fixed.py    # Fixed client for HTTP transport
├── test_mcp_connection.py # Connection tester
├── run_servers.sh         # Server startup script
├── requirements.txt       # Python dependencies
├── todos.db              # SQLite database (created automatically)
└── README_FASTMCP.md     # This file
```

## Next Steps

1. Deploy MCP server to FastMCP Cloud for production use
2. Add authentication to MCP server
3. Implement more complex tools (bulk operations, analytics)
4. Create a web UI that uses the MCP client
5. Add WebSocket support for real-time updates

## Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [MCP Specification](https://modelcontextprotocol.io)