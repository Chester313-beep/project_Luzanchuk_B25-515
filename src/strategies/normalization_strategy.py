from src.models.data_item import NewsItem
from src.strategies.base_strategy import ProcessingStrategy


class NormalizationStrategy(ProcessingStrategy):
    def process(self, items):
        processed = []
        for item in items:
            if not item.content or not item.content.strip():
                continue

            cleaned = ' '.join(item.content.split()).lower()
            word_count = len(cleaned.split())

            new_item = NewsItem(
                id=item.id,
                title=item.title,
                content=cleaned,
                source=item.metadata.get('source'),
                category=item.metadata.get('category')
            )
            new_item.metadata['word_count'] = word_count
            for k, v in item.metadata.items():
                if k not in ('source', 'category'):
                    new_item.metadata[k] = v

            processed.append(new_item)
        return processed
