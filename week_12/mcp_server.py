#!/usr/bin/env python3
"""
FastMCP Server Example with Todo Integration
This server provides MCP tools to interact with the Todo FastAPI application
"""

from fastmcp import FastMCP
import httpx
import json
from typing import Dict, List, Optional

# Initialize FastMCP server
mcp = FastMCP("Todo MCP Server")

# Base URL for the Todo API
TODO_API_BASE = "http://localhost:8000"

@mcp.tool
def greet(name: str) -> str:
    """
    Simple greeting tool

    Args:
        name: Name to greet

    Returns:
        Greeting message
    """
    return f"Hello, {name}! Welcome to the Todo MCP Server."

@mcp.tool
async def get_todos(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: int = 10
) -> Dict:
    """
    Retrieve todos from the API with optional filters

    Args:
        completed: Filter by completion status (optional)
        priority: Filter by priority level (low/medium/high) (optional)
        limit: Maximum number of todos to return

    Returns:
        Dictionary containing list of todos
    """
    params = {"limit": limit}

    if completed is not None:
        params["completed"] = completed

    if priority:
        params["priority"] = priority

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TODO_API_BASE}/todos", params=params)
        response.raise_for_status()
        todos = response.json()

    return {
        "count": len(todos),
        "todos": todos
    }

@mcp.tool
async def create_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium"
) -> Dict:
    """
    Create a new todo item

    Args:
        title: Title of the todo
        description: Optional description
        priority: Priority level (low/medium/high)

    Returns:
        Created todo item
    """
    todo_data = {
        "title": title,
        "priority": priority
    }

    if description:
        todo_data["description"] = description

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TODO_API_BASE}/todos",
            json=todo_data
        )
        response.raise_for_status()

    return response.json()

@mcp.tool
async def update_todo(
    todo_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[str] = None
) -> Dict:
    """
    Update an existing todo item

    Args:
        todo_id: ID of the todo to update
        title: New title (optional)
        description: New description (optional)
        completed: Completion status (optional)
        priority: New priority level (optional)

    Returns:
        Updated todo item
    """
    update_data = {}

    if title is not None:
        update_data["title"] = title

    if description is not None:
        update_data["description"] = description

    if completed is not None:
        update_data["completed"] = completed

    if priority is not None:
        update_data["priority"] = priority

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{TODO_API_BASE}/todos/{todo_id}",
            json=update_data
        )
        response.raise_for_status()

    return response.json()

@mcp.tool
async def delete_todo(todo_id: int) -> Dict:
    """
    Delete a todo item

    Args:
        todo_id: ID of the todo to delete

    Returns:
        Confirmation message
    """
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{TODO_API_BASE}/todos/{todo_id}")
        response.raise_for_status()

    return {"message": f"Todo {todo_id} deleted successfully"}

@mcp.tool
async def complete_todo(todo_id: int) -> Dict:
    """
    Mark a todo as completed

    Args:
        todo_id: ID of the todo to complete

    Returns:
        Updated todo item
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TODO_API_BASE}/todos/{todo_id}/complete")
        response.raise_for_status()

    return response.json()

@mcp.tool
async def get_todo_stats() -> Dict:
    """
    Get statistics about todos

    Returns:
        Dictionary with todo statistics
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TODO_API_BASE}/todos/stats/summary")
        response.raise_for_status()

    return response.json()

@mcp.tool
def calculate_completion_rate(total: int, completed: int) -> Dict:
    """
    Calculate the completion rate of todos

    Args:
        total: Total number of todos
        completed: Number of completed todos

    Returns:
        Completion statistics
    """
    if total == 0:
        rate = 0
    else:
        rate = (completed / total) * 100

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "completion_rate": f"{rate:.1f}%"
    }

if __name__ == "__main__":
    # Run the server
    # For stdio transport (default)
    mcp.run()

    # For HTTP transport, uncomment:
    # mcp.run(transport="http", port=8001)