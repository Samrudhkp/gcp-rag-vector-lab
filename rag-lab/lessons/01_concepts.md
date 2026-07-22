# Lesson 1 — RAG & vector search concepts

**Goal:** Understand *what* we will build and *why*, before touching Google Cloud.

**No cloud work in this lesson.** No APIs, no `gcloud`, no cost.

---

## What is RAG?

**Retrieval-Augmented Generation** means: before the LLM answers, look up relevant text from *your* documents, then ask the model to answer *using that context*.

| Approach | What the model sees |
|----------|---------------------|
| Prompt only | Training knowledge + whatever you paste |
| RAG | Same, plus fresh snippets retrieved for *this* question |

Use RAG when answers must come from **your** docs: policies, notes, product manuals, internal FAQs — data that is private, changing, or too large to stuff into every prompt.

---

## What is an embedding?

An **embedding** is a list of numbers (a vector) that represents meaning. Similar text maps to nearby vectors.

Intuition (not real dimensions):

- `"How do I reset my password?"` ≈ `"password reset steps"`
- Far from `"quarterly revenue forecast"`

In this course we use **Vertex AI text embedding models** to turn both document chunks and user questions into vectors.

---

## What is a vector database? (and why BigQuery?)

A vector store answers: *which stored vectors are closest to this query vector?* (often cosine similarity or Euclidean distance).

For this course, **BigQuery is our vector database**:

1. Store each chunk’s text + its embedding.
2. Embed the question the same way.
3. Run BigQuery **`VECTOR_SEARCH`** to get the top-k nearest chunks.

You do **not** need a separate vector DB product for these lessons.

---

## End-to-end flow we will build

```text
Documents
   │
   ▼
Chunk text ──► Vertex embeddings ──► BigQuery (text + vector)
                                              │
User question ──► same embedding model ───────┤
                                              ▼
                                    VECTOR_SEARCH (top-k)
                                              │
                                              ▼
                         Gemini (answer using retrieved chunks)
```

Steps in order:

1. Split docs into chunks (a few hundred tokens each).
2. Embed each chunk with Vertex AI; store text + vector in BigQuery.
3. Embed the user question the same way.
4. `VECTOR_SEARCH` → top-k similar chunks.
5. Prompt Gemini: answer using only those chunks; cite them when possible.

---

## What each later folder is for

| Folder / file | Later role |
|---------------|------------|
| `data/sample_docs/` | Small plain-text files we will chunk |
| `sql/` | Create dataset/table; run vector search |
| `src/embed.py` | Call Vertex embeddings |
| `src/ingest.py` | Chunk → embed → write BigQuery |
| `src/retrieve.py` | Query BigQuery for neighbors |
| `src/generate.py` | Call Gemini with context |
| `src/rag_pipeline.py` | Glue: question → retrieve → answer |

Those files stay stubs until their lesson.

---

## Check your understanding

Reply with short answers (a sentence each is fine):

1. In one sentence, what does RAG add that prompting alone does not?
2. Why embed both documents *and* the question the same way?
3. Where do embeddings live in *this* course’s architecture?

When those feel solid, we unlock **Lesson 2** (project auth and which APIs to enable). Lesson 2 will only **list** commands for you to approve — nothing runs until you say so.
