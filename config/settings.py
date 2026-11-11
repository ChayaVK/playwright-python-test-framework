"""Loads the settings for the chosen environment.

Pick the environment with TEST_ENV (local, qa, staging). Values come from env/.env.<TEST_ENV>.
Anything already set in the terminal or in CI wins over the file, so secrets never need to be in Git.
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
TEST_ENV = os.environ.get("TEST_ENV", "local")
load_dotenv(ROOT / "env" / f".env.{TEST_ENV}", override=False)


def _get(key: str, default: str | None = None) -> str:
    value = os.environ.get(key, default)
    if value is None:
        raise RuntimeError(f'Missing setting "{key}". Add it to env/.env.{TEST_ENV} or set it in your terminal.')
    return value


@dataclass(frozen=True)
class Settings:
    env_name: str
    base_url: str
    api_url: str
    username: str
    password: str
    locked_user: str
    start_demo_app: bool


settings = Settings(
    env_name=TEST_ENV,
    base_url=_get("BASE_URL", "http://localhost:3000").rstrip("/"),
    api_url=_get("API_URL", "http://localhost:3000/api").rstrip("/"),
    username=_get("APP_USERNAME", "standard_user"),
    password=_get("APP_PASSWORD", "Test@123"),
    locked_user=_get("LOCKED_USERNAME", "locked_user"),
    start_demo_app=_get("START_DEMO_APP", "true").lower() == "true",
)
