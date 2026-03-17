import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, AsyncIterator, Callable, Iterable


class TaskManager:

    def __init__(self, executor_type: str = 'thread', max_workers: int = None):
        if executor_type == 'thread':
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
        elif executor_type == 'process':
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            raise ValueError("executor_type must be 'thread' or 'process'")
        self.loop = asyncio.get_event_loop()

    async def map_ordered(self, func: Callable, items: Iterable) -> AsyncIterator[Any]:
        tasks = [self.loop.run_in_executor(self.executor, func, item) for item in items]
        results = await asyncio.gather(*tasks)
        for res in results:
            yield res

    def shutdown(self):
        self.executor.shutdown(wait=True)
