#!/usr/bin/env python3
"""
FastMCP Client Example
This client demonstrates how to interact with the MCP server
"""

import asyncio
from fastmcp import Client
import json

# MCP Server URL (when running in HTTP mode)
MCP_SERVER_URL = "http://localhost:8001/mcp"

async def demo_client():
    """
    Demonstrate various MCP tool calls
    """
    # Create client instance
    client = Client(MCP_SERVER_URL)

    async with client:
        print("=== MCP Client Demo ===\n")

        # 1. Simple greeting
        print("1. Greeting Tool:")
        result = await client.call_tool("greet", {"name": "Developer"})
        print(f"   Response: {result}\n")

        # 2. Get todo statistics
        print("2. Todo Statistics:")
        stats = await client.call_tool("get_todo_stats", {})
        print(f"   Stats: {json.dumps(stats, indent=2)}\n")

        # 3. Calculate completion rate
        print("3. Completion Rate:")
        if stats:
            rate = await client.call_tool(
                "calculate_completion_rate",
                {
                    "total": stats["total"],
                    "completed": stats["completed"]
                }
            )
            print(f"   Rate: {json.dumps(rate, indent=2)}\n")

        # 4. Get pending high-priority todos
        print("4. High Priority Pending Todos:")
        high_priority = await client.call_tool(
            "get_todos",
            {
                "completed": False,
                "priority": "high",
                "limit": 5
            }
        )
        print(f"   Found {high_priority['count']} high priority todos")
        for todo in high_priority["todos"]:
            print(f"   - [{todo['id']}] {todo['title']}")
        print()

        # 5. Create a new todo
        print("5. Creating New Todo:")
        new_todo = await client.call_tool(
            "create_todo",
            {
                "title": "Test MCP Integration",
                "description": "Created via MCP client",
                "priority": "medium"
            }
        )
        print(f"   Created: {new_todo['title']} (ID: {new_todo['id']})\n")

        # 6. Update the todo
        print("6. Updating Todo:")
        updated_todo = await client.call_tool(
            "update_todo",
            {
                "todo_id": new_todo["id"],
                "description": "Updated via MCP client - testing update functionality"
            }
        )
        print(f"   Updated description: {updated_todo['description']}\n")

        # 7. Complete the todo
        print("7. Completing Todo:")
        completed_todo = await client.call_tool(
            "complete_todo",
            {"todo_id": new_todo["id"]}
        )
        print(f"   Todo marked as completed: {completed_todo['completed']}\n")

        # 8. Get all todos (first 5)
        print("8. List Recent Todos:")
        all_todos = await client.call_tool(
            "get_todos",
            {"limit": 5}
        )
        print(f"   Showing {len(all_todos['todos'])} of {all_todos['count']} todos:")
        for todo in all_todos["todos"]:
            status = "✓" if todo["completed"] else "○"
            print(f"   {status} [{todo['priority']}] {todo['title']}")
        print()

        # 9. Delete the test todo
        print("9. Cleaning Up:")
        delete_result = await client.call_tool(
            "delete_todo",
            {"todo_id": new_todo["id"]}
        )
        print(f"   {delete_result['message']}\n")

        print("=== Demo Complete ===")

async def interactive_client():
    """
    Interactive client for manual testing
    """
    client = Client(MCP_SERVER_URL)

    print("=== Interactive MCP Client ===")
    print("Available tools:")
    print("  - greet(name)")
    print("  - get_todos(completed?, priority?, limit?)")
    print("  - create_todo(title, description?, priority?)")
    print("  - update_todo(todo_id, title?, description?, completed?, priority?)")
    print("  - delete_todo(todo_id)")
    print("  - complete_todo(todo_id)")
    print("  - get_todo_stats()")
    print("  - calculate_completion_rate(total, completed)")
    print("\nType 'quit' to exit\n")

    async with client:
        while True:
            try:
                tool_name = input("Enter tool name: ").strip()

                if tool_name.lower() == 'quit':
                    break

                params_str = input("Enter parameters as JSON (or {} for none): ").strip()
                params = json.loads(params_str) if params_str else {}

                result = await client.call_tool(tool_name, params)
                print(f"\nResult:\n{json.dumps(result, indent=2)}\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}\n")

    print("\nGoodbye!")

if __name__ == "__main__":
    # Choose which mode to run
    print("FastMCP Client")
    print("1. Run automated demo")
    print("2. Interactive mode")

    choice = input("\nSelect mode (1 or 2): ").strip()

    if choice == "1":
        asyncio.run(demo_client())
    elif choice == "2":
        asyncio.run(interactive_client())
    else:
        print("Invalid choice. Running demo mode...")
        asyncio.run(demo_client())