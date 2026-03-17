import json
import os

from src.models.data_item import NewsItem
from src.sources.base_source import BaseDataSource


class FileNewsSource(BaseDataSource):
    def __init__(self, file_path: str, name: str = "File News", source_type: str = "file"):
        super().__init__(name, source_type)
        self.file_path = file_path
    def fetch(self):
        if not os.path.exists(self.file_path):
            print(f"Предупреждение: файл {self.file_path} не найден. Возвращаем пустой список.")
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения файла {self.file_path}: {e}. Возвращаем пустой список.")
            return []
        items = []
        for idx, item_data in enumerate(data, start=1):
            title = item_data.get('title', '')
            content = item_data.get('content', '')
            category = item_data.get('category', 'без категории')
            item = NewsItem(
                id=idx,
                title=title,
                content=content,
                source=self.name,
                category=category,
            )
            items.append(item)
        return items
