from src.sources.base_source import BaseDataSource
from src.sources.file_source import FileNewsSource
from src.sources.mock_source import DemoNewsSource


class SourceFactory:
    @staticmethod
    def create_source(source_config: dict) -> BaseDataSource:
        source_type = source_config.get('type')
        if source_type == 'demo':
            return DemoNewsSource(
                name=source_config.get('name', 'Demo News')
            )
        elif source_type == 'file':
            return FileNewsSource(
                file_path=source_config['file_path'],
                name=source_config.get('name', 'File News')
            )
        else:
            raise ValueError(f"Неизвестный тип источника: {source_type}")