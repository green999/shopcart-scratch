from decimal import Decimal

import pytest

from shopcart.money import round_cents, to_decimal


def test_to_decimal_accepts_str_and_int():
    assert to_decimal("19.99") == Decimal("19.99")
    assert to_decimal(5) == Decimal("5")


def test_to_decimal_rejects_float():
    with pytest.raises(ValueError):
        to_decimal(19.99)


def test_round_cents_rounds_half_up():
    assert round_cents(Decimal("1.005")) == Decimal("1.01")
    assert round_cents(Decimal("1.004")) == Decimal("1.00")
