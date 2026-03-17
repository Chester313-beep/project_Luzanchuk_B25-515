import asyncio
import time

from src.hybrid_app import HybridApp
from src.presenters.console_presenter import ConsolePresenter
from src.sources.async_demo_source import AsyncDemoNewsSource
from src.sources.async_file_source import AsyncFileNewsSource
from src.strategies.async_normalization_strategy import AsyncNormalizationStrategy


async def run_app(use_executor: bool):
    demo_source = AsyncDemoNewsSource(name="Async Demo")
    file_source = AsyncFileNewsSource(file_path="data/news.jsonl", name="Async File")
    sources = [demo_source, file_source]

    strategy = AsyncNormalizationStrategy()
    presenter = ConsolePresenter()

    app = HybridApp(sources, strategy, presenter, use_executor=use_executor, executor_type='thread')
    await app.run()
    app.shutdown()

if __name__ == "__main__":
    print("=== Чистый асинхронный режим (без executor) ===")
    start = time.perf_counter()
    asyncio.run(run_app(use_executor=False))
    elapsed_async = time.perf_counter() - start
    print(f"Время выполнения (async only): {elapsed_async:.4f} сек\n")

    print("=== Гибридный режим (async + thread executor) ===")
    start = time.perf_counter()
    asyncio.run(run_app(use_executor=True))
    elapsed_hybrid = time.perf_counter() - start
    print(f"Время выполнения (hybrid): {elapsed_hybrid:.4f} сек")
