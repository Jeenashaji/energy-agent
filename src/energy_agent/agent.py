"""CONCEPT: the agent loop + memory.
create_agent() builds a LangGraph graph: the LLM decides -> a tool runs -> the result goes
back to the LLM -> repeat until it answers.
The checkpointer saves every step to SQLite, so a conversation (thread) can be continued
later, even after the program restarts. That is the basis of long-running agents."""
import logging
import sqlite3

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite import SqliteSaver

from energy_agent.config import MEMORY_DB, MODEL, RECURSION_LIMIT

log = logging.getLogger("energy_agent")

SYSTEM_PROMPT = """You are an energy-market data analyst for the German/Luxembourg bidding zone.
Rules:
- For numbers: call describe_data, then run_sql. Every number you report must come from a SQL result.
- For explanations: call search_docs and base the explanation on what it returns.
- Never invent values. If the data or documents cannot answer, say so.
- Answer in 1-4 sentences. Mention the key number(s) and, if you used documents, the source file."""


def get_checkpointer(path=MEMORY_DB) -> SqliteSaver:
    path.parent.mkdir(parents=True, exist_ok=True)
    return SqliteSaver(sqlite3.connect(path, check_same_thread=False))


def build_agent(tools: list, checkpointer=None):
    return create_agent(init_chat_model(MODEL), tools=tools, system_prompt=SYSTEM_PROMPT,
                        checkpointer=checkpointer)


def ask(agent, question: str, thread_id: str = "default") -> str:
    """Send one question. Same thread_id = the agent remembers the earlier conversation."""
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": RECURSION_LIMIT}
    result = agent.invoke({"messages": [{"role": "user", "content": question}]}, config=config)
    for m in result["messages"][-8:]:                       # log what the agent did (observability)
        for call in getattr(m, "tool_calls", None) or []:
            log.info("tool call: %s(%s)", call["name"], call["args"])
    return result["messages"][-1].text
