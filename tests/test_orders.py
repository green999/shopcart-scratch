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


def test_single_item_single_page():
    page = paginate([1], page=1, per_page=20)
    assert page.total_pages == 1
    assert page.items == [1]


def test_page_attributes_are_reported():
    page = paginate(list(range(45)), page=2, per_page=20)
    assert (page.page, page.per_page, page.total_items) == (2, 20, 45)
    assert page.has_next
    assert page.has_previous


def test_empty_sequence_rejects_page_two():
    with pytest.raises(ValueError):
        paginate([], page=2)


def test_exact_multiple_of_per_page_has_no_extra_page():
    page = paginate(list(range(40)), page=2, per_page=20)
    assert page.total_pages == 2
    assert not page.has_next


def test_page_past_the_end_rejected_for_exact_multiple():
    with pytest.raises(ValueError):
        paginate(list(range(40)), page=3, per_page=20)
