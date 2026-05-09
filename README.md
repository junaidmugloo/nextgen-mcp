# NextGen MCP Boilerplate

Developed by **Junaid Mugloo** as a production-grade, modular boilerplate for Model Context Protocol (MCP) servers.

This repository provides a clean, scalable, and professional architecture for building high-performance MCP servers. It is battle-tested for both local development and production environments like Railway.

## 🏗️ Architecture

The project is organized into a modular package structure to ensure maintainability and scalability:

- **`src/nextgen_mcp/`**: Core package directory.
  - **`main.py`**: The application entry point. Handles environment loading, transport selection (SSE/stdio), and server startup.
  - **`middlewares/`**: Contains cross-cutting logic.
    - `logging.py`: A built-in decorator-based middleware that logs tool execution time, input arguments, and error states.
  - **`tools/`**: Domain-specific logic.
    - `weather.py`: Example implementation of weather tools using the NWS API. Add your custom tools here.
  - **`server/`**: Server configuration.
    - `config.py`: Central hub for initializing the `FastMCP` instance and registering tools from the `tools/` package.

## ✨ Features

- **Production-Ready Structure**: Industry-standard `src` layout.
- **Advanced Middleware**: Automated logging and performance monitoring for every tool call.
- **Environment Management**: Robust configuration using `.env` files and `python-dotenv`.
- **Dual Transport Support**: 
  - **SSE**: For hosted environments (Railway, Render, etc.) and web-based access.
  - **stdio**: For local CLI use and direct integration with Claude Desktop.
- **Security Optimized**: Pre-configured to handle "Invalid Host header" issues in hosted environments by disabling DNS rebinding protection where appropriate.

## 🚀 Getting Started

### 1. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd nextgen-mcp

# Install dependencies using uv
uv sync
```

### 2. Configuration
Create your local environment file:
```bash
cp .env.example .env
```
Default settings in `.env`:
- `MCP_TRANSPORT=stdio` (Change to `sse` for web server mode)
- `PORT=8000`
- `HOST=0.0.0.0`

### 3. Running Locally

**As a Web Server (SSE):**
```powershell
$env:MCP_TRANSPORT="sse"; uv run nextgen-mcp
```

**As a Local Tool (stdio):**
```bash
uv run nextgen-mcp
```

## 🤖 Claude Desktop Integration

Add this to your `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nextgen-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/Junaid Fayaz/Desktop/weather",
        "run",
        "nextgen-mcp"
      ]
    }
  }
}
```

## ☁️ Deployment (Railway)

This boilerplate is optimized for Railway using **Docker** for a consistent and reliable production environment.

1. **Service**: Create a new service from your GitHub repo.
2. **Environment Variable**: Ensure `MCP_TRANSPORT=sse` is set in the Railway dashboard.
3. **Health Check**: Set the path to `/health` (this is automatically configured in `railway.json`).
4. **Build**: Railway will automatically detect the `Dockerfile` and build the image using `uv`.

## 🔄 Restarting the Server

For convenience, a restart script is provided that automatically kills the existing process on port 8000 and starts a new one:

**Windows (PowerShell):**
```powershell
.\scripts\restart.ps1
```

**Linux / macOS:**
```bash
bash scripts/restart.sh
```

---
*Created and maintained by **Junaid Mugloo**.*
