"""
FastAPI wrapper around the LangGraph RAG pipeline.

To Run:
   python -m uvicorn app.main:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.graph import ask
from app import config

app = FastAPI(
    title="Agentic AI eBook RAG Chatbot",
    description="A RAG chatbot answering questions strictly grounded in the Agentic AI eBook, "
                "built with LangGraph, ChromaDB, and Google Gemini.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str


class RetrievedChunk(BaseModel):
    text: str
    chunk_id: Optional[int] = None
    page: Optional[int] = None
    distance: float
    similarity: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: List[RetrievedChunk]
    confidence: float


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Agentic AI eBook RAG Chatbot is running. POST to /chat with a 'question' field.",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "vector_db": config.VECTOR_DB, "llm_model": config.LLM_MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    try:
        result = ask(request.question)
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    return ChatResponse(**result)