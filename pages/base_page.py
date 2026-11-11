import re

from playwright.sync_api import Locator, Page, expect

from components.header import Header


class BasePage:
    """Shared helpers every page object inherits."""

    path = ""  # page path relative to BASE_URL, for example "products.html"

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

    def open(self) -> None:
        self.page.goto(self.path)

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(self.path)))

    @staticmethod
    def texts(locator: Locator) -> list[str]:
        """Reads the text of every element a locator matches, trimmed."""
        return [t.strip() for t in locator.all_inner_texts()]
