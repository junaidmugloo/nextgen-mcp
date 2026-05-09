from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from ..tools import weather

def create_server() -> FastMCP:
    """Initialize and configure the FastMCP server instance."""
    mcp = FastMCP("nextgen-mcp")

    # Register tools
    mcp.tool()(weather.get_alerts)
    mcp.tool()(weather.get_forecast)

    # Health check endpoint
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request):
        return JSONResponse({"status": "healthy 💚", "server": "nextgen-mcp"})

    return mcp
