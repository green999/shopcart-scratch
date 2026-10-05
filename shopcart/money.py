"""Decimal helpers. All money in this library is ``decimal.Decimal``."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_decimal(value: Decimal | int | str) -> Decimal:
    """Convert ``value`` to ``Decimal``.

    Floats are rejected because they cannot represent most prices exactly.
    """
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("money values must be Decimal, int or str, not float or bool")
    return Decimal(value)


def round_cents(amount: Decimal) -> Decimal:
    """Round ``amount`` to two places, halves rounding away from zero."""
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)
