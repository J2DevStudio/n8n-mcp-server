# In Python, imports are like 'require' or 'import' in JavaScript
import json  # Similar to JSON in JavaScript
import logging  # Like console.log but more powerful
import httpx  # Like fetch API in JavaScript
import uvicorn  # Like the HTTP server in Node.js
from fastapi import FastAPI  # Like Express in Node.js
from mcp.server.fastmcp import FastMCP  # Our MCP server
from starlette.routing import Mount  # For mounting our MCP app

# Configure logging (similar to setting up a logger in Node.js)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("n8n-mcp-bridge")

# Constants (like const in JavaScript)
SERVER_HOST = "127.0.0.1"  # Same as localhost
SERVER_PORT = 3002
N8N_SSE_ENDPOINT = f"http://{SERVER_HOST}:{SERVER_PORT}/sse"
N8N_MESSAGES_ENDPOINT = f"http://{SERVER_HOST}:{SERVER_PORT}/messages"

# Create the MCP server (similar to creating an Express app)
mcp = FastMCP("n8nMCPBridge")

# Create a FastAPI app (this is like creating an Express app)
app = FastAPI(title="n8n MCP Bridge")

# This decorator @mcp.tool() is similar to app.get() in Express
@mcp.tool()
async def hello_world() -> str:  # async/await works just like in JavaScript
    """
    A simple test function.
    Python docstrings (these comments) are like JSDoc comments.
    """
    try:
        return "Hello from n8n MCP Bridge!"
    except Exception as e:
        logger.error(f"Error in hello_world: {str(e)}")
        return f"Error: {str(e)}"

# Mount our MCP server to the FastAPI app (similar to app.use() in Express)
app.mount("/", mcp.sse_app())

# Run the server (similar to app.listen() in Express)
if __name__ == "__main__":  # This is like checking if this is the main module
    try:
        logger.info("Starting n8n MCP Bridge server...")
        logger.info(f"Server will be available at http://{SERVER_HOST}:{SERVER_PORT}")
        logger.info(f"n8n SSE endpoint: {N8N_SSE_ENDPOINT}")
        logger.info(f"n8n Messages endpoint: {N8N_MESSAGES_ENDPOINT}")
        
        # This is similar to app.listen(3002, '127.0.0.1') in Express
        uvicorn.run(
            app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
