import asyncio
from src.runner import AppRunner

def main():
    runner = AppRunner({
        "sources": [
            {"type": "demo", "name": "Демо-новости"},
            {"type": "file", "file_path": "data/news.jsonl", "name": "Новости из файла"},
            {"type": "web", "base_url": "https://jsonplaceholder.typicode.com", "name": "Веб-новости"}
        ],
        "strategy": "normalization",
        "mode": "threads"
    })
    asyncio.run(runner.run_and_print())

if __name__ == "__main__":
    main()
