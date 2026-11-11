from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "index.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error = page.get_by_test_id("error")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
