import re

import pytest
from playwright.sync_api import expect

from pages.products_page import ProductsPage
from utils.data_reader import read_json

CATALOG = read_json("products.json")["products"]


@pytest.fixture(autouse=True)
def open_products(products_page: ProductsPage):
    products_page.open()


@pytest.mark.smoke
def test_every_product_has_a_name_and_a_price(products_page: ProductsPage):
    expect(products_page.items).to_have_count(len(CATALOG))
    for item in products_page.items.all():
        expect(item.locator(".item-name")).not_to_be_empty()
        expect(item.locator(".item-price")).to_have_text(re.compile(r"^\$\d+\.\d{2}$"))


@pytest.mark.regression
def test_prices_match_the_catalog_data(products_page: ProductsPage):
    for product in CATALOG:
        assert products_page.price_of(product["name"]) == product["price"], product["name"]


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, by, reverse",
    [("az", "name", False), ("za", "name", True), ("lohi", "price", False), ("hilo", "price", True)],
    ids=["name A to Z", "name Z to A", "price low to high", "price high to low"],
)
def test_sorting(products_page: ProductsPage, option: str, by: str, reverse: bool):
    products_page.sort_by(option)
    values = products_page.product_names() if by == "name" else products_page.product_prices()
    assert values == sorted(values, reverse=reverse)


@pytest.mark.smoke
def test_adding_and_removing_updates_the_cart_badge(products_page: ProductsPage):
    products_page.add_to_cart("Laptop Bag", "Desk Lamp")
    expect(products_page.header.cart_badge).to_have_text("2")
    products_page.remove_from_cart("Laptop Bag")
    expect(products_page.header.cart_badge).to_have_text("1")
