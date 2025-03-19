"""HTTP fetching utilities for URL Fetch MCP."""

import base64
from typing import Dict, Tuple, Optional, Union, Any

import httpx


async def fetch_content(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> Tuple[int, Dict[str, str], bytes]:
    """Fetch content from a URL and return status code, headers, and content.
    
    Args:
        url: The URL to fetch
        headers: Additional headers to send with the request
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (status_code, headers_dict, content_bytes)
        
    Raises:
        httpx.HTTPError: If an HTTP error occurs
        Exception: For any other error
    """
    request_headers = {
        "User-Agent": "URL-Fetch-MCP/0.1.0",
    }
    
    if headers:
        request_headers.update(headers)
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()
        
        return (
            response.status_code,
            dict(response.headers),
            response.content
        )


def encode_image(image_bytes: bytes) -> str:
    """Encode image bytes as base64 string.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Base64 encoded string
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def create_image_content(image_bytes: bytes, mime_type: str) -> Dict[str, Any]:
    """Create an image content object for MCP.
    
    Args:
        image_bytes: Raw image bytes
        mime_type: MIME type of the image
        
    Returns:
        Dictionary with image content
    """
    return {
        "type": "image",
        "data": encode_image(image_bytes),
        "mimeType": mime_type
    }


def is_probably_binary(content_type: str) -> bool:
    """Determine if a content type is likely binary.
    
    Args:
        content_type: MIME type to check
        
    Returns:
        True if the content is likely binary, False otherwise
    """
    binary_types = [
        "image/",
        "audio/",
        "video/",
        "application/octet-stream",
        "application/pdf",
        "application/zip",
        "application/gzip",
    ]
    
    return any(content_type.startswith(prefix) for prefix in binary_types)