import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """
    Example of a local MCP client connecting via stdio.
    This starts the server as a background process.
    """
    # 1. Server configuration
    # Note: Use "python -m nextgen_mcp.main" or the project script name
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "nextgen-mcp"],
        env=None
    )

    print("--- Local MCP Client Starting ---")
    
    # 2. Establish connection
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3. Handshake
            await session.initialize()
            print("Connected to server!")

            # 4. List tools
            tools_response = await session.list_tools()
            print(f"Server Tools: {[t.name for t in tools_response.tools]}")

            # 5. Call 'greet_user'
            name = input("Enter your name: ")
            print(f"Calling tool 'greet_user' with name='{name}'...")
            
            result = await session.call_tool("greet_user", arguments={"name": name})
            
            # 6. Display response
            print(f"\nServer Response: {result.content[0].text}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
