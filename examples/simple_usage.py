"""Example of how to use the URL Fetch MCP client API."""

import asyncio
import logging
import sys
import subprocess
import os
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def create_simple_test_file():
    """Create a simple test script to verify the server is working."""
    test_file = "test_server.py"
    content = """
import sys
print("TEST SERVER STARTED")
print("ARGS:", sys.argv)
print("CWD:", os.getcwd())
print("ENV:", dict(os.environ))
print("TEST SERVER READY")
sys.stdout.flush()

while True:
    try:
        line = input()
        print(f"RECEIVED: {line!r}")
        sys.stdout.flush()
        if line == "exit":
            break
    except EOFError:
        print("EOF RECEIVED")
        break
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.stdout.flush()

print("TEST SERVER EXITING")
"""
    with open(test_file, "w") as f:
        f.write(content)
    return test_file

async def test_simple_stdio():
    """Test if basic stdio communication works."""
    test_file = await create_simple_test_file()
    logger.info("Starting basic stdio test...")
    
    proc = subprocess.Popen(
        [sys.executable, test_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    
    # Send some data
    proc.stdin.write("hello\n")
    proc.stdin.flush()
    
    # Read response
    for _ in range(10):  # Read up to 10 lines
        line = proc.stdout.readline().strip()
        logger.info(f"Test server: {line}")
        if "RECEIVED: 'hello'" in line:
            logger.info("Basic stdio test succeeded!")
            break
    
    # Cleanup
    proc.stdin.write("exit\n")
    proc.stdin.flush()
    proc.terminate()
    proc.wait(timeout=5)
    os.unlink(test_file)

async def main():
    """Run the example."""
    # First test basic stdio communication
    await test_simple_stdio()
    
    logger.info("Starting URL Fetch MCP test...")
    
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",  # Executable
        args=["-m", "url_fetch_mcp", "run", "--debug"],  # Server module with run command
        cwd=os.getcwd(),  # Explicitly set working directory
        env=os.environ.copy(),  # Copy current environment
    )
    
    logger.info(f"Starting server with params: {server_params}")
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            logger.info("Connected to server")
            async with ClientSession(read, write) as session:
                # Initialize the connection
                logger.info("Initializing session...")
                init_result = await session.initialize()
                logger.info(f"Initialization result: {init_result}")
                
                # List available tools
                logger.info("Listing tools...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                logger.info(f"Available tools: {[tool.name for tool in tools]}")
                
                # Call fetch_url tool
                logger.info("\nFetching example.com...")
                result = await session.call_tool("fetch_url", {
                    "url": "https://example.com"
                })
                logger.info(f"Result type: {type(result)}")
                logger.info(f"First 150 characters: {result.content[0].text[:150]}...")
                
                # Call fetch_json tool
                logger.info("\nFetching JSON data...")
                result = await session.call_tool("fetch_json", {
                    "url": "https://jsonplaceholder.typicode.com/todos/1"
                })
                logger.info(f"JSON result:\n{result.content[0].text}")
                
                # Call fetch_image tool
                logger.info("\nFetching image...")
                result = await session.call_tool("fetch_image", {
                    "url": "https://picsum.photos/200/300"
                })
                logger.info(f"Image content type: {result.content[0].mimeType}")
                logger.info(f"Image result received: {len(result.content[0].blob)} bytes")
                
                logger.info("Test completed successfully!")
    except Exception as e:
        logger.exception(f"Error during test: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())