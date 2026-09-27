"""CONCEPT: agent as an MCP client.
Instead of importing the tools directly, the agent starts the MCP server and discovers its
tools through the protocol. Same agent, tools from anywhere.
  uv run python -m energy_agent.mcp_client "How many hours had negative prices?\""""
import asyncio
import os
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient

from energy_agent.agent import build_agent
from energy_agent.config import RECURSION_LIMIT

# The server runs as a child process; pass our environment (API keys, settings) to it.
SERVERS = {"energy": {"command": sys.executable, "args": ["-m", "energy_agent.mcp_server"],
                      "transport": "stdio", "env": dict(os.environ)}}


async def get_mcp_tools():
    return await MultiServerMCPClient(SERVERS).get_tools()


async def main_async(question: str) -> None:
    tools = await get_mcp_tools()
    print("Tools discovered via MCP:", [t.name for t in tools])
    agent = build_agent(tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]},
                                 config={"recursion_limit": RECURSION_LIMIT})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main_async(" ".join(sys.argv[1:]) or "Describe the data."))
