"""Tests run offline: fake embeddings, no API key needed."""
import os

os.environ["EMBEDDING_MODEL"] = "fake"

from pathlib import Path  # noqa: E402

import pytest  # noqa: E402

from energy_agent.app import build_toolbox  # noqa: E402
from energy_agent.config import KNOWLEDGE_DIR  # noqa: E402

SAMPLE = Path(__file__).parent / "fixtures" / "sample.csv"


@pytest.fixture
def toolbox():
    return build_toolbox(SAMPLE, KNOWLEDGE_DIR)
