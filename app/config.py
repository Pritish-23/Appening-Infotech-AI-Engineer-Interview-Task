"""
A Central configuration for the RAG app.
Loads everything from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.1-flash-lite")

VECTOR_DB = os.getenv("VECTOR_DB", "chroma")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db")
CHROMA_COLLECTION_NAME = "agentic_ai_ebook"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

PDF_URL = os.getenv("PDF_URL", "https://konverge.ai/pdf/Ebook-Agentic-AI.pdf")
PDF_LOCAL_PATH = os.getenv("PDF_LOCAL_PATH", "data/Ebook-Agentic-AI.pdf")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 8

def validate():

    if not GOOGLE_API_KEY:
        raise EnvironmentError("Missing required environment variables: GOOGLE_API_KEY")