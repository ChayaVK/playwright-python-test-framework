"""Shared fixtures. Tests ask for what they need (products_page, api ...) by name, and pytest builds it."""
import base64
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, expect

from api.api_client import ApiClient
from api.users_api import UsersApi
from config.settings import ROOT, settings
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.complete_page import CompletePage
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
from pages.practice_page import PracticePage
from pages.products_page import ProductsPage



def _is_up(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=1) as response:
            return response.status == 200
    except OSError:
        return False


# ---------- the app under test ----------
_server: subprocess.Popen | None = None


def pytest_sessionstart(session):
    """Starts the bundled Practice Shop once per run, before any test.
    Skipped when it is already running, when START_DEMO_APP=false, and inside parallel
    workers (pytest -n), because the main process has already started it for them."""
    global _server
    health = f"{settings.api_url}/health"
    if hasattr(session.config, "workerinput") or not settings.start_demo_app or _is_up(health):
        return
    _server = subprocess.Popen([sys.executable, str(ROOT / "demo_app" / "server.py")])
    for _ in range(50):
        if _is_up(health):
            return
        time.sleep(0.2)
    _server.kill()
    raise RuntimeError(f"The Practice Shop did not start at {settings.base_url}")


def pytest_sessionfinish(session):
    if _server is not None:
        _server.terminate()
        _server.wait()


@pytest.fixture(scope="session", autouse=True)
def test_id_attribute(playwright: Playwright):
    """The app marks elements with data-test="...", so get_by_test_id() looks for that attribute."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def base_url() -> str:
    """page.goto("products.html") works because every page gets this base URL."""
    return settings.base_url + "/"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """When a UI test fails, put a screenshot of the page into the HTML report."""
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page")
    if report.when == "call" and report.failed and page is not None and not page.is_closed():
        html_plugin = item.config.pluginmanager.getplugin("html")
        if html_plugin is not None:
            screenshot = base64.b64encode(page.screenshot()).decode()
            report.extras = getattr(report, "extras", []) + [html_plugin.extras.png(screenshot, "Screenshot")]


# ---------- log in once, reuse the session ----------
@pytest.fixture(scope="session")
def auth_state(browser: Browser, base_url: str, tmp_path_factory) -> str:
    """Logs in once per run (once per worker with -n) and saves cookies and local storage to a file."""
    path = tmp_path_factory.mktemp("auth") / "user.json"
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    login = LoginPage(page)
    login.open()
    login.login(settings.username, settings.password)
    expect(page).to_have_url(f"{base_url}products.html")
    context.storage_state(path=path)
    context.close()
    return str(path)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_state):
    """Every test page starts logged in. Mark a test with
    @pytest.mark.browser_context_args(storage_state=None) to start logged out."""
    return {**browser_context_args, "storage_state": auth_state}


# ---------- page objects ----------
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def overview_page(page: Page) -> OverviewPage:
    return OverviewPage(page)


@pytest.fixture
def complete_page(page: Page) -> CompletePage:
    return CompletePage(page)


@pytest.fixture
def practice_page(page: Page) -> PracticePage:
    return PracticePage(page)


# ---------- API ----------
@pytest.fixture
def api_request(playwright: Playwright):
    context = playwright.request.new_context()
    yield context
    context.dispose()


@pytest.fixture
def api(api_request) -> ApiClient:
    return ApiClient(api_request)


@pytest.fixture
def auth_api(api_request) -> ApiClient:
    client = ApiClient(api_request)
    client.login()
    return client


@pytest.fixture
def users_api(auth_api) -> UsersApi:
    return UsersApi(auth_api)


@pytest.fixture
def upload_file() -> Path:
    return ROOT / "test-files" / "sample-upload.txt"
