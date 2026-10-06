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


def test_to_decimal_rejects_bool():
    with pytest.raises(ValueError):
        to_decimal(True)


def test_to_decimal_passes_decimal_through():
    assert to_decimal(Decimal("1.50")) == Decimal("1.50")


@pytest.mark.parametrize("value", ["abc", "", "NaN", "Infinity", "-Infinity"])
def test_to_decimal_rejects_non_numeric_and_non_finite(value):
    with pytest.raises(ValueError):
        to_decimal(value)


def test_round_cents_negative_halves_round_away_from_zero():
    assert round_cents(Decimal("-1.005")) == Decimal("-1.01")


def test_round_cents_zero():
    assert round_cents(Decimal("0")) == Decimal("0.00")
