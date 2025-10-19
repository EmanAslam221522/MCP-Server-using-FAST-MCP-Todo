#!/usr/bin/env python3
"""
Fixed FastMCP Client for HTTP Transport
Properly handles the HTTP/SSE transport used by FastMCP
"""

import asyncio
from mcp import ClientSession
import json
from typing import Dict, Any, Optional

# MCP Server URL
MCP_SERVER_URL = "http://localhost:8001/mcp"

async def call_mcp_tool(
    session: ClientSession,
    tool_name: str,
    arguments: Dict[str, Any]
) -> Any:
    """
    Helper function to call MCP tools

    Args:
        session: MCP client session
        tool_name: Name of the tool to call
        arguments: Tool arguments

    Returns:
        Tool result
    """
    result = await session.call_tool(tool_name, arguments)
    # Extract the actual content from the result
    if hasattr(result, 'content'):
        # Parse JSON if it's a string
        if isinstance(result.content, str):
            try:
                return json.loads(result.content)
            except json.JSONDecodeError:
                return result.content
        return result.content
    return result

async def demo_client():
    """
    Demonstrate various MCP tool calls using proper HTTP transport
    """
    print("=== MCP Client Demo (HTTP Transport) ===\n")

    try:
        # Create client session with HTTP transport
        async with ClientSession(
            uri=MCP_SERVER_URL,
            transport="http"
        ) as session:
            # Initialize the session
            await session.initialize()
            print("✅ Connected to MCP server\n")

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}")
            print()

            # 1. Simple greeting
            print("1. Testing Greeting Tool:")
            result = await call_mcp_tool(
                session,
                "greet",
                {"name": "Developer"}
            )
            print(f"   Response: {result}\n")

            # 2. Get todo statistics
            print("2. Getting Todo Statistics:")
            try:
                stats = await call_mcp_tool(session, "get_todo_stats", {})
                print(f"   Stats: {json.dumps(stats, indent=2)}\n")

                # 3. Calculate completion rate
                print("3. Calculating Completion Rate:")
                rate = await call_mcp_tool(
                    session,
                    "calculate_completion_rate",
                    {
                        "total": stats.get("total", 0),
                        "completed": stats.get("completed", 0)
                    }
                )
                print(f"   Rate: {json.dumps(rate, indent=2)}\n")
            except Exception as e:
                print(f"   ⚠️  Could not get stats (FastAPI server may be down): {e}\n")

            # 4. Get high priority todos
            print("4. Getting High Priority Todos:")
            try:
                high_priority = await call_mcp_tool(
                    session,
                    "get_todos",
                    {
                        "completed": False,
                        "priority": "high",
                        "limit": 5
                    }
                )
                if isinstance(high_priority, dict):
                    print(f"   Found {high_priority.get('count', 0)} high priority todos")
                    for todo in high_priority.get("todos", []):
                        print(f"   - [{todo['id']}] {todo['title']}")
                print()
            except Exception as e:
                print(f"   ⚠️  Could not get todos: {e}\n")

            # 5. Create a test todo
            print("5. Creating Test Todo:")
            try:
                new_todo = await call_mcp_tool(
                    session,
                    "create_todo",
                    {
                        "title": "Test MCP Integration",
                        "description": "Created via fixed MCP client",
                        "priority": "medium"
                    }
                )
                print(f"   ✅ Created: {new_todo.get('title', 'Unknown')} (ID: {new_todo.get('id', 'Unknown')})")

                # 6. Complete the todo
                if 'id' in new_todo:
                    print(f"\n6. Marking Todo as Complete:")
                    completed = await call_mcp_tool(
                        session,
                        "complete_todo",
                        {"todo_id": new_todo["id"]}
                    )
                    print(f"   ✅ Todo marked as completed: {completed.get('completed', False)}")

                    # 7. Delete the test todo
                    print(f"\n7. Cleaning Up:")
                    delete_result = await call_mcp_tool(
                        session,
                        "delete_todo",
                        {"todo_id": new_todo["id"]}
                    )
                    print(f"   ✅ {delete_result.get('message', 'Deleted')}")
            except Exception as e:
                print(f"   ⚠️  Could not complete todo operations: {e}")

            print("\n=== Demo Complete ===")

    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print(f"   Make sure the MCP server is running:")
        print(f"   fastmcp run mcp_server.py:mcp --transport http --port 8001")

async def interactive_client():
    """
    Interactive client for manual testing with proper HTTP transport
    """
    print("=== Interactive MCP Client (HTTP Transport) ===")

    try:
        async with ClientSession(
            uri=MCP_SERVER_URL,
            transport="http"
        ) as session:
            await session.initialize()
            print("✅ Connected to MCP server\n")

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description[:60]}...")

            print("\nType 'quit' to exit")
            print("Type 'list' to see tools again\n")

            while True:
                try:
                    tool_name = input("Enter tool name: ").strip()

                    if tool_name.lower() == 'quit':
                        break
                    elif tool_name.lower() == 'list':
                        for tool in tools.tools:
                            print(f"  - {tool.name}")
                        continue

                    params_str = input("Enter parameters as JSON (or {} for none): ").strip()
                    params = json.loads(params_str) if params_str else {}

                    result = await call_mcp_tool(session, tool_name, params)

                    print(f"\nResult:")
                    if isinstance(result, (dict, list)):
                        print(json.dumps(result, indent=2))
                    else:
                        print(result)
                    print()

                except KeyboardInterrupt:
                    break
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON: {e}\n")
                except Exception as e:
                    print(f"❌ Error: {e}\n")

    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print(f"   Make sure the MCP server is running with HTTP transport")

    print("\nGoodbye!")

async def test_connection():
    """
    Quick test to verify MCP server connectivity
    """
    print("Testing MCP Server Connection...")
    try:
        async with ClientSession(
            uri=MCP_SERVER_URL,
            transport="http"
        ) as session:
            await session.initialize()
            print("✅ Successfully connected to MCP server")

            tools = await session.list_tools()
            print(f"✅ Found {len(tools.tools)} tools available")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("FastMCP Client (Fixed for HTTP Transport)\n")

    # First test connection
    if not asyncio.run(test_connection()):
        print("\n⚠️  Please start the MCP server first:")
        print("  fastmcp run mcp_server.py:mcp --transport http --port 8001")
        exit(1)

    print("\n" + "=" * 50)
    print("Select mode:")
    print("1. Run automated demo")
    print("2. Interactive mode")

    choice = input("\nSelect mode (1 or 2): ").strip()

    if choice == "1":
        asyncio.run(demo_client())
    elif choice == "2":
        asyncio.run(interactive_client())
    else:
        print("Running demo mode...")
        asyncio.run(demo_client())