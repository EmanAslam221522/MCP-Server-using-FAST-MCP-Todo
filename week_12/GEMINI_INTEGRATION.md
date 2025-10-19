# Gemini CLI Integration with Todo MCP Server

This guide explains how to integrate your Todo MCP server with Gemini CLI for natural language interaction with your todo application.

## Overview

Gemini CLI can use MCP (Model Context Protocol) servers to extend its capabilities. Your Todo MCP server provides tools that Gemini can use to manage todos through natural language commands.

## Integration Architecture

```
┌─────────────┐  stdio   ┌──────────────┐  HTTP   ┌──────────────┐
│ Gemini CLI  │ ◄──────► │ MCP Server   │ ◄─────► │ FastAPI      │
│             │           │ (Python)     │         │ (Port 8000)  │
└─────────────┘           └──────────────┘         └──────────────┘
     User                      Tools                    Database
```

## Setup Instructions

### Prerequisites

1. **Install Gemini CLI** (if not already installed):
```bash
# Using npm
npm install -g @gemini/cli

# Or using Homebrew (macOS)
brew install gemini-cli
```

2. **Ensure Python environment is ready**:
```bash
cd /Users/tayyab/Desktop/week_12
source .venv/bin/activate
pip install -r requirements.txt
```

### Method 1: Automatic Setup

Run the setup script:
```bash
./setup_gemini_mcp.sh
```

This will create the Gemini configuration automatically.

### Method 2: Manual Setup

1. **Create Gemini config directory**:
```bash
mkdir -p ~/.config/gemini
```

2. **Create configuration file** (`~/.config/gemini/config.json`):
```json
{
  "mcpServers": {
    "todo-server": {
      "command": "/Users/tayyab/Desktop/week_12/.venv/bin/python",
      "args": ["/Users/tayyab/Desktop/week_12/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/tayyab/Desktop/week_12"
      },
      "cwd": "/Users/tayyab/Desktop/week_12"
    }
  }
}
```

### Alternative: Using Environment Variable

You can also set the MCP server path using an environment variable:
```bash
export GEMINI_MCP_SERVERS='{"todo-server": {"command": "python", "args": ["mcp_server.py"], "cwd": "/Users/tayyab/Desktop/week_12"}}'
```

## Usage

### 1. Start the FastAPI Server

First, ensure your FastAPI todo application is running:
```bash
cd /Users/tayyab/Desktop/week_12
source .venv/bin/activate
python main.py
```

### 2. Use Gemini with MCP Tools

#### Basic Commands

```bash
# List all todos
gemini --use todo-server "Show me all my todos"

# Create a new todo
gemini --use todo-server "Create a todo: Review pull requests with high priority"

# Get statistics
gemini --use todo-server "What are my todo statistics?"

# Complete a todo
gemini --use todo-server "Mark todo ID 5 as complete"

# Filter todos
gemini --use todo-server "Show me only high priority incomplete todos"
```

#### Interactive Mode

Start an interactive session:
```bash
gemini --use todo-server
```

Then you can have a conversation:
```
> What todos do I have?
> Create a new todo called "Setup CI/CD pipeline"
> Show me my completion rate
> Delete todo number 3
```

### 3. Complex Examples

```bash
# Multi-step operations
gemini --use todo-server "Create three todos: 1) Write tests (high priority), 2) Update documentation (low priority), 3) Code review (medium priority)"

# Analytical queries
gemini --use todo-server "What percentage of my high priority tasks are incomplete?"

# Bulk operations
gemini --use todo-server "Mark all todos with 'test' in the title as complete"
```

## Available MCP Tools

| Tool | Natural Language Examples |
|------|--------------------------|
| `greet` | "Say hello to John" |
| `get_todos` | "Show all todos", "List incomplete high priority tasks" |
| `create_todo` | "Add a todo: Fix bug in payment module" |
| `update_todo` | "Change todo 5 title to 'Updated task'" |
| `delete_todo` | "Delete todo number 10" |
| `complete_todo` | "Mark todo 7 as done" |
| `get_todo_stats` | "Show todo statistics" |
| `calculate_completion_rate` | "What's my completion rate?" |

## Troubleshooting

### Issue: "MCP server not found"

**Solution**: Verify the configuration path:
```bash
cat ~/.config/gemini/config.json
```

### Issue: "Connection refused"

**Solution**: Ensure FastAPI is running:
```bash
curl http://localhost:8000/health
```

### Issue: "Module not found"

**Solution**: Check Python path and dependencies:
```bash
cd /Users/tayyab/Desktop/week_12
source .venv/bin/activate
python -c "import fastmcp; print('FastMCP installed')"
```

### Issue: "Permission denied"

**Solution**: Make Python executable:
```bash
chmod +x /Users/tayyab/Desktop/week_12/.venv/bin/python
```

## Advanced Configuration

### Using Multiple MCP Servers

You can configure multiple MCP servers in Gemini:

```json
{
  "mcpServers": {
    "todo-server": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/Users/tayyab/Desktop/week_12"
    },
    "another-server": {
      "command": "node",
      "args": ["another_server.js"],
      "cwd": "/path/to/another/server"
    }
  }
}
```

Then use them:
```bash
gemini --use todo-server,another-server "Your command"
```

### Custom Environment Variables

Add environment variables for API keys or configurations:

```json
{
  "mcpServers": {
    "todo-server": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "TODO_API_URL": "http://localhost:8000",
        "LOG_LEVEL": "DEBUG"
      },
      "cwd": "/Users/tayyab/Desktop/week_12"
    }
  }
}
```

## Testing the Integration

### Quick Test Script

Create `test_gemini_integration.sh`:
```bash
#!/bin/bash

echo "Testing Gemini MCP Integration"

# Test 1: Greeting
echo "Test 1: Greeting"
gemini --use todo-server "Say hello to Tester"

# Test 2: List todos
echo -e "\nTest 2: List todos"
gemini --use todo-server "Show all todos"

# Test 3: Create todo
echo -e "\nTest 3: Create todo"
gemini --use todo-server "Create a test todo"

echo -e "\nIntegration test complete!"
```

### Verify MCP Tools are Available

```bash
# List available tools
gemini --use todo-server --list-tools
```

## Best Practices

1. **Keep FastAPI Running**: The MCP server depends on FastAPI being available
2. **Use Descriptive Commands**: Be specific in your natural language requests
3. **Handle Errors Gracefully**: Check if operations succeeded
4. **Monitor Logs**: Check both Gemini and FastAPI logs for debugging

## Security Considerations

1. **Local Only**: By default, this setup only works locally
2. **No Authentication**: Add auth if exposing to network
3. **Input Validation**: The MCP server validates inputs, but be cautious
4. **Environment Isolation**: Use virtual environments

## Next Steps

1. **Add More Tools**: Extend `mcp_server.py` with additional functionality
2. **Implement Batch Operations**: Add tools for bulk todo management
3. **Add Natural Language Search**: Implement semantic search for todos
4. **Create Shortcuts**: Define Gemini aliases for common operations
5. **Integrate with Calendar**: Sync todos with calendar applications

## Resources

- [Gemini CLI Documentation](https://gemini-cli.dev)
- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://gofastmcp.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)