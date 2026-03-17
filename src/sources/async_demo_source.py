import asyncio

from src.models.data_item import NewsItem
from src.sources.async_base_source import AsyncBaseDataSource


class AsyncDemoNewsSource(AsyncBaseDataSource):
    def __init__(self, name: str = "Async Demo News", source_type: str = "async_demo"):
        super().__init__(name, source_type)

    async def fetch(self):
        items = [
            NewsItem(1, "Первый заголовок",
                     "Это текст первой новости. Он содержит несколько предложений.",
                     source=self.name, category="политика"),
            NewsItem(2, "Вторая новость", "Короткий текст.",
                     source=self.name, category="экономика"),
            NewsItem(3, "", "Пустой заголовок, но контент есть",
                     source=self.name, category="спорт"),
            NewsItem(4, "Пустой контент", "",
                     source=self.name, category="технологии"),
        ]
        for item in items:
            # Имитируем асинхронное чтение с задержкой
            await asyncio.sleep(0.05)  # 50 мс на запись
            yield item
