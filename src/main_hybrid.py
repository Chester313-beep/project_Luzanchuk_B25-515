
from src.hybrid_app import HybridApp
from src.presenters.console_presenter import ConsolePresenter
from src.sources.async_demo_source import AsyncDemoNewsSource
from src.sources.async_file_source import AsyncFileNewsSource
from src.sources.async_web_source import AsyncWebNewsSource
from src.strategies.async_normalization_strategy import AsyncNormalizationStrategy


async def run_app(use_executor: bool):
    demo_source = AsyncDemoNewsSource(name="Async Demo")
    file_source = AsyncFileNewsSource(file_path="data/news.jsonl", name="Async File")
    web_source = AsyncWebNewsSource(
        base_url="https://jsonplaceholder.typicode.com",
        name="JSONPlaceholder News",
        max_concurrent=2,
        max_retries=3,
        request_delay=0.3
    )

    sources = [demo_source, file_source, web_source]  # теперь три источника

    strategy = AsyncNormalizationStrategy()
    presenter = ConsolePresenter()

    app = HybridApp(sources, strategy, presenter, use_executor=use_executor, executor_type='thread')
    await app.run()
    app.shutdown()
