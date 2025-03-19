"""Command line interface for URL Fetch MCP."""

import click
import sys
import os
from pathlib import Path
import tempfile
import json

from . import __version__
from .main import app, cli as app_cli


@click.group()
@click.version_option(__version__)
def cli():
    """URL Fetch MCP - A Claude tool for fetching web content."""
    pass


@cli.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
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
def run(transport, port, debug):
    """Run the URL Fetch MCP server."""
    # Set log level based on debug flag
    import logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)
    
    # Only pass port for SSE transport
    if transport == "sse":
        app.run(transport=transport, port=port)
    else:
        app.run(transport=transport)


@cli.command()
def install_desktop():
    """Install the URL Fetch MCP server in Claude Desktop."""
    try:
        # Check if mcp CLI is installed
        import subprocess
        result = subprocess.run(["mcp", "--version"], capture_output=True, text=True)
        click.echo(f"Found MCP CLI version: {result.stdout.strip()}")
    except (ImportError, FileNotFoundError):
        click.echo("Error: mcp CLI not found. Please install it with 'pip install \"mcp[cli]\"'")
        sys.exit(1)
    
    click.echo("Installing URL Fetch MCP in Claude Desktop...")
    
    # Create a temporary Python file that imports our module
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "url_fetcher.py")
    
    with open(temp_file, "w") as f:
        f.write("""
# URL Fetcher MCP Server
from url_fetch_mcp.main import app

if __name__ == "__main__":
    app.run()
""")
    
    # Run the mcp install command with the file path
    try:
        cmd = ["mcp", "install", temp_file, "-n", "URL Fetcher"]
        click.echo(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, text=True)
        click.echo("Installation successful!")
        click.echo("You can now use the URL Fetcher tool in Claude Desktop.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during installation: {str(e)}")
        click.echo("\nAlternative installation method:")
        click.echo("1. Create a Python file that imports url_fetch_mcp.main.app")
        click.echo("2. Run: mcp install your_file.py -n \"URL Fetcher\"")
        sys.exit(1)
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file)
            os.rmdir(temp_dir)
        except:
            pass


if __name__ == "__main__":
    cli()