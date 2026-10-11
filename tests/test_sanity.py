"""Sanity checks: pytest runs, and a first look at Python syntax."""


def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b


def test_sum():  # test_ is defined by pytest as test not function
    assert add(2, 3) == 5


def test_string_formatting():
    name = "Aquilonny"
    greeting = f"Hello, {name}!"
    assert greeting == "Hello, Aquilonny!"


def test_dict_looks_like_json():
    booking = {"firstname": "Jim", "totalprice": 111, "depositpaid": True}
    assert booking["firstname"] == "Jim"
    assert "lastname" not in booking
