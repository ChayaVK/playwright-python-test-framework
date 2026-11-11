import pytest
from playwright.sync_api import expect

from pages.checkout_page import CheckoutPage, Customer
from pages.overview_page import OverviewPage
from pages.products_page import ProductsPage
from utils.data_reader import read_csv, read_json
from utils.price import sum_prices, tax_for

FORM_CASES = read_csv("checkout_cases.csv")
CATALOG = read_json("products.json")
PRICES = {p["name"]: p["price"] for p in CATALOG["products"]}


@pytest.mark.data
@pytest.mark.parametrize("case", FORM_CASES, ids=[c["case"] for c in FORM_CASES])
def test_checkout_form_shows_an_error(products_page: ProductsPage, checkout_page: CheckoutPage, case: dict):
    products_page.open()
    products_page.add_to_cart("Desk Lamp")
    checkout_page.open()
    checkout_page.submit(Customer(case["first_name"], case["last_name"], case["postal_code"]))
    expect(checkout_page.error).to_have_text(case["error"])


@pytest.mark.data
@pytest.mark.parametrize("order", CATALOG["orders"], ids=[o["case"] for o in CATALOG["orders"]])
def test_order_totals_are_right(
    products_page: ProductsPage, checkout_page: CheckoutPage, overview_page: OverviewPage, order: dict
):
    products_page.open()
    products_page.add_to_cart(*order["items"])
    checkout_page.open()
    checkout_page.submit(Customer("Sam", "Lee", "10001"))
    expected_subtotal = sum_prices([PRICES[name] for name in order["items"]])
    amounts = overview_page.amounts()
    assert amounts["subtotal"] == expected_subtotal
    assert amounts["tax"] == tax_for(expected_subtotal, CATALOG["taxRate"])
    assert amounts["total"] == sum_prices([expected_subtotal, amounts["tax"]])
