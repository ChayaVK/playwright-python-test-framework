from dataclasses import dataclass

from playwright.sync_api import Page

from pages.base_page import BasePage


@dataclass
class Customer:
    first_name: str
    last_name: str
    postal_code: str


class CheckoutPage(BasePage):
    """Step 1 of checkout: the customer information form."""

    path = "checkout.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.get_by_label("First Name")
        self.last_name = page.get_by_label("Last Name")
        self.postal_code = page.get_by_label("Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.error = page.get_by_test_id("error")

    def fill(self, customer: Customer) -> None:
        self.first_name.fill(customer.first_name)
        self.last_name.fill(customer.last_name)
        self.postal_code.fill(customer.postal_code)

    def submit(self, customer: Customer) -> None:
        self.fill(customer)
        self.continue_button.click()
