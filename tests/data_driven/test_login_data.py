import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from utils.data_reader import read_json

CASES = read_json("login_cases.json")


# One test per row in data/login_cases.json. Add a row, get a new test.
@pytest.mark.data
@pytest.mark.browser_context_args(storage_state=None)
@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_login_shows_an_error(login_page: LoginPage, case: dict):
    login_page.open()
    login_page.login(case["username"], case["password"])
    expect(login_page.error).to_have_text(case["error"])
