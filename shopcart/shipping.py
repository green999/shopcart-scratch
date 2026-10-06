"""Shipping cost calculation."""

from decimal import Decimal

RATES: dict[str, Decimal] = {
    "standard": Decimal("5.99"),
    "express": Decimal("14.99"),
    "pickup": Decimal("0.00"),
}

FREE_STANDARD_THRESHOLD = Decimal("50.00")


def shipping_cost(subtotal: Decimal, method: str = "standard") -> Decimal:
    """Return the shipping cost for ``subtotal`` using ``method``.

    Method names are case-insensitive and surrounding whitespace is ignored. An
    unknown method or a negative subtotal raises ``ValueError``. A subtotal of 0
    is valid. Standard shipping is free at a subtotal of exactly 50.00 or more;
    express and pickup ignore the threshold.
    """
    key = method.strip().lower()
    if key not in RATES:
        raise ValueError(f"unknown shipping method: {method!r}")
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if key == "standard" and subtotal >= FREE_STANDARD_THRESHOLD:
        return Decimal("0.00")
    return RATES[key]
