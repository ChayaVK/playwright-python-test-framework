from playwright.sync_api import Page

from pages.base_page import BasePage


class CompletePage(BasePage):
    path = "complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator("#complete-header")
        self.message = page.locator("#complete-text")
        self.back_home = page.get_by_role("button", name="Back to products")
