from src.processors.text_processor import NewsProcessor
from src.sources.mock_source import MockNewsSource


class App:
    def __init__(self):
        self.source = MockNewsSource(name="Demo News", source_type="mock")
        self.processor = NewsProcessor()
    def run(self):
        items = self.source.fetch()
        if not items:
            print("Источник не вернул данных.")
            return
        print(f"Получено записей: {len(items)}")
        processed_items = self.processor.process(items)
        self._display_results(processed_items, original_count=len(items))

    def _display_results(self, items, original_count):
        filtered = original_count - len(items)
        print(f"После обработки осталось записей: {len(items)} "
        f"(отфильтровано {filtered})")
        if not items:
            print("Нет данных для отображения.")
            return
        print("\n--- Обработанные записи ---")
        for item in items:
            print(item)
            print(f"   Содержимое: {item.content[:50]}...")
            print(f"   Слов в тексте: {item.metadata.get('word_count', 'N/A')}\n")
        if items:
            total_words = sum(item.metadata.get('word_count', 0) for item in items)
            avg_words = total_words / len(items)
            print(f"Среднее количество слов в записи: {avg_words:.1f}")