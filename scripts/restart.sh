#!/bin/bash
PORT=8000
echo "Restarting NextGen MCP server on port $PORT..."

# Kill process on port
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "Stopping existing process..."
    lsof -ti:$PORT | xargs kill -9
    sleep 1
fi

# Set transport and run
export MCP_TRANSPORT=sse
uv run nextgen-mcp
