"""Test data factory: valid booking payloads with realistic random values (Faker)."""

from datetime import timedelta
from typing import Any

from faker import Faker

fake = Faker()  # fake object of the Faker class


def build_booking(**overrides: Any) -> dict[str, Any]:
    """Return a valid booking payload; any field can be overridden, e.g. depositpaid=False."""
    checkin = fake.date_between(start_date="+1d", end_date="+60d")
    checkout = checkin + timedelta(days=fake.random_int(min=1, max=14))
    booking = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=1000),
        "depositpaid": fake.boolean(),
        "bookingdates": {"checkin": checkin.isoformat(), "checkout": checkout.isoformat()},
        "additionalneeds": fake.random_element(["Breakfast", "Late checkout", "Parking"]),
    }
    return {**booking, **overrides}
