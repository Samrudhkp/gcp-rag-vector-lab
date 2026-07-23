# RAG Lab — Vertex AI + BigQuery + Gemini

Hands-on course for learning Retrieval-Augmented Generation (RAG) and vector search on Google Cloud project `cursor-rag-lab-sam`.

**Rule:** No Google Cloud commands, API calls, or deployments run without your explicit approval.

## Stack

- Python
- Vertex AI embeddings
- BigQuery vector search
- Gemini
- Google Cloud

## Folder map

| Path | Purpose |
|------|---------|
| `lessons/` | One markdown file per lesson |
| `data/sample_docs/` | Tiny text corpus for RAG practice |
| `sql/` | BigQuery DDL and `VECTOR_SEARCH` queries |
| `src/` | Python modules (embed → ingest → retrieve → generate) |
| `notebooks/` | Optional later; we start with scripts |
| `.env.example` | Config template (no secrets) |

## Lessons

1. Concepts → [`lessons/01_concepts.md`](lessons/01_concepts.md)
2. Auth & project → [`lessons/02_auth_and_project.md`](lessons/02_auth_and_project.md)
3. Vertex embeddings → [`lessons/03_embeddings.md`](lessons/03_embeddings.md)
4. BigQuery vectors → [`lessons/04_bigquery_vectors.md`](lessons/04_bigquery_vectors.md)
5. Ingest → [`lessons/05_ingest.md`](lessons/05_ingest.md)
6. Retrieve → [`lessons/06_retrieve.md`](lessons/06_retrieve.md)
7. Gemini RAG → [`lessons/07_gemini_rag.md`](lessons/07_gemini_rag.md)

## Demo (after setup)

```bash
cd rag-lab
source .venv/bin/activate
pip install -r requirements.txt
python -m src.ingest
python -m src.rag_pipeline "How do I reset my password?"
```

## How we work

1. Read the current lesson.
2. Answer the check questions (or say if something is unclear).
3. Approve the next lesson before any cloud work starts.
