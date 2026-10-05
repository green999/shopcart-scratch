"""Discounts applied to an amount."""

from decimal import Decimal

from shopcart.money import round_cents, to_decimal

COUPONS: dict[str, Decimal] = {
    "WELCOME10": Decimal("10"),
    "SPRING25": Decimal("25"),
}


def apply_percent_discount(amount: Decimal, percent: Decimal | int | str) -> Decimal:
    """Return ``amount`` reduced by ``percent``, rounded to cents.

    ``percent`` must be between 0 and 100 inclusive. 0 returns the amount
    unchanged and 100 returns 0.00.
    """
    rate = to_decimal(percent)
    if rate < 0 or rate > 100:
        raise ValueError("percent must be between 0 and 100")
    return round_cents(amount * (Decimal("100") - rate) / Decimal("100"))


def apply_coupon(amount: Decimal, code: str) -> Decimal:
    """Apply the coupon ``code`` to ``amount``.

    Codes are case-insensitive and surrounding whitespace is ignored. An unknown
    code raises ``ValueError``.
    """
    key = code.strip().upper()
    if key not in COUPONS:
        raise ValueError(f"unknown coupon code: {code!r}")
    return apply_percent_discount(amount, COUPONS[key])


def bulk_discount_rate(quantity: int) -> Decimal:
    """Return the bulk discount percentage for a line of ``quantity`` units.

    Orders of 10 or more units get 5% off, and orders of 50 or more get 10% off.
    Smaller orders get no discount.
    """
    if quantity > 50:
        return Decimal("10")
    if quantity > 10:
        return Decimal("5")
    return Decimal("0")


def apply_bulk_discount(unit_price: Decimal, quantity: int) -> Decimal:
    """Return the line total for ``quantity`` units after the bulk discount."""
    return apply_percent_discount(unit_price * quantity, bulk_discount_rate(quantity))
