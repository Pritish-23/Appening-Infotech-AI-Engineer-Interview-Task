# Agentic AI eBook — RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **strictly grounded** in the
[Agentic AI eBook](https://konverge.ai/pdf/Ebook-Agentic-AI.pdf), built with **LangGraph**, **ChromaDB**,
local sentence-transformer embeddings, and **Google Gemini**.

Built as part of the AI Engineer Intern interview task for Appening Infotech.

---

## Architecture

```
PDF (Agentic AI eBook)
│
▼
[ingest.py] → download → split into chunks → embed (local, free) → store in ChromaDB
│
▼
ChromaDB (persisted locally, cosine similarity)
│
▼
[LangGraph pipeline: graph.py]
START → retrieve (top-k similarity search)
→ generate (Gemini, prompt-constrained to context only)
→ END
│
▼
Exposed via:
• FastAPI (app/main.py) → POST /chat
• Streamlit UI (app/streamlit_app.py) → chat interface
```

**Why these choices:**
- **ChromaDB** — local, free, no signup, persists to disk.
- **sentence-transformers (`all-MiniLM-L6-v2`)** — free, local embeddings, no API cost/key needed.
- **Gemini (`gemini-3.1-flash-lite`)** — free-tier LLM for generation.
- **LangGraph** — explicit `retrieve → generate` state graph, easy to extend later.
- **Confidence score** — cosine similarity of retrieved chunks, averaged (`1 - cosine_distance`), giving a 0–1 interpretable score per answer.

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/Pritish-23/Appening-Infotech-AI-Engineer-Interview-Task.git

cd rag-app

pip install -r requirements.txt
```

### 2. Configure environment variables
```bash

cp .env.example .env

```
Edit `.env` and add your free Gemini API key (you can get one for free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)):

GOOGLE_API_KEY=your_key_here

### 3. Ingest the eBook (one-time)
```bash

python -m app.ingest

```
This downloads the PDF, chunks it, embeds it, and stores it in a local ChromaDB at `data/chroma_db/`.

### 4. Run it — pick any one (or both)

**Option A: Streamlit chat UI**

```bash

python -m streamlit run app/streamlit_app.py

```
Opens up at `http://localhost:8501` with a full chat interface, showing the answer, confidence score, and expandable retrieved chunks.

**Option B: FastAPI**

```bash

python -m uvicorn app.main:app --reload

```

Visit `http://127.0.0.1:8000/docs` for interactive API docs.

---

## Sample Queries

See [`sample_queries.md`](./sample_queries.md) for 5–6 example questions and their answers.

---

## Project Structure

```
rag-app/
├── app/
│ ├── init.py
│ ├── config.py # env/config loading
│ ├── embeddings.py # local embedding model loader
│ ├── vectorstore.py # Chroma/Pinecone abstraction
│ ├── ingest.py # PDF -> chunks -> embeddings -> vector DB
│ ├── graph.py # LangGraph retrieve -> generate pipeline
│ ├── main.py # FastAPI chat API
│ └── streamlit_app.py # Streamlit chat UI
├── data/ # downloaded PDF + persisted ChromaDB (gitignored)
├── requirements.txt
├── .env.example
├── sample_queries.md
└── README.md
```

---

## Notes on grounding

The generation prompt explicitly instructs Gemini to answer **only** from retrieved context/chunks, and say
*"I don't have enough information in the eBook to answer that"* when the context doesn't cover the question asked by the user.
This, combined with returning the raw retrieved chunks in every response, lets a user verify every answer against the source material directly.