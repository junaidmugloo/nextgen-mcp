import asyncio
import os
from mcp import ClientSession
from mcp.client.sse import sse_client
from dotenv import load_dotenv

load_dotenv()

async def main():
    """
    Example of a remote MCP client connecting via SSE.
    This connects to a live server (Local or Railway).
    """
    # 1. Server URL (Change to your Railway URL when live)
    url = os.getenv("SSE_URL", "http://localhost:8000/mcp")
    
    print(f"--- Remote MCP Client Connecting to: {url} ---")
    
    try:
        # 2. Establish connection
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                # 3. Handshake
                await session.initialize()
                print("Connected successfully!")

                # 4. List tools
                tools_response = await session.list_tools()
                print(f"Server Tools: {[t.name for t in tools_response.tools]}")

                # 5. Call 'greet_user'
                name = input("Enter your name for the remote server: ")
                result = await session.call_tool("greet_user", arguments={"name": name})
                
                # 6. Display response
                print(f"\nServer Response: {result.content[0].text}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your server is running in SSE mode!")
        print("Run: $env:MCP_TRANSPORT='sse'; uv run nextgen-mcp")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
