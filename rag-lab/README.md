# RAG Lab — Vertex AI + BigQuery + Gemini

Working RAG + vector search on Google Cloud project **`cursor-rag-lab-sam`**.

## What this project demonstrates

```text
Sample docs  →  chunk + Vertex embed  →  BigQuery doc_chunks (vectors)
                                              │
User question → same embed model → VECTOR_SEARCH (top-k, cosine)
                                              │
                         Gemini answers using only retrieved chunks
                                              │
                                   query_log stores each demo run
```

| Cloud resource | Purpose |
|----------------|---------|
| Project `cursor-rag-lab-sam` | All lab resources |
| API: Vertex AI | Embeddings + Gemini |
| API: BigQuery | Vector store + search |
| Dataset `rag_lab` | Lab dataset |
| Table `doc_chunks` | Chunk text + 768-dim embeddings |
| Table `query_log` | Logged Q&A for demos |
| Vector index | Optional at ≥5000 rows; lab uses `VECTOR_SEARCH` directly |

## Folder map

| Path | Purpose |
|------|---------|
| `lessons/` | Tutor write-ups |
| `data/sample_docs/` | IT, HR, security, expense policies |
| `sql/` | Dataset / table / index DDL |
| `src/` | Python pipeline |
| `.env.example` | Config template |

## Quick demo

```bash
cd rag-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # PROJECT_ID=cursor-rag-lab-sam
python -m src.setup_bq
python -m src.ingest
python -m src.demo
```

Single question:

```bash
python -m src.rag_pipeline "What should I do if I get a phishing email?"
```

## Console links

- Project home: https://console.cloud.google.com/home/dashboard?project=cursor-rag-lab-sam
- BigQuery `doc_chunks`: https://console.cloud.google.com/bigquery?project=cursor-rag-lab-sam
- Search table name `doc_chunks` or `query_log` in the BigQuery explorer

## Lessons

1. Concepts → [`lessons/01_concepts.md`](lessons/01_concepts.md)
2. Auth & project → [`lessons/02_auth_and_project.md`](lessons/02_auth_and_project.md)
3. Vertex embeddings → [`lessons/03_embeddings.md`](lessons/03_embeddings.md)
4. BigQuery vectors → [`lessons/04_bigquery_vectors.md`](lessons/04_bigquery_vectors.md)
5. Ingest → [`lessons/05_ingest.md`](lessons/05_ingest.md)
6. Retrieve → [`lessons/06_retrieve.md`](lessons/06_retrieve.md)
7. Gemini RAG → [`lessons/07_gemini_rag.md`](lessons/07_gemini_rag.md)
8. Go further → [`lessons/08_go_further.md`](lessons/08_go_further.md)
