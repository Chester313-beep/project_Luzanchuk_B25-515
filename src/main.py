from src.app import App
from src.config.config import AppConfig
from src.factories.source_factory import SourceFactory
from src.presenters.console_presenter import ConsolePresenter
from src.strategies.filter_strategy import FilterStrategy
from src.strategies.normalization_strategy import NormalizationStrategy


def main():
    config = AppConfig()
    config.load({
        "sources": [
            {"type": "demo", "name": "Демо-новости"},
            {"type": "file", "file_path": "data/news.jsonl", "name": "Новости из файла"}
        ],
        "strategy": "normalization"
    })
    sources = []
    for source_cfg in config.sources:
        source = SourceFactory.create_source(source_cfg)
        sources.append(source)
    strategy_name = config.strategy
    if strategy_name == "normalization":
        strategy = NormalizationStrategy()
    elif strategy_name == "filter":
        strategy = FilterStrategy(min_length=5)
    else:
        raise ValueError(f"Неизвестная стратегия: {strategy_name}")
    presenter = ConsolePresenter()
    app = App(sources, strategy, presenter)
    app.run()

if __name__ == "__main__":
    main()
