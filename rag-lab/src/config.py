"""Load lab settings from environment / .env. No network I/O."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    project_id: str
    location: str
    bq_dataset: str
    bq_table: str
    embedding_model: str
    gemini_model: str


def get_settings() -> Settings:
    project_id = os.getenv("PROJECT_ID", "").strip()
    if not project_id:
        raise ValueError("PROJECT_ID is required. Copy .env.example to .env and set it.")

    return Settings(
        project_id=project_id,
        location=os.getenv("LOCATION", "us-central1").strip(),
        bq_dataset=os.getenv("BQ_DATASET", "rag_lab").strip(),
        bq_table=os.getenv("BQ_TABLE", "doc_chunks").strip(),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-005").strip(),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip(),
    )
