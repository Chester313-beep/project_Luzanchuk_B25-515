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
            print(f"Предупреждение: файл {self.file_path} не найден.")
            return iter(())

        with open(self.file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

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

