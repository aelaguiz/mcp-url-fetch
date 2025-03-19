#!/usr/bin/env python
"""
Install URL Fetch MCP in Claude Desktop.

This script creates a standalone Python file that imports the URL Fetch MCP app
and then installs it in Claude Desktop using the mcp CLI.
"""

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
        print("\nAlternative installation method:")
        print("1. Create a Python file (url_fetcher.py) with the following content:")
        print("""
from url_fetch_mcp.main import app

if __name__ == "__main__":
    app.run()
""")
        print("2. Run: mcp install url_fetcher.py -n \"URL Fetcher\"")
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