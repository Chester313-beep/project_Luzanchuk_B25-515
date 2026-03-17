import asyncio
from typing import AsyncIterator

import aiohttp

from src.models.data_item import NewsItem
from src.sources.async_base_source import AsyncBaseDataSource


class AsyncWebNewsSource(AsyncBaseDataSource):
    def __init__(
        self,
        base_url: str,
        name: str = "Async Web News",
        source_type: str = "async_web",
        max_concurrent: int = 3,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        request_delay: float = 0.5,
    ):
        super().__init__(name, source_type)
        self.base_url = base_url.rstrip('/')
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.request_delay = request_delay
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.stats = {
            "attempts": 0,
            "success": 0,
            "errors": 0,
            "retries": 0,
        }
    async def fetch(self) -> AsyncIterator[NewsItem]:
        pages = [1, 2, 3]
        tasks = [self._fetch_page(page) for page in pages]
        for coro in asyncio.as_completed(tasks):
            page_items = await coro
            for item in page_items:
                yield item
        print(f"[{self.name}] Статистика: "
              f"попыток {self.stats['attempts']}, "
              f"успешно {self.stats['success']}, "
              f"ошибок {self.stats['errors']}, "
              f"повторов {self.stats['retries']}")

    async def _fetch_page(self, page: int) -> list[NewsItem]:
        url = f"{self.base_url}/posts?_page={page}&_limit=10"
        for attempt in range(1, self.max_retries + 1):
            async with self.semaphore:
                self.stats["attempts"] += 1
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                self.stats["success"] += 1
                                items = []
                                for idx, post in enumerate(data):
                                    item = NewsItem(
                                        id=(page-1)*10 + idx + 1,
                                        title=post.get("title", ""),
                                        content=post.get("body", ""),
                                        source=self.name,
                                        category="web"
                                    )
                                    items.append(item)
                                await asyncio.sleep(self.request_delay)
                                return items
                            elif 500 <= resp.status < 600:
                                self.stats["errors"] += 1
                                if attempt < self.max_retries:
                                    self.stats["retries"] += 1
                                    await asyncio.sleep(self.retry_delay * attempt)
                                    continue
                            else:
                                self.stats["errors"] += 1
                                print(f"[{self.name}] Ошибка {resp.status} для {url}")
                                return []
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    self.stats["errors"] += 1
                    if attempt < self.max_retries:
                        self.stats["retries"] += 1
                        await asyncio.sleep(self.retry_delay * attempt)
                        continue
                    else:
                        print(f"[{self.name}] Не удалось загрузить {url}: {e}")
                        return []
        return []
