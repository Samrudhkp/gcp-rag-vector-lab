"""Retrieve nearest chunks from BigQuery VECTOR_SEARCH."""

from __future__ import annotations

import argparse
import json
import sys

from google.cloud import bigquery

from src.config import get_settings
from src.embed import embed_texts


def retrieve(question: str, *, top_k: int = 3) -> list[dict]:
    settings = get_settings()
    query_vector = embed_texts([question], task_type="RETRIEVAL_QUERY")[0]
    client = bigquery.Client(project=settings.project_id)
    table_id = f"{settings.project_id}.{settings.bq_dataset}.{settings.bq_table}"

    sql = f"""
    SELECT
      base.id AS id,
      base.doc_id AS doc_id,
      base.content AS content,
      distance
    FROM VECTOR_SEARCH(
      TABLE `{table_id}`,
      'embedding',
      (SELECT @query_embedding AS embedding),
      top_k => @top_k,
      distance_type => 'COSINE'
    )
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("query_embedding", "FLOAT64", query_vector),
            bigquery.ScalarQueryParameter("top_k", "INT64", top_k),
        ]
    )
    rows = client.query(sql, job_config=job_config).result()
    return [
        {
            "id": row["id"],
            "doc_id": row["doc_id"],
            "content": row["content"],
            "distance": float(row["distance"]),
        }
        for row in rows
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vector search over ingested chunks")
    parser.add_argument("question", nargs="?", default="How do I reset my password?")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args(argv)

    hits = retrieve(args.question, top_k=args.top_k)
    print(json.dumps({"question": args.question, "hits": hits}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
