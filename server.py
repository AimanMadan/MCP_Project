#mcp_server
from flask import Flask 
import tools

mcp = Flask(__name__)

@mcp.route("/")
def test():
    return "<p>MCP Server</p>"


@mcp.post("tools/list_files")
async def list_file