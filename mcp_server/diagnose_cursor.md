# Troubleshooting Cursor MCP Integration

## Steps to diagnose the issue:

### 1. Check Cursor MCP Logs
- Open Cursor
- Press `Ctrl+Shift+U` (or `Cmd+Shift+U` on Mac) to open Output panel
- In the dropdown at the top right, select "MCP" or "Model Context Protocol"
- Look for any error messages related to "openshift-python-wrapper"

### 2. Try the simplest configuration
Update your `~/.cursor/mcp.json` to:
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "/home/myakove/git/openshift-python-wrapper/mcp_server/launch.sh"
    }
  }
}
```

### 3. Restart Cursor completely
- Close all Cursor windows
- Make sure no Cursor processes are running: `ps aux | grep -i cursor`
- Start Cursor fresh

### 4. Test with absolute path to uv
If the above doesn't work, try finding your uv path and using it directly:
```bash
which uv
```

Then update mcp.json:
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "/full/path/to/uv",
      "args": ["run", "/home/myakove/git/openshift-python-wrapper/mcp_server/server.py"]
    }
  }
}
```

### 5. Check if the server runs manually
```bash
cd /home/myakove/git/openshift-python-wrapper
uv run python mcp_server/server.py
```

### 6. Enable verbose logging in Cursor
Add this to your Cursor settings.json:
```json
{
  "mcp.debug": true
}
```

### 7. Common issues:
- **Python environment**: Make sure uv is in your PATH
- **Permissions**: Check that all files are readable
- **JSON syntax**: Validate your mcp.json with a JSON validator
- **Path issues**: Use absolute paths everywhere

### 8. Alternative: Use npx wrapper
Create a simple npx wrapper if uv is causing issues:
```bash
npm init -y
npm install fastmcp
```

Then use npx in your mcp.json:
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "npx",
      "args": ["fastmcp", "run", "/home/myakove/git/openshift-python-wrapper/mcp_server/server.py"]
    }
  }
}
```
