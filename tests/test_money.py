from decimal import Decimal

import pytest

from shopcart.money import format_money, parse_money, round_cents, to_decimal


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


@pytest.mark.parametrize(
    ("currency", "symbol"), [("USD", "$"), ("EUR", "€"), ("GBP", "£"), ("eur", "€")]
)
def test_format_money_currencies(currency, symbol):
    assert format_money(Decimal("1234.5"), currency) == f"{symbol}1,234.50"


def test_format_money_default_is_usd():
    assert format_money(Decimal("1234.5")) == "$1,234.50"


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("999.99", "$999.99"),
        ("1000", "$1,000.00"),
        ("1000000", "$1,000,000.00"),
    ],
)
def test_format_money_grouping(amount, expected):
    assert format_money(Decimal(amount)) == expected


def test_format_money_negative_and_zero():
    assert format_money(Decimal("-5")) == "-$5.00"
    assert format_money(Decimal("0")) == "$0.00"


def test_format_money_rounds_half_up_and_never_negative_zero():
    assert format_money(Decimal("-0.004")) == "$0.00"
    assert format_money(Decimal("1.005")) == "$1.01"
    assert format_money(Decimal("-1.005")) == "-$1.01"


def test_format_money_unknown_currency():
    with pytest.raises(ValueError):
        format_money(Decimal("1"), "JPY")


def test_parse_money_valid():
    assert parse_money(" -$1,234.50 ") == Decimal("-1234.50")
    assert parse_money("€5") == Decimal("5")
    assert parse_money("+£0.99") == Decimal("0.99")
    assert parse_money("1000000") == Decimal("1000000")


@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP"])
@pytest.mark.parametrize("amount", ["0", "-0.004", "999.99", "1000", "1234.565", "-1000000", "-5"])
def test_round_trip(currency, amount):
    x = Decimal(amount)
    assert parse_money(format_money(x, currency)) == round_cents(x)


@pytest.mark.parametrize(
    "text", ["", "   ", "abc", "$12.3.4", "$", "-", "1,23", "12,3456", "$$5", "¥5"]
)
def test_parse_money_invalid(text):
    with pytest.raises(ValueError):
        parse_money(text)
