from src.models.data_item import NewsItem


class MockNewsSource:
    def __init__(self, name: str, source_type: str = "mock"):
        self.name = name
        self.source_type = source_type
    def fetch(self):
        return [
    NewsItem(
        1,
        "Первый заголовок",
        "Это текст первой новости. Он содержит несколько предложений.",
        source=self.name,
        category="политика",
    ),
    NewsItem(
        2,
        "Вторая новость",
        "Короткий текст.",
        source=self.name,
        category="экономика",
    ),
    NewsItem(
        3,
        "",
        "Пустой заголовок, но контент есть",
        source=self.name,
        category="спорт",
    ),
    NewsItem(
        4,
        "Пустой контент",
        "",
        source=self.name,
        category="технологии",
    ),
]