from decimal import Decimal

import pytest

from shopcart import tax_for, total_with_tax


@pytest.mark.parametrize(
    ("region", "expected"),
    [("CA", "7.25"), ("NY", "4.00"), ("TX", "6.25"), ("OR", "0.00")],
)
def test_tax_for_each_region(region, expected):
    assert tax_for(Decimal("100.00"), region) == Decimal(expected)


def test_zero_rate_region_has_no_tax():
    assert tax_for(Decimal("999.99"), "OR") == Decimal("0.00")
    assert total_with_tax(Decimal("999.99"), "OR") == Decimal("999.99")


@pytest.mark.parametrize("region", ["ca", " CA ", "\tcA\n"])
def test_region_case_and_whitespace(region):
    assert tax_for(Decimal("100.00"), region) == Decimal("7.25")


def test_zero_amount():
    assert tax_for(Decimal("0"), "CA") == Decimal("0.00")
    assert total_with_tax(Decimal("0"), "CA") == Decimal("0.00")


def test_rounding_ca_10_07():
    assert tax_for(Decimal("10.07"), "CA") == Decimal("0.73")


def test_halves_round_up():
    assert tax_for(Decimal("0.10"), "NY") == Decimal("0.00")
    assert tax_for(Decimal("0.125"), "NY") == Decimal("0.01")
    assert tax_for(Decimal("20.00"), "CA") == Decimal("1.45")


def test_total_with_tax():
    assert total_with_tax(Decimal("100.00"), "CA") == Decimal("107.25")
    assert total_with_tax(Decimal("10.07"), "CA") == Decimal("10.80")


def test_total_with_tax_rounds_once():
    assert total_with_tax(Decimal("0.125"), "NY") == Decimal("0.13")


def test_unknown_region_rejected():
    with pytest.raises(ValueError):
        tax_for(Decimal("10.00"), "ZZ")
    with pytest.raises(ValueError):
        total_with_tax(Decimal("10.00"), "ZZ")


def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        tax_for(Decimal("-0.01"), "CA")
    with pytest.raises(ValueError):
        total_with_tax(Decimal("-0.01"), "CA")
