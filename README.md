# n8n MCP Server

A Model Context Protocol (MCP) server that integrates Cursor with n8n workflow automation. This server enables seamless communication between Cursor's AI capabilities and n8n workflows.

## Prerequisites

- Python 3.12+
- n8n instance running (typically in Docker)
- Cursor IDE
- n8n-nodes-mcp community node installed in n8n

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/n8n-mcp-server.git
   cd n8n-mcp-server
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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
