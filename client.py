#mcp_client 
import ollama
import requests
import json 

# MCP server URL
mcp_server = "http://127.0.0.1:5000" # Update based on your server's URL

# Tools thats the LLM will have access too 
MCP_TOOLS = [
    {
        "name": "list_files",
        "description": "Lists all the sound packs (files or folders) in a given directory.",
        "parameters": {
            "path": {"type": "string", "description": "The relative path to the directory to scan." }
        },
        "required": ["path"]
        
    }
]

# Function to format the MCP_TOOLS into a format that LLMs can Understand 
def get_MCP_TOOLS_description():
    desc = "You have access to the tools listed below. Respond with a JSON list of tool calls to achieve the user's goal. Each tool call should be an object with 'tool_name' and 'arguments' (an object of key-value pairs).\n\n"




