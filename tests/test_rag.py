from energy_agent.config import KNOWLEDGE_DIR
from energy_agent.rag import build_vector_store, load_documents


def test_knowledge_documents_load():
    assert len(load_documents(KNOWLEDGE_DIR)) >= 3


def test_search_returns_chunks_with_source(toolbox):
    out = toolbox.search_docs("Why are prices negative?")
    assert out.startswith("[") and ".md]" in out


def test_vector_store_has_chunks():
    store = build_vector_store(KNOWLEDGE_DIR)
    assert len(store.store) >= 3
