from decimal import Decimal

import pytest

from shopcart import shipping_cost


@pytest.mark.parametrize(
    ("method", "expected"),
    [("standard", "5.99"), ("express", "14.99"), ("pickup", "0.00")],
)
def test_base_rates(method, expected):
    assert shipping_cost(Decimal("10.00"), method) == Decimal(expected)


def test_default_method_is_standard():
    assert shipping_cost(Decimal("10.00")) == Decimal("5.99")


@pytest.mark.parametrize(
    ("subtotal", "expected"),
    [("49.99", "5.99"), ("50.00", "0.00"), ("50.01", "0.00")],
)
def test_standard_free_threshold(subtotal, expected):
    assert shipping_cost(Decimal(subtotal), "standard") == Decimal(expected)


@pytest.mark.parametrize("subtotal", ["49.99", "50.00", "50.01"])
def test_express_and_pickup_ignore_threshold(subtotal):
    assert shipping_cost(Decimal(subtotal), "express") == Decimal("14.99")
    assert shipping_cost(Decimal(subtotal), "pickup") == Decimal("0.00")


def test_zero_subtotal_is_valid():
    assert shipping_cost(Decimal("0"), "standard") == Decimal("5.99")


@pytest.mark.parametrize("method", ["EXPRESS", "  express  ", " ExPress\t"])
def test_method_case_and_whitespace(method):
    assert shipping_cost(Decimal("10.00"), method) == Decimal("14.99")


def test_unknown_method_rejected():
    with pytest.raises(ValueError):
        shipping_cost(Decimal("10.00"), "drone")


def test_negative_subtotal_rejected():
    with pytest.raises(ValueError):
        shipping_cost(Decimal("-0.01"))
