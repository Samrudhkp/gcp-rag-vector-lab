# Lesson 7 — Gemini RAG answer

Pass retrieved chunks to Gemini and answer from that context only.

```bash
python -m src.rag_pipeline "How do I reset my password?"
python -m src.rag_pipeline "How many vacation days do employees get?"
```

Demo flow: retrieve → generate → show citations.
