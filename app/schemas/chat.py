from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class ChatMessageIn(BaseModel):
    session_id: str = Field(..., examples=["sess-001"])
    user_id: str = Field(..., examples=["user-123"])
    text: str = Field(..., min_length=1, examples=["Estou com acesso negado no WinSCP"])
    channel: str = Field("web", examples=["blip", "whatsapp", "web"])
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatMessageOut(BaseModel):
    reply_text: str
    intent: str
    confidence: float
    entities: Dict[str, Any]
    actions_taken: list[str]
    trace_id: str