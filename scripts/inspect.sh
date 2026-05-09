#!/bin/bash
# Run the MCP Inspector locally
# This will start the server in stdio mode and wrap it with the inspector UI

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv could not be found. Please install it first."
    exit 1
fi

echo "Starting MCP Inspector..."
uv run mcp dev dev.py
