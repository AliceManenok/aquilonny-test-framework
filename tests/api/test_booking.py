"""API tests for Restful-Booker bookings."""

import pytest

from framework.api.clients.booking_client import BookingClient
from framework.api.models.booking import Booking, CreateBookingResponse
from framework.utils.data_factory import build_booking

pytestmark = pytest.mark.api  # tags all tests in file as api


@pytest.mark.smoke  # only this test is smoke
def test_get_booking_returns_created_data(
    booking_client: BookingClient, created_booking: CreateBookingResponse
):
    # Arrange: created_booking fixture has already created a booking

    # Act
    response = booking_client.get_booking(created_booking.bookingid)

    # Assert
    assert response.status_code == 200
    assert Booking.model_validate_json(response.text) == created_booking.booking
    # model compares the whole booking


def test_update_booking_without_token_is_forbidden(
    booking_client: BookingClient, created_booking: CreateBookingResponse
):
    # Arrange
    new_data = build_booking()

    # Act
    response = booking_client.update_booking(created_booking.bookingid, new_data)

    # Assert
    assert response.status_code == 403
    unchanged = Booking.model_validate_json(
        booking_client.get_booking(created_booking.bookingid).text
    )  # we check that data hasn't changed after the failed update 403
    assert unchanged == created_booking.booking


@pytest.mark.parametrize(
    "overrides",
    [
        {"depositpaid": False},
        {"firstname": "A" * 100},
        {"firstname": "Иван", "lastname": "Петров"},
        {"bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-01"}},
    ],
    # will run 4 times/4 tests for each **overrides set of parameters
    ids=["no-deposit", "long-name", "cyrillic", "same-day"],
)
def test_create_booking_with_various_data(
    booking_client: BookingClient, booking_cleanup: list[int], overrides: dict
):
    # Arrange
    data = build_booking(**overrides)

    # Act
    response = booking_client.create_booking(data)

    # Assert
    assert response.status_code == 200
    booking_cleanup.append(response.json()["bookingid"])  # saved id to bookings to delete after
    created = CreateBookingResponse.model_validate_json(response.text)
    assert created.booking.model_dump(mode="json") == data  # compare data we sent with received
