"""Build RAGAS samples from the eval dataset using the live RAG pipeline or injections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.generate import generate_answer
from src.rag_pipeline import answer_question

_DATASET_PATH = Path(__file__).resolve().parent / "dataset.json"


def load_dataset(path: Path | None = None) -> list[dict[str, Any]]:
    dataset_path = path or _DATASET_PATH
    with dataset_path.open(encoding="utf-8") as f:
        return json.load(f)


def _chunks_to_contexts(chunks: list[dict]) -> list[str]:
    return [c["content"] for c in chunks]


def _fake_chunks_from_texts(texts: list[str]) -> list[dict]:
    return [
        {
            "id": f"injected-{i}",
            "doc_id": "injected",
            "content": text,
            "distance": 1.0,
            "similarity": 0.0,
        }
        for i, text in enumerate(texts, start=1)
    ]


def collect_sample(case: dict[str, Any]) -> dict[str, Any]:
    """Return one RAGAS-ready sample dict for a dataset case."""
    mode = case.get("mode", "live")
    question = case["user_input"]
    reference = case["reference"]

    if mode == "live":
        result = answer_question(question, top_k=3, max_distance=0.7, write_log=False)
        contexts = _chunks_to_contexts(result["chunks"])
        response = result["answer"]
        retrieved_doc_ids = [c["doc_id"] for c in result["chunks"]]
    elif mode == "inject_contexts":
        texts = case["injected_contexts"]
        fake_chunks = _fake_chunks_from_texts(texts)
        contexts = list(texts)
        response = generate_answer(question, fake_chunks)
        retrieved_doc_ids = ["injected"] * len(texts)
    elif mode == "inject_answer":
        # Retrieve for real (or empty), but force a weak/wrong answer.
        if case.get("mode_retrieve", "live") == "live":
            result = answer_question(question, top_k=3, max_distance=0.7, write_log=False)
            contexts = _chunks_to_contexts(result["chunks"])
            retrieved_doc_ids = [c["doc_id"] for c in result["chunks"]]
        else:
            contexts = case.get("injected_contexts", [])
            retrieved_doc_ids = ["injected"] * len(contexts)
        response = case["injected_response"]
    else:
        raise ValueError(f"Unknown mode for case {case.get('id')}: {mode}")

    return {
        "id": case["id"],
        "case_type": case.get("case_type", "unknown"),
        "mode": mode,
        "user_input": question,
        "retrieved_contexts": contexts,
        "response": response,
        "reference": reference,
        "retrieved_doc_ids": retrieved_doc_ids,
        "notes": case.get("notes", ""),
    }


def collect_all(path: Path | None = None) -> list[dict[str, Any]]:
    return [collect_sample(case) for case in load_dataset(path)]
