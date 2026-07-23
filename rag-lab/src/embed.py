"""Vertex AI text embeddings (Lesson 3)."""

from __future__ import annotations

import argparse
import sys

import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from src.config import get_settings


def embed_texts(texts: list[str], *, task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed one or more strings. Returns one float vector per input."""
    if not texts:
        return []

    settings = get_settings()
    vertexai.init(project=settings.project_id, location=settings.location)
    model = TextEmbeddingModel.from_pretrained(settings.embedding_model)

    inputs = [TextEmbeddingInput(text=t, task_type=task_type) for t in texts]
    results = model.get_embeddings(inputs)
    return [list(r.values) for r in results]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Embed a string with Vertex AI")
    parser.add_argument(
        "text",
        nargs="?",
        default="How do I reset my password?",
        help="Text to embed",
    )
    args = parser.parse_args(argv)

    settings = get_settings()
    vectors = embed_texts([args.text])
    vector = vectors[0]

    print(f"project:   {settings.project_id}")
    print(f"location:  {settings.location}")
    print(f"model:     {settings.embedding_model}")
    print(f"text:      {args.text!r}")
    print(f"dimension: {len(vector)}")
    print(f"preview:   {vector[:8]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
