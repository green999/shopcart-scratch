"""The cart and its line items."""

from dataclasses import dataclass
from decimal import Decimal

from shopcart.discounts import apply_bulk_discount
from shopcart.money import round_cents, to_decimal


@dataclass
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int

    @property
    def total(self) -> Decimal:
        """Unrounded line total."""
        return self.unit_price * self.quantity


class Cart:
    """A collection of line items keyed by SKU."""

    def __init__(self) -> None:
        self._items: dict[str, LineItem] = {}

    def add_item(self, sku: str, unit_price: Decimal | int | str, quantity: int = 1) -> None:
        """Add ``quantity`` of ``sku``.

        Adding a SKU that is already in the cart increases its quantity.
        """
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        price = to_decimal(unit_price)
        if price < 0:
            raise ValueError("unit_price must not be negative")
        self._items[sku] = LineItem(sku=sku, unit_price=price, quantity=quantity)

    def remove_item(self, sku: str, quantity: int | None = None) -> None:
        """Remove ``quantity`` of ``sku``, or the whole line when ``quantity`` is None."""
        if sku not in self._items:
            raise ValueError(f"{sku} is not in the cart")
        item = self._items[sku]
        if quantity is None or quantity >= item.quantity:
            del self._items[sku]
            return
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        item.quantity -= quantity

    @property
    def items(self) -> list[LineItem]:
        return list(self._items.values())

    def quantity_of(self, sku: str) -> int:
        """Quantity of ``sku`` in the cart, 0 when absent."""
        item = self._items.get(sku)
        return item.quantity if item else 0

    def subtotal(self) -> Decimal:
        """Sum of line totals, rounded to cents. An empty cart is 0.00."""
        return round_cents(sum((item.total for item in self._items.values()), Decimal("0")))

    def total_with_bulk_discount(self) -> Decimal:
        """Sum of line totals after each line's bulk discount, rounded to cents."""
        return round_cents(
            sum(
                (apply_bulk_discount(item.unit_price, item.quantity) for item in self.items),
                Decimal("0"),
            )
        )
