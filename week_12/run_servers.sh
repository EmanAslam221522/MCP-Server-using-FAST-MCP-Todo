#!/bin/bash

# Script to run all servers

echo "Starting Todo MCP Application..."
echo "================================"

# Activate virtual environment
source .venv/bin/activate

# Function to run servers in different terminals (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Starting FastAPI server..."
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && source .venv/bin/activate && python main.py"'

    echo "Starting MCP server (HTTP mode)..."
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && source .venv/bin/activate && fastmcp run mcp_server.py:mcp --transport http --port 8001"'

    echo ""
    echo "Servers are starting in separate terminal windows..."
    echo ""
    echo "FastAPI Server: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "MCP Server: http://localhost:8001"
    echo ""
    echo "To test the MCP client, run in a new terminal:"
    echo "  source .venv/bin/activate"
    echo "  python mcp_client.py"
else
    # Linux/Unix - use background processes
    echo "Starting FastAPI server in background..."
    python main.py &
    FASTAPI_PID=$!

    sleep 2

    echo "Starting MCP server in background (HTTP mode)..."
    fastmcp run mcp_server.py:mcp --transport http --port 8001 &
    MCP_PID=$!

    echo ""
    echo "Servers started with PIDs:"
    echo "  FastAPI: $FASTAPI_PID"
    echo "  MCP: $MCP_PID"
    echo ""
    echo "FastAPI Server: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "MCP Server: http://localhost:8001"
    echo ""
    echo "To test the MCP client, run:"
    echo "  python mcp_client.py"
    echo ""
    echo "Press Ctrl+C to stop all servers"

    # Wait for interrupt
    trap "kill $FASTAPI_PID $MCP_PID; exit" INT
    wait
fi