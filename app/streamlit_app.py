"""
Streamlit chat UI for the Agentic AI eBook RAG Chatbot.

To Run:
    python -m streamlit run app/streamlit_app.py
"""


import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.graph import ask
from app import config

if not os.path.exists(config.CHROMA_PERSIST_DIR) or not os.listdir(config.CHROMA_PERSIST_DIR):
    with st.spinner("First-time setup: downloading and indexing the eBook (this may take a minute)..."):
        from app.ingest import run as run_ingest
        run_ingest()

st.set_page_config(page_title="Agentic AI eBook Chatbot", page_icon="🤖", layout="wide")

st.title("Agentic AI eBook — RAG Chatbot")
st.caption(
    f"Answers are strictly grounded in the Agentic AI eBook."
    f"Vector DB: `{config.VECTOR_DB}` · LLM: `{config.LLM_MODEL}`"
)

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask a question about the Agentic AI eBook...")

if question:
    with st.spinner("Retrieving context and generating answer..."):
        try:
            result = ask(question)
            st.session_state.history.append(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        st.write(item["answer"])

        st.markdown(f"**Confidence:** `{item['confidence']:.4f}`")

        with st.expander(f"Retrieved context chunks ({len(item['retrieved_chunks'])})"):
            for i, chunk in enumerate(item["retrieved_chunks"], start=1):
                st.markdown(
                    f"**Chunk {i}** — similarity: `{chunk['similarity']:.4f}` "
                    f"· page: `{chunk.get('page')}`"
                )
                st.text(chunk["text"])
                st.divider()