import asyncio
from fastmcp import Client

async def call_greet():
    client = Client("http://localhost:8001/mcp")
    async with client:
        result = await client.call_tool("greet", {"name": "Gemini"})
        print(result)

if __name__ == "__main__":
    asyncio.run(call_greet())