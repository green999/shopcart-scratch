from decimal import Decimal

import pytest

from shopcart.cart import Cart


def test_empty_cart_subtotal_is_zero():
    assert Cart().subtotal() == Decimal("0.00")


def test_subtotal_sums_line_totals():
    cart = Cart()
    cart.add_item("pen", "1.50", 4)
    cart.add_item("notebook", "3.25", 2)
    assert cart.subtotal() == Decimal("12.50")


def test_add_same_item_accumulates():
    cart = Cart()
    cart.add_item("pen", "1.50", 2)
    cart.add_item("pen", "1.50", 3)
    assert cart.quantity_of("pen") == 5
    assert cart.subtotal() == Decimal("7.50")


def test_add_same_item_with_different_price_is_rejected():
    cart = Cart()
    cart.add_item("pen", "1.50")
    with pytest.raises(ValueError):
        cart.add_item("pen", "1.75")


def test_add_item_rejects_non_positive_quantity():
    with pytest.raises(ValueError):
        Cart().add_item("pen", "1.50", 0)


def test_remove_part_of_a_line():
    cart = Cart()
    cart.add_item("pen", "1.50", 5)
    cart.remove_item("pen", 2)
    assert cart.quantity_of("pen") == 3


def test_remove_whole_line():
    cart = Cart()
    cart.add_item("pen", "1.50", 5)
    cart.remove_item("pen")
    assert cart.items == []


def test_remove_missing_item_is_rejected():
    with pytest.raises(ValueError):
        Cart().remove_item("pen")


def test_total_with_bulk_discount():
    cart = Cart()
    cart.add_item("pen", "1.00", 20)
    cart.add_item("notebook", "3.00", 2)
    assert cart.total_with_bulk_discount() == Decimal("25.00")


def test_total_with_bulk_discount_empty_cart():
    assert Cart().total_with_bulk_discount() == Decimal("0.00")


def test_total_with_bulk_discount_exactly_ten_units():
    cart = Cart()
    cart.add_item("pen", "1.00", 10)
    assert cart.total_with_bulk_discount() == Decimal("9.50")


def test_total_with_bulk_discount_rounds_only_once():
    cart = Cart()
    for sku in ("a", "b", "c"):
        cart.add_item(sku, "0.01", 10)
    assert cart.total_with_bulk_discount() == Decimal("0.29")


def _cart_with_subtotal(amount: str) -> Cart:
    cart = Cart()
    cart.add_item("thing", amount, 1)
    return cart


def test_total_adds_shipping_below_threshold():
    cart = _cart_with_subtotal("49.99")
    assert cart.total() == Decimal("55.98")
    assert cart.total("express") == Decimal("64.98")
    assert cart.total("pickup") == Decimal("49.99")


def test_total_standard_free_at_threshold():
    assert _cart_with_subtotal("50.00").total() == Decimal("50.00")
    assert _cart_with_subtotal("50.01").total() == Decimal("50.01")


def test_total_express_not_free_above_threshold():
    assert _cart_with_subtotal("50.00").total("express") == Decimal("64.99")


def test_total_method_is_case_and_whitespace_insensitive():
    assert _cart_with_subtotal("10.00").total(" EXPRESS ") == Decimal("24.99")


def test_total_unknown_method_rejected():
    with pytest.raises(ValueError):
        _cart_with_subtotal("10.00").total("drone")


@pytest.mark.parametrize("method", ["standard", "express", "pickup"])
def test_empty_cart_total_is_zero_for_every_method(method):
    assert Cart().total(method) == Decimal("0.00")
