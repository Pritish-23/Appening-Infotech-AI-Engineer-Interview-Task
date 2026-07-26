"""
Ingestion pipeline:
  1. Download/Load the Agentic AI eBook PDF
  2. Extract and split text into overlapping chunks
  3. Embed each chunk using the embedding model
  4. Store embeddings + text + metadata in the vector DB

Run:
    python -m app.ingest
"""

import os
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config
from app.embeddings import get_embedding_model
from app.vectorstore import get_vectorstore


def download_pdf():
    if os.path.exists(config.PDF_LOCAL_PATH):

        print(f"[ingest] PDF already present at {config.PDF_LOCAL_PATH}, skipping download.")
        return config.PDF_LOCAL_PATH

    os.makedirs(os.path.dirname(config.PDF_LOCAL_PATH), exist_ok=True)

    print(f"[ingest] Downloading PDF from {config.PDF_URL} ...")

    response = requests.get(config.PDF_URL, timeout=30)
    response.raise_for_status()

    with open(config.PDF_LOCAL_PATH, "wb") as f:
        f.write(response.content)

    print(f"[ingest] Saved to {config.PDF_LOCAL_PATH}")
    return config.PDF_LOCAL_PATH


def load_and_chunk(pdf_path):
    print("[ingest] Loading PDF pages ...")

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    print(f"[ingest] Loaded {len(pages)} pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["source"] = "Agentic AI eBook"

    print(f"[ingest] Split into {len(chunks)} chunks ",
          f"(chunk_size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP}).")
    
    return chunks


def embed_and_store(chunks):
    print(f"[ingest] Loading embedding model: {config.EMBEDDING_MODEL} ...")
    embeddings = get_embedding_model()

    print(f"[ingest] Connecting to vector DB backend: {config.VECTOR_DB} ...")
    store = get_vectorstore(embeddings)

    print(f"[ingest] Ingesting {len(chunks)} chunks into the vector DB ...")
    store.add_documents(chunks)

    # if config.VECTOR_DB == "chroma":
    #     store.persist()

    print("[ingest] Done. Vector DB is now ready for retrieval.")


def run():
    config.validate()
    pdf_path = download_pdf()
    chunks = load_and_chunk(pdf_path)
    embed_and_store(chunks)


if __name__ == "__main__":
    run()