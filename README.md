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
## OR
```
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp",
        "--transport",
        "sse"
      ]
    }
  }
}
```



## 🔍 MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an essential tool for testing and debugging your MCP server. It provides a web-based UI to interact with your tools, view logs, and verify the server's behavior.

### Running Inspector Locally
We have provided convenient scripts to launch the inspector:

**Windows (PowerShell):**
```powershell
.\scripts\inspect.ps1
```

**Linux / macOS:**
```bash
bash scripts/inspect.sh
```

Alternatively, you can run it directly using `uv`:
```bash
uv run mcp dev dev.py
```

### Inspecting your Railway Deployment
Once your server is live on Railway, you can inspect the remote SSE endpoint using `npx`:

```bash
npx @modelcontextprotocol/inspector https://your-service.up.railway.app/mcp
```

## ☁️ Deployment (Railway)

This boilerplate is optimized for Railway using **Docker**.

1. **New Project**: Create a new project on Railway and connect your GitHub repository.
2. **Environment Variables**: Add the following in the Railway dashboard:
   - `MCP_TRANSPORT=sse`
   - `PORT=8000`
   - `HOST=0.0.0.0`
3. **Public URL**: Generate a domain in the **Settings** tab.
4. **Health Check**: (Optional) Railway will use the `/health` endpoint if configured.

## 🔒 Authentication (SSE)

When hosting your server publicly (e.g., on Railway), it is highly recommended to protect your endpoint with an API Key.

### 1. Enable Authentication
Set the `API_KEY` environment variable in your `.env` file or Railway dashboard:
```bash
API_KEY=my_secret_token
```

### 2. Client-Side Usage
Once enabled, clients must provide the key using one of these methods:

#### Method A: HTTP Header (Recommended)
Add the `X-API-Key` header to your requests. If you are using `mcp-remote` to connect Claude:
```bash
npx mcp-proxy http://your-service.up.railway.app/mcp --header "X-API-Key: my_secret_token"
```

#### Method B: Query Parameter
Append `?api_key=your_token` to the URL:
```bash
https://your-service.up.railway.app/mcp?api_key=my_secret_token
```

### 3. Testing with Inspector
To inspect a protected remote server:
```bash
npx @modelcontextprotocol/inspector https://your-service.up.railway.app/mcp?api_key=my_secret_token
```

---
*Created and maintained by **Junaid Mugloo**.*
