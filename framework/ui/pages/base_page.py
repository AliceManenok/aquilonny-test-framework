"""Base page object: what every page of the app under test has in common."""

from abc import ABC, abstractmethod  # Abstract Base Class
from typing import Self

from playwright.sync_api import Page


class BasePage(ABC):
    """A page that knows its path; each subclass defines how to tell it has loaded."""

    path: str  # set by every subclass, e.g. path = "/inventory.html"

    def __init__(self, page: Page, base_url: str) -> None:  # does smth, returns None
        self.page = page
        self.base_url = base_url

    def open(self) -> Self:  # e.g. returns itself, LoginPage.open() returns LoginPage
        """Go to base_url + path, wait until the page is ready, return the page itself."""
        self.page.goto(self.base_url + self.path)
        self.expect_loaded()  # waits for the page to load
        return self

    @abstractmethod
    def expect_loaded(self) -> None:  # does smth, returns None
        """Wait until an element that proves the page is ready becomes visible."""

    # open(self), expect_loaded(self) - same method behaves differently depending on the subclass
