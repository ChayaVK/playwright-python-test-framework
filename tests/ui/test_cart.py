import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.price import sum_prices


@pytest.fixture(autouse=True)
def open_products(products_page: ProductsPage):
    products_page.open()


@pytest.mark.smoke
def test_cart_shows_exactly_the_added_items(products_page: ProductsPage, cart_page: CartPage):
    added = ["Wireless Mouse", "USB-C Cable", "Water Bottle"]
    products_page.add_to_cart(*added)
    products_page.header.open_cart()
    assert sorted(cart_page.item_names()) == sorted(added)


@pytest.mark.regression
def test_cart_prices_match_the_product_page(products_page: ProductsPage, cart_page: CartPage):
    expected = [products_page.price_of("Laptop Bag"), products_page.price_of("Desk Lamp")]
    products_page.add_to_cart("Laptop Bag", "Desk Lamp")
    cart_page.open()
    assert sum_prices(cart_page.item_prices()) == sum_prices(expected)


@pytest.mark.regression
def test_removing_the_last_item_shows_the_empty_message(products_page: ProductsPage, cart_page: CartPage):
    products_page.add_to_cart("Desk Lamp")
    cart_page.open()
    cart_page.remove("Desk Lamp")
    expect(cart_page.items).to_have_count(0)
    expect(cart_page.empty_message).to_be_visible()


@pytest.mark.regression
def test_cart_is_kept_after_a_reload(products_page: ProductsPage, cart_page: CartPage, page: Page):
    products_page.add_to_cart("Bluetooth Speaker")
    cart_page.open()
    page.reload()
    assert cart_page.item_names() == ["Bluetooth Speaker"]
