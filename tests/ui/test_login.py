"""UI tests for logging in to Sauce Demo."""

import pytest
from playwright.sync_api import expect

from framework.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_login_with_valid_user(login_page: LoginPage, ui_users: dict):
    # LoginPage is already opened by fixture
    # Arrange
    user = ui_users["standard"]

    # Act
    inventory = login_page.login(user["username"], user["password"])

    # Assert
    expect(inventory.title).to_have_text("Products")  # Awaits for the title to be visible
    expect(inventory.item_name).to_have_count(6)  # Awaits for all 6 to load and be visible


def test_locked_out_user_sees_error(login_page: LoginPage, ui_users: dict):
    # Arrange
    user = ui_users["locked_out"]

    # Act
    login_page.submit_credentials(user["username"], user["password"])

    # Assert
    expect(login_page.error_message).to_contain_text("this user has been locked out")


@pytest.mark.parametrize(
    ("username", "password", "error"),
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    # will run 3 times/3 tests for each set of parameters
    ids=["wrong-password", "empty-username", "empty-password"],
)
def test_login_with_invalid_credentials_shows_error(
    login_page: LoginPage, username: str, password: str, error: str
):
    # Act
    login_page.submit_credentials(username, password)

    # Assert
    expect(login_page.error_message).to_contain_text(error)  # Awaits for the error message
