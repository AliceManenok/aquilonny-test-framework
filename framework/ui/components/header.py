"""Header shared by Sauce Demo pages after login: the cart icon and the side menu."""

from playwright.sync_api import Locator


class HeaderComponent:
    """A part of several pages, not a page itself: it has no URL and is found inside a page."""

    # That's why Header is a component not a page (not inherited from BasePage), shared

    def __init__(self, root: Locator) -> None:  # Find the root of header component
        self.cart_link = root.get_by_test_id("shopping-cart-link")
        self.cart_badge = root.get_by_test_id("shopping-cart-badge")
        self.menu_button = root.get_by_role("button", name="Open Menu")
        self.logout_link = root.get_by_test_id("logout-sidebar-link")

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
