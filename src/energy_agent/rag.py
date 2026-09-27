"""CONCEPT: RAG (retrieval-augmented generation).
1. load documents  2. split into chunks  3. embed each chunk as a vector
4. store vectors   5. at question time, return the chunks closest to the question.
The agent reads those chunks instead of relying on what the LLM remembers."""
from pathlib import Path

from langchain.embeddings import init_embeddings
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from energy_agent.config import EMBEDDING_MODEL


def get_embeddings():
    if EMBEDDING_MODEL == "fake":            # used by tests and CI: no API key, no cost
        return DeterministicFakeEmbedding(size=256)
    return init_embeddings(EMBEDDING_MODEL)


def load_documents(folder: Path) -> list[Document]:
    return [Document(page_content=p.read_text(encoding="utf-8"), metadata={"source": p.name})
            for p in sorted(folder.glob("*.md"))]


def build_vector_store(folder: Path) -> InMemoryVectorStore:
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(load_documents(folder))
    store = InMemoryVectorStore(get_embeddings())
    store.add_documents(chunks)
    return store
