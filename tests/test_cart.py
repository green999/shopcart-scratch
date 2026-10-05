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
