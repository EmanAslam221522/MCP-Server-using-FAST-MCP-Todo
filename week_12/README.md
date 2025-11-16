# MCP Server with FastAPI Todo Application

A complete, production-ready demonstration of integrating an **MCP (Model Context Protocol) Server** with a **FastAPI REST API** and **Gemini CLI**, showcasing a Todo management system with 7 callable tools.

## ✨ Features

- **FastAPI REST API** — Full CRUD todo management with SQLite database
- **FastMCP Server** — 7 callable tools exposing the REST API via Model Context Protocol
- **Gemini CLI Integration** — Call MCP tools directly from Gemini command line
- **Security First** — No hardcoded secrets, environment variable configuration
- **Fully Documented** — Comprehensive setup, usage, and deployment guides
- **Production Optimized** — Clean code, error handling, logging, validation

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Gemini CLI (or MCP Client)                  │
│         Calls: gemini mcp invoke todo-mcp-server        │
└────────────────────┬─────────────────────────────────────┘
                     │ (stdio/HTTP)
┌────────────────────▼─────────────────────────────────────┐
│         FastMCP Server (Port: stdio/8001)               │
│    Provides 7 Tools: greet, create_todo, get_todos...   │
└────────────────────┬─────────────────────────────────────┘
                     │ (HTTP calls)
