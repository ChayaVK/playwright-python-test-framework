from playwright.sync_api import Page


class Header:
    """The top bar shown on every page after login. A component, reused by all pages."""

    def __init__(self, page: Page):
        self.title = page.locator(".app-title")
        self.products_link = page.locator("#products-link")
        self.cart_link = page.locator("#cart-link")
        self.cart_badge = page.locator("#cart-badge")
        self.practice_link = page.locator("#practice-link")
        self.logout_link = page.locator("#logout-link")

    def cart_count(self) -> int:
        return int(self.cart_badge.inner_text()) if self.cart_badge.count() else 0

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.logout_link.click()
