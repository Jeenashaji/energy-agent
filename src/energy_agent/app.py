"""Wires everything together once, so the CLI, API and MCP server share the same setup."""
from energy_agent.config import DATA_FILE, KNOWLEDGE_DIR
from energy_agent.data import load_smard_csv, make_database
from energy_agent.rag import build_vector_store
from energy_agent.tools import Toolbox


def build_toolbox(data_file=DATA_FILE, knowledge_dir=KNOWLEDGE_DIR) -> Toolbox:
    if not data_file.exists():
        raise SystemExit(f"Data file not found: {data_file}\nSee data/README.md for how to download it.")
    df = load_smard_csv(data_file)
    return Toolbox(df, make_database(df), build_vector_store(knowledge_dir))
