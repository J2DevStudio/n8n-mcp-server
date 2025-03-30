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
N8N_HOST = "localhost"
N8N_PORT = 5678
N8N_BASE_URL = f"http://{N8N_HOST}:{N8N_PORT}/api/v1"
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

@mcp.tool()
async def list_n8n_workflows() -> str:
    """
    Lists available workflows from n8n.

    Returns:
        A formatted list of workflows
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{N8N_BASE_URL}/workflows",
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                workflows = response.json()
                result = "Available n8n Workflows:\n"
                for workflow in workflows:
                    result += f"- ID: {workflow.get('id')}, Name: {workflow.get('name')}\n"
                return result
            else:
                return f"Error listing workflows: {response.status_code} - {response.text}"

        except Exception as e:
            logger.error(f"Error listing workflows: {str(e)}")
            return f"Error: {str(e)}"

@mcp.tool()
async def trigger_n8n_workflow(workflow_id: str, data: str = "{}") -> str:
    """
    Triggers an n8n workflow by its ID.

    Args:
        workflow_id: The ID of the workflow to trigger
        data: Optional JSON string with data to pass to the workflow

    Returns:
        The result of the workflow execution
    """
    try:
        # Parse the data string as JSON
        payload = json.loads(data)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{N8N_BASE_URL}/workflows/{workflow_id}/execute",
                headers={"Content-Type": "application/json"},
                json=payload
            )

            if response.status_code in (200, 201):
                return f"Workflow {workflow_id} triggered successfully"
            else:
                return f"Error triggering workflow: {response.status_code} - {response.text}"

    except json.JSONDecodeError:
        return "Error: Invalid JSON in data parameter"
    except Exception as e:
        logger.error(f"Error triggering workflow: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
async def send_to_n8n_mcp(message: str) -> str:
    """
    Sends a message to the n8n MCP API endpoint.

    Args:
        message: The message to send to n8n

    Returns:
        The response from n8n
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_MESSAGES_ENDPOINT,
                headers={"Content-Type": "application/json"},
                json={"message": message}
            )

            if response.status_code == 200:
                return f"Message sent to n8n: {response.json()}"
            else:
                return f"Error sending message: {response.status_code} - {response.text}"

    except Exception as e:
        logger.error(f"Error sending message to n8n: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
async def analyze_text_with_n8n(text: str, workflow_id: str) -> str:
    """
    Analyzes text using a specific n8n workflow.

    Args:
        text: The text to analyze
        workflow_id: The ID of the workflow to use for analysis

    Returns:
        Analysis results from the workflow
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{N8N_BASE_URL}/workflows/{workflow_id}/execute",
                headers={"Content-Type": "application/json"},
                json={"text": text}
            )

            if response.status_code in (200, 201):
                return f"Analysis complete: {json.dumps(response.json(), indent=2)}"
            else:
                return f"Error analyzing text: {response.status_code} - {response.text}"

    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
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
