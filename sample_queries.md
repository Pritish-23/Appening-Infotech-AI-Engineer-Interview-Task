# Sample Queries

Below are 6 sample interactions with the RAG chatbot, run against the live system (ChromaDB + local embeddings + Gemini generation).
Each demonstrates a different aspect of the pipeline's behavior.

---

### 1. What is Agentic AI?

**Answer:**
> Agentic AI refers to systems capable of autonomous decision-making and action in pursuit of specific objectives. It represents a shift from reactive to proactive problem-solving, acting as a collaborator that understands goals, anticipates needs, and takes proactive steps to help users succeed.
>
> At its core, Agentic AI functions as:
> - A Chef: Expertly manages every task to create the perfect outcome.
> - A Coach: Continuously adapts strategies and leads the team to success.
> - A Coordinator: Orchestrates complex workflows with precision and harmony.
> - A Project Manager: Drives progress with minimal supervision, ensuring smooth execution.

**Confidence:** `0.7346` · **Retrieved chunks:** 8

---

### 2. How does Agentic AI differ from traditional AI or generative AI?

**Answer:**
> Based on the provided text, the differences are as follows:
> - **Traditional AI**: Focuses on basic automation and rule-based systems, executing predefined rules and logic.
> - **Generative AI**: Focuses on creating new content or solutions, such as generating text, images, or other media.
> - **Agentic AI**: Is defined by its capability for autonomous decision-making. Unlike traditional or non-agentic AI, which lack autonomy and independent action, Agentic AI learns and adapts to new situations.
>
> Additionally, while LLMs (a form of generative AI) are powerful tools for processing and generating text, agents are goal-driven systems capable of performing actions autonomously in a dynamic environment.

**Confidence:** `0.6359` · **Retrieved chunks:** 8

---

### 3. What are the key benefits of implementing Agentic AI in a business?

**Answer:**
> Based on the provided eBook, the key benefits of implementing Agentic AI in a business include:
> - **Employee Productivity**: AI support systems provide employees with 30% more time to focus on high-priority projects.
> - **Improved Customer Service**: 24/7 AI support increases customer satisfaction by 25%.
> - **Smarter Forecasting**: Predictive analytics improve forecasting accuracy by 12%.
> - **Operational Efficiency**: Automated task processing reduces manual work by 40% and operational costs by 15%.
> - **Ultra-Personalization**: Tailored shopping experiences boost conversion rates by 18% and improve loyalty.
> - **General Performance**: Agentic AI can decrease forecasting errors by 50%, reduce excess inventory, improve lead times, and reduce review cycle times by 20–60%.

**Confidence:** `0.7140` · **Retrieved chunks:** 8

---

### 4. What are some challenges or risks associated with Agentic AI?

**Answer:**
> I don't have enough information in the eBook to answer that.

**Confidence:** `0.6532` · **Retrieved chunks:** 8

*It Demonstrates the grounding constraint holding even when retrieved chunks are somewhat related (moderate confidence) but might not actually contain a direct answer to the question. Therefore, the model refuses to answer rather than inferring or using outside knowledge.*

---

### 5. What are the key building blocks of an Agentic AI system?

**Answer:**
> The key building blocks (or components) of an Agentic AI system are:
> - Perception
> - Reasoning
> - Planning
> - Learning
> - Execution

**Confidence:** `0.6937` · **Retrieved chunks:** 8

---

### 6. What is the capital of France? *(out-of-scope test)*

**Answer:**
> I don't have enough information in the eBook to answer that.

**Confidence:** `0.0779` · **Retrieved chunks:** 8

*It Demonstrates that the question is unrelated to the eBook's content. The confidence drop (0.0779) compared to the in-scope refusal above (0.6532), serves as a meaningful signal a reviewer can use to distinguish "somewhat related but unanswered" from "completely out of scope."*

---

## Summary

| # | Query | Confidence | Answered(Yes/No) |
|---|-------|-----------|-----------|
| 1 | What is Agentic AI? | 0.7346 | Yes |
| 2 | Agentic AI vs traditional/generative AI | 0.6359 | Yes |
| 3 | Key business benefits | 0.7140 | Yes |
| 4 | Challenges/risks | 0.6532 | No (correctly refused) |
| 5 | Key building blocks | 0.6937 | Yes |
| 6 | Capital of France (out-of-scope) | 0.0779 | No (correctly refused) |

The confidence score (average cosine similarity of retrieved chunks) tracks reasonably well with answer quality and correctly separates genuinely out-of-scope questions from in-scope-but-unanswerable ones.