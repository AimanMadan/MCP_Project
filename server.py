#mcp_server
from flask import Flask 
import tools

mcp = Flask(__name__)

@mcp.route("/")
def test():
    return "<p>MCP Server</p>"