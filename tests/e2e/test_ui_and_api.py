import pytest
from playwright.sync_api import Page, Route, expect

from api.api_client import ApiClient
from pages.cart_page import CartPage
from pages.practice_page import PracticePage
from pages.products_page import ProductsPage
from utils.price import sum_prices

pytestmark = pytest.mark.regression


def test_product_prices_on_the_page_match_the_api(api: ApiClient, products_page: ProductsPage):
    api_products = api.get("/products").json()
    products_page.open()
    for product in api_products:
        assert products_page.price_of(product["name"]) == product["price"], product["name"]


def test_seed_the_cart_then_check_out_in_the_ui(page: Page, cart_page: CartPage):
    # Faster than clicking: put the cart straight into localStorage before the page loads.
    page.add_init_script(
        """if (!sessionStorage.getItem('seeded')) {
             localStorage.setItem('cart', JSON.stringify(['laptop-bag', 'desk-lamp']));
             sessionStorage.setItem('seeded', 'yes');
           }"""
    )
    cart_page.open()
    assert cart_page.item_names() == ["Laptop Bag", "Desk Lamp"]
    assert sum_prices(cart_page.item_prices()) == 74.98


def test_mock_a_network_response(page: Page, practice_page: PracticePage):
    def fake_products(route: Route):
        route.fulfill(json=[{"id": 99, "name": "Mocked Item", "price": 1}])

    page.route("**/api/products", fake_products)
    practice_page.open()
    names = page.evaluate("async () => (await (await fetch('/api/products')).json()).map(p => p.name)")
    assert names == ["Mocked Item"]


def test_captures_a_screenshot_as_evidence(products_page: ProductsPage, page: Page, tmp_path):
    products_page.open()
    shot = page.screenshot(path=tmp_path / "products-page.png")
    assert len(shot) > 1000
    expect(products_page.items.first).to_be_visible()
