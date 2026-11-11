import re

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

# Login tests must start logged out, so they skip the saved session.
pytestmark = pytest.mark.browser_context_args(storage_state=None)


@pytest.fixture(autouse=True)
def open_login(login_page: LoginPage):
    login_page.open()


@pytest.mark.smoke
def test_valid_user_lands_on_products_page(login_page: LoginPage, products_page: ProductsPage, page: Page):
    login_page.login(settings.username, settings.password)
    expect(page).to_have_url(re.compile(r"products\.html"))
    expect(products_page.header.title).to_have_text("Products")


@pytest.mark.regression
def test_locked_user_sees_an_error(login_page: LoginPage):
    login_page.login(settings.locked_user, settings.password)
    expect(login_page.error).to_have_text("This user has been locked out")


@pytest.mark.regression
def test_page_without_login_sends_you_to_login(page: Page, login_page: LoginPage):
    page.goto("cart.html")
    expect(page).to_have_url(re.compile(r"index\.html"))
    expect(login_page.error).to_have_text("You must log in to view this page")


@pytest.mark.regression
def test_logout_clears_the_session(login_page: LoginPage, products_page: ProductsPage, page: Page):
    login_page.login(settings.username, settings.password)
    products_page.header.logout()
    expect(page).to_have_url(re.compile(r"index\.html"))
    page.goto("products.html")
    expect(page).to_have_url(re.compile(r"index\.html"))
