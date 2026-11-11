"""Money helpers: pages show prices as text, tests need exact numbers."""
import re


def parse_price(text: str) -> float:
    """Turns "$49.99" or "Item total: $49.99" into 49.99."""
    match = re.search(r"-?\d+(\.\d+)?", text.replace(",", ""))
    if not match:
        raise ValueError(f'No price found in "{text}"')
    return float(match.group())


def sum_prices(values: list[float]) -> float:
    """Adds money without floating point noise: 49.99 + 9.99 = 59.98, not 59.980000000000004."""
    return sum(round(v * 100) for v in values) / 100


def tax_for(subtotal: float, rate: float) -> float:
    """Tax rounded to cents, the same way the app does it."""
    return round(subtotal * rate * 100) / 100
