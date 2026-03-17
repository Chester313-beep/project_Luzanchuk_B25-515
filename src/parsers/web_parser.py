import json
import os

import requests


class WebNewsParser:

    def __init__(self, output_file: str = "data/web_news.jsonl"):
        self.output_file = output_file
        self.api_url = "https://jsonplaceholder.typicode.com/posts"

    def fetch_and_save(self):
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return False
        except ValueError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return False

        if not data:
            print("API вернуло пустой ответ.")
            return False
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for idx, item in enumerate(data, start=1):
                    record = {
                        "title": item.get("title", ""),
                        "content": item.get("body", ""),
                        "category": "web",
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
            print(f"Данные успешно сохранены в {self.output_file}")
            return True
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")
            return False
