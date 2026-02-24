import logging
import uuid
from fastapi import APIRouter
from sqlmodel import Session
from ..schemas.chat import ChatMessageIn, ChatMessageOut
from ..services.orchestrator import orchestrate
from ..db.session import engine
from ..db.models import Message
from ..db.models import Message, Ticket


router = APIRouter()
logger = logging.getLogger("chat")

@router.post("/chat/message", response_model=ChatMessageOut)
def chat_message(payload: ChatMessageIn):
    trace_id = str(uuid.uuid4())

    reply_text, intent, confidence, entities, actions = orchestrate(
        text=payload.text,
        user_id=payload.user_id,
        metadata=payload.metadata,
    )

    # Persistir mensagem
    with Session(engine) as session:
        msg = Message(
            session_id=payload.session_id,
            user_id=payload.user_id,
            text=payload.text,
            intent=intent,
        )
        session.add(msg)
        session.commit()

    # Persistir ticket (quando aplicável)
    if "OPEN_TICKET" in actions and "ticket_id" in entities:
        t = Ticket(
            ticket_id=entities["ticket_id"],
            user_id=payload.user_id,
            summary=intent,
            status="OPEN",
        )
        session.add(t)
        session.commit()    

    logger.info(
        "message_processed",
        extra={
            "trace_id": trace_id,
            "session_id": payload.session_id,
            "user_id": payload.user_id,
            "intent": intent,
        },
    )

    return ChatMessageOut(
        reply_text=reply_text,
        intent=intent,
        confidence=confidence,
        entities=entities,
        actions_taken=actions,
        trace_id=trace_id,
    )