# Lesson 2 — Auth & project setup

**Goal:** Know how this machine (or your laptop) will talk to Google Cloud project `cursor-gcp-practice`, and which APIs we will enable — **without running anything until you approve**.

**Still no cloud work until you say yes to specific commands below.**

---

## What “auth” means here

Python code needs permission to call:

- **Vertex AI** (embeddings + Gemini)
- **BigQuery** (store vectors + `VECTOR_SEARCH`)

Common local/dev options:

| Method | When to use |
|--------|-------------|
| `gcloud auth application-default login` | You, on a laptop/dev machine (interactive browser login) |
| Service account JSON key | Automation / CI (we will avoid keys unless you ask) |
| Workload Identity | Cloud Run / GKE (later; not Lesson 2) |

For this course we prefer **Application Default Credentials (ADC)** via `gcloud` — no key files in the repo.

---

## Project facts (this course)

| Setting | Value |
|---------|--------|
| Project ID | `cursor-gcp-practice` |
| Suggested region | `us-central1` (change only if you prefer another) |
| Config template | [`.env.example`](../.env.example) |

You will eventually copy `.env.example` → `.env` (gitignored). We have not created `.env` yet on purpose.

---

## APIs we will need (Lesson 3+)

| API | Why |
|-----|-----|
| `aiplatform.googleapis.com` | Vertex AI embeddings + Gemini |
| `bigquery.googleapis.com` | Tables + vector search |

Optional later (not required for the core pipeline): Cloud Storage if we load large files from GCS.

---

## Commands (for **your** approval — do not run yet unless you choose to)

These are listed so you can copy them when ready. **Reply which ones you approve**, or run them yourself and tell me the outcome.

### A) Point gcloud at the project

```bash
gcloud config set project cursor-gcp-practice
gcloud config get-value project
```

Expected: prints `cursor-gcp-practice`.

### B) Application Default Credentials (for Python)

```bash
gcloud auth application-default login
```

Opens a browser; grants local apps permission to call GCP as you.

### C) Enable APIs

```bash
gcloud services enable aiplatform.googleapis.com bigquery.googleapis.com --project=cursor-gcp-practice
```

### D) Sanity checks (read-only-ish)

```bash
gcloud services list --enabled --project=cursor-gcp-practice \
  --filter="config.name:(aiplatform.googleapis.com OR bigquery.googleapis.com)"
```

---

## What we will *not* do in Lesson 2

- No embedding calls, no BigQuery tables, no Gemini prompts.
- No service account keys committed to git.
- No deploys.

---

## Check your understanding

Reply with short answers:

1. What is ADC, and why do we prefer it over putting a JSON key in the repo?
2. Which two Google APIs does this RAG lab need first?
3. After Lesson 2, have we stored any document embeddings yet? (yes/no + why)

## Your action for this lesson

Tell me one of:

- **“Approve A–D”** — I will run those commands here (if this environment has `gcloud` and browser/auth works), **or**
- **“I’ll run them myself”** — paste any errors or the output of the sanity check, **or**
- **“Explain more first”** — ask about any step before approving.
