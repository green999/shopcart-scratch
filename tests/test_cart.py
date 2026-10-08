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


def test_add_item_rejects_negative_unit_price():
    with pytest.raises(ValueError):
        Cart().add_item("pen", "-0.01")


def test_add_item_accepts_zero_unit_price():
    cart = Cart()
    cart.add_item("freebie", "0.00", 1)
    assert cart.subtotal() == Decimal("0.00")


@pytest.mark.parametrize("quantity", [0, -1])
def test_remove_item_rejects_non_positive_quantity(quantity):
    cart = Cart()
    cart.add_item("pen", "1.50", 5)
    with pytest.raises(ValueError):
        cart.remove_item("pen", quantity)
    assert cart.quantity_of("pen") == 5


def test_remove_item_quantity_equal_to_line_removes_it():
    cart = Cart()
    cart.add_item("pen", "1.50", 5)
    cart.remove_item("pen", 5)
    assert cart.quantity_of("pen") == 0


def test_quantity_of_missing_sku_is_zero():
    assert Cart().quantity_of("nope") == 0


def test_subtotal_rounds_half_up_once():
    cart = Cart()
    cart.add_item("a", "0.005", 1)
    assert cart.subtotal() == Decimal("0.01")


def _three_item_cart() -> Cart:
    cart = Cart()
    cart.add_item("pen", "1.50", 2)
    cart.add_item("notebook", "0.10", 3)
    cart.add_item("bag", "19.99", 1)
    return cart


def test_to_dict_shape_and_order():
    assert _three_item_cart().to_dict() == {
        "items": [
            {"sku": "pen", "unit_price": "1.50", "quantity": 2},
            {"sku": "notebook", "unit_price": "0.10", "quantity": 3},
            {"sku": "bag", "unit_price": "19.99", "quantity": 1},
        ]
    }


def test_to_dict_is_json_serializable():
    import json

    data = _three_item_cart().to_dict()
    assert json.loads(json.dumps(data)) == data


def test_round_trip_with_several_items():
    cart = _three_item_cart()
    rebuilt = Cart.from_dict(cart.to_dict())
    assert rebuilt.items == cart.items
    assert rebuilt.subtotal() == cart.subtotal()
    assert [item.sku for item in rebuilt.items] == ["pen", "notebook", "bag"]


def test_round_trip_through_json():
    import json

    cart = _three_item_cart()
    rebuilt = Cart.from_dict(json.loads(json.dumps(cart.to_dict())))
    assert rebuilt.items == cart.items


def test_empty_cart_round_trips():
    assert Cart().to_dict() == {"items": []}
    assert Cart.from_dict(Cart().to_dict()).items == []


def test_price_survives_exactly():
    cart = Cart()
    cart.add_item("dime", "0.10", 1)
    rebuilt = Cart.from_dict(cart.to_dict())
    assert str(rebuilt.items[0].unit_price) == "0.10"
    assert rebuilt.items[0].unit_price == Decimal("0.10")


def test_from_dict_ignores_unknown_keys():
    data = {
        "version": 2,
        "items": [{"sku": "pen", "unit_price": "1.50", "quantity": 2, "note": "x"}],
    }
    assert Cart.from_dict(data).quantity_of("pen") == 2


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"items": [{"unit_price": "1.50", "quantity": 1}]},
        {"items": [{"sku": "pen", "quantity": 1}]},
        {"items": [{"sku": "pen", "unit_price": "1.50"}]},
        {"items": None},
        {"items": [None]},
        None,
    ],
)
def test_from_dict_rejects_missing_keys_and_malformed_data(data):
    with pytest.raises(ValueError):
        Cart.from_dict(data)


def test_from_dict_rejects_float_price():
    with pytest.raises(ValueError):
        Cart.from_dict({"items": [{"sku": "pen", "unit_price": 1.5, "quantity": 1}]})


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "2"])
def test_from_dict_rejects_bad_quantity(quantity):
    with pytest.raises(ValueError):
        Cart.from_dict({"items": [{"sku": "pen", "unit_price": "1.50", "quantity": quantity}]})


def test_from_dict_applies_add_item_validation():
    with pytest.raises(ValueError):
        Cart.from_dict({"items": [{"sku": "pen", "unit_price": "-1.00", "quantity": 1}]})
    with pytest.raises(ValueError):
        Cart.from_dict(
            {
                "items": [
                    {"sku": "pen", "unit_price": "1.50", "quantity": 1},
                    {"sku": "pen", "unit_price": "1.75", "quantity": 1},
                ]
            }
        )


@pytest.mark.parametrize("sku", [5, None, [], 1.5])
def test_from_dict_rejects_non_string_sku(sku):
    with pytest.raises(ValueError):
        Cart.from_dict({"items": [{"sku": sku, "unit_price": "1.50", "quantity": 1}]})


@pytest.mark.parametrize("price", [None, [], {}, "abc", "NaN"])
def test_from_dict_rejects_invalid_price_with_value_error(price):
    with pytest.raises(ValueError):
        Cart.from_dict({"items": [{"sku": "pen", "unit_price": price, "quantity": 1}]})


def test_from_dict_accepts_int_price():
    cart = Cart.from_dict({"items": [{"sku": "pen", "unit_price": 3, "quantity": 1}]})
    assert cart.subtotal() == Decimal("3.00")


def test_add_99_at_once_is_allowed():
    cart = Cart()
    cart.add_item("pen", "1.50", 99)
    assert cart.quantity_of("pen") == 99


def test_add_100_at_once_is_rejected():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item("pen", "1.50", 100)
    assert cart.quantity_of("pen") == 0
    assert cart.items == []


def test_add_to_reach_exactly_99_is_allowed():
    cart = Cart()
    cart.add_item("pen", "1.50", 95)
    cart.add_item("pen", "1.50", 4)
    assert cart.quantity_of("pen") == 99


def test_add_beyond_99_is_rejected_and_cart_unchanged():
    cart = Cart()
    cart.add_item("pen", "1.50", 95)
    with pytest.raises(ValueError):
        cart.add_item("pen", "1.50", 5)
    assert cart.quantity_of("pen") == 95


def test_max_quantity_error_names_sku_and_limit():
    cart = Cart()
    with pytest.raises(ValueError, match=r"pen.*99"):
        cart.add_item("pen", "1.50", 100)
