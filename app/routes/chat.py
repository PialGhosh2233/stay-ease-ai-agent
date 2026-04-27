from __future__ import annotations

from fastapi import APIRouter, HTTPException

from agent.graph import stayease_graph
from agent.state import AgentState
from schemas.chat import (
    ChatHistoryResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationMessageModel,
)

router = APIRouter()


def build_initial_state(conversation_id: str, message: str) -> AgentState:
    """Create the initial state passed into the LangGraph workflow."""
    return {
        "conversation_id": conversation_id,
        "user_message": message,
        "intent": None,
        "location": None,
        "check_in_date": None,
        "check_out_date": None,
        "guests": None,
        "listing_id": None,
        "available_properties": [],
        "listing_details": None,
        "booking_result": None,
        "messages": [],
        "response_text": None,
        "error": None,
    }


@router.post("/{conversation_id}/message", response_model=ChatMessageResponse)
def send_message(conversation_id: str, request: ChatMessageRequest) -> ChatMessageResponse:
    """Process one guest message through the LangGraph agent."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")

    result = stayease_graph.invoke(build_initial_state(conversation_id, request.message))
    return ChatMessageResponse(
        conversation_id=conversation_id,
        intent=result["intent"],
        response=result["response_text"] or "",
        messages=[ConversationMessageModel(**item) for item in result["messages"]],
    )


@router.get("/{conversation_id}/history", response_model=ChatHistoryResponse)
def get_history(conversation_id: str) -> ChatHistoryResponse:
    """Return a sample conversation history for the requested conversation."""
    if not conversation_id:
        raise HTTPException(status_code=404, detail="conversation not found")

    messages = [
        ConversationMessageModel(
            role="guest",
            content="Tell me about listing 101",
        ),
        ConversationMessageModel(
            role="assistant",
            content="Sea View Apartment in Cox's Bazar costs BDT 4,500 per night and includes WiFi and AC.",
        ),
    ]
    return ChatHistoryResponse(conversation_id=conversation_id, messages=messages)
