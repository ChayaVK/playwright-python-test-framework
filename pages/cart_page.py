from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.price import parse_price


class CartPage(BasePage):
    path = "cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator(".cart-item")
        self.empty_message = page.locator("#empty-cart")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping = page.get_by_role("button", name="Continue shopping")

    def item_names(self) -> list[str]:
        return self.texts(self.items.locator(".item-name"))

    def item_prices(self) -> list[float]:
        return [parse_price(t) for t in self.texts(self.items.locator(".item-price"))]

    def remove(self, name: str) -> None:
        self.items.filter(has_text=name).get_by_role("button", name="Remove").click()
        self.items.filter(has_text=name).wait_for(state="detached")

    def checkout(self) -> None:
        self.checkout_button.click()
