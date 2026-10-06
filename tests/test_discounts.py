from decimal import Decimal

import pytest

from shopcart.discounts import (
    apply_bulk_discount,
    apply_coupon,
    apply_percent_discount,
    bulk_discount_rate,
)


def test_percent_discount():
    assert apply_percent_discount(Decimal("200.00"), 15) == Decimal("170.00")


def test_percent_discount_boundaries():
    assert apply_percent_discount(Decimal("80.00"), 0) == Decimal("80.00")
    assert apply_percent_discount(Decimal("80.00"), 100) == Decimal("0.00")


def test_percent_discount_rejects_out_of_range():
    with pytest.raises(ValueError):
        apply_percent_discount(Decimal("80.00"), 101)
    with pytest.raises(ValueError):
        apply_percent_discount(Decimal("80.00"), -1)


def test_coupon_is_case_insensitive_and_trimmed():
    assert apply_coupon(Decimal("100.00"), " welcome10 ") == Decimal("90.00")


def test_unknown_coupon_is_rejected():
    with pytest.raises(ValueError):
        apply_coupon(Decimal("100.00"), "NOPE")


def test_bulk_discount_rate_tiers():
    assert bulk_discount_rate(5) == Decimal("0")
    assert bulk_discount_rate(20) == Decimal("5")
    assert bulk_discount_rate(100) == Decimal("10")


def test_apply_bulk_discount():
    assert apply_bulk_discount(Decimal("2.00"), 20) == Decimal("38.00")
    assert apply_bulk_discount(Decimal("2.00"), 100) == Decimal("180.00")


def test_bulk_discount_rate_boundaries():
    assert bulk_discount_rate(9) == Decimal("0")
    assert bulk_discount_rate(10) == Decimal("5")
    assert bulk_discount_rate(49) == Decimal("5")
    assert bulk_discount_rate(50) == Decimal("10")


@pytest.mark.parametrize("quantity", [0, -1])
def test_bulk_discount_rate_rejects_non_positive_quantity(quantity):
    with pytest.raises(ValueError):
        bulk_discount_rate(quantity)


def test_percent_discount_rejects_float_percent():
    with pytest.raises(ValueError):
        apply_percent_discount(Decimal("80.00"), 12.5)


def test_percent_discount_rounds_half_up():
    assert apply_percent_discount(Decimal("0.05"), 10) == Decimal("0.05")
    assert apply_percent_discount(Decimal("0.15"), 50) == Decimal("0.08")


def test_percent_discount_on_zero_amount():
    assert apply_percent_discount(Decimal("0"), 50) == Decimal("0.00")


def test_every_coupon_applies_its_rate():
    assert apply_coupon(Decimal("100.00"), "SPRING25") == Decimal("75.00")
    assert apply_coupon(Decimal("100.00"), "WELCOME10") == Decimal("90.00")
