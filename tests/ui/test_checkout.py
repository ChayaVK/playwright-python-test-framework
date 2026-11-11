import re

import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.complete_page import CompletePage
from pages.overview_page import OverviewPage
from pages.products_page import ProductsPage
from utils.data_reader import read_json
from utils.logger import step
from utils.price import sum_prices, tax_for
from utils.random_data import random_customer

TAX_RATE = read_json("products.json")["taxRate"]


@pytest.mark.smoke
def test_places_an_order_end_to_end(
    products_page: ProductsPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
    overview_page: OverviewPage,
    complete_page: CompletePage,
):
    with step("Add two products"):
        products_page.open()
        products_page.add_to_cart("Laptop Bag", "Wireless Mouse")
    with step("Fill customer details"):
        products_page.header.open_cart()
        cart_page.checkout()
        checkout_page.submit(random_customer())
    with step("Check totals and finish"):
        amounts = overview_page.amounts()
        assert amounts["subtotal"] == sum_prices(overview_page.item_prices())
        assert amounts["tax"] == tax_for(amounts["subtotal"], TAX_RATE)
        assert amounts["total"] == sum_prices([amounts["subtotal"], amounts["tax"]])
        overview_page.finish()
    expect(complete_page.heading).to_have_text("Thank you for your order!")
    expect(complete_page.header.cart_badge).to_have_count(0)


@pytest.mark.regression
def test_cancel_on_the_form_goes_back_to_the_cart(products_page: ProductsPage, checkout_page: CheckoutPage, page: Page):
    products_page.open()
    products_page.add_to_cart("USB-C Cable")
    checkout_page.open()
    checkout_page.cancel_button.click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
