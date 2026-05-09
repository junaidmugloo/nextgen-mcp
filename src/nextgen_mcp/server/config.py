from mcp.server.fastmcp import FastMCP
from ..tools import weather

def create_server() -> FastMCP:
    """Initialize and configure the FastMCP server instance."""
    mcp = FastMCP("nextgen-mcp")

    # Register tools
    mcp.tool()(weather.get_alerts)
    mcp.tool()(weather.get_forecast)

    return mcp
