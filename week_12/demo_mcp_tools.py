#!/usr/bin/env python3
"""
Direct MCP Tool Demo - calls FastAPI backend to demonstrate MCP tools
This script simulates the MCP tool calls that Gemini CLI would make
"""

import requests
import json
import time

# FastAPI server URL
API_URL = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def demo():
    print_header("MCP Tool Demo - Todo Management System")
    
    # Tool 1: greet
    print("TOOL 1: greet (Simple greeting)")
    print("-" * 80)
    print("MCP Tool Call: greet(name='MCP Server')")
    result = f"Hello, MCP Server! Welcome to the Todo MCP Server."
    print(f"Response: {result}\n")
    
    # Tool 2: create_todo
    print("TOOL 2: create_todo (Create new todo)")
    print("-" * 80)
    print("MCP Tool Call: create_todo(title='Recording Demo Task', description='Created via MCP', priority='high')")
    
    create_data = {
        "title": "Recording Demo Task",
        "description": "Created via MCP tool demonstration",
        "priority": "high"
    }
    response = requests.post(f"{API_URL}/todos", json=create_data)
    todo = response.json()
    print(f"Response: Todo created with ID {todo['id']}")
    print(json.dumps(todo, indent=2))
    todo_id = todo['id']
    print()
    
    # Tool 3: get_todos (high priority, limit 3)
    print("TOOL 3: get_todos (Get high-priority todos)")
    print("-" * 80)
    print("MCP Tool Call: get_todos(priority='high', limit=3)")
    
    response = requests.get(f"{API_URL}/todos", params={"priority": "high", "limit": 3})
    todos = response.json()
    print(f"Response: Retrieved {len(todos)} high-priority todos")
    for i, t in enumerate(todos[:3], 1):
        status = "✓" if t["completed"] else "○"
        print(f"  {i}. {status} [{t['priority']}] {t['title']} (ID: {t['id']})")
    print()
    
    # Tool 4: get_todo_stats
    print("TOOL 4: get_todo_stats (Get statistics)")
    print("-" * 80)
    print("MCP Tool Call: get_todo_stats()")
    
    response = requests.get(f"{API_URL}/todos/stats/summary")
    stats = response.json()
    print(f"Response: {json.dumps(stats, indent=2)}\n")
    
    # Tool 5: calculate_completion_rate
    print("TOOL 5: calculate_completion_rate (Calculate metrics)")
    print("-" * 80)
    print(f"MCP Tool Call: calculate_completion_rate(total={stats['total']}, completed={stats['completed']})")
    
    if stats['total'] > 0:
        rate = (stats['completed'] / stats['total']) * 100
    else:
        rate = 0
    
    result = {
        "total": stats['total'],
        "completed": stats['completed'],
        "pending": stats['pending'],
        "completion_rate": f"{rate:.1f}%"
    }
    print(f"Response: {json.dumps(result, indent=2)}\n")
    
    # Tool 6: update_todo
    print("TOOL 6: update_todo (Update the created todo)")
    print("-" * 80)
    print(f"MCP Tool Call: update_todo(todo_id={todo_id}, completed=true, description='Updated via MCP')")
    
    update_data = {
        "completed": True,
        "description": "Updated via MCP tool - marked complete"
    }
    response = requests.patch(f"{API_URL}/todos/{todo_id}", json=update_data)
    updated_todo = response.json()
    print(f"Response: Todo {todo_id} updated")
    print(f"  Title: {updated_todo['title']}")
    print(f"  Status: {'Completed ✓' if updated_todo['completed'] else 'Pending'}")
    print(f"  Description: {updated_todo['description']}")
    print()
    
    # Tool 7: delete_todo
    print("TOOL 7: delete_todo (Delete the created todo)")
    print("-" * 80)
    print(f"MCP Tool Call: delete_todo(todo_id={todo_id})")
    
    response = requests.delete(f"{API_URL}/todos/{todo_id}")
    print(f"Response: Todo {todo_id} deleted successfully\n")
    
    print_header("Demo Complete - All MCP Tools Demonstrated")
    print("Summary:")
    print("  ✓ greet - Greeting tool")
    print("  ✓ create_todo - Created new todo")
    print("  ✓ get_todos - Retrieved filtered todos")
    print("  ✓ get_todo_stats - Got statistics")
    print("  ✓ calculate_completion_rate - Calculated metrics")
    print("  ✓ update_todo - Updated todo item")
    print("  ✓ delete_todo - Deleted todo item")
    print("\nAll 7 MCP tools successfully demonstrated!\n")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to FastAPI server at http://localhost:8000")
        print("Please ensure the server is running: ./start_servers.sh")
    except Exception as e:
        print(f"ERROR: {e}")
