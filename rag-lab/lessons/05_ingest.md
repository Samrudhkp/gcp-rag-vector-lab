# Lesson 5 — Ingest documents

Chunk sample docs → Vertex embeddings → insert into `rag_lab.doc_chunks`.

```bash
cd rag-lab
source .venv/bin/activate
python -m src.ingest
```

One row per chunk: `id`, `doc_id`, `content`, `embedding`.
