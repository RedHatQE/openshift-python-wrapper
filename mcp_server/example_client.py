#!/usr/bin/env python
"""
Example client for the OpenShift Python Wrapper MCP Server

This example demonstrates how to connect to and use the MCP server.
"""

import asyncio

from fastmcp import FastMCPClient


async def main():
    # Connect to the MCP server
    async with FastMCPClient() as client:
        # Connect to the server running on stdio
        await client.connect_stdio(cmd=["python", "mcp_server/server.py"])

        print("Connected to OCP Resources MCP Server")
        print("=" * 50)

        # Get available resource types
        print("\n1. Getting available resource types:")
        result = await client.call_tool(name="get_resource_types")
        print(f"Available resource types: {len(result['resource_types'])}")
        print(f"Categories: {list(result['categories'].keys())}")

        # List namespaces
        print("\n2. Listing namespaces:")
        result = await client.call_tool(name="list_resources", arguments={"resource_type": "namespace", "limit": 5})
        print(f"Found {result['count']} namespaces")
        for ns in result["resources"][:3]:
            print(f"  - {ns['name']}")

        # Get a specific namespace
        print("\n3. Getting default namespace:")
        result = await client.call_tool(
            name="get_resource", arguments={"resource_type": "namespace", "name": "default"}
        )
        print(f"  Name: {result['name']}")
        print(f"  UID: {result['uid']}")
        print(f"  Created: {result['creationTimestamp']}")

        # List pods in default namespace
        print("\n4. Listing pods in default namespace:")
        result = await client.call_tool(
            name="list_resources", arguments={"resource_type": "pod", "namespace": "default"}
        )
        print(f"Found {result['count']} pods")

        # Example: Create a ConfigMap
        print("\n5. Creating a ConfigMap:")
        yaml_content = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-config
  namespace: default
data:
  key1: value1
  key2: value2
"""
        result = await client.call_tool(name="apply_yaml", arguments={"yaml_content": yaml_content})
        if result.get("successful"):
            print("  ConfigMap created successfully!")

        # Get events
        print("\n6. Getting recent events:")
        result = await client.call_tool(
            name="get_resource_events", arguments={"resource_type": "Pod", "namespace": "default", "limit": 5}
        )
        print(f"Found {result['event_count']} events")
        for event in result["events"][:3]:
            print(f"  - {event['type']}: {event['reason']} - {event['message']}")


if __name__ == "__main__":
    asyncio.run(main())
