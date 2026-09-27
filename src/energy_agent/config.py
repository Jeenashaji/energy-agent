"""CONCEPT: configuration.
All settings live here. Secrets come from the .env file, never from the code."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "prices.csv"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
MEMORY_DB = PROJECT_ROOT / "data" / "memory.sqlite"

MODEL = os.getenv("MODEL", "google_genai:gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google_genai:gemini-embedding-001")  # "fake" = offline tests

MAX_ROWS = 50          # guardrail: max rows sent back to the model per query
RECURSION_LIMIT = 12   # guardrail: max agent steps per question (stops loops)
TOP_K_DOCS = 3         # how many document chunks RAG returns
