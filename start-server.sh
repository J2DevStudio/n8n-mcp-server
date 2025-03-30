#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Unalias python if it exists (to avoid conflicts)
unalias python 2>/dev/null

# Start the server using the virtual environment's Python
./venv/bin/python server.py 