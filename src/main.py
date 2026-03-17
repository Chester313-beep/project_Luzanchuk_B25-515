
import concurrent.futures
import time
import asyncio
from src.runner import AppRunner
from src.config.config import AppConfig
from src.factories.source_factory import SourceFactory
from src.parsers.web_parser import WebNewsParser
from src.presenters.console_presenter import ConsolePresenter
from src.strategies.filter_strategy import FilterStrategy
from src.strategies.normalization_strategy import NormalizationStrategy

if __name__ == "__main__":
    runner = AppRunner({
        "sources": [
            {"type": "demo", "name": "Демо-новости"},
            {"type": "file", "file_path": "data/news.jsonl", "name": "Новости из файла"},
            {"type": "web", "base_url": "https://jsonplaceholder.typicode.com", "name": "Веб-новости"}
        ],
        "strategy": "normalization",
        "mode": "async"
    })
    asyncio.run(runner.run_and_print())
def process_source(source, strategy):
    items = source.fetch()
    return list(strategy.process(items))

def main():
    config = AppConfig()
    config.load({
        "sources": [
            {"type": "demo", "name": "Демо-новости"},
            {"type": "file", "file_path": "data/news.jsonl", "name": "Новости из файла"},
            {"type": "file", "file_path": "data/web_news.jsonl", "name": "Новости из веб-API"}
        ],
        "strategy": "normalization",
        "mode": "threads"
    })
    parser = WebNewsParser(output_file="data/web_news.jsonl")
    parser.fetch_and_save()
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
    mode = config.processing_mode
    print(f"Режим обработки: {mode}")

    start_time = time.perf_counter()

    if mode == "sequential":
        all_processed = []
        for source in sources:
            all_processed.extend(process_source(source, strategy))
    elif mode == "threads":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_source, source, strategy) for source in sources]
            all_processed = []
            for future in concurrent.futures.as_completed(futures):
                all_processed.extend(future.result())
    elif mode == "processes":
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(process_source, source, strategy) for source in sources]
            all_processed = []
            for future in concurrent.futures.as_completed(futures):
                all_processed.extend(future.result())
    else:
        raise ValueError(f"Неизвестный режим: {mode}")
    received_stats = {}
    for item in all_processed:
        src = item.metadata.get('source', 'unknown')
        received_stats[src] = received_stats.get(src, 0) + 1
    elapsed = time.perf_counter() - start_time
    print(f"Время обработки: {elapsed:.4f} секунд")
    presenter.display_results(iter(all_processed), received_stats)
    print("\n--- Вывод по производительности ---")
    print("Последовательный режим подходит для малых объёмов данных или когда важна простота.")
    print("Потоки (threads) эффективны при наличии операций ввода-вывода (ожидание ответов от источников), но в нашем случае все источники локальные, поэтому прирост может быть незначительным.")
    print("Процессы (processes) позволяют задействовать несколько ядер CPU для параллельных вычислений, что даёт ускорение при интенсивной обработке (например, сложные преобразования текста).")
    print("В данном проекте с текущим объёмом данных и простой обработкой разница может быть мала. Для реального эффекта нужно увеличить объём или сложность обработки.")
if __name__ == "__main__":
    main()
