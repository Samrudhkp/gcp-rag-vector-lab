"""Persist RAG runs to BigQuery query_log for demos and debugging."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from google.cloud import bigquery

from src.config import get_settings


def log_query(
    question: str,
    answer: str,
    chunks: list[dict],
) -> str:
    settings = get_settings()
    client = bigquery.Client(project=settings.project_id)
    table_id = f"{settings.project_id}.{settings.bq_dataset}.query_log"
    query_id = str(uuid.uuid4())
    row = {
        "query_id": query_id,
        "question": question,
        "answer": answer,
        "retrieved_ids": [c["id"] for c in chunks],
        "distances": [float(c["distance"]) for c in chunks],
        "embedding_model": settings.embedding_model,
        "gemini_model": settings.gemini_model,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        raise RuntimeError(f"Failed to write query_log: {errors}")
    return query_id
