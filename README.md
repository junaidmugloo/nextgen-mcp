# Weather MCP Server

Developed by **Junaid Mugloo** as a boilerplate for Model Context Protocol (MCP) servers.

A Model Context Protocol (MCP) server that provides real-time weather alerts and forecasts using the National Weather Service (NWS) API.

## Features

- **Get Weather Alerts**: Fetch active weather alerts for any US state.
- **Get Forecast**: Get detailed 5-period forecasts for any latitude/longitude coordinates.
- **Dual Transport Support**: Works via `stdio` (local) and `sse` (hosted/web).

## Prerequisites

- [Python 3.12+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd weather

# Install dependencies
uv sync
```

## Local Usage

### 1. Run as a Web Server (SSE)
To run the server locally as an HTTP service (e.g., for testing Railway-style behavior):

**PowerShell:**
```powershell
$env:MCP_TRANSPORT="sse"; $env:PORT="8000"; uv run main.py
```

**Bash:**
```bash
MCP_TRANSPORT=sse PORT=8000 uv run main.py
```
The server will be available at `http://localhost:8000/mcp`.

### 2. Run via stdio
This is the standard mode for local CLI tools and direct Claude Desktop integration.
```bash
uv run main.py
```

## Claude Desktop Configuration

To use this server in Claude Desktop, add the following to your configuration file:

**Location:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Option A: Local (Recommended)
Claude starts/stops the server automatically.
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/Junaid Fayaz/Desktop/weather",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Option B: Hosted/Local URL (SSE)
Use this if the server is already running (locally or on Railway).
```json
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Deployment (Railway)

1.  **Environment Variables**:
    - `MCP_TRANSPORT`: Set to `sse`.
    - `PORT`: Automatically provided by Railway (defaults to 8000).
2.  **Health Check**:
    - Set the health check path to `/mcp`.
3.  **Start Command**:
    - `uv run main.py`

## Troubleshooting

### Invalid Host Header
If you see an "Invalid Host header" error when running in SSE mode, ensure `MCP_TRANSPORT` is set to `sse`. The server is configured to allow all hosts (`*`) and has DNS rebinding protection disabled for maximum compatibility in hosted environments.
