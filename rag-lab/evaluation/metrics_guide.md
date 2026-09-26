# RAGAS metrics used in this lab

Scores are typically **0.0–1.0**. Higher is better unless noted.

## Faithfulness (groundedness)

- **Meaning:** Are the claims in the generated answer supported by the retrieved context?
- **Inputs:** `response`, `retrieved_contexts`
- **Good score (~0.8–1.0):** Answer sticks to the docs (grounded).
- **Bad score (~0.0–0.4):** Hallucinations or invented policy details.

## Answer Relevancy (`answer_relevancy` / Response Relevancy)

- **Meaning:** Does the answer address the user’s question (on-topic), regardless of factual grounding?
- **Inputs:** `user_input`, `response` (uses embeddings + LLM)
- **Good score:** Direct, useful answer to the question asked.
- **Bad score:** Off-topic, evasive, or incomplete relative to the question.

## Context Relevancy (`nv_context_relevance` / ContextRelevance)

- **Meaning:** Are the retrieved chunks pertinent to the question?
- **Inputs:** `user_input`, `retrieved_contexts`
- **Good score:** Retrieved IT/HR/security/expense text matches the ask.
- **Bad score:** Wrong-topic chunks (e.g., vacation text for a password question).

## Retrieval quality — Context Precision (`llm_context_precision_with_reference`)

- **Meaning:** Are useful contexts ranked highly vs the reference answer?
- **Inputs:** `user_input`, `retrieved_contexts`, `reference`
- **Good score:** Relevant chunks appear early in the ranked list.
- **Bad score:** Irrelevant chunks dominate the top of retrieval.

## Retrieval quality — Context Recall (`context_recall`)

- **Meaning:** Does the retrieved context contain the information needed for the reference answer?
- **Inputs:** `user_input`, `retrieved_contexts`, `reference`
- **Good score:** Reference facts are covered by retrieved text.
- **Bad score:** Key facts missing from retrieval (incomplete context).

## How to read good vs bad cases in `dataset.json`

| case_type | What we expect |
|-----------|----------------|
| `good` | High faithfulness, relevancy, and retrieval scores |
| `bad_retrieval` | Low context relevance / precision / recall |
| `bad_answer` | Low faithfulness and/or answer relevancy |
