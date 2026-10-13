"""Client for the Restful-Booker booking API: one method per endpoint."""

from typing import Any

import httpx

from framework.api.clients.base_client import BaseApiClient


class BookingClient(BaseApiClient):
    """Sends booking requests and returns raw responses; tests decide what is correct."""

    def authenticate(self, token: str) -> None:  # None - no return value, only changes data
        """Send the token with every next request; Restful-Booker reads it from a cookie."""
        self._client.cookies.set("token", token)

    def create_token(self, username: str, password: str) -> httpx.Response:
        credentials = {"username": username, "password": password}
        return self._request("POST", "/auth", log_body=False, json=credentials)  # body has token

    def create_booking(self, data: dict[str, Any]) -> httpx.Response:
        return self._request("POST", "/booking", json=data)

    def find_bookings(self, **filters: str) -> httpx.Response:
        """GET /booking?firstname=...: a list of {"bookingid": ...} for matching bookings."""
        return self._request("GET", "/booking", params=filters)  # Params turn filters into query

    def get_booking(self, booking_id: int) -> httpx.Response:
        return self._request("GET", f"/booking/{booking_id}")  # f-string builds the path

    def update_booking(self, booking_id: int, data: dict[str, Any]) -> httpx.Response:
        return self._request("PUT", f"/booking/{booking_id}", json=data)

    def delete_booking(self, booking_id: int) -> httpx.Response:
        return self._request("DELETE", f"/booking/{booking_id}")
