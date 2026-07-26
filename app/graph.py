"""
LangGraph RAG pipeline:
  retrieve chunks -> generate output

- retrieve: embeds the user question and fetches top-k similar chunks from the vector DB
- generate: feeds fetched chunks + question to Gemini, forcing the answer to stay strictly grounded in the retrieved context
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

from app import config
from app.embeddings import get_embedding_model
from app.vectorstore import get_vectorstore


class RAGState(TypedDict):
    question: str
    chunks: List[dict]
    answer: str
    confidence: float


_embeddings = None
_store = None
_llm = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = get_embedding_model()
    return _embeddings


def _get_store():
    global _store
    if _store is None:
        _store = get_vectorstore(_get_embeddings())
    return _store


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0,
        )
    return _llm


def retrieve_node(state: RAGState) -> RAGState:
    store = _get_store()
    results = store.similarity_search_with_score(state["question"], k=config.TOP_K)

    chunks = []
    for doc, score in results:
        chunks.append({
            "text": doc.page_content,
            "chunk_id": doc.metadata.get("chunk_id"),
            "page": doc.metadata.get("page"),
            "distance": float(score),
            "similarity": round(1 - float(score), 4),
        })

    state["chunks"] = chunks
    return state


GROUNDED_PROMPT = """
You are an assistant that answers questions STRICTLY using the provided context from the Agentic AI eBook.

Rules:
- Only use information present in the context below.
- If the answer is not in the context, just say: "I don't have enough information in the eBook to answer that."
- Do not use outside knowledge or make assumptions at all.
- Be concise and clear.

Context:
{context}

Question: {question}

Answer:
"""


def generate_node(state: RAGState) -> RAGState:
    context_text = "\n\n-------\n\n".join(c["text"] for c in state["chunks"])
    prompt = GROUNDED_PROMPT.format(context=context_text, question=state["question"])

    llm = _get_llm()
    response = llm.invoke(prompt)
    state["answer"] = response.content[0]["text"].strip()

    if state["chunks"]:
        state["confidence"] = round(
            sum(c["similarity"] for c in state["chunks"]) / len(state["chunks"]), 4
        )
    else:
        state["confidence"] = 0.0

    return state


def build_graph():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def ask(question: str) -> dict:
    """Convenience/Helper function: run a question through the full RAG graph."""

    config.validate()

    graph = get_graph()
    result = graph.invoke({"question": question, "chunks": [], "answer": "", "confidence": 0.0})

    return {
        "question": question,
        "answer": result["answer"],
        "retrieved_chunks": result["chunks"],
        "confidence": result["confidence"],
    }


if __name__ == "__main__":
    q = input("Ask a question about the Agentic AI eBook: ")

    result = ask(q)

    print("\nAnswer:", result["answer"])
    print("\nConfidence:", result["confidence"])
    print("\nRetrieved chunks:")

    for c in result["retrieved_chunks"]:
        print(f"  - [similarity={c['similarity']:.4f}], {c['text']}")