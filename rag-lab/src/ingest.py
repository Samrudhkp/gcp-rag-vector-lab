"""Ingest sample docs: chunk → embed → insert into BigQuery."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from google.cloud import bigquery

from src.config import get_settings
from src.embed import embed_texts

_ROOT = Path(__file__).resolve().parents[1]
_DOCS_DIR = _ROOT / "data" / "sample_docs"


def chunk_text(text: str, *, max_chars: int = 500) -> list[str]:
    """Split on blank lines, then pack into ~max_chars chunks."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(para) <= max_chars:
                current = para
            else:
                for i in range(0, len(para), max_chars):
                    chunks.append(para[i : i + max_chars])
                current = ""
    if current:
        chunks.append(current)
    return chunks


def load_documents(docs_dir: Path = _DOCS_DIR) -> list[tuple[str, str]]:
    """Return list of (doc_id, full_text)."""
    docs: list[tuple[str, str]] = []
    for path in sorted(docs_dir.glob("*.txt")):
        docs.append((path.stem, path.read_text(encoding="utf-8")))
    return docs


def chunk_id(doc_id: str, content: str) -> str:
    digest = hashlib.sha256(f"{doc_id}:{content}".encode()).hexdigest()[:16]
    return f"{doc_id}-{digest}"


def ingest(*, replace: bool = True) -> int:
    settings = get_settings()
    client = bigquery.Client(project=settings.project_id)
    table_id = f"{settings.project_id}.{settings.bq_dataset}.{settings.bq_table}"

    if replace:
        client.query(f"DELETE FROM `{table_id}` WHERE TRUE").result()

    rows: list[dict] = []
    for doc_id, text in load_documents():
        for content in chunk_text(text):
            rows.append(
                {
                    "id": chunk_id(doc_id, content),
                    "doc_id": doc_id,
                    "content": content,
                }
            )

    if not rows:
        print("No documents found to ingest.")
        return 1

    print(f"Embedding {len(rows)} chunks with {settings.embedding_model}...")
    vectors = embed_texts([r["content"] for r in rows], task_type="RETRIEVAL_DOCUMENT")
    for row, vector in zip(rows, vectors, strict=True):
        row["embedding"] = vector

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print("Insert errors:", errors)
        return 1

    print(f"Inserted {len(rows)} rows into {table_id}")
    for row in rows:
        print(f"  - {row['id']} ({row['doc_id']}, {len(row['content'])} chars)")
    return 0


def main() -> int:
    return ingest(replace=True)


if __name__ == "__main__":
    sys.exit(main())
