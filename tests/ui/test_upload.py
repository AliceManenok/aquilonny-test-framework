"""UI test for uploading a file: the public stand-in for uploading a lease PDF."""

from pathlib import Path

import pytest
from playwright.sync_api import expect

from framework.ui.pages.upload_page import UploadPage

pytestmark = pytest.mark.ui


def test_upload_pdf(upload_page: UploadPage, sample_lease_pdf: Path):
    # Act
    upload_page.upload(sample_lease_pdf)

    # Assert
    expect(upload_page.uploaded_files).to_have_text(sample_lease_pdf.name)  # Awaits for file upload
