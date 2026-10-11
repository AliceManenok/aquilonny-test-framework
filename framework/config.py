"""Test settings: one place for URLs, timeouts and credentials.

Values are read from config/<TEST_ENV>.env, then from .env (local secrets).
Environment variables override both; this is how CI injects secrets.
"""

import os
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # path to project root, two folders up
CONFIG_DIR = PROJECT_ROOT / "config"  # path to the folder config


class Settings(BaseSettings):
    """Typed settings of a test run; pydantic validates every value on load."""

    api_base_url: str
    ui_base_url: str
    upload_url: str
    timeout: int = 10
    headless: bool = True
    api_username: str
    api_password: SecretStr


def load_settings() -> Settings:
    """Build Settings for the environment named in TEST_ENV (default: demo)."""
    env_name = os.getenv("TEST_ENV", "demo")  # reads env var TEST_ENV, if not set then demo
    env_file = CONFIG_DIR / f"{env_name}.env"  # creates path to env
    if not env_file.exists():
        available = sorted(path.stem for path in CONFIG_DIR.glob("*.env"))
        raise FileNotFoundError(
            f"TEST_ENV='{env_name}', but {env_file} does not exist. Available: {available}"
        )
    return Settings(_env_file=(env_file, PROJECT_ROOT / ".env"), _env_file_encoding="utf-8")
