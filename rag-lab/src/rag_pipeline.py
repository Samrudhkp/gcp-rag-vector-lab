"""End-to-end RAG: question → retrieve → Gemini answer → optional query_log."""

from __future__ import annotations

import argparse
import sys

from src.generate import generate_answer
from src.log_query import log_query
from src.retrieve import retrieve


def answer_question(
    question: str,
    *,
    top_k: int = 3,
    max_distance: float | None = 0.7,
    write_log: bool = True,
) -> dict:
    chunks = retrieve(question, top_k=top_k, max_distance=max_distance)
    answer = generate_answer(question, chunks)
    query_id = None
    if write_log:
        query_id = log_query(question, answer, chunks)
    return {
        "question": question,
        "chunks": chunks,
        "answer": answer,
        "query_id": query_id,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run RAG over BigQuery + Gemini")
    parser.add_argument("question", nargs="?", default="How do I reset my password?")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--max-distance", type=float, default=0.7)
    parser.add_argument("--no-log", action="store_true", help="Skip writing query_log")
    args = parser.parse_args(argv)

    max_distance = None if args.max_distance >= 1.0 else args.max_distance
    result = answer_question(
        args.question,
        top_k=args.top_k,
        max_distance=max_distance,
        write_log=not args.no_log,
    )
    print("Question:", result["question"])
    if result["query_id"]:
        print("Logged as:", result["query_id"])
    print("\nRetrieved chunks:")
    if not result["chunks"]:
        print("  (none under distance threshold)")
    for i, chunk in enumerate(result["chunks"], start=1):
        print(
            f"  [{i}] {chunk['doc_id']} "
            f"(distance={chunk['distance']:.4f}, similarity={chunk['similarity']:.4f})"
        )
        preview = chunk["content"].replace("\n", " ")[:120]
        print(f"      {preview}...")
    print("\nAnswer:")
    print(result["answer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
