from src.models.data_item import NewsItem
from src.sources.base_source import BaseDataSource


class DemoNewsSource(BaseDataSource):
    def __init__(self, name: str = "Demo News", source_type: str = "demo"):
        super().__init__(name, source_type)

    def fetch(self):
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
            yield item
