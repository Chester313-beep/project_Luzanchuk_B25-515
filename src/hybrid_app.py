import asyncio

from src.task_manager import TaskManager


class HybridApp:

    def __init__(self, sources, async_strategy, presenter,
                 use_executor: bool = False, executor_type: str = 'thread'):
        self.sources = sources
        self.async_strategy = async_strategy
        self.presenter = presenter
        self.use_executor = use_executor
        if use_executor:
            self.task_manager = TaskManager(executor_type=executor_type)

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

        if self.use_executor:
            from src.strategies.heavy_processing import heavy_normalize
            processed_items = []
            async for result in self.task_manager.map_ordered(heavy_normalize, all_items):
                if result is not None:
                    processed_items.append(result)
        else:
            processed_items = []
            async for processed in self.async_strategy.process(self._async_iter(all_items)):
                processed_items.append(processed)
        self.presenter.display_results(iter(processed_items), received_stats)

    async def _collect_source_items(self, source):
        items = []
        async for item in source.fetch():
            items.append(item)
        return items, source.name

    @staticmethod
    async def _async_iter(items):
        for item in items:
            yield item
            await asyncio.sleep(0)

    def shutdown(self):
        if self.use_executor:
            self.task_manager.shutdown()
