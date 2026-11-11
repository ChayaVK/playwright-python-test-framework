from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.price import parse_price


class OverviewPage(BasePage):
    """Step 2 of checkout: order summary with subtotal, tax and total."""

    path = "checkout-overview.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator("#summary-items .cart-item")
        self.subtotal = page.locator("#subtotal")
        self.tax = page.locator("#tax")
        self.total = page.locator("#total")
        self.finish_button = page.get_by_role("button", name="Finish")

    def amounts(self) -> dict[str, float]:
        return {
            "subtotal": parse_price(self.subtotal.inner_text()),
            "tax": parse_price(self.tax.inner_text()),
            "total": parse_price(self.total.inner_text()),
        }

    def item_prices(self) -> list[float]:
        return [parse_price(t) for t in self.texts(self.items.locator(".item-price"))]

    def finish(self) -> None:
        self.finish_button.click()
