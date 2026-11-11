from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from utils.price import parse_price


class ProductsPage(BasePage):
    path = "products.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.sort = page.get_by_label("Sort by")
        self.items = page.locator(".inventory-item")
        self.names = page.locator(".inventory-item .item-name")
        self.prices = page.locator(".inventory-item .item-price")

    def item(self, name: str) -> Locator:
        """Card of one product, found by its visible name."""
        return self.items.filter(has_text=name)

    def add_to_cart(self, *names: str) -> None:
        for name in names:
            self.item(name).get_by_role("button", name="Add to cart").click()
            self.item(name).get_by_role("button", name="Remove").wait_for()

    def remove_from_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Remove").click()
        self.item(name).get_by_role("button", name="Add to cart").wait_for()

    def sort_by(self, option: str) -> None:
        """option is one of: az, za, lohi, hilo"""
        self.sort.select_option(option)

    def product_names(self) -> list[str]:
        return self.texts(self.names)

    def product_prices(self) -> list[float]:
        return [parse_price(t) for t in self.texts(self.prices)]

    def price_of(self, name: str) -> float:
        return parse_price(self.item(name).locator(".item-price").inner_text())
