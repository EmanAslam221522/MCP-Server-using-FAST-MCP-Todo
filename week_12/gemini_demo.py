#!/usr/bin/env python3
"""
Enhanced MCP Client with Gemini Integration Examples
Demonstrates how to use the MCP server with Gemini CLI
"""

import asyncio
import json
from typing import Dict, Any
import subprocess
import sys

class GeminiMCPDemo:
    """Demo class showing MCP tool usage patterns"""
    
    @staticmethod
    def run_gemini_cli_command(tools: str = "list"):
        """
        Run Gemini CLI commands to interact with MCP server
        
        Usage examples:
        - gemini mcp list          (List all available MCP tools)
        - gemini mcp invoke <tool> (Invoke a specific tool)
        """
        print(f"\n{'='*80}")
        print(f"GEMINI CLI MCP COMMAND: gemini mcp {tools}")
        print(f"{'='*80}\n")
        
        try:
            # This would be run in actual Gemini CLI environment
            # Example commands:
            # $ gemini mcp list
            # $ gemini mcp invoke greet --name "Developer"
            # $ gemini mcp invoke create_todo --title "My Task" --priority "high"
            print("[NOTE] Run these commands in your terminal with Gemini CLI installed:")
            print(f"  $ gemini mcp {tools}")
            print()
        except Exception as e:
            print(f"Error: {e}")
    
    @staticmethod
    def show_mcp_tools():
        """Display all available MCP tools"""
        tools = [
            {
                "name": "greet",
                "description": "Simple greeting tool",
                "parameters": {"name": "str"}
            },
            {
                "name": "get_todos",
                "description": "Retrieve todos with optional filters",
                "parameters": {
                    "completed": "Optional[bool]",
                    "priority": "Optional[str]",
                    "limit": "int"
                }
            },
            {
                "name": "create_todo",
                "description": "Create a new todo item",
                "parameters": {
                    "title": "str",
                    "description": "Optional[str]",
                    "priority": "str"
                }
            },
            {
                "name": "update_todo",
                "description": "Update an existing todo",
                "parameters": {
                    "todo_id": "int",
                    "title": "Optional[str]",
                    "description": "Optional[str]",
                    "completed": "Optional[bool]",
                    "priority": "Optional[str]"
                }
            },
            {
                "name": "delete_todo",
                "description": "Delete a todo item",
                "parameters": {"todo_id": "int"}
            },
            {
                "name": "complete_todo",
                "description": "Mark a todo as completed",
                "parameters": {"todo_id": "int"}
            },
            {
                "name": "get_todo_stats",
                "description": "Get todo statistics",
                "parameters": {}
            },
            {
                "name": "calculate_completion_rate",
                "description": "Calculate completion metrics",
                "parameters": {
                    "total": "int",
                    "completed": "int"
                }
            }
        ]
        
        print("\n" + "="*80)
        print("AVAILABLE MCP TOOLS")
        print("="*80)
        
        for tool in tools:
            print(f"\n[{tool['name']}]")
            print(f"  Description: {tool['description']}")
            print(f"  Parameters: {json.dumps(tool['parameters'], indent=4)}")
        
        print("\n" + "="*80)

async def main():
    """Run demo examples"""
    
    print("\n" + "="*80)
    print("MCP SERVER WITH GEMINI CLI INTEGRATION - DEMO")
    print("="*80)
    print("\nThis example shows how to integrate and use the MCP server with Gemini CLI")
    
    # Show available tools
    GeminiMCPDemo.show_mcp_tools()
    
    # Show example Gemini CLI commands
    print("\n" + "="*80)
    print("EXAMPLE GEMINI CLI COMMANDS")
    print("="*80)
    
    examples = [
        ("gemini mcp list", "List all available MCP tools"),
        ("gemini mcp invoke greet --name Developer", "Call the greet tool"),
        ("gemini mcp invoke create_todo --title 'My Task' --priority high", "Create a todo"),
        ("gemini mcp invoke get_todos --priority high --limit 5", "Get high-priority todos"),
        ("gemini mcp invoke get_todo_stats", "Get statistics"),
    ]
    
    for cmd, description in examples:
        print(f"\n$ {cmd}")
        print(f"  # {description}")

if __name__ == "__main__":
    asyncio.run(main())
