import asyncio


class AsyncApp:
    def __init__(self, sources, strategy, presenter):
        self.sources = sources
        self.strategy = strategy
        self.presenter = presenter

    async def run(self):
        tasks = [self._collect_source_items(source) for source in self.sources]
        source_results = await asyncio.gather(*tasks)

        all_items = []
        for items, source_name in source_results:
            all_items.extend(items)

        received_stats = {}
        for item in all_items:
            src = item.metadata.get('source', 'unknown')
            received_stats[src] = received_stats.get(src, 0) + 1

        processed_items = []
        async for processed in self.strategy.process(self._async_iter(all_items)):
            processed_items.append(processed)

        self.presenter.display_results(iter(processed_items), received_stats)

    async def _collect_source_items(self, source):
        """Собирает все элементы из асинхронного источника в список."""
        items = []
        async for item in source.fetch():
            items.append(item)
        return items, source.name

    @staticmethod
    async def _async_iter(items):
        """Преобразует список в асинхронный итератор."""
        for item in items:
            yield item
            await asyncio.sleep(0)
