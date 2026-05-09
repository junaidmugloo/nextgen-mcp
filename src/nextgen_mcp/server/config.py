from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from ..tools import weather

def create_server() -> FastMCP:
    """Initialize and configure the FastMCP server instance."""
    mcp = FastMCP("nextgen-mcp")

    # Register tools
    mcp.tool()(weather.get_alerts)
    mcp.tool()(weather.get_forecast)

    # Root endpoint for basic verification
    @mcp.custom_route("/", methods=["GET"])
    async def root(request):
        return JSONResponse({
            "message": "NextGen MCP Server is running! 🚀",
            "docs": "https://github.com/your-repo",
            "endpoints": {
                "health": "/health",
                "mcp": "/mcp (SSE)"
            }
        })

    # Health check endpoint
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request):
        return JSONResponse({"status": "healthy 💚", "server": "nextgen-mcp"})

    return mcp
