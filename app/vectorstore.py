"""
Vector DB abstraction. Supports:
  - chroma
  - pinecone

Can switch via VECTOR_DB env var.
"""

import os
from app import config


def get_vectorstore(embeddings):
    return _get_chroma_store(embeddings)


def _get_chroma_store(embeddings):
    from langchain_community.vectorstores import Chroma

    os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)

    return Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=config.CHROMA_PERSIST_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )