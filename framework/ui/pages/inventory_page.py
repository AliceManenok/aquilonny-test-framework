"""Inventory (product catalog) page of Sauce Demo: where a user lands after login."""

from playwright.sync_api import Page, expect

from framework.ui.components.header import HeaderComponent
from framework.ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.header = HeaderComponent(page.get_by_test_id("primary-header"))
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_name = page.get_by_test_id("inventory-item-name")

    def expect_loaded(self) -> None:
        expect(self.title).to_have_text("Products")

    def product_names(self) -> list[str]:  # List or array of strings, each string is a product name
        return self.item_name.all_inner_texts()

    def add_to_cart(self, product_name: str) -> None:
        item = self.items.filter(has_text=product_name)  # Find the item with the given product name
        item.get_by_role("button", name="Add to cart").click()  # Adds that name's item
