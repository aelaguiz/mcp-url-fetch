#!/usr/bin/env python
"""Direct test of URL Fetch MCP functionality."""

import asyncio
import logging
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fetch_url(url, headers=None, timeout=10):
    """Directly test the URL fetching functionality."""
    logger.info(f"Fetching URL: {url}")
    
    request_headers = {
        "User-Agent": "URL-Fetch-MCP/0.1.0",
    }
    
    if headers:
        request_headers.update(headers)
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        try:
            response = await client.get(url, headers=request_headers)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "text/plain")
            logger.info(f"Successfully fetched content ({len(response.text)} bytes, type: {content_type})")
            
            preview = response.text[:150] + "..." if len(response.text) > 150 else response.text
            logger.info(f"Content preview: {preview}")
            
            return response.text
        
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None

async def test_fetch_url():
    """Test URL fetching functionality."""
    # Test example.com
    content = await fetch_url("https://example.com")
    if content and "<title>Example Domain</title>" in content:
        logger.info("Successfully fetched example.com")
    else:
        logger.error("Failed to fetch example.com correctly")
        return False
    
    # Test JSON API
    content = await fetch_url("https://jsonplaceholder.typicode.com/todos/1")
    if content and "userId" in content and "title" in content:
        logger.info("Successfully fetched JSON data")
    else:
        logger.error("Failed to fetch JSON correctly")
        return False
    
    # Test image URL (just check that we get a response)
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get("https://picsum.photos/200/300")
            response.raise_for_status()
            if response.headers.get("content-type", "").startswith("image/"):
                logger.info(f"Successfully fetched image ({len(response.content)} bytes)")
            else:
                logger.error("Received non-image content type")
                return False
    except Exception as e:
        logger.error(f"Error fetching image: {str(e)}")
        return False
    
    return True

async def main():
    """Run the test."""
    logger.info("Testing URL fetching functionality directly...")
    
    success = await test_fetch_url()
    
    if success:
        logger.info("All tests passed!")
        return 0
    else:
        logger.error("Tests failed!")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))