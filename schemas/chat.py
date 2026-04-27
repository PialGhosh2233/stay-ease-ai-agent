from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessageModel(BaseModel):
    role: Literal["guest", "assistant"]
    content: str


class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="Message sent to the AI agent")


class ChatMessageResponse(BaseModel):
    conversation_id: str
    intent: str | None
    response: str
    messages: list[ConversationMessageModel]


class ChatHistoryResponse(BaseModel):
    conversation_id: str
    messages: list[ConversationMessageModel]
