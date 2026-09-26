"""Vertex AI LLM + embeddings wrappers for RAGAS (ADC, no API keys)."""

from __future__ import annotations

from evaluation.compat import ensure_ragas_vertex_imports

ensure_ragas_vertex_imports()

from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper

from src.config import get_settings


def build_evaluator_llm():
    settings = get_settings()
    # Chat model used as the RAGAS judge
    chat = ChatVertexAI(
        model_name=settings.gemini_model,
        project=settings.project_id,
        location=settings.location,
        temperature=0.0,
        max_output_tokens=2048,
    )
    return LangchainLLMWrapper(chat)


def build_evaluator_embeddings():
    settings = get_settings()
    emb = VertexAIEmbeddings(
        model_name=settings.embedding_model,
        project=settings.project_id,
        location=settings.location,
    )
    return LangchainEmbeddingsWrapper(emb)
