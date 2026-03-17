import pytest
from src.models.data_item import NewsItem

def test_news_item_creation():
    item = NewsItem(1, "Test", "content", source="src", category="cat")
    assert item.id == 1
    assert item.title == "Test"
    assert item.content == "content"
    assert item.metadata["source"] == "src"
    assert item.metadata["category"] == "cat"

def test_str_representation():
    item = NewsItem(1, "Test", "content", source="src", category="cat")
    assert str(item) == "[1] Test (cat)"

def test_repr():
    item = NewsItem(1, "Test", "content")
    assert repr(item) == "NewsItem(id=1, title='Test', content_len=7)"

def test_lt_comparison():
    item1 = NewsItem(1, "A", "short")
    item2 = NewsItem(2, "B", "much longer text")
    assert item1 < item2
    assert not (item2 < item1)

def test_eq_by_id():
    item1 = NewsItem(1, "A", "content")
    item2 = NewsItem(1, "B", "other")
    assert item1 == item2
    item3 = NewsItem(2, "A", "content")
    assert item1 != item3

def test_hash():
    item1 = NewsItem(1, "A", "c")
    item2 = NewsItem(1, "B", "d")
    assert hash(item1) == hash(item2)
    assert len({item1, item2}) == 1
