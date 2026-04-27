from __future__ import annotations

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from agent.state import BookingResult, ListingDetails, ListingSummary


class SearchAvailablePropertiesInput(BaseModel):
    location: str = Field(..., description="Guest destination")
    check_in_date: str = Field(..., description="Check-in date(YYYY-MM-DD)")
    check_out_date: str = Field(..., description="Check-out date(YYYY-MM-DD)")
    guests: int = Field(..., ge=1, description="Number of guests")


class GetListingDetailsInput(BaseModel):
    listing_id: int = Field(..., gt=0, description="Unique listing ID")


class CreateBookingInput(BaseModel):
    conversation_id: str = Field(..., description="Conversation ID for the booking session")
    listing_id: int = Field(..., gt=0, description="Listing ID to reserve")
    check_in_date: str = Field(..., description="Check-in date(YYYY-MM-DD)")
    check_out_date: str = Field(..., description="Check-out date(YYYY-MM-DD)")
    guests: int = Field(..., ge=1, description="Number of guests")


@tool(args_schema=SearchAvailablePropertiesInput)
def search_available_properties(
    location: str,
    check_in_date: str,
    check_out_date: str,
    guests: int,
) -> list[ListingSummary]:
    """Return available properties for a destination, date range, and guest count."""
    sample_inventory: dict[str, list[ListingSummary]] = {
        "cox's bazar": [
            {
                "listing_id": 101,
                "title": "Sea View Apartment",
                "location": "Cox's Bazar",
                "price_per_night_bdt": 4500.0,
                "max_guests": 2,
            },
            {
                "listing_id": 102,
                "title": "Coral Reef Studio",
                "location": "Cox's Bazar",
                "price_per_night_bdt": 3800.0,
                "max_guests": 3,
            },
        ],
        "sylhet": [
            {
                "listing_id": 201,
                "title": "Tea Garden Retreat",
                "location": "Sylhet",
                "price_per_night_bdt": 5200.0,
                "max_guests": 4,
            }
        ],
        "bandarban": [
            {
                "listing_id": 204,
                "title": "Hill View Cottage",
                "location": "Bandarban",
                "price_per_night_bdt": 4200.0,
                "max_guests": 2,
            },
            {
                "listing_id": 205,
                "title": "Meghla Cabin",
                "location": "Bandarban",
                "price_per_night_bdt": 3600.0,
                "max_guests": 2,
            },
        ],
    }
    results = sample_inventory.get(location.lower(), [])
    return [listing for listing in results if listing["max_guests"] >= guests]


@tool(args_schema=GetListingDetailsInput)
def get_listing_details(listing_id: int) -> ListingDetails:
    """Return detailed information for one listing."""
    sample_details: dict[int, ListingDetails] = {
        101: {
            "listing_id": 101,
            "title": "Sea View Apartment",
            "location": "Cox's Bazar",
            "description": "Beachfront apartment within walking distance of Laboni Beach.",
            "price_per_night_bdt": 4500.0,
            "amenities": ["WiFi", "AC", "Kitchen"],
            "max_guests": 2,
        },
        102: {
            "listing_id": 102,
            "title": "Coral Reef Studio",
            "location": "Cox's Bazar",
            "description": "Compact studio suited for short beach stays.",
            "price_per_night_bdt": 3800.0,
            "amenities": ["WiFi", "AC"],
            "max_guests": 3,
        },
        201: {
            "listing_id": 201,
            "title": "Tea Garden Retreat",
            "location": "Sylhet",
            "description": "Quiet stay near tea estates with balcony views.",
            "price_per_night_bdt": 5200.0,
            "amenities": ["Breakfast", "WiFi", "Parking"],
            "max_guests": 4,
        },
        204: {
            "listing_id": 204,
            "title": "Hill View Cottage",
            "location": "Bandarban",
            "description": "Cottage stay with mountain views and breakfast included.",
            "price_per_night_bdt": 4200.0,
            "amenities": ["Breakfast", "WiFi", "Mountain View"],
            "max_guests": 2,
        },
    }
    return sample_details[listing_id]


@tool(args_schema=CreateBookingInput)
def create_booking(
    conversation_id: str,
    listing_id: int,
    check_in_date: str,
    check_out_date: str,
    guests: int,
) -> BookingResult:
    """Create a booking record for a confirmed stay."""
    return {
        "booking_id": 9001,
        "listing_id": listing_id,
        "status": "confirmed",
        "total_price_bdt": 9000.0,
    }
