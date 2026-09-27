"""CONCEPT: serving the agent as a web API (what you deploy to the cloud).
  uv run uvicorn energy_agent.api:app --reload      then open http://127.0.0.1:8000/docs"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from energy_agent.agent import ask, build_agent, get_checkpointer
from energy_agent.app import build_toolbox

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["agent"] = build_agent(build_toolbox().as_langchain_tools(), checkpointer=get_checkpointer())
    yield


app = FastAPI(title="Energy-market analyst agent", lifespan=lifespan)


class Question(BaseModel):
    question: str
    thread_id: str = "default"


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "agent_ready": "agent" in state}


@app.post("/ask")
def ask_endpoint(q: Question) -> dict:
    return {"answer": ask(state["agent"], q.question, q.thread_id), "thread_id": q.thread_id}
