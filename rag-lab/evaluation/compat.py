"""Import compatibility shims for RAGAS 0.4.x + modern langchain packages."""

from __future__ import annotations

import sys
from types import ModuleType


def ensure_ragas_vertex_imports() -> None:
    """RAGAS 0.4.x imports ChatVertexAI from langchain_community; newer packages moved it.

    Call this before importing ragas.
    """
    try:
        from langchain_community.chat_models.vertexai import ChatVertexAI  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    from langchain_google_vertexai import ChatVertexAI, VertexAI

    mod = ModuleType("langchain_community.chat_models.vertexai")
    mod.ChatVertexAI = ChatVertexAI
    sys.modules["langchain_community.chat_models.vertexai"] = mod

    import langchain_community.llms as llms_pkg

    llms_pkg.VertexAI = VertexAI
