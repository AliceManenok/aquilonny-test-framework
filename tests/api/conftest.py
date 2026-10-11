"""Fixtures for API tests: clients, a token and a booking that cleans up after itself."""

from collections.abc import Iterator

import pytest

from framework.api.clients.booking_client import BookingClient
from framework.api.models.booking import CreateBookingResponse
from framework.config import Settings
from framework.utils.data_factory import build_booking


@pytest.fixture(scope="session")
def booking_client(settings: Settings) -> Iterator[BookingClient]:
    """Client without a token: for reads and for checks that access is denied."""
    client = BookingClient(settings.api_base_url, settings.timeout)
    yield client
    client.close()
    # settings object of Settings class
    # Iterator because we have yield
    # yield - pause the function and return the value, then resume after the 'client' is done


@pytest.fixture(scope="session")
def auth_token(booking_client: BookingClient, settings: Settings) -> str:
    """Token for write operations, requested once per test run."""
    response = booking_client.create_token(
        settings.api_username, settings.api_password.get_secret_value()
    )
    token = response.json().get("token")
    assert token, f"No token in the response: {response.text}"
    return token


@pytest.fixture(scope="session")
def authorized_client(settings: Settings, auth_token: str) -> Iterator[BookingClient]:
    """A separate client that sends the token: for update and delete."""
    client = BookingClient(settings.api_base_url, settings.timeout)
    client.authenticate(auth_token)
    yield client
    client.close()


@pytest.fixture
def created_booking(
    booking_client: BookingClient, authorized_client: BookingClient
) -> Iterator[CreateBookingResponse]:
    """A fresh booking for one test; deleted afterwards, even if the test fails."""
    response = booking_client.create_booking(build_booking())
    assert response.status_code == 200, f"Could not create a booking: {response.text}"
    created = CreateBookingResponse.model_validate_json(response.text)
    yield created
    authorized_client.delete_booking(created.bookingid)


@pytest.fixture
def booking_cleanup(authorized_client: BookingClient) -> Iterator[list[int]]:
    """List for ids of bookings a test creates itself; all of them are deleted afterwards."""
    booking_ids: list[int] = []
    yield booking_ids
    for booking_id in booking_ids:
        authorized_client.delete_booking(booking_id)
