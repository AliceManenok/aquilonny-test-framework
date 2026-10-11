"""Pydantic models of Restful-Booker payloads: the API contract written as code."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    """Base for API models: types are checked strictly and unknown fields are rejected."""

    model_config = ConfigDict(strict=True, extra="forbid")


class BookingDates(ApiModel):
    checkin: date
    checkout: date


class Booking(ApiModel):
    """A booking as GET /booking/{id} returns it."""

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str | None = None  # string or none (not required)


class CreateBookingResponse(ApiModel):
    """Response of POST /booking: the new id and the saved booking."""

    bookingid: int
    booking: Booking  # class Booking from line 19
