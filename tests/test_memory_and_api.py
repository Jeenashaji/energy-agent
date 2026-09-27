from fastapi.testclient import TestClient

from energy_agent.agent import get_checkpointer
from energy_agent.api import app


def test_checkpointer_creates_database(tmp_path):
    get_checkpointer(tmp_path / "memory.sqlite")
    assert (tmp_path / "memory.sqlite").exists()


def test_health_endpoint():
    assert TestClient(app).get("/health").json()["status"] == "ok"
