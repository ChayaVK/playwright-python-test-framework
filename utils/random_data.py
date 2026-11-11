"""Small test data helpers, so every run uses fresh values."""
import random
import uuid

from pages.checkout_page import Customer

FIRST = ["Alex", "Sam", "Jordan", "Taylor", "Riya", "Arjun", "Maya", "Leo"]
LAST = ["Brown", "Patel", "Garcia", "Lee", "Khan", "Miller", "Rao", "Lopez"]


def unique_id() -> str:
    return uuid.uuid4().hex[:8]


def random_email(prefix: str = "user") -> str:
    return f"{prefix}.{unique_id()}@example.com"


def random_customer() -> Customer:
    return Customer(random.choice(FIRST), random.choice(LAST), str(random.randint(10000, 99999)))
