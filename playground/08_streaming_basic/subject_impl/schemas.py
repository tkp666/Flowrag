from __future__ import annotations

from pydantic import BaseModel


class ChatStreamRequest(BaseModel):
    question: str
    kb_id: str = "kb-stage8"
    simulate_retrieval_error: bool = False
    simulate_llm_error: bool = False
