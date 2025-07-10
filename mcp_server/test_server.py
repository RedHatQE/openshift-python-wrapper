#!/usr/bin/env python
"""Test script to verify MCP server functionality"""

import subprocess
import time
import sys


def test_server():
    """Test if the MCP server starts and responds correctly"""
    print("Testing MCP server...")

    # Start the server process
    cmd = ["uv", "run", "python", "server.py"]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/home/myakove/git/openshift-python-wrapper/mcp_server",
    )

    # Give it a moment to start
    time.sleep(2)

    # Check if process is still running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print("Server failed to start!")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return False

    print("Server started successfully!")
    print("Check the Output panel in Cursor for MCP logs")

    # Terminate the test process
    process.terminate()
    return True


if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
