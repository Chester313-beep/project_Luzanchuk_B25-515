import pytest
from src.sources.mock_source import DemoNewsSource

def test_demo_source():
    source = DemoNewsSource(name="test_demo")
    items = list(source.fetch())
    assert len(items) == 4
    assert items[0].title == "Первый заголовок"
    assert items[0].metadata["source"] == "test_demo"
