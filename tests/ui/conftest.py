"""Fixtures for UI tests: opened page objects built on pytest-playwright's page fixture."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, Playwright

from framework.config import PROJECT_ROOT, Settings
from framework.ui.pages.login_page import LoginPage
from framework.ui.pages.upload_page import UploadPage

TEST_DATA_DIR = PROJECT_ROOT / "test_data"  # Path to test data directory, relative to project root


@pytest.fixture(scope="session", autouse=True)  # Fixture applies automatically to all session tests
def test_id_attribute(playwright: Playwright) -> None:
    """Sauce Demo marks elements with data-test, so get_by_test_id() looks for that attribute."""
    # Sets the test ID attribute for Playwright selectors to "data-test" for all tests in session
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page, settings: Settings) -> LoginPage:
    return LoginPage(page, settings.ui_base_url).open()


@pytest.fixture
def upload_page(page: Page, settings: Settings) -> UploadPage:
    return UploadPage(page, settings.upload_base_url).open()


@pytest.fixture(scope="session")
def ui_users() -> dict[str, dict[str, str]]:
    # Dictionary of dictionaries: role -> {username, password}
    """Sauce Demo accounts; their passwords are public and printed on the site's login page."""
    return json.loads((TEST_DATA_DIR / "users.json").read_text(encoding="utf-8"))  # Read as text


@pytest.fixture(scope="session")
def sample_lease_pdf() -> Path:
    return TEST_DATA_DIR / "files" / "sample_lease.pdf"
