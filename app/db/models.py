from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str
    user_id: str
    text: str
    intent: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str
    user_id: str
    summary: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)