from abc import ABC, abstractmethod


class ProcessingStrategy(ABC):

    @abstractmethod
    def process(self, items):
        pass
