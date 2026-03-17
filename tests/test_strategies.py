import pytest
import asyncio
from src.strategies.normalization_strategy import AsyncNormalizationStrategy
from src.strategies.filter_strategy import FilterStrategy

async def async_iter(items):
    for item in items:
        yield item
        await asyncio.sleep(0)

@pytest.mark.asyncio
async def test_normalization_strategy(sample_items):
    strategy = AsyncNormalizationStrategy()
    result = []
    async for item in strategy.process(async_iter(sample_items)):
        result.append(item)
    assert len(result) == 2
    assert result[0].content == "content one"
    assert result[0].metadata["word_count"] == 2
    assert result[1].content == "another content"
    assert result[1].metadata["word_count"] == 2

@pytest.mark.asyncio
async def test_filter_strategy(sample_items):
    strategy = FilterStrategy(min_length=5)
    result = list(strategy.process(iter(sample_items)))
    assert len(result) == 2
    assert result[0].content == "content one"
    assert result[1].content == "another content"