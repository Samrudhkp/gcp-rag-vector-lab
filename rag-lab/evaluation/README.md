# RAGAS evaluation (isolated from the main RAG app)

This folder evaluates the existing Vertex + BigQuery RAG pipeline with **RAGAS**.
It calls `src.rag_pipeline.answer_question` and `src.generate.generate_answer` but does **not** change those modules.

## Where the app retrieves / generates (for reference)

| Step | Location |
|------|----------|
| Retrieve | `src/retrieve.py` → BigQuery `VECTOR_SEARCH` |
| Context → Gemini | `src/generate.py` → `build_prompt()` |
| Final answer | `src/generate.py` → `generate_answer()` |

## Setup

```bash
cd rag-lab
source .venv/bin/activate
pip install -r requirements.txt
# Requires Application Default Credentials for Vertex AI
# gcloud auth application-default login
```

## Run evaluation

```bash
cd rag-lab
source .venv/bin/activate
python -m evaluation.run_eval
```

Outputs:

- `evaluation/results/collected_samples.json` — questions, contexts, answers used
- `evaluation/results/ragas_scores.csv` — per-row metric scores
- Console table of each question + scores + averages

## Dataset

See [`dataset.json`](dataset.json): ~10 cases including intentional bad retrieval and bad answers.

Metric meanings: [`metrics_guide.md`](metrics_guide.md)
