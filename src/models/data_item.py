class NewsItem:
    def __init__(self, id: int, title: str, content: str, source: str = None, category: str = None):
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

    def __repr__(self):
        return f"NewsItem(id={self.id}, title={self.title!r}, content_len={len(self.content)})"

    def __lt__(self, other):
        if not isinstance(other, NewsItem):
            return NotImplemented
        return len(self.content) < len(other.content)

    def __eq__(self, other):
        if not isinstance(other, NewsItem):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
