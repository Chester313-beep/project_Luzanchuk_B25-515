
class App:
    def __init__(self, sources, strategy, presenter):
        self.sources = sources
        self.strategy = strategy
        self.presenter = presenter

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

        self.presenter.display_summary(source_stats)

        # Используем стратегию
        processed_items = self.strategy.process(all_items)

        for item in processed_items:
            source_name = item.metadata.get('source', 'unknown')
            if source_name not in source_stats:
                source_stats[source_name] = {'received': 0, 'processed': 0}
            current = source_stats[source_name].get('processed', 0)
            source_stats[source_name]['processed'] = current + 1

        self.presenter.display_results(processed_items, source_stats)
