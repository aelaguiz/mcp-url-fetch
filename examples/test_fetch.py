#!/usr/bin/env python
"""Simple test script for URL Fetch MCP."""

import argparse
import logging
import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_url_fetch(url="https://example.com"):
    """Test the URL Fetch MCP by fetching a URL."""
    logger.info(f"Testing URL Fetch MCP with URL: {url}")
    
    # Start the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "url_fetch_mcp", "run", "--debug"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=os.environ.copy(),
    )
    
    try:
        logger.info("Connecting to URL Fetch MCP server...")
        async with stdio_client(server_params) as (read, write):
            logger.info("Connected to server")
            
            # Create client session
            async with ClientSession(read, write) as session:
                # Initialize session
                logger.info("Initializing session...")
                await session.initialize()
                logger.info("Session initialized")
                
                # List available tools
                logger.info("Listing tools...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                tool_names = [tool.name for tool in tools]
                logger.info(f"Available tools: {tool_names}")
                
                if "fetch_url" not in tool_names:
                    logger.error("fetch_url tool not found!")
                    return False
                
                # Fetch URL
                logger.info(f"Fetching URL: {url}")
                result = await session.call_tool("fetch_url", {"url": url})
                
                # Log result
                logger.info(f"Fetch successful!")
                content_text = result.content[0].text[:150] + "..." if len(result.content[0].text) > 150 else result.content[0].text
                logger.info(f"Content (truncated): {content_text}")
                
                return True
                
    except Exception as e:
        logger.exception(f"Error testing URL Fetch MCP: {e}")
        return False

def main():
    """Run the test."""
    parser = argparse.ArgumentParser(description="Test URL Fetch MCP")
    parser.add_argument("--url", default="https://example.com", help="URL to fetch")
    args = parser.parse_args()
    
    success = asyncio.run(test_url_fetch(args.url))
    
    if success:
        logger.info("Test completed successfully!")
        return 0
    else:
        logger.error("Test failed!")
        return 1

if __name__ == "__main__":
    exit(main())