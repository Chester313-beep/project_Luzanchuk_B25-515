class ConsolePresenter:

    @staticmethod
    def display_summary(source_stats):
        print("=== Сбор данных завершён ===")
        for name, stat in source_stats.items():
            print(f"Источник '{name}' ({stat['source_type']}): "
                  f"получено {stat['received']} записей")

    @staticmethod
    def display_results(processed_items, source_stats):
        print("\n=== Результаты обработки ===")
        for name, stat in source_stats.items():
            processed = stat.get('processed', 0)
            print(f"Источник '{name}': осталось после обработки "
                  f"{processed} из {stat['received']}")

        print("\n--- Обработанные записи ---")
        for item in processed_items:
            print(item)
            print(f"   Содержимое: {item.content[:50]}...")
            print(f"   Слов: {item.metadata.get('word_count', 'N/A')}\n")

        if processed_items:
            total_words = sum(item.metadata.get('word_count', 0) for item in processed_items)
            avg_words = total_words / len(processed_items)
            print(f"Среднее количество слов в обработанной записи: {avg_words:.1f}")
