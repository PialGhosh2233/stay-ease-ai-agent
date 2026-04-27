from __future__ import annotations

from typing import Literal, TypedDict


Intent = Literal["search", "details", "book", "human_escalation"]
Role = Literal["guest", "assistant"]


class ConversationMessage(TypedDict):
    role: Role
    content: str


class ListingSummary(TypedDict):
    listing_id: int
    title: str
    location: str
    price_per_night_bdt: float
    max_guests: int


class ListingDetails(TypedDict):
    listing_id: int
    title: str
    location: str
    description: str
    price_per_night_bdt: float
    amenities: list[str]
    max_guests: int


class BookingResult(TypedDict):
    booking_id: int
    listing_id: int
    status: str
    total_price_bdt: float


class AgentState(TypedDict):
    conversation_id: str
    user_message: str
    intent: Intent | None
    location: str | None
    check_in_date: str | None
    check_out_date: str | None
    guests: int | None
    listing_id: int | None
    available_properties: list[ListingSummary]
    listing_details: ListingDetails | None
    booking_result: BookingResult | None
    messages: list[ConversationMessage]
    response_text: str | None
    error: str | None


class StateUpdate(TypedDict, total=False):
    intent: Intent | None
    location: str | None
    check_in_date: str | None
    check_out_date: str | None
    guests: int | None
    listing_id: int | None
    available_properties: list[ListingSummary]
    listing_details: ListingDetails | None
    booking_result: BookingResult | None
    messages: list[ConversationMessage]
    response_text: str | None
    error: str | None
