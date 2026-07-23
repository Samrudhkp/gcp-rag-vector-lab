# Lesson 3 — Vertex AI embeddings

**Goal:** Turn one string into a vector using Vertex AI in project `cursor-rag-lab-sam`.

**Prerequisite:** Lessons 1–2 done (project, billing, ADC).

---

## Idea

An embedding model maps text → a fixed-length list of floats.

Same meaning → nearby vectors. That is what BigQuery `VECTOR_SEARCH` will use later.

In this lesson we only:

1. Read config (`PROJECT_ID`, `LOCATION`, `EMBEDDING_MODEL`)
2. Call Vertex AI once
3. Print vector length and a few numbers

No BigQuery yet. No Gemini answers yet.

---

## Files

| File | Role |
|------|------|
| [`src/config.py`](../src/config.py) | Load env vars |
| [`src/embed.py`](../src/embed.py) | Call the embedding model |
| [`requirements.txt`](../requirements.txt) | Python packages |

---

## Run

```bash
cd rag-lab
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # if you do not already have .env
python -m src.embed "How do I reset my password?"
```

---

## What to notice

- Output includes **dimension** (how many floats per vector). Remember this for BigQuery later.
- Calling the same text twice should give (nearly) the same vector.
- Different text → different vector.

---

## Check your understanding

1. What does the embedding model return for one input string?
2. Why do we care about the vector **dimension** before creating a BigQuery table?
3. Have we built RAG yet after this lesson? (yes/no + why)

When those are solid, Lesson 4 creates a BigQuery table that can store these vectors.
