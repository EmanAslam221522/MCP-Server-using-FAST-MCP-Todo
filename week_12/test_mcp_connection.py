#!/usr/bin/env python3
"""
Test MCP Server Connection
Simple script to verify MCP server is running correctly
"""

import httpx
import asyncio
import json

async def test_connection():
    """Test if MCP server is responding"""

    # Test basic HTTP endpoint
    print("Testing MCP Server Connection...")
    print("=" * 40)

    try:
        # Test if server is running
        async with httpx.AsyncClient() as client:
            # Try to access the MCP endpoint
            response = await client.get("http://localhost:8001/")
            print(f"Server Status Code: {response.status_code}")
            print(f"Server Response: {response.text[:200]}...")

            # Try SSE endpoint with proper headers
            headers = {
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache"
            }

            print("\nTrying SSE connection...")
            response = await client.get(
                "http://localhost:8001/mcp",
                headers=headers,
                timeout=5.0
            )
            print(f"SSE Status Code: {response.status_code}")

    except httpx.ConnectError:
        print("❌ Could not connect to MCP server at http://localhost:8001")
        print("   Make sure the MCP server is running:")
        print("   fastmcp run mcp_server.py:mcp --transport http --port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")

async def test_with_mcp_client():
    """Test using the MCP client library"""
    print("\n" + "=" * 40)
    print("Testing with MCP Client Library...")
    print("=" * 40)

    try:
        from mcp import ClientSession

        # Create a session for HTTP transport
        async with ClientSession(
            uri="http://localhost:8001/mcp",
            transport="http"
        ) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"\nAvailable tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description[:50]}...")

            # Try calling the greet tool
            print("\nTesting greet tool...")
            result = await session.call_tool(
                "greet",
                {"name": "Tester"}
            )
            print(f"Result: {result.content}")

    except ImportError:
        print("❌ MCP client library not properly installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("MCP Server Connection Test")
    print("=" * 40)

    # Run both tests
    asyncio.run(test_connection())
    asyncio.run(test_with_mcp_client())