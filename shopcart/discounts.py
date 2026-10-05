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
