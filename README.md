# URL Fetch MCP

A clean Model Context Protocol (MCP) implementation that enables Claude or any LLM to fetch content from URLs.

<a href="https://glama.ai/mcp/servers/@aelaguiz/mcp-url-fetch">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@aelaguiz/mcp-url-fetch/badge" alt="URL Fetch MCP server" />
</a>

## Features

- Fetch content from any URL
- Support for multiple content types (HTML, JSON, text, images)
- Control over request parameters (headers, timeout)
- Clean error handling
- Works with both Claude Code and Claude Desktop

## Repository Structure

```
url-fetch-mcp/
├── examples/               # Example scripts and usage demos
├── scripts/                # Helper scripts (installation, etc.)
├── src/
│   └── url_fetch_mcp/      # Main package code
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # Command-line interface
│       ├── fetch.py        # URL fetching utilities
│       ├── main.py         # Core MCP server implementation
│       └── utils.py        # Helper utilities
├── LICENSE
├── pyproject.toml          # Project configuration
├── README.md
└── url_fetcher.py          # Standalone launcher for Claude Desktop
```

## Installation

```bash
# Install from source
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Running the Server

```bash
# Run with stdio transport (for Claude Code)
python -m url_fetch_mcp run

# Run with HTTP+SSE transport (for remote connections)
python -m url_fetch_mcp run --transport sse --port 8000
```

### Installing in Claude Desktop

There are three ways to install in Claude Desktop:

#### Method 1: Direct installation

```bash
# Install the package
pip install -e .

# Install in Claude Desktop using the included script
mcp install url_fetcher.py -n "URL Fetcher"
```

The `url_fetcher.py` file contains:

```python
#!/usr/bin/env python
"""
URL Fetcher MCP Server

This is a standalone script for launching the URL Fetch MCP server.
It's used for installing in Claude Desktop with the command:
    mcp install url_fetcher.py -n "URL Fetcher"
"""

from url_fetch_mcp.main import app

if __name__ == "__main__":
    app.run()
```

#### Method 2: Use the installer script

```bash
# Install the package
pip install -e .

# Run the installer script
python scripts/install_desktop.py
```

The `scripts/install_desktop.py` script:
```python
#!/usr/bin/env python
import os
import sys
import tempfile
import subprocess

def install_desktop():
    """Install URL Fetch MCP in Claude Desktop."""
    print("Installing URL Fetch MCP in Claude Desktop...")
    
    # Create a temporary Python file that imports our module
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "url_fetcher.py")
    
    with open(temp_file, "w") as f:
        f.write("""#!/usr/bin/env python
# URL Fetcher MCP Server
from url_fetch_mcp.main import app

if __name__ == "__main__":
    app.run()
""")
    
    # Make the file executable
    os.chmod(temp_file, 0o755)
    
    # Run the mcp install command with the file path
    try:
        cmd = ["mcp", "install", temp_file, "-n", "URL Fetcher"]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, text=True)
        print("Installation successful!")
        print("You can now use the URL Fetcher tool in Claude Desktop.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {str(e)}")
        return 1
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file)
            os.rmdir(temp_dir)
        except:
            pass

if __name__ == "__main__":
    sys.exit(install_desktop())
```

#### Method 3: Use CLI command

```bash
# Install the package
pip install -e .

# Install using the built-in CLI command
python -m url_fetch_mcp install-desktop
```

## Core Implementation

The main MCP implementation is in `src/url_fetch_mcp/main.py`:

```python
from typing import Annotated, Dict, Optional
import base64
import json
import httpx
from pydantic import AnyUrl, Field
from mcp.server.fastmcp import FastMCP, Context

# Create the MCP server
app = FastMCP(
    name="URL Fetcher",
    version="0.1.0",
    description="A clean MCP implementation for fetching content from URLs",
)

@app.tool()
async def fetch_url(
    url: Annotated[AnyUrl, Field(description="The URL to fetch")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    """Fetch content from a URL and return it as text."""
    # Implementation details...

@app.tool()
async def fetch_image(
    url: Annotated[AnyUrl, Field(description="The URL to fetch the image from")],
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> Dict:
    """Fetch an image from a URL and return it as an image."""
    # Implementation details...

@app.tool()
async def fetch_json(
    url: Annotated[AnyUrl, Field(description="The URL to fetch JSON from")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    """Fetch JSON from a URL, parse it, and return it formatted."""
    # Implementation details...
```

## Tool Capabilities

### fetch_url

Fetches content from a URL and returns it as text.

Parameters:
- `url` (required): The URL to fetch
- `headers` (optional): Additional headers to send with the request
- `timeout` (optional): Request timeout in seconds (default: 10)

### fetch_image

Fetches an image from a URL and returns it as an image.

Parameters:
- `url` (required): The URL to fetch the image from
- `timeout` (optional): Request timeout in seconds (default: 10)

### fetch_json

Fetches JSON from a URL, parses it, and returns it formatted.

Parameters:
- `url` (required): The URL to fetch JSON from
- `headers` (optional): Additional headers to send with the request
- `timeout` (optional): Request timeout in seconds (default: 10)

## Examples

The `examples` directory contains example scripts:

- `quick_test.py`: Quick test of the MCP server
- `simple_usage.py`: Example of using the client API
- `interactive_client.py`: Interactive CLI for testing

```python
# Example of fetching a URL
result = await session.call_tool("fetch_url", {
    "url": "https://example.com"
})

# Example of fetching JSON data
result = await session.call_tool("fetch_json", {
    "url": "https://api.example.com/data",
    "headers": {"Authorization": "Bearer token"}
})

# Example of fetching an image
result = await session.call_tool("fetch_image", {
    "url": "https://example.com/image.jpg"
})
```

## Testing

To test basic functionality:

```bash
# Run a direct test of URL fetching
python direct_test.py

# Run a simplified test with the MCP server
python examples/quick_test.py
```

## License

MIT