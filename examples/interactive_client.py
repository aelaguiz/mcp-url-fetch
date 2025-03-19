"""Interactive client for testing URL Fetch MCP."""

import asyncio
import os
import sys
import json
import logging
from typing import Any, Dict, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import mcp.types as types

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def display_content(content: List[Any]) -> None:
    """Display different types of content."""
    for item in content:
        if isinstance(item, types.TextContent) or getattr(item, 'type', None) == 'text':
            print(f"\n--- Text Content ---\n{item.text}\n")
        elif isinstance(item, types.ImageContent) or getattr(item, 'type', None) == 'image':
            print(f"\n--- Image Content ---")
            print(f"MIME Type: {item.mimeType}")
            print(f"Size: {len(item.blob)} bytes")
            print("(Image data is base64-encoded and not displayed)")
        else:
            print(f"\n--- Unknown Content Type ---\n{item}\n")


async def interactive_session() -> None:
    """Run an interactive session with the URL Fetch MCP server."""
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",  # Executable
        args=["-m", "url_fetch_mcp", "run", "--debug"],  # Server module with run command
        cwd=os.getcwd(),  # Set explicit working directory
        env=os.environ.copy(),  # Use current environment
    )
    
    print("Connecting to URL Fetch MCP server...")
    
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            while True:
                print("\n--- URL Fetch MCP Interactive Client ---")
                print("1. Fetch URL (plain text)")
                print("2. Fetch Image")
                print("3. Fetch JSON")
                print("4. List tool details")
                print("5. Exit")
                
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    url = input("Enter URL to fetch: ").strip()
                    headers_str = input("Enter headers as JSON (or leave empty): ").strip()
                    headers = json.loads(headers_str) if headers_str else None
                    
                    print(f"Fetching {url}...")
                    result = await session.call_tool(
                        "fetch_url", 
                        {"url": url, "headers": headers}
                    )
                    await display_content(result.content)
                
                elif choice == "2":
                    url = input("Enter image URL to fetch: ").strip()
                    print(f"Fetching image from {url}...")
                    result = await session.call_tool(
                        "fetch_image", 
                        {"url": url}
                    )
                    await display_content(result.content)
                
                elif choice == "3":
                    url = input("Enter JSON URL to fetch: ").strip()
                    headers_str = input("Enter headers as JSON (or leave empty): ").strip()
                    headers = json.loads(headers_str) if headers_str else None
                    
                    print(f"Fetching JSON from {url}...")
                    result = await session.call_tool(
                        "fetch_json", 
                        {"url": url, "headers": headers}
                    )
                    await display_content(result.content)
                
                elif choice == "4":
                    for tool in tools:
                        print(f"\n--- {tool.name} ---")
                        print(f"Description: {tool.description}")
                        print(f"Input Schema: {json.dumps(tool.inputSchema, indent=2)}")
                
                elif choice == "5":
                    print("Exiting...")
                    break
                
                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        asyncio.run(interactive_session())
    except KeyboardInterrupt:
        print("\nSession terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)