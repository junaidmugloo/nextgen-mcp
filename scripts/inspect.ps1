# Run the MCP Inspector locally
# This will start the server in stdio mode and wrap it with the inspector UI

if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv could not be found. Please install it first." -ForegroundColor Red
    exit 1
}

Write-Host "Starting MCP Inspector..." -ForegroundColor Cyan
uv run mcp dev dev.py
