"""File upload page of The Internet: the closest public stand-in for uploading a lease PDF."""

from pathlib import Path
from typing import Self

from playwright.sync_api import Page, Route, expect

from framework.ui.pages.base_page import BasePage

STATIC_FILES = {"stylesheet", "script", "image", "font"}


def skip_static_files(route: Route) -> None:  # Skips non-HTML files to speed up the test
    """Let the HTML through and drop styles, scripts, images and fonts."""
    if route.request.resource_type in STATIC_FILES:
        route.abort()
    else:
        route.continue_()


class UploadPage(BasePage):
    path = "/upload"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.file_input = page.locator("#file-upload")
        self.upload_button = page.get_by_role("button", name="Upload")
        self.uploaded_files = page.locator("#uploaded-files")

    def open(self) -> Self:
        # The demo server takes up to 30 s per static file; the plain HTML form works without them.
        self.page.route("**/*", skip_static_files)
        return super().open()

    def expect_loaded(self) -> None:
        expect(self.upload_button).to_be_visible()

    def upload(self, file_path: Path) -> None:
        self.file_input.set_input_files(file_path)  # Sets the file input to the given file path
        self.upload_button.click()
