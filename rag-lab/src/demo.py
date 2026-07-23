"""Run a multi-question RAG demo and print a summary for showcasing."""

from __future__ import annotations

import sys

from src.rag_pipeline import answer_question

DEMO_QUESTIONS = [
    "How do I reset my password?",
    "How many vacation days do employees get?",
    "What should I do if I get a phishing email?",
    "What is the daily meal limit while traveling?",
    "Can I work remotely three days a week?",
]


def main() -> int:
    print("=" * 60)
    print("RAG demo — Vertex embeddings + BigQuery VECTOR_SEARCH + Gemini")
    print("=" * 60)

    for question in DEMO_QUESTIONS:
        print("\n" + "-" * 60)
        result = answer_question(question, top_k=3, max_distance=0.7, write_log=True)
        print(f"Q: {result['question']}")
        print(f"log: {result['query_id']}")
        print("sources:")
        for i, chunk in enumerate(result["chunks"], start=1):
            print(
                f"  [{i}] {chunk['doc_id']} "
                f"sim={chunk['similarity']:.3f} dist={chunk['distance']:.3f}"
            )
        print(f"A: {result['answer']}")

    print("\n" + "=" * 60)
    print("Demo complete. Inspect BigQuery tables:")
    print("  - rag_lab.doc_chunks  (vectors)")
    print("  - rag_lab.query_log   (this run's Q&A)")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
