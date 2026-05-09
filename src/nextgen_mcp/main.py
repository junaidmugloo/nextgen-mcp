import os
import sys
from dotenv import load_dotenv
from .server.config import create_server

def main():
    """Main entry point for the NextGen MCP server."""
    # Load environment variables from .env file (if it exists)
    load_dotenv()
    
    mcp = create_server()
    
    # On Railway, make sure to set MCP_TRANSPORT=sse in the dashboard!
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"--- NextGen MCP Startup ---")
    print(f"Transport: {transport}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Python Version: {sys.version}")
    
    # Log environment info for debugging
    print(f"Env PORT: {os.getenv('PORT')}")
    print(f"Env HOST: {os.getenv('HOST')}")
    print(f"Env MCP_TRANSPORT: {os.getenv('MCP_TRANSPORT')}")
    print(f"---------------------------")

    if transport == "sse":
        print(f"Starting SSE server...")
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.settings.sse_path = "/mcp"
        
        # Security settings for hosted environments
        mcp.settings.transport_security.enable_dns_rebinding_protection = False
        mcp.settings.transport_security.allowed_hosts = ["*"]
        mcp.settings.transport_security.allowed_origins = ["*"]
        
        
        print(f"Health check available at: http://{host}:{port}/health")
        print(f"MCP SSE endpoint available at: http://{host}:{port}/mcp")
        
        mcp.run(transport="sse")
    else:
        print(f"Starting STDIO server...")
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
