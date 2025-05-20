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
        "description": "Lists all the sound packs (files or folders) in a given directory. Use '.' for the root sound pack directory.",
        "parameters": { # This structure describes the 'arguments' object Llama should generate
            "type": "object", # Standard JSON schema: type of the parameters object itself
            "properties": {   # Standard JSON schema: dictionary of named parameters
                "path": { # This key must match what your server expects (FastAPI's Pydantic model)
                    "type": "string",
                    "description": "The relative path to the directory to scan (e.g., '.', 'drums', 'synths/pads')."
                }
            }
        },
        "required": ["path"] # Llama needs to know this field is required within the arguments object
    },
    # Test function
    {
        "name": "Do Not Use",
        "description": "You should avoid this function because it is useless",
    }
]

# Function to format the MCP_TOOLS into a format that LLMs can Understand
def get_MCP_TOOLS():
    desc = (
        "You are a helpful AI assistant that can use tools to interact with a file system for sound packs. "
        "You must respond with a JSON object or a JSON list of objects representing tool calls. "
        "Each tool call object must have a 'tool_name' key and an 'arguments' key. "
        "The 'arguments' key should correspond to an object matching the tool's parameters. "
        "Only use the tools provided below. If you need to call multiple tools, provide a JSON list of tool call objects.\n\n"
        "Available tools:\n"
    )
    for tool in MCP_TOOLS:
        desc += f"- Tool Name: {tool['name']}\n"
        desc += f"  Description: {tool['description']}\n"
        # This condition now correctly processes the updated MCP_TOOLS structure for list_files
        if "parameters" in tool and "properties" in tool["parameters"]:
            desc += f"  Arguments JSON schema: {json.dumps(tool['parameters'])}\n\n" # Pass the whole schema
        elif "parameters" in tool: # Fallback for simpler parameter structures if any (like Do Not Use if it had params)
            desc += f"  Arguments: {json.dumps(tool['parameters'])}\n\n"
        else:
            desc += "\n"
    return desc

# print(get_MCP_TOOLS())

# Function to Execute the tools based on the LLMs response (oh lord have mercy)
def exe_MCP_TOOLS(tool_calls_json: str):

    try:
        actions = json.loads(tool_calls_json) # parse JSON data and convert it into a Python data structure

        if not isinstance(actions, list): # if not a list
            print(f"No list was returned. Response: {actions}")

            # Attempt to wrap if it's a single dictionary action
            if isinstance(actions, dict) and "tool_name" in actions:
                actions = [actions]
            else:
                print("Error: LLM response is not a list of actions or a single valid action dictionary.") 
                return 

    except json.JSONDecodeError:
        print(f"Error decoding LLM response: {tool_calls_json}")
        return

    # Ensure actions is iterable and not None if the above logic somehow allows it
    if not actions:
        print("No valid actions to execute.")
        return

    for action in actions:
        # Additional check for robustness inside the loop
        if not isinstance(action, dict) or "tool_name" not in action:
            print(f"Skipping invalid action structure: {action}")
            continue

        tool_name = action.get("tool_name")
        arguments = action.get("arguments", {})
        print(f"Executing tool: {tool_name} with arguments: {arguments}")

        # Find the MCP tool's endpoint and make the request
        endpoint = f"{mcp_server}/tools/{tool_name}"
        try:
            response = requests.post(endpoint, json=arguments)
            response.raise_for_status() # Raise an exception for HTTP errors
            # Attempt to parse JSON, but provide text if it fails (e.g. server sends plain text on success)
            try:
                print(f"Tool {tool_name} executed: {response.json()}")
            except requests.exceptions.JSONDecodeError:
                print(f"Tool {tool_name} executed. Response (non-JSON): {response.text}")
        except requests.exceptions.HTTPError as http_err: # More specific exception first
            print(f"HTTP error calling tool {tool_name}: {http_err}")
            if http_err.response is not None:
                print(f"Server response: {http_err.response.status_code} - {http_err.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error calling tool {tool_name}: {e}")
            if hasattr(e, 'response') and e.response is not None: # General check for response attribute
                print(f"Server response: {e.response.text}")


def main():
    # get user's request
    user_query = input("What would you like to do with your sound packs?\n> ")

    system_instructions = get_MCP_TOOLS() # This is the detailed explanation of tools and expected format

    # The user query is what the LLM should try to accomplish using the tools
    user_content_for_llm = (
        f"User query: \"{user_query}\"\n\n"
        "Based on the available tools and the user query, provide your response as a JSON object "
        "for a single tool call, or a JSON list of objects for multiple tool calls. "
        "Ensure the JSON is well-formed and only contains the tool calls."
    )


    messages_for_ollama = [
        {
            'role': 'system',
            'content': system_instructions
        },
        {
            'role': 'user',
            'content': user_content_for_llm
        }
    ]

    print("\n--- Contacting Llama 3.2 via Ollama ---")
    try:
        response = ollama.chat(
            model='llama3.2:3b',  # MODEL
            messages=messages_for_ollama,
            format='json',  # Request JSON output format from Ollama
            options={
                "temperature": 0.0,  
            }
        )
        llama_response_content = response['message']['content']
        print(f"\nLlama's proposed actions (raw JSON string from Ollama):\n{llama_response_content}")
        exe_MCP_TOOLS(llama_response_content)

    except Exception as e:
        print(f"\nError during Ollama API call or processing: {e}")
    
        # if ollama library raises its own exceptions for connection errors.
        if hasattr(e, 'response') and e.response is not None: # Check if it's an error with an HTTP response 
            try:
                print(f"Ollama server error details: {e.response.text}")
            except:
                 pass

if __name__ == "__main__":
    main()