# URL Fetch MCP Examples

This directory contains examples demonstrating how to use the URL Fetch MCP server.

## Files

- `simple_usage.py`: Basic example of using the client API to fetch content
- `interactive_client.py`: Interactive CLI for testing the server

## Running the Examples

1. Install the package:
   ```bash
   pip install -e ..
   ```

2. Run the simple example:
   ```bash
   python simple_usage.py
   ```

3. Run the interactive client:
   ```bash
   python interactive_client.py
   ```

## Example Usages

### Fetch a web page:
```python
result = await session.call_tool("fetch_url", {
    "url": "https://example.com"
})
```

### Fetch JSON data:
```python
result = await session.call_tool("fetch_json", {
    "url": "https://jsonplaceholder.typicode.com/todos/1"
})
```

### Fetch an image:
```python
result = await session.call_tool("fetch_image", {
    "url": "https://picsum.photos/200/300"
})
```