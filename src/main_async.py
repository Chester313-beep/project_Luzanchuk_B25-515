import asyncio
import time

from src.async_app import AsyncApp
from src.presenters.console_presenter import ConsolePresenter
from src.sources.async_demo_source import AsyncDemoNewsSource
from src.sources.async_file_source import AsyncFileNewsSource
from src.strategies.async_normalization_strategy import AsyncNormalizationStrategy


async def main_async():
    demo_source = AsyncDemoNewsSource(name="Асинхронный демо")
    file_source = AsyncFileNewsSource(file_path="data/news.jsonl", name="Асинхронный файл")

    sources = [demo_source, file_source]
    strategy = AsyncNormalizationStrategy()
    presenter = ConsolePresenter()

    app = AsyncApp(sources, strategy, presenter)
    await app.run()

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main_async())
    elapsed = time.perf_counter() - start
    print(f"Асинхронный режим выполнен за {elapsed:.4f} секунд")
