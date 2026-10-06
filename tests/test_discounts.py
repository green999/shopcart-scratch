from dataclasses import FrozenInstanceError
from datetime import date, datetime
from decimal import Decimal

import pytest

from shopcart.discounts import (
    COUPONS,
    Coupon,
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


TODAY = date(2026, 6, 1)


def test_coupon_dataclass_defaults_and_frozen():
    coupon = Coupon(percent=Decimal("5"))
    assert coupon.min_spend == Decimal("0")
    assert coupon.expires_on is None
    with pytest.raises(FrozenInstanceError):
        coupon.percent = Decimal("6")


def test_registered_coupons():
    assert COUPONS["WELCOME10"] == Coupon(percent=Decimal("10"))
    assert COUPONS["SPRING25"] == Coupon(
        percent=Decimal("25"), min_spend=Decimal("40.00"), expires_on=date(2026, 12, 31)
    )


def test_welcome10_has_no_conditions():
    assert apply_coupon(Decimal("0.00"), "WELCOME10", today=date(2099, 1, 1)) == Decimal("0.00")
    assert apply_coupon(Decimal("1.00"), "WELCOME10", today=date(2099, 1, 1)) == Decimal("0.90")


def test_spring25_below_minimum_rejected():
    with pytest.raises(ValueError, match="minimum spend of 40.00"):
        apply_coupon(Decimal("39.99"), "SPRING25", today=TODAY)


def test_spring25_at_minimum_qualifies():
    assert apply_coupon(Decimal("40.00"), "SPRING25", today=TODAY) == Decimal("30.00")


def test_spring25_above_minimum_qualifies():
    assert apply_coupon(Decimal("40.01"), "SPRING25", today=TODAY) == Decimal("30.01")


def test_spring25_day_before_expiry_valid():
    assert apply_coupon(Decimal("100.00"), "SPRING25", today=date(2026, 12, 30)) == Decimal("75.00")


def test_spring25_on_expiry_date_valid():
    assert apply_coupon(Decimal("100.00"), "SPRING25", today=date(2026, 12, 31)) == Decimal("75.00")


def test_spring25_day_after_expiry_rejected():
    with pytest.raises(ValueError, match="expired on 2026-12-31"):
        apply_coupon(Decimal("100.00"), "SPRING25", today=date(2027, 1, 1))


def test_expired_and_below_minimum_reports_expiry():
    with pytest.raises(ValueError, match="expired"):
        apply_coupon(Decimal("1.00"), "SPRING25", today=date(2027, 1, 1))


def test_today_defaults_to_date_today(monkeypatch):
    class FixedDate(date):
        @classmethod
        def today(cls):
            return cls(2027, 1, 1)

    monkeypatch.setattr("shopcart.discounts.date", FixedDate)
    with pytest.raises(ValueError, match="expired"):
        apply_coupon(Decimal("100.00"), "SPRING25")


@pytest.mark.parametrize("code", ["WELCOME10", "SPRING25"])
def test_negative_amount_rejected_with_clear_message(code):
    with pytest.raises(ValueError, match="amount must not be negative"):
        apply_coupon(Decimal("-0.01"), code, today=TODAY)


@pytest.mark.parametrize("amount", [Decimal("NaN"), Decimal("Infinity")])
def test_non_finite_amount_rejected(amount):
    with pytest.raises(ValueError, match="finite"):
        apply_coupon(amount, "WELCOME10", today=TODAY)


def test_datetime_today_is_treated_as_its_date():
    assert apply_coupon(
        Decimal("100.00"), "SPRING25", today=datetime(2026, 12, 31, 23, 59)
    ) == Decimal("75.00")
    with pytest.raises(ValueError, match="expired"):
        apply_coupon(Decimal("100.00"), "SPRING25", today=datetime(2027, 1, 1, 0, 0))
