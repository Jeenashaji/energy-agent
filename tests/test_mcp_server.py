import asyncio

from energy_agent.mcp_server import create_server


def test_mcp_server_exposes_three_tools(toolbox):
    tools = asyncio.run(create_server(toolbox).list_tools())
    assert {t.name for t in tools} == {"describe_data", "run_sql", "search_docs"}
