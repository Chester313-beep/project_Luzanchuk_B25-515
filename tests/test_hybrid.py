import pytest
from unittest.mock import MagicMock
from src.models.data_item import NewsItem
from src.hybrid_app import HybridApp
from src.sources.async_base_source import AsyncBaseDataSource
from src.strategies.normalization_strategy import AsyncNormalizationStrategy
from src.presenters.console_presenter import ConsolePresenter

class MockSource(AsyncBaseDataSource):
    def __init__(self, name, items):
        super().__init__(name, "mock")
        self.items = items
    async def fetch(self):
        for item in self.items:
            yield item

@pytest.mark.asyncio
async def test_hybrid_app_without_executor():
    items = [
        NewsItem(1, "t1", "content one", source="src1"),
        NewsItem(2, "t2", "another", source="src2"),
    ]
    sources = [MockSource("src1", items[:1]), MockSource("src2", items[1:])]
    strategy = AsyncNormalizationStrategy()
    mock_presenter = MagicMock()
    app = HybridApp(sources, strategy, mock_presenter, use_executor=False)
    await app.run()
    assert mock_presenter.display_results.called
