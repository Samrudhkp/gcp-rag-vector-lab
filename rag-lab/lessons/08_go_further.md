# Lesson 8 — Go further (logging, richer corpus, index notes)

What we added after the basic RAG loop:

1. **More documents** — security + expense policies (better demo questions)
2. **`query_log` table** — every RAG run stores question, answer, retrieved chunk ids
3. **Distance filter + similarity** — drop weak matches; show `similarity ≈ 1 - distance`
4. **`python -m src.demo`** — multi-question showcase script
5. **Vector index note** — BigQuery IVF indexes need ≥5000 rows; our tiny lab uses `VECTOR_SEARCH` directly (still a real vector DB workflow)

## Commands

```bash
cd rag-lab
source .venv/bin/activate
python -m src.setup_bq
python -m src.ingest
python -m src.demo
```

## What to open in Cloud Console

- BigQuery → `rag_lab.doc_chunks` → Preview (text + embedding arrays)
- BigQuery → `rag_lab.query_log` → Preview (your demo questions/answers)
