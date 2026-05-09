from pathlib import Path
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse, FileResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from ..tools import greetings

def create_server() -> FastMCP:
    """Initialize and configure the FastMCP server instance."""
    mcp = FastMCP("nextgen-mcp")
    
    # Path to assets
    base_dir = Path(__file__).parent.parent
    favicon_folder = base_dir / "favicon_io"
    favicon_path = favicon_folder / "favicon.ico"
    logo_path = favicon_folder / "android-chrome-512x512.png"

    # Register tools
    mcp.tool()(greetings.greet_user)

    # Favicon endpoint
    @mcp.custom_route("/favicon.ico", methods=["GET"])
    async def favicon(request):
        if favicon_path.exists():
            return FileResponse(favicon_path)
        return JSONResponse({"error": "Favicon not found"}, status_code=404)

    # Logo endpoint (to be used in HTML)
    @mcp.custom_route("/logo.png", methods=["GET"])
    async def logo(request):
        if logo_path.exists():
            return FileResponse(logo_path)
        return JSONResponse({"error": "Logo not found"}, status_code=404)

    # Root endpoint for basic verification (HTML Status Page)
    @mcp.custom_route("/", methods=["GET"])
    async def root(request):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>NextGen MCP Server</title>
            <link rel="icon" href="/favicon.ico" type="image/x-icon">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background-color: #f4f7f6; color: #333; }}
                .container {{ text-align: center; background: white; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }}
                img {{ width: 120px; height: 120px; margin-bottom: 1.5rem; }}
                h1 {{ margin: 0 0 1rem; color: #2c3e50; }}
                p {{ color: #7f8c8d; line-height: 1.6; }}
                .status {{ display: inline-block; padding: 0.5rem 1rem; background: #27ae60; color: white; border-radius: 20px; font-weight: bold; font-size: 0.9rem; margin-bottom: 1.5rem; }}
                .links {{ display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; }}
                .links a {{ text-decoration: none; color: #3498db; font-weight: 500; transition: color 0.2s; }}
                .links a:hover {{ color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="/logo.png" alt="Server Logo">
                <div class="status">● ONLINE</div>
                <h1>NextGen MCP</h1>
                <p>Professional weather forecasts and alerts, powered by the Model Context Protocol.</p>
                <div class="links">
                    <a href="/health">Health Check</a>
                    <a href="/mcp">SSE Endpoint</a>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    # Health check endpoint
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request):
        return JSONResponse({"status": "healthy 💚", "server": "nextgen-mcp"})

    return mcp
