"""Login page of Sauce Demo."""

from playwright.sync_api import Page, expect

from framework.ui.pages.base_page import BasePage
from framework.ui.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)  # execute parent's (BasePage) init constructor/method
        self.username_input = page.get_by_test_id("username")  # This and following are locators
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def expect_loaded(self) -> None:
        expect(self.login_button).to_be_visible()  # Awaits Login button to be visible

    def submit_credentials(self, username: str, password: str) -> None:  # Negative, no return value
        """Fill in the form and press Login; use it for logins that are expected to fail."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login(self, username: str, password: str) -> InventoryPage:  # Login returns InventoryPage
        """Log in successfully and return the page the user lands on."""
        self.submit_credentials(username, password)
        inventory = InventoryPage(self.page, self.base_url)
        inventory.expect_loaded()
        return inventory
