class ConsolePresenter:
    @staticmethod
    def display_summary(source_stats):
        print("=== Сбор данных завершён ===")
        for name, stat in source_stats.items():
            if isinstance(stat, dict):
                received = stat.get('received', stat)
            else:
                received = stat
            print(f"Источник '{name}': получено {received} записей")

    @staticmethod
    def display_results(processed_iter, received_stats):
        processed_stats = {}
        total_words = 0
        total_processed = 0

        print("\n--- Обработанные записи ---")
        for item in processed_iter:
            src = item.metadata.get('source', 'unknown')
            processed_stats[src] = processed_stats.get(src, 0) + 1

            print(item)
            print(f"   Содержимое: {item.content[:50]}...")
            print(f"   Слов: {item.metadata.get('word_count', 'N/A')}\n")

            wc = item.metadata.get('word_count', 0)
            if wc:
                total_words += wc
                total_processed += 1

        print("\n=== Результаты обработки ===")
        all_sources = set(received_stats.keys()) | set(processed_stats.keys())
        for src in all_sources:
            received = received_stats.get(src, 0)
            if isinstance(received, dict):
                received = received.get('received', 0)
            processed = processed_stats.get(src, 0)
            print(f"Источник '{src}': осталось после обработки {processed} из {received}")

        if total_processed > 0:
            avg_words = total_words / total_processed
            print(f"Среднее количество слов в обработанной записи: {avg_words:.1f}")
