"""Order-history pagination."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: list[T]
    page: int
    per_page: int
    total_items: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1


def paginate(items: Sequence[T], page: int = 1, per_page: int = 20) -> Page[T]:
    """Return page ``page`` (1-based) of ``items``, ``per_page`` to a page.

    An empty sequence has one empty page. Asking for a page past the end
    raises ``ValueError``.
    """
    if page < 1:
        raise ValueError("page must be 1 or greater")
    if per_page < 1:
        raise ValueError("per_page must be 1 or greater")
    total_items = len(items)
    total_pages = max(1, -(-total_items // per_page))
    if page > total_pages:
        raise ValueError(f"page {page} is past the last page ({total_pages})")
    start = (page - 1) * per_page
    return Page(
        items=list(items[start : start + per_page]),
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
    )
