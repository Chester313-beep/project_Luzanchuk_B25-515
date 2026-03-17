import time

from src.models.data_item import NewsItem


def heavy_normalize(item: NewsItem) -> NewsItem:
    if not item.content or not item.content.strip():
        return None
    time.sleep(0.02)

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
    return new_item
