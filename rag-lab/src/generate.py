"""Generate an answer with Gemini using retrieved context."""

from __future__ import annotations

import vertexai
from vertexai.generative_models import GenerativeModel

from src.config import get_settings


def build_prompt(question: str, chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"[{i}] doc_id={chunk['doc_id']} id={chunk['id']}\n{chunk['content']}"
        )
    context = "\n\n".join(context_blocks) if context_blocks else "(no context retrieved)"
    return f"""You are a helpful assistant for Acme Corp internal docs.
Answer the question using ONLY the context below.
If the context is insufficient, say you do not know.
Cite chunk numbers like [1] when you use them.

Context:
{context}

Question: {question}

Answer:"""


def generate_answer(question: str, chunks: list[dict]) -> str:
    settings = get_settings()
    vertexai.init(project=settings.project_id, location=settings.location)
    model = GenerativeModel(settings.gemini_model)
    prompt = build_prompt(question, chunks)
    response = model.generate_content(prompt)
    return (response.text or "").strip()
