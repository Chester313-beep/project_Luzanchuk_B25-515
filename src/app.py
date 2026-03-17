class App:
    def __init__(self, sources, processor):
        self.sources = sources
        self.processor = processor

    def run(self):
        all_items = []
        source_stats = {}
        for source in self.sources:
            items = source.fetch()
            all_items.extend(items)
            source_stats[source.name] = {
                'received': len(items),
                'source_type': source.source_type,
            }
        if not all_items:
            print("Нет данных ни от одного источника.")
            return
        print("=== Сбор данных завершён ===")
        for name, stat in source_stats.items():
            print(f"Источник '{name}' ({stat['source_type']}): получено {stat['received']} записей")
        processed_items = self.processor.process(all_items)
        for item in processed_items:
            source_name = item.metadata.get('source', 'unknown')
            if source_name not in source_stats:
                source_stats[source_name] = {'received': 0, 'processed': 0}
            source_stats[source_name]['processed'] = source_stats[source_name].get('processed', 0) + 1
        print("\n=== Результаты обработки ===")
        for name, stat in source_stats.items():
            processed = stat.get('processed', 0)
            print(f"Источник '{name}': осталось после обработки {processed} из {stat['received']}")
        print("\n--- Обработанные записи ---")
        for item in processed_items:
            print(item)
            print(f"   Содержимое: {item.content[:50]}...")
            print(f"   Слов: {item.metadata.get('word_count', 'N/A')}\n")
        if processed_items:
            avg_words = sum(item.metadata.get('word_count', 0) for item in processed_items) / len(processed_items)
            print(f"Среднее количество слов в обработанной записи: {avg_words:.1f}")
