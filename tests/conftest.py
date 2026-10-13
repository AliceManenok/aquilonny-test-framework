"""Shared fixtures available to every test under tests/."""

import logging

import pytest

from framework.config import Settings, load_settings


@pytest.fixture(scope="session")  # fixture is a precondition for a test
def settings() -> Settings:
    """Settings of the current TEST_ENV, loaded once per test run."""
    return load_settings()


@pytest.fixture(scope="session", autouse=True)
def quiet_library_loggers() -> None:
    """Keep only our own logs in reports: these libraries repeat or flood them."""
    for name in ("httpx", "httpcore", "faker"):
        logging.getLogger(name).setLevel(logging.WARNING)
