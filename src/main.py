from src.app import App
from src.processors.text_processor import NewsProcessor
from src.sources.file_source import FileNewsSource
from src.sources.mock_source import DemoNewsSource


def main():
    demo_source = DemoNewsSource(name="Демо-новости")
    file_source = FileNewsSource(file_path="data/news.json", name="Новости из файла")
    sources = [
        demo_source,
        file_source,
    ]
    processor = NewsProcessor()
    app = App(sources, processor)
    app.run()

if __name__ == "__main__":
    main()
