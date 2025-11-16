#!/bin/bash
# Start FastAPI and MCP servers for the Todo application

cd /home/eman-aslam/Documents/FMS/lectures/week_12

# Kill any existing servers on these ports
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 1

# Start FastAPI server
echo "Starting FastAPI server on port 8000..."
/home/eman-aslam/Documents/FMS/lectures/week_12/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
FASTAPI_PID=$!
echo "FastAPI PID: $FASTAPI_PID"
sleep 2

# Start MCP server in stdio mode (will be accessed via stdin/stdout)
echo "Starting MCP server on stdio transport..."
/home/eman-aslam/Documents/FMS/lectures/week_12/.venv/bin/python mcp_server.py > mcp.log 2>&1 &
MCP_PID=$!
echo "MCP PID: $MCP_PID"

# Save PIDs
echo "FASTAPI_PID=$FASTAPI_PID" > pids.txt
echo "MCP_PID=$MCP_PID" >> pids.txt

sleep 1

echo "Servers started!"
echo "FastAPI running at http://localhost:8000"
echo "FastAPI docs at http://localhost:8000/docs"
echo ""
echo "PIDs saved to pids.txt"
tail -20 fastapi.log
