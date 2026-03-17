from src.models.data_item import NewsItem
from src.strategies.base_strategy import ProcessingStrategy


class FilterStrategy(ProcessingStrategy):
    def __init__(self, min_length=0):
        self.min_length = min_length

    def process(self, items):
        for item in items:
            if not item.content or len(item.content.strip()) < self.min_length:
                continue
            new_item = NewsItem(
                id=item.id,
                title=item.title,
                content=item.content,
                source=item.metadata.get('source'),
                category=item.metadata.get('category')
            )
            for k, v in item.metadata.items():
                if k not in ('source', 'category'):
                    new_item.metadata[k] = v
            yield new_item
