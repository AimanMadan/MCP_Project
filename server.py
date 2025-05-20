#mcp_server
from flask import Flask, request, jsonify
import tools

mcp = Flask(__name__)

@mcp.route("/")
def test():
    return "<p>MCP Server Vroom Vroom 🏎️!</p>"


@mcp.route("/tools/list_files", methods=["POST"])
def list_files_tool():
    
    data = request.get_json() # checks if the HTTP request has any JSON object
    
    if not data or "path" not in data:
        return jsonify({"error": "Missing 'path' in request body"}), 400
    
    relative_path = data["path"]
    result = tools.list_files_implementation(relative_path)
    
    
    # error handling
    if "error" in result:
        error_message = result["error"]
        if "Path not found" in error_message:
            return jsonify(result), 404  # Not Found
        
        elif "Invalid path: '..' sequence not allowed." in error_message:
            return jsonify(result), 400  # Bad Request
        
        elif "Invalid path: Attempt to access outside the base directory." in error_message:
            return jsonify(result), 403  # Forbidden
        
        elif "Path is not a directory" in error_message:
            return jsonify(result), 400  # Bad Request 
        
        elif "An unexpected error occurred" in error_message:
            # log unexpected server errors
            mcp.logger.error(f"Unexpected server error for path '{relative_path}': {error_message}")
            return jsonify(result), 500  # Internal Server Error
        else:
            # An unexpected error
            return jsonify(result), 400  # Bad Request
            
    return jsonify(result), 200


if __name__ == "__main__":
    mcp.run(debug=True)