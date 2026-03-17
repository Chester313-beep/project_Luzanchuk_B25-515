from abc import ABC, abstractmethod


class AsyncBaseDataSource(ABC):

    def __init__(self, name: str, source_type: str):
        self.name = name
        self.source_type = source_type

    @abstractmethod
    async def fetch(self):
        pass