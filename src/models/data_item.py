class NewsItem:
    def __init__(
    self,
    id: int,
    title: str,
    content: str,
    source: str = None,
    category: str = None,
):
        self.id = id
        self.title = title
        self.content = content
        self.metadata = {
            "source": source,
            "category": category,
        }

    def __str__(self):
        cat = self.metadata.get('category', 'без категории')
        return f"[{self.id}] {self.title} ({cat})"