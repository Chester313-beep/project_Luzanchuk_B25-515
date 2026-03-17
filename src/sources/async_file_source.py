import asyncio
import json
import os

from src.models.data_item import NewsItem
from src.sources.async_base_source import AsyncBaseDataSource


class AsyncFileNewsSource(AsyncBaseDataSource):
    def __init__(self, file_path: str, name: str = "Async File News", source_type: str = "async_file"):
        super().__init__(name, source_type)
        self.file_path = file_path

    async def fetch(self):
        if not os.path.exists(self.file_path):
            print(f"Предупреждение: файл {self.file_path} не найден.")
            return

        with open(self.file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                await asyncio.sleep(0.03)

                title = data.get('title', '')
                content = data.get('content', '')
                category = data.get('category', 'без категории')
                yield NewsItem(
                    id=idx,
                    title=title,
                    content=content,
                    source=self.name,
                    category=category
                )