┌────────────────────▼─────────────────────────────────────┐
│      FastAPI Server (http://localhost:8000)            │
│    REST Endpoints: GET/POST/PATCH/DELETE /todos        │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│         SQLite Database (todos.db)                       │
│       Stores todos with metadata & timestamps           │
└──────────────────────────────────────────────────────────┘
```

## 📦 What's Included

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with CRUD endpoints |
| `database.py` | SQLAlchemy models and DB setup |
| `schemas.py` | Pydantic validation schemas |
| `mcp_server.py` | FastMCP server with 7 tools |
| `demo_mcp_tools.py` | Demonstration script (no HTTP needed) |
| `gemini_config.yaml` | Gemini CLI configuration |
| `requirements.txt` | Python dependencies |
| `start_servers.sh` | Automated server startup script |
| `.env.example` | Template for environment variables |
| `.gitignore` | Prevents accidental secret commits |

## 🚀 Quick Start

### 1. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/EmanAslam221522/MCP-Server-Using-FAST-MCP.git
cd MCP-Server-Using-FAST-MCP

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Servers
```bash
# Make startup script executable
chmod +x start_servers.sh

# Start FastAPI and MCP servers
./start_servers.sh
```

Expected output:
```
Starting FastAPI server on port 8000...
Starting MCP server on stdio transport...
FastAPI running at http://localhost:8000
```

### 3. Test the Application

**Option A — Using the demo script (easiest, no HTTP setup needed):**
```bash
source .venv/bin/activate
python demo_mcp_tools.py
```

This demonstrates all 7 MCP tools with responses:
- greet
- create_todo
- get_todos
- get_todo_stats
- calculate_completion_rate
- update_todo
- delete_todo

**Option B — Using FastAPI REST API directly:**
```bash
# Health check
curl -s http://localhost:8000/health | jq .

# Create a todo
curl -s -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","priority":"high"}' | jq .

# View API documentation
open http://localhost:8000/docs
```

**Option C — Using Gemini CLI (requires Gemini CLI installed):**
```bash
# Set your API key
export GEMINI_API_KEY="your-api-key-here"

# List available MCP servers
gemini mcp list

# Invoke a tool
gemini mcp invoke todo-mcp-server greet --name "Developer"
gemini mcp invoke todo-mcp-server get_todo_stats
gemini mcp invoke todo-mcp-server create_todo --title "New Task" --priority high
```

## 🛠️ Available MCP Tools

All tools are callable via Gemini CLI or the MCP client. Each tool handles errors gracefully and returns structured JSON responses.

### 1. `greet(name: str)` → str
Simple greeting tool for testing connectivity.
```bash
gemini mcp invoke todo-mcp-server greet --name "World"
# Returns: "Hello, World! Welcome to the Todo MCP Server."
```

### 2. `create_todo(title, description?, priority?)` → Todo
Create a new todo item.
```bash
gemini mcp invoke todo-mcp-server create_todo \
  --title "Buy groceries" \
  --description "Milk, eggs, bread" \
  --priority high
```

### 3. `get_todos(completed?, priority?, limit?)` → List[Todo]
Retrieve todos with optional filtering.
```bash
gemini mcp invoke todo-mcp-server get_todos --priority high --limit 5
```

### 4. `update_todo(todo_id, title?, description?, completed?, priority?)` → Todo
Update an existing todo.
```bash
gemini mcp invoke todo-mcp-server update_todo --todo_id 1 --completed true
```

### 5. `delete_todo(todo_id)` → Dict
Delete a todo permanently.
```bash
gemini mcp invoke todo-mcp-server delete_todo --todo_id 1
```

### 6. `complete_todo(todo_id)` → Todo
Shortcut to mark a todo as completed.
```bash
gemini mcp invoke todo-mcp-server complete_todo --todo_id 1
```

### 7. `get_todo_stats()` → Dict
Get aggregate statistics (total, completed, pending, breakdown by priority).
```bash
gemini mcp invoke todo-mcp-server get_todo_stats
# Returns: {"total": 10, "completed": 3, "pending": 7, "pending_by_priority": {...}}
```

### 8. `calculate_completion_rate(total, completed)` → Dict
Calculate completion metrics.
```bash
gemini mcp invoke todo-mcp-server calculate_completion_rate --total 10 --completed 7
# Returns: {"total": 10, "completed": 7, "pending": 3, "completion_rate": "70.0%"}
```

## 🔐 Security

This project follows security best practices:

✅ **No Hardcoded Secrets**
- API keys must be set via environment variables
- `.env` files are git-ignored
- `.env.example` provides a template

✅ **Input Validation**
- All inputs validated with Pydantic
- SQLAlchemy prevents SQL injection
- Error messages don't expose internals

✅ **Database Security**
- SQLite with SQLAlchemy ORM (parameterized queries)
- No raw SQL strings
- Models enforce constraints

✅ **Dependency Management**
- `requirements.txt` pins all versions
- Regular updates recommended for security patches
- No unnecessary dependencies

### Setup with Environment Variables
```bash
# Copy the example
cp .env.example .env.local

# Edit .env.local and add your actual API key
# NEVER commit .env.local to git!

# Load in your shell session
export $(cat .env.local | xargs)

# Or source it in start_servers.sh
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root / welcome message |
| GET | `/health` | Health check |
| GET | `/docs` | API documentation (Swagger UI) |
| POST | `/todos` | Create todo |
| GET | `/todos` | List todos (with filters) |
| GET | `/todos/{id}` | Get single todo |
| PATCH | `/todos/{id}` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |
| POST | `/todos/{id}/complete` | Mark as complete |
| GET | `/todos/stats/summary` | Get statistics |

## 🧪 Testing

### Unit Test Example (Python)
```python
import requests

# Test health endpoint
response = requests.get('http://localhost:8000/health')
assert response.status_code == 200
assert response.json()['status'] == 'healthy'

# Test create todo
response = requests.post('http://localhost:8000/todos', json={
    'title': 'Test Todo',
    'priority': 'high'
})
assert response.status_code == 201
assert 'id' in response.json()
```

### Manual Testing
```bash
# All 4 curl examples from "Quick Start" section above
bash demo_recording_commands.sh  # Runs all test commands
```

## 📚 Project Structure

```
.
├── main.py                 # FastAPI application
├── database.py            # Database models (SQLAlchemy)
├── schemas.py             # Request/response schemas (Pydantic)
├── mcp_server.py          # MCP server with 7 tools
├── demo_mcp_tools.py      # Standalone demo (no HTTP)
├── gemini_config.yaml     # Gemini CLI config (add API key here)
├── start_servers.sh       # Startup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore patterns
├── todos.db              # SQLite database (created on first run)
└── README.md             # This file
```

## 🚧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Then restart
./start_servers.sh
```

### Error: "All connection attempts failed" (MCP client)
```bash
# Ensure both servers are running
ps aux | grep -E 'uvicorn|mcp_server'

# Check FastAPI is responsive
curl http://localhost:8000/health

# Use demo_mcp_tools.py instead (doesn't need HTTP)
python demo_mcp_tools.py
```

### Gemini CLI not finding your server
```bash
# Verify your API key is set
echo $GEMINI_API_KEY

# Check gemini_config.yaml exists and is readable
cat gemini_config.yaml

# Try listing servers with debug
gemini mcp list -d
```

## 📖 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **FastMCP Docs:** https://gofastmcp.com
- **MCP Specification:** https://modelcontextprotocol.io
- **SQLAlchemy:** https://docs.sqlalchemy.org
- **Pydantic:** https://docs.pydantic.dev

## 📝 License

MIT License — feel free to use, modify, and distribute this code.

## 🎯 Next Steps

1. ✅ Clone the repository
2. ✅ Set up the virtual environment
3. ✅ Configure your Gemini API key (or skip for demo)
4. ✅ Run `./start_servers.sh`
5. ✅ Test with `python demo_mcp_tools.py`
6. ✅ Integrate into your Gemini CLI workflow

## 💬 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review **API documentation** at http://localhost:8000/docs
3. Check server logs: `tail -n 100 fastapi.log` or `tail -n 100 mcp.log`
4. Open an issue on GitHub

---

**Status:** ✅ Production Ready | **Last Updated:** November 2025
