import pytest
from src.models.data_item import NewsItem

@pytest.fixture
def sample_items():
    return [
        NewsItem(1, "Title1", "content one", source="test", category="cat1"),
        NewsItem(2, "Title2", "another content", source="test", category="cat2"),
        NewsItem(3, "", "   ", source="test", category="cat3"),  # пустой контент
    ]

@pytest.fixture
def async_strategy():
    from src.strategies.async_normalization_strategy import AsyncNormalizationStrategy
    return AsyncNormalizationStrategy()

@pytest.fixture
def sync_strategy():
    from src.strategies.filter_strategy import FilterStrategy
    return FilterStrategy(min_length=5)
