A professional, easy-to-use template for building and hosting **Model Context Protocol (MCP)** servers.

Created by **Junaid Mugloo**.

---

## 🛠️ Quick Start (Local)

### 1. Setup
Make sure you have [uv](https://docs.astral.sh/uv/) installed, then run:
```bash
# Install everything
uv sync

# Create your settings file
cp .env.example .env
```

### 2. Run the Server
Choose how you want to run it:

*   **For Claude Desktop (Standard):**
    ```bash
    uv run nextgen-mcp
    ```
*   **As a Web Server (SSE):**
    ```powershell
    $env:MCP_TRANSPORT="sse"; uv run nextgen-mcp
    ```

---

## 🔍 Testing with Inspector

The **Inspector** is a web-tool to test your tools without opening Claude.

**Run it locally:**
```powershell
.\scripts\inspect.ps1
```
*This will open a browser window where you can use the `greet_user` tool.*

---

## 🤖 Adding to Claude Desktop

To give Claude powers, add this to your `claude_desktop_config.json`:

### Option A: Local Connection (Fastest)
```json
{
  "mcpServers": {
    "mcp-boilerplate": {
      "command": "uv",
      "args": [
        "--directory",
        "<PATH_TO_YOUR_PROJECT_FOLDER>",
        "run",
        "nextgen-mcp"
      ]
    }
  }
}
```

### Option B: Cloud Connection (Railway)
If you have deployed to Railway, use the URL:
```json
{
  "mcpServers": {
    "mcp-cloud": {
      "url": "https://your-app.up.railway.app/mcp"
    }
  }
}
```

---

## ☁️ Deploy to Railway (Host for Free)

1.  **Upload** this code to your GitHub.
2.  **Create** a new project on [Railway.app](https://railway.app/).
3.  **Connect** your GitHub repo.
4.  **Set these Variables** in the Railway dashboard:
    *   `MCP_TRANSPORT` = `sse`
    *   `PORT` = `8000`
5.  **Enable Public Access** in the "Settings" tab to get your URL.

## 🔌 Using MCP Clients

We have included two Python scripts in the `clients/` folder to show you how to build your own app that talks to this server.

### 1. Local Client (stdio)
Starts the server in the background and calls the greeting tool.
```bash
uv run clients/stdio_client.py
```

### 2. Remote Client (SSE)
Connects to a live server (Local or Railway).
```bash
# First, start the server in a separate terminal:
# $env:MCP_TRANSPORT="sse"; uv run nextgen-mcp

# Then run the client:
uv run clients/sse_client.py
```

---
## 📁 Folder Structure
 (For Developers)

*   `src/tools/` ➔ **Add your own tools here!**
*   `src/main.py` ➔ The "brain" that starts the server.
*   `dev.py` ➔ Used by the Inspector for local testing.

---
*Maintained by **Junaid Mugloo**.*
