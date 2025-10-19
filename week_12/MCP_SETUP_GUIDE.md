# MCP Configuration for Cursor IDE

## Overview
This guide helps you configure your Todo MCP server (running on localhost:8001) with Cursor IDE.

## Prerequisites
- Your MCP server is running on localhost:8001
- Cursor IDE is installed
- Python environment is set up

## Configuration Steps

### 1. Start Your MCP Server
First, ensure your MCP server is running:
```bash
# Option 1: Use the provided script
./run_servers.sh

# Option 2: Manual start
source .venv/bin/activate
fastmcp run mcp_server.py:mcp --transport http --port 8001
```

### 2. Configure Cursor IDE
To configure MCP in Cursor, you need to:

1. **Open Cursor Settings** (Cmd+, on macOS)
2. **Go to Extensions** → **MCP**
3. **Add New Server** with these settings:
   - **Name**: `todo-mcp-server`
   - **Command**: `python`
   - **Args**: `["-m", "fastmcp", "run", "mcp_server.py:mcp", "--transport", "http", "--port", "8001"]`
   - **Working Directory**: `/Users/tayyab/Desktop/week_12`
   - **Environment Variables**: 
     - `PYTHONPATH`: `/Users/tayyab/Desktop/week_12`

### 3. Alternative: JSON Configuration
You can also use the provided configuration files:
- `cursor-mcp-settings.json` - Main configuration
- `cursor-mcp-config.json` - Alternative format

### 4. Available MCP Tools
Once configured, you'll have access to these tools in Cursor:

- **greet(name)**: Simple greeting tool
- **get_todos(completed?, priority?, limit?)**: Retrieve todos with filters
- **create_todo(title, description?, priority?)**: Create new todo
- **update_todo(todo_id, title?, description?, completed?, priority?)**: Update todo
- **delete_todo(todo_id)**: Delete todo
- **complete_todo(todo_id)**: Mark todo as completed
- **get_todo_stats()**: Get todo statistics
- **calculate_completion_rate(total, completed)**: Calculate completion rate

## Testing the Connection

### 1. Verify Server is Running
```bash
curl http://localhost:8001/health
```

### 2. Test MCP Client
```bash
python mcp_client.py
```

### 3. In Cursor IDE
Once configured, you should see MCP tools available in Cursor's context menu or when using the AI assistant.

## Troubleshooting

### Common Issues:
1. **Server not starting**: Check if port 8001 is available
2. **Connection refused**: Ensure the server is running before configuring Cursor
3. **Permission errors**: Make sure Cursor has access to the project directory

### Debug Steps:
1. Check server logs for errors
2. Verify the server is accessible: `curl http://localhost:8001`
3. Test with the MCP client first
4. Check Cursor's MCP logs in the developer console

## Files Created:
- `cursor-mcp-settings.json` - Main Cursor MCP configuration
- `cursor-mcp-config.json` - Alternative configuration format
- `.cursorrules` - Cursor rules and documentation
- `MCP_SETUP_GUIDE.md` - This setup guide

## Next Steps:
1. Start your MCP server
2. Configure Cursor using the settings above
3. Test the connection
4. Start using MCP tools in your Cursor IDE!

