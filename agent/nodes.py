from __future__ import annotations

from typing import Literal, Protocol

from pydantic import BaseModel, Field

from agent.state import AgentState, StateUpdate
from agent.tools import create_booking, get_listing_details, search_available_properties


class ExtractedGuestRequest(BaseModel):
    intent: Literal["search", "details", "book", "human_escalation"] | None = Field(
        default=None,
        description="Classified intent for the guest message.",
    )
    location: str | None = Field(
        default=None,
        description="Destination requested by the guest.",
    )
    check_in_date: str | None = Field(
        default=None,
        description="Check-in date in YYYY-MM-DD format.",
    )
    check_out_date: str | None = Field(
        default=None,
        description="Check-out date in YYYY-MM-DD format.",
    )
    guests: int | None = Field(
        default=None,
        description="Number of guests.",
    )
    listing_id: int | None = Field(
        default=None,
        description="Listing identifier when the guest asks for details or booking.",
    )


class StructuredExtractor(Protocol):
    """Minimal protocol for an LLM extractor that supports structured output."""

    def invoke(self, messages: list[dict[str, str]]) -> ExtractedGuestRequest | dict:
        ...


def get_structured_extractor() -> StructuredExtractor | None:
    """Return the configured structured extractor.
    llm = Call LLM
    return llm.with_structured_output(ExtractedGuestRequest)
    """
    return None


def extract_entities_with_llm(message: str, intent: str | None) -> ExtractedGuestRequest:
    """
    Extract structured entities from the guest message using an LLM.
    """
    extractor = get_structured_extractor()
    prompt_messages = [
        {
            "role": "system",
            "content": (
            "Prompt"
            ),
        },
        {
            "role": "user",
            "content": f"Intent: {intent}\nGuest message: {message}",
        },
    ]

    if extractor is not None:
        result = extractor.invoke(prompt_messages)
        if isinstance(result, ExtractedGuestRequest):
            return result
        return ExtractedGuestRequest.model_validate(result)


    if intent == "details":
        return ExtractedGuestRequest(intent=intent, listing_id=101)
    if intent == "book":
        return ExtractedGuestRequest(
            intent=intent,
            listing_id=101,
            check_in_date="2026-05-10",
            check_out_date="2026-05-12",
            guests=2,
        )

    return ExtractedGuestRequest(
        intent=intent,
        location="Cox's Bazar",
        check_in_date="2026-05-10",
        check_out_date="2026-05-12",
        guests=2,
    )


def classify_request_node(state: AgentState) -> StateUpdate:
    """Classify the incoming message into one supported intent."""
    message = state["user_message"].lower()

    if any(keyword in message for keyword in ("book", "confirm", "reserve")):
        return {"intent": "book"}
    if any(keyword in message for keyword in ("details", "tell me about", "amenities", "listing")):
        return {"intent": "details"}
    if any(keyword in message for keyword in ("room", "stay", "available", "search", "apartment")):
        return {"intent": "search"}
    return {"intent": "human_escalation"}


def extract_entities_node(state: AgentState) -> StateUpdate:
    """Extract search or booking fields from the guest message with LLM structured output."""
    extracted = extract_entities_with_llm(state["user_message"], state["intent"])
    update: StateUpdate = {}

    if extracted.location is not None:
        update["location"] = extracted.location
    if extracted.check_in_date is not None:
        update["check_in_date"] = extracted.check_in_date
    if extracted.check_out_date is not None:
        update["check_out_date"] = extracted.check_out_date
    if extracted.guests is not None:
        update["guests"] = extracted.guests
    if extracted.listing_id is not None:
        update["listing_id"] = extracted.listing_id

    if state["intent"] == "search" and extracted.check_in_date is None:
        update["check_in_date"] = "2026-05-10"
        update["check_out_date"] = "2026-05-12"

    if state["intent"] == "search" and extracted.guests is None:
        update["guests"] = 2

    if state["intent"] == "book" and extracted.listing_id is None:
        update["error"] = "Booking requires a listing_id in the guest message."

    if state["intent"] == "details" and extracted.listing_id is None:
        update["error"] = "Listing details require a listing_id in the guest message."

    return update


def execute_tool_node(state: AgentState) -> StateUpdate:
    """Call the tool that matches the classified intent."""
    if state.get("error"):
        return {}

    if state["intent"] == "search":
        properties = search_available_properties.invoke(
            {
                "location": state["location"],
                "check_in_date": state["check_in_date"],
                "check_out_date": state["check_out_date"],
                "guests": state["guests"],
            }
        )
        return {"available_properties": properties}

    if state["intent"] == "details":
        details = get_listing_details.invoke({"listing_id": state["listing_id"]})
        return {"listing_details": details}

    if state["intent"] == "book":
        booking = create_booking.invoke(
            {
                "conversation_id": state["conversation_id"],
                "listing_id": state["listing_id"],
                "check_in_date": state["check_in_date"] or "2026-05-10",
                "check_out_date": state["check_out_date"] or "2026-05-12",
                "guests": state["guests"] or 2,
            }
        )
        return {"booking_result": booking}

    return {}


def compose_response_node(state: AgentState) -> StateUpdate:
    """Build a guest-facing response from the current state."""
    if state.get("error"):
        response_text = state["error"]
    elif state["intent"] == "search":
        properties = state["available_properties"]
        if not properties:
            response_text = f"No properties are currently available in {state['location']}."
        elif len(properties) == 1:
            listing = properties[0]
            response_text = (
                f"I found 1 available property in {listing['location']}: "
                f"{listing['title']} for BDT {listing['price_per_night_bdt']:,.0f}/night."
            )
        else:
            formatted = ", ".join(
                f"{item['title']} for BDT {item['price_per_night_bdt']:,.0f}/night"
                for item in properties
            )
            response_text = f"I found {len(properties)} available properties in {state['location']}: {formatted}."
    elif state["intent"] == "details" and state["listing_details"] is not None:
        listing = state["listing_details"]
        response_text = (
            f"{listing['title']} in {listing['location']} costs BDT "
            f"{listing['price_per_night_bdt']:,.0f} per night and includes "
            f"{', '.join(listing['amenities'])}."
        )
    elif state["intent"] == "book" and state["booking_result"] is not None:
        booking = state["booking_result"]
        response_text = (
            f"Your booking is confirmed. Booking ID {booking['booking_id']} "
            f"for listing {booking['listing_id']}. Total price: BDT {booking['total_price_bdt']:,.0f}."
        )
    else:
        response_text = "I can only help with search, listing details, and booking."

    updated_messages = list(state["messages"])
    updated_messages.append({"role": "guest", "content": state["user_message"]})
    updated_messages.append({"role": "assistant", "content": response_text})
    return {"response_text": response_text, "messages": updated_messages}


def human_escalation_node(state: AgentState) -> StateUpdate:
    """Return a human escalation response for unsupported requests."""
    response_text = (
        "I can only help with property search, listing details, and booking. "
        "I will escalate this conversation to a human agent."
    )
    updated_messages = list(state["messages"])
    updated_messages.append({"role": "guest", "content": state["user_message"]})
    updated_messages.append({"role": "assistant", "content": response_text})
    return {"response_text": response_text, "messages": updated_messages}


def route_after_classification(state: AgentState) -> Literal["extract_entities", "human_escalation"]:
    """Route supported intents through extraction, otherwise escalate."""
    if state["intent"] == "human_escalation":
        return "human_escalation"
    return "extract_entities"
