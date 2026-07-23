# Showcase — what to show in Google Cloud

Use this when presenting that you implemented RAG + a vector database on GCP.

## 1. Project
Open **cursor-rag-lab-sam** in the console. Point out billing + enabled APIs (Vertex AI, BigQuery).

## 2. Vector database (BigQuery)
Open **BigQuery → rag_lab → doc_chunks**.

Show:
- Rows = document chunks (IT/HR/security/expense)
- `embedding` column = 768 floats from Vertex `text-embedding-005`
- This table is the vector store

Optional: mention that BigQuery supports IVF vector indexes at larger scale (≥5000 rows); this lab uses brute-force `VECTOR_SEARCH`, which is correct for a small corpus.

## 3. Live RAG
From the repo:

```bash
python -m src.demo
```

Explain the flow out loud:
1. Question is embedded with the **same** model as the docs
2. BigQuery `VECTOR_SEARCH` finds nearest chunks
3. Gemini answers **only** from those chunks (with citations like [1])

## 4. Proof the run happened
Open **BigQuery → rag_lab → query_log**.
Each demo question writes: question, answer, retrieved chunk ids, distances, models used.
