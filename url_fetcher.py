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