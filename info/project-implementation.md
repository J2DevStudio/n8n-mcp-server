# Revised Implementation Plan: Connecting Cursor to n8n via MCP Server

Based on your specific setup with n8n running in Docker and the MCP endpoints configured, here's a revised step-by-step guide to implement your MCP server.

## Prerequisites

- macOS (your current system)
- Python 3.12+ (you have 3.12.9)
- n8n running in Docker container (accessible at http://localhost:5678)
- n8n-nodes-mcp community node installed
- n8n MCP Client SSE API configured at http://localhost:3002/sse
- n8n messages endpoint at http://localhost:3002/messages

## Step 1: Set Up Python Environment

First, let's create a proper virtual environment and install dependencies:

```bash
# Create a project directory if you haven't already
mkdir -p n8n-mcp-server
cd n8n-mcp-server

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install required packages
pip install mcp requests httpx
```

## Step 2: Create the MCP Server Implementation

Create a new file `server.py` with the following content:

```python
import json
import logging
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("n8n-mcp-bridge")

# n8n MCP endpoints (based on your configuration)
N8N_SSE_ENDPOINT = "http://localhost:3002/sse"
N8N_MESSAGES_ENDPOINT = "http://localhost:3002/messages"

# Initialize the MCP server
mcp = FastMCP("n8nMCPBridge")

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
                "http://localhost:5678/api/v1/workflows",
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
                f"http://localhost:5678/api/v1/workflows/{workflow_id}/execute",
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
                f"http://localhost:5678/api/v1/workflows/{workflow_id}/execute",
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

# Run the server when executed directly
if __name__ == "__main__":
    logger.info("Starting n8n MCP Bridge server...")
    logger.info(f"n8n SSE endpoint: {N8N_SSE_ENDPOINT}")
    logger.info(f"n8n Messages endpoint: {N8N_MESSAGES_ENDPOINT}")
    mcp.run(host="0.0.0.0", port=8000)
```

## Step 3: Configure Cursor to Connect to Your MCP Server

Create or update the `mcp.json` file in the Cursor application support directory:

```bash
# Path to mcp.json file
cd ~/Library/Application\ Support/com.cursor.app/
```

Add the following content to the `mcp.json` file:

```json
[
  {
    "name": "n8n Integration",
    "type": "sse",
    "url": "http://localhost:8000"
  }
]
```

## Step 4: Start the MCP Server

Run the server with the virtual environment activated:

```bash
# Ensure you're in the project directory with the venv activated
cd n8n-mcp-server
source venv/bin/activate

# Run the server
python server.py
```

## Step 5: Test the Integration

1. Ensure your n8n Docker container is running
2. Verify that your MCP server is running
3. Restart Cursor to apply the new MCP configuration
4. In Cursor, test one of the available tools such as `list_n8n_workflows`

## Advanced Implementation (Optional)

### Adding SSE Communication with n8n

To implement full bidirectional communication via SSE, you can enhance the server with:

```python
import json
import httpx
import asyncio
import logging
from mcp.server.fastmcp import FastMCP, Context
from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI, Request
from starlette.routing import Mount

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("n8n-mcp-bridge")

# n8n MCP endpoints
N8N_SSE_ENDPOINT = "http://localhost:3002/sse"
N8N_MESSAGES_ENDPOINT = "http://localhost:3002/messages"

# Initialize the MCP server
mcp = FastMCP("n8nMCPBridge")

# Create FastAPI app for additional endpoints
app = FastAPI()

# Forward SSE events from n8n to our clients
@app.get("/forward-sse")
async def forward_sse(request: Request):
    async def event_generator():
        client = httpx.AsyncClient()
        try:
            async with client.stream("GET", N8N_SSE_ENDPOINT) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        yield {"data": data}
        except Exception as e:
            logger.error(f"SSE connection error: {str(e)}")
            yield {"data": f"Error: {str(e)}"}
        finally:
            await client.aclose()

    return EventSourceResponse(event_generator())

# Mount our FastAPI app to the MCP server
app.mount("/", mcp.sse_app())

# Define MCP tools as in the basic implementation
# [Include all the tool definitions from above]

# Run the combined server
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting enhanced n8n MCP Bridge server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Troubleshooting

### Server Won't Start

- Make sure the virtual environment is activated (`source venv/bin/activate`)
- Verify all dependencies are installed (`pip install mcp requests httpx`)
- Check if port 8000 is already in use (`lsof -i :8000`)

### Connection Issues

- Verify n8n Docker container is running (`docker ps`)
- Check if the n8n MCP Client SSE API endpoint is accessible
- Make sure Cursor has been restarted after updating the `mcp.json` file

### Protocol Changes

- If you encounter MCP protocol compatibility issues, update to the latest mcp package:
  ```bash
  pip install --upgrade mcp
  ```
- Review the updated specification at https://spec.modelcontextprotocol.io/specification/2025-03-26/

## Resources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/specification/2025-03-26/)
- [n8n API Documentation](https://docs.n8n.io/api/)
