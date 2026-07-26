"""
Loads sentence-transformers embedding model.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from app import config


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)