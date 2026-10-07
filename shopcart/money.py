"""Decimal helpers. All money in this library is ``decimal.Decimal``."""

import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")
SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£"}
_AMOUNT = re.compile(
    r"(?P<sign>[+-])?(?P<symbol>[$€£])?(?P<number>(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)",
    re.ASCII,
)


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


def format_money(amount: Decimal, currency: str = "USD") -> str:
    """Format ``amount`` as e.g. ``$1,234.50``, rounded to cents (halves up).

    The sign precedes the symbol. An amount that rounds to zero is ``$0.00``,
    never ``-$0.00``. An unknown currency raises ``ValueError``.
    """
    if not isinstance(currency, str) or currency.upper() not in SYMBOLS:
        raise ValueError(f"unsupported currency: {currency!r}")
    symbol = SYMBOLS[currency.upper()]
    rounded = round_cents(to_decimal(amount))
    sign = "-" if rounded < 0 else ""
    return f"{sign}{symbol}{abs(rounded):,.2f}"


def parse_money(text: str) -> Decimal:
    """Parse text such as `` -$1,234.50 `` into a ``Decimal``.

    Accepts an optional sign, an optional supported symbol, optional valid
    thousands commas and surrounding whitespace. An empty string or invalid
    amount raises ``ValueError``.
    """
    if not isinstance(text, str):
        raise ValueError("money text must be a string")
    match = _AMOUNT.fullmatch(text.strip())
    if match is None:
        raise ValueError(f"not a valid money amount: {text!r}")
    value = Decimal(match["number"].replace(",", ""))
    return -value if match["sign"] == "-" else value
