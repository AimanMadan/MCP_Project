#mcp_client 
# import ollama
import requests
import json 

# MCP server URL
mcp_server = "http://127.0.0.1:5000"

MCP_TOOLS = [
    {
        "name": "list_files",
        "description": "Lists all the sound packs (files or folders) in a given directory.",
        
        
    }
]



