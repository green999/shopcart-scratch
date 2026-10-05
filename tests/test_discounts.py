from decimal import Decimal

import pytest

from shopcart.discounts import apply_coupon, apply_percent_discount


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
