"""CONCEPT: MCP (Model Context Protocol).
MCP is a standard way to offer tools to ANY AI application (Claude Desktop, IDEs, other
agents). This file exposes the same three tools as an MCP server over stdio.
  uv run energy-agent-mcp"""
from mcp.server.fastmcp import FastMCP

from energy_agent.app import build_toolbox


def create_server(toolbox=None) -> FastMCP:
    toolbox = toolbox or build_toolbox()
    server = FastMCP("energy-market-data")
    for fn in (toolbox.describe_data, toolbox.run_sql, toolbox.search_docs):
        server.add_tool(fn)
    return server


def main() -> None:
    create_server().run()   # stdio transport


if __name__ == "__main__":
    main()
