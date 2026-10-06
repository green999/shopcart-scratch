"""Sales tax by region."""

from decimal import Decimal

from shopcart.money import round_cents

TAX_RATES: dict[str, Decimal] = {
    "CA": Decimal("7.25"),
    "NY": Decimal("4"),
    "TX": Decimal("6.25"),
    "OR": Decimal("0"),
}


def _raw_tax(amount: Decimal, region: str) -> Decimal:
    key = region.strip().upper()
    if key not in TAX_RATES:
        raise ValueError(f"unknown region: {region!r}")
    if amount < 0:
        raise ValueError("amount must not be negative")
    return amount * TAX_RATES[key] / Decimal("100")


def tax_for(amount: Decimal, region: str) -> Decimal:
    """Return the sales tax due on ``amount`` in ``region``, rounded to cents.

    Region codes are case-insensitive and surrounding whitespace is ignored.
    Halves round up. A zero amount (or the 0% region) returns 0.00. A negative
    amount or an unknown region raises ``ValueError``.
    """
    return round_cents(_raw_tax(amount, region))


def total_with_tax(amount: Decimal, region: str) -> Decimal:
    """Return ``amount`` plus its sales tax in ``region``, rounded once at the end.

    A zero amount returns 0.00. A negative amount or an unknown region raises
    ``ValueError``.
    """
    return round_cents(amount + _raw_tax(amount, region))
