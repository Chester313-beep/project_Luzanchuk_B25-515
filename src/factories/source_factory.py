from src.sources.async_demo_source import AsyncDemoNewsSource
from src.sources.async_file_source import AsyncFileNewsSource
from src.sources.async_web_source import AsyncWebNewsSource

class SourceFactory:
    @staticmethod
    def create_source(source_config: dict):
        source_type = source_config.get('type')
        if source_type == 'demo':
            return AsyncDemoNewsSource(
                name=source_config.get('name', 'Async Demo News')
            )
        elif source_type == 'file':
            return AsyncFileNewsSource(
                file_path=source_config['file_path'],
                name=source_config.get('name', 'Async File News')
            )
        elif source_type == 'web':
            return AsyncWebNewsSource(
                base_url=source_config['base_url'],
                name=source_config.get('name', 'Async Web News'),
                max_concurrent=source_config.get('max_concurrent', 3),
                max_retries=source_config.get('max_retries', 3),
                request_delay=source_config.get('request_delay', 0.5)
            )
        else:
            raise ValueError(f"Неизвестный тип источника: {source_type}")
