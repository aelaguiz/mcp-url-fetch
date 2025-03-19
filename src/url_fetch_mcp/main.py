"""Main module for the URL Fetch MCP server."""

import base64
import json
from typing import Annotated, Dict, Optional, Union, Any

import click
import httpx
from pydantic import AnyUrl, Field
from mcp.server.fastmcp import FastMCP, Context

# Create the MCP server with version information
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
    """Fetch content from a URL and return it as text.
    
    This tool allows Claude to retrieve content from any accessible web URL.
    The content is returned as text, making it suitable for HTML, plain text,
    and other text-based content types.
    """
    if ctx:
        await ctx.info(f"Fetching content from URL: {url}")
    
    request_headers = {
        "User-Agent": "URL-Fetch-MCP/0.1.0",
    }
    
    if headers:
        request_headers.update(headers)
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        try:
            response = await client.get(str(url), headers=request_headers)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "text/plain")
            
            if ctx:
                await ctx.info(f"Successfully fetched content ({len(response.text)} bytes, type: {content_type})")
            
            return response.text
        
        except Exception as e:
            error_message = f"Error fetching URL {url}: {str(e)}"
            if ctx:
                await ctx.error(error_message)
            return error_message


@app.tool()
async def fetch_image(
    url: Annotated[AnyUrl, Field(description="The URL to fetch the image from")],
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> Union[str, Dict[str, Any]]:
    """Fetch an image from a URL and return it as an image.
    
    This tool allows Claude to retrieve images from any accessible web URL.
    The image is returned in a format that Claude can display.
    """
    if ctx:
        await ctx.info(f"Fetching image from URL: {url}")
    
    request_headers = {
        "User-Agent": "URL-Fetch-MCP/0.1.0",
    }
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        try:
            response = await client.get(str(url), headers=request_headers)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            
            if not content_type.startswith("image/"):
                error_message = f"URL did not return an image (content-type: {content_type})"
                if ctx:
                    await ctx.error(error_message)
                return error_message
            
            image_data = base64.b64encode(response.content).decode("utf-8")
            
            if ctx:
                await ctx.info(f"Successfully fetched image ({len(response.content)} bytes, type: {content_type})")
            
            # Return image directly - FastMCP handles conversion to MCP types
            return {
                "type": "image",
                "data": image_data,
                "mimeType": content_type
            }
        
        except Exception as e:
            error_message = f"Error fetching image from URL {url}: {str(e)}"
            if ctx:
                await ctx.error(error_message)
            return error_message


@app.tool()
async def fetch_json(
    url: Annotated[AnyUrl, Field(description="The URL to fetch JSON from")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    """Fetch JSON from a URL, parse it, and return it formatted.
    
    This tool allows Claude to retrieve and parse JSON data from any accessible web URL.
    The JSON is prettified for better readability.
    """
    if ctx:
        await ctx.info(f"Fetching JSON from URL: {url}")
    
    request_headers = {
        "User-Agent": "URL-Fetch-MCP/0.1.0",
        "Accept": "application/json",
    }
    
    if headers:
        request_headers.update(headers)
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        try:
            response = await client.get(str(url), headers=request_headers)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            
            if "json" not in content_type and not content_type.startswith("application/json"):
                # Try to parse anyway, but warn
                if ctx:
                    await ctx.warning(f"URL did not return JSON content-type (got: {content_type})")
            
            # Parse and format JSON
            try:
                json_data = response.json()
                formatted_json = json.dumps(json_data, indent=2)
                
                if ctx:
                    await ctx.info(f"Successfully fetched and parsed JSON ({len(formatted_json)} bytes)")
                
                return formatted_json
            
            except json.JSONDecodeError as e:
                error_message = f"Failed to parse JSON from response: {str(e)}"
                if ctx:
                    await ctx.error(error_message)
                return error_message
        
        except Exception as e:
            error_message = f"Error fetching JSON from URL {url}: {str(e)}"
            if ctx:
                await ctx.error(error_message)
            return error_message


@click.command(name="url-fetch-mcp")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type (stdio for Claude Code, sse for Claude Desktop)",
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind to for SSE transport",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug logging",
)
def cli(transport: str, port: int, debug: bool) -> None:
    """Run the URL Fetch MCP server.
    
    This server provides tools for fetching content from URLs.
    """
    # Set log level based on debug flag
    import logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)
    
    # Only pass port for SSE transport
    if transport == "sse":
        app.run(transport=transport, port=port)
    else:
        app.run(transport=transport)


# Entry point for direct execution
if __name__ == "__main__":
    cli()