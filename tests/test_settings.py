"""Checks that the loaded settings are usable before real tests rely on them."""

from framework.config import Settings


def test_urls_use_https(settings: Settings):
    assert settings.api_base_url.startswith("https://")
    assert settings.ui_base_url.startswith("https://")
    assert settings.upload_base_url.startswith("https://")


def test_timeout_is_positive(settings: Settings):
    assert settings.timeout > 0


def test_password_is_not_empty(settings: Settings):
    # get_secret_value() reveals the password: compare it, never print it.
    assert settings.api_password.get_secret_value() != ""
