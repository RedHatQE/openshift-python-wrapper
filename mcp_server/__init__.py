"""
MCP Server for OpenShift Python Wrapper

This module provides an MCP (Model Context Protocol) server that exposes
ocp_resources functionality through FastMCP.
"""

from mcp_server.server import mcp

__all__ = ["mcp"]
