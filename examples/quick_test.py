#!/usr/bin/env python
"""Quick test for URL Fetch MCP."""

import asyncio
import os
import logging
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    """Run a quick test of the URL Fetch MCP server."""
    print("Testing URL Fetch MCP...")
    
    # Start the MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "url_fetch_mcp", "run"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    
    try:
        # Connect to the server with a timeout
        async with asyncio.timeout(10):  # 10 second timeout
            async with stdio_client(server_params) as (read, write):
                print("Connected to server")
                
                # Create client session
                async with ClientSession(read, write) as session:
                    # Initialize session
                    print("Initializing session...")
                    await session.initialize()
                    print("Session initialized")
                    
                    # List available tools
                    print("Listing tools...")
                    tools_result = await session.list_tools()
                    tool_names = [tool.name for tool in tools_result.tools]
                    print(f"Available tools: {tool_names}")
                    
                    # Fetch a URL with a short timeout
                    print("Fetching URL...")
                    result = await session.call_tool("fetch_url", {
                        "url": "https://example.com",
                        "timeout": 5
                    })
                    
                    # Print result
                    print("Fetch successful!")
                    content = result.content[0].text[:100] + "..." if len(result.content[0].text) > 100 else result.content[0].text
                    print(f"Content preview: {content}")
                    
                    print("Test passed!")
                    return 0
    
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds!")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))