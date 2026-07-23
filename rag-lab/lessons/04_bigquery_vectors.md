# Lesson 4 — BigQuery as a vector store

**Goal:** Create a BigQuery dataset and table that can store document chunks + 768-dim embeddings.

**Prerequisite:** Lesson 3 (you know embeddings are a list of floats; ours are length **768**).

---

## Idea

BigQuery is our vector database for this course.

Each row = one chunk:

| Column | Meaning |
|--------|---------|
| `id` | Unique chunk id |
| `doc_id` | Which source document |
| `content` | The text chunk |
| `embedding` | `ARRAY<FLOAT64>` of length 768 |

Later lessons insert rows and run `VECTOR_SEARCH`.

---

## Files

| File | Role |
|------|------|
| [`sql/01_create_dataset.sql`](../sql/01_create_dataset.sql) | Create dataset `rag_lab` |
| [`sql/02_create_embeddings_table.sql`](../sql/02_create_embeddings_table.sql) | Create table `doc_chunks` |

---

## What we create in project `cursor-rag-lab-sam`

- Dataset: `rag_lab` (US multi-region is fine for learning)
- Table: `rag_lab.doc_chunks`

---

## Check your understanding

1. What does one **row** in `doc_chunks` represent?
2. Why is the embedding column an array of floats with length 768?
3. Does creating the table put any document text into BigQuery yet? (yes/no)

Next lesson: ingest sample docs (chunk → embed → insert).
