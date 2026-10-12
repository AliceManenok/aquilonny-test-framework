"""Fixtures for UI tests: opened page objects built on pytest-playwright's page fixture."""

import pytest
from playwright.sync_api import Page, Playwright

from framework.config import Settings
from framework.ui.pages.login_page import LoginPage
from framework.ui.pages.upload_page import UploadPage


@pytest.fixture(scope="session", autouse=True)
def test_id_attribute(playwright: Playwright) -> None:
    """Sauce Demo marks elements with data-test, so get_by_test_id() looks for that attribute."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page, settings: Settings) -> LoginPage:
    return LoginPage(page, settings.ui_base_url).open()


@pytest.fixture
def upload_page(page: Page, settings: Settings) -> UploadPage:
    return UploadPage(page, settings.upload_base_url).open()
