"""End-to-end RAG: question → retrieve → Gemini answer."""

from __future__ import annotations

import argparse
import sys

from src.generate import generate_answer
from src.retrieve import retrieve


def answer_question(question: str, *, top_k: int = 3) -> dict:
    chunks = retrieve(question, top_k=top_k)
    answer = generate_answer(question, chunks)
    return {"question": question, "chunks": chunks, "answer": answer}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run RAG over BigQuery + Gemini")
    parser.add_argument("question", nargs="?", default="How do I reset my password?")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args(argv)

    result = answer_question(args.question, top_k=args.top_k)
    print("Question:", result["question"])
    print("\nRetrieved chunks:")
    for i, chunk in enumerate(result["chunks"], start=1):
        print(f"  [{i}] {chunk['doc_id']} (distance={chunk['distance']:.4f})")
        preview = chunk["content"].replace("\n", " ")[:120]
        print(f"      {preview}...")
    print("\nAnswer:")
    print(result["answer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
