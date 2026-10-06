"""Decimal helpers. All money in this library is ``decimal.Decimal``."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")


def to_decimal(value: Decimal | int | str) -> Decimal:
    """Convert ``value`` to ``Decimal``.

    Floats are rejected because they cannot represent most prices exactly.
    Non-numeric strings, NaN and infinities raise ``ValueError``.
    """
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("money values must be Decimal, int or str, not float or bool")
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"not a valid decimal: {value!r}") from None
    if not result.is_finite():
        raise ValueError(f"money values must be finite, got {value!r}")
    return result


def round_cents(amount: Decimal) -> Decimal:
    """Round ``amount`` to two places, halves rounding away from zero."""
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)
