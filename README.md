# shopcart

A small shopping-cart library: money rounding, a cart, discounts and order-history pagination.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
```

## Layout

| Path | What it holds |
| --- | --- |
| `shopcart/money.py` | Decimal helpers and cent rounding |
| `shopcart/cart.py` | `Cart` and `LineItem` |
| `shopcart/discounts.py` | Percentage and coupon discounts |
| `shopcart/orders.py` | Order-history pagination |
| `shopcart/shipping.py` | Shipping cost by method and subtotal |
| `shopcart/tax.py` | Sales tax by region |
| `tests/` | pytest suite |
