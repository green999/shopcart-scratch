import pytest

from shopcart.orders import paginate


def test_first_page():
    page = paginate(list(range(45)), page=1, per_page=20)
    assert page.items == list(range(20))
    assert page.total_pages == 3
    assert page.has_next
    assert not page.has_previous


def test_last_partial_page():
    page = paginate(list(range(45)), page=3, per_page=20)
    assert page.items == list(range(40, 45))
    assert not page.has_next
    assert page.has_previous


def test_empty_sequence_has_one_empty_page():
    page = paginate([], page=1, per_page=20)
    assert page.items == []
    assert page.total_pages == 1
    assert not page.has_next


def test_page_past_the_end_is_rejected():
    with pytest.raises(ValueError):
        paginate(list(range(45)), page=4, per_page=20)


def test_invalid_arguments_are_rejected():
    with pytest.raises(ValueError):
        paginate([1, 2, 3], page=0)
    with pytest.raises(ValueError):
        paginate([1, 2, 3], per_page=0)
