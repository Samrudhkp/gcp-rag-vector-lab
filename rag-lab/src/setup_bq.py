"""Ensure BigQuery tables and vector index exist."""

from __future__ import annotations

import sys

from google.cloud import bigquery

from src.config import get_settings


def _run(client: bigquery.Client, sql: str) -> None:
    print("SQL:", " ".join(sql.split())[:120], "...")
    client.query(sql).result()


def setup() -> int:
    settings = get_settings()
    client = bigquery.Client(project=settings.project_id)
    project = settings.project_id
    dataset = settings.bq_dataset
    table = settings.bq_table

    _run(
        client,
        f"""
        CREATE SCHEMA IF NOT EXISTS `{project}.{dataset}`
        OPTIONS (location = 'US')
        """,
    )
    _run(
        client,
        f"""
        CREATE TABLE IF NOT EXISTS `{project}.{dataset}.{table}` (
          id STRING NOT NULL,
          doc_id STRING NOT NULL,
          content STRING NOT NULL,
          embedding ARRAY<FLOAT64>,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """,
    )
    _run(
        client,
        f"""
        CREATE TABLE IF NOT EXISTS `{project}.{dataset}.query_log` (
          query_id STRING NOT NULL,
          question STRING NOT NULL,
          answer STRING,
          retrieved_ids ARRAY<STRING>,
          distances ARRAY<FLOAT64>,
          embedding_model STRING,
          gemini_model STRING,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """,
    )

    # Vector index needs >=5000 rows for IVF in BigQuery.
    # Small lab corpora should call VECTOR_SEARCH directly (still correct).
    print(
        "Vector index: skipped for small corpora "
        "(BigQuery IVF requires >=5000 rows). VECTOR_SEARCH still works."
    )

    print("BigQuery setup complete.")
    return 0


def main() -> int:
    return setup()


if __name__ == "__main__":
    sys.exit(main())
