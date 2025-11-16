#!/usr/bin/env python3
"""
HTTP wrapper for FastMCP server
Runs the Todo MCP server over HTTP/SSE transport instead of STDIO
"""

import sys
import asyncio
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import json
from mcp import ClientSession, Resource, Tool
from mcp.server import Server
from mcp.server.stdio import StdioServerTransport
from contextlib import asynccontextmanager
import httpx

# Import the MCP server instance
from mcp_server import mcp

app = FastAPI()

# Global server instance
server = None

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp/invoke")
async def invoke_tool(request: dict):
    """Invoke a tool via the MCP server"""
    tool_name = request.get("tool")
    arguments = request.get("arguments", {})
    
    # Call the tool directly from the mcp instance
    try:
        result = await mcp._handle_tool_call(tool_name, arguments)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
