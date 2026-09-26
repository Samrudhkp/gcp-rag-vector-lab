"""Run RAGAS evaluation over the local eval dataset using Vertex AI judges."""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import pandas as pd

from evaluation.compat import ensure_ragas_vertex_imports

ensure_ragas_vertex_imports()

from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.metrics import (
    AnswerRelevancy,
    ContextRelevance,
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)

from evaluation.collect_samples import collect_all
from evaluation.vertex_ragas import build_evaluator_embeddings, build_evaluator_llm

_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_OUT = Path(__file__).resolve().parent / "results"


def _build_metrics(llm, embeddings):
    # Instantiate metric objects (required by current RAGAS).
    return [
        Faithfulness(llm=llm),
        AnswerRelevancy(llm=llm, embeddings=embeddings),
        ContextRelevance(llm=llm),
        LLMContextPrecisionWithReference(llm=llm),
        LLMContextRecall(llm=llm),
    ]


def _print_report(df: pd.DataFrame, meta: list[dict]) -> None:
    metric_cols = [
        c
        for c in [
            "faithfulness",
            "answer_relevancy",
            "nv_context_relevance",
            "context_relevance",
            "llm_context_precision_with_reference",
            "context_precision",
            "context_recall",
        ]
        if c in df.columns
    ]

    print("\n" + "=" * 78)
    print("RAGAS evaluation results (per question)")
    print("=" * 78)

    for i, row in df.iterrows():
        m = meta[i] if i < len(meta) else {}
        print("\n" + "-" * 78)
        print(f"[{m.get('id', i)}] case_type={m.get('case_type')} mode={m.get('mode')}")
        print(f"Q: {row.get('user_input', m.get('user_input', ''))}")
        if m.get("notes"):
            print(f"note: {m['notes']}")
        preview = str(row.get("response", ""))[:160].replace("\n", " ")
        print(f"A: {preview}{'...' if len(str(row.get('response', ''))) > 160 else ''}")
        print(f"retrieved_doc_ids: {m.get('retrieved_doc_ids')}")
        for col in metric_cols:
            val = row.get(col)
            try:
                print(f"  {col}: {float(val):.4f}")
            except (TypeError, ValueError):
                print(f"  {col}: {val}")

    print("\n" + "=" * 78)
    print("Averages")
    print("=" * 78)
    for col in metric_cols:
        series = pd.to_numeric(df[col], errors="coerce")
        print(f"  {col}: {series.mean():.4f}")


def run(output_dir: Path, skip_collect_save: bool = False) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Collecting RAG samples (live retrieve/generate + intentional bad cases)...")
    samples_raw = collect_all()
    samples_path = output_dir / "collected_samples.json"
    samples_path.write_text(json.dumps(samples_raw, indent=2), encoding="utf-8")
    print(f"Wrote {samples_path}")

    ragas_samples = [
        SingleTurnSample(
            user_input=s["user_input"],
            retrieved_contexts=s["retrieved_contexts"],
            response=s["response"],
            reference=s["reference"],
        )
        for s in samples_raw
    ]
    dataset = EvaluationDataset(samples=ragas_samples)

    print("Building Vertex AI evaluator LLM + embeddings from .env / ADC...")
    llm = build_evaluator_llm()
    embeddings = build_evaluator_embeddings()
    metrics = _build_metrics(llm, embeddings)

    print("Running RAGAS evaluate() ...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = evaluate(dataset=dataset, metrics=metrics, llm=llm, embeddings=embeddings)

    df = result.to_pandas()
    csv_path = output_dir / "ragas_scores.csv"
    json_path = output_dir / "ragas_scores.json"
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")

    _print_report(df, samples_raw)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run RAGAS eval for the rag-lab pipeline")
    parser.add_argument(
        "--out",
        type=Path,
        default=_DEFAULT_OUT,
        help="Directory for collected samples and score tables",
    )
    args = parser.parse_args(argv)
    return run(args.out)


if __name__ == "__main__":
    # Allow `python -m evaluation.run_eval` from rag-lab/
    sys.path.insert(0, str(_ROOT))
    sys.exit(main())
