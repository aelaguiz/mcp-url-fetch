"""Utility functions for URL Fetch MCP."""

import json
from typing import Any, Dict, Optional
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Check if a URL is valid.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def format_json(data: Any) -> str:
    """Format JSON data with nice indentation.
    
    Args:
        data: JSON-serializable data
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=2, sort_keys=True)


def safe_get_content_type(headers: Dict[str, str]) -> str:
    """Safely extract content type from headers.
    
    Args:
        headers: Response headers
        
    Returns:
        Content type or default value
    """
    content_type = headers.get("content-type", "")
    if ";" in content_type:
        # Strip charset and other parameters
        content_type = content_type.split(";", 1)[0].strip()
    return content_type or "application/octet-stream"


def generate_user_agent() -> str:
    """Generate a user agent string.
    
    Returns:
        User agent string
    """
    return "URL-Fetch-MCP/0.1.0"