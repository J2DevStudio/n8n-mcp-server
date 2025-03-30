# n8n MCP Server

A Model Context Protocol (MCP) server that integrates Cursor with n8n workflow automation. This server enables seamless communication between Cursor's AI capabilities and n8n workflows.

## Getting Started

### First Time Setup

```bash
# Clone the repository
git clone https://github.com/J2DevStudio/n8n-mcp-server.git
cd n8n-mcp-server

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Starting the Server

```bash
# Navigate to project directory (if not already there)
cd /path/to/n8n-mcp-server

# Activate the virtual environment
source venv/bin/activate

# Start the server
python server.py
```

The server will be available at:

- Main endpoint: http://127.0.0.1:3002
- SSE endpoint: http://127.0.0.1:3002/sse
- Messages endpoint: http://127.0.0.1:3002/messages

### Development Setup

When working in Cursor:

1. Open the project in Cursor
2. Select the correct Python interpreter:
   - Press `Cmd + Shift + P`
   - Type "Python: Select Interpreter"
   - Choose the interpreter from the `venv` folder

## Prerequisites

- Python 3.12+
- n8n instance running (typically in Docker)
- Cursor IDE
- n8n-nodes-mcp community node installed in n8n

## Configuration

1. Ensure your n8n instance is running and accessible
2. Configure the Cursor MCP settings in:
   ```
   ~/Library/Application Support/com.cursor.app/mcp.json
   ```
   Add:
   ```json
   {
     "n8n-mcp-server": {
       "url": "http://127.0.0.1:3002/sse",
       "description": "Local MCP server that integrates with n8n workflow automation"
     }
   }
   ```

## Usage

1. Start the server:

   ```bash
   python server.py
   ```

2. The server will start on http://127.0.0.1:3002

3. Restart Cursor to connect to the MCP server

## Features

- [x] Basic MCP server implementation
- [x] SSE endpoint for Cursor connection
- [ ] n8n workflow listing
- [ ] Workflow triggering
- [ ] Workflow status checking
- [ ] Message passing to n8n

## Development

This project uses:

- FastAPI for the web framework
- MCP SDK for Cursor integration
- httpx for async HTTP requests

## License

MIT

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
