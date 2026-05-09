import os
from dotenv import load_dotenv
from .server.config import create_server

def main():
    """Main entry point for the NextGen MCP server."""
    load_dotenv()
    
    mcp = create_server()
    
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    if transport == "sse":
        print(f"Starting NextGen MCP server on {host}:{port} with sse transport at /mcp")
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.settings.sse_path = "/mcp"
        mcp.settings.transport_security.enable_dns_rebinding_protection = False
        mcp.settings.transport_security.allowed_hosts = ["*"]
        mcp.settings.transport_security.allowed_origins = ["*"]
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
