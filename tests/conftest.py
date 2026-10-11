"""Shared fixtures available to every test under tests/."""

import pytest

from framework.config import Settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Settings of the current TEST_ENV, loaded once per test run."""
    return load_settings()
