#!/bin/bash
# Launcher script for OCP Resources MCP Server

# Add local bin to PATH to ensure uv is found
export PATH="$HOME/.local/bin:$PATH"

# Change to the project directory
cd /home/myakove/git/openshift-python-wrapper

# Activate the virtual environment and run the server
exec uv run python mcp_server/server.py "$@"
