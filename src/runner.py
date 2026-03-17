import asyncio
from typing import List, Optional, Dict, Any
from src.config.config import AppConfig
from src.factories.source_factory import SourceFactory
from src.sources.async_base_source import AsyncBaseDataSource
from src.strategies.normalization_strategy import AsyncNormalizationStrategy
from src.strategies.filter_strategy import FilterStrategy
from src.presenters.console_presenter import ConsolePresenter
from src.hybrid_app import HybridApp
from src.sources.async_web_source import AsyncWebNewsSource

class AppRunner:

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self.config = AppConfig()
        if config_dict:
            self.config.load(config_dict)
        self.sources: List[AsyncBaseDataSource] = []
        self.presenter = ConsolePresenter()
        self.last_result = None

    def _create_sources(self):
        for source_cfg in self.config.sources:
            source_type = source_cfg.get('type')
            if source_type == 'web':
                source = AsyncWebNewsSource(
                    base_url=source_cfg['base_url'],
                    name=source_cfg.get('name', 'Web News'),
                    max_concurrent=source_cfg.get('max_concurrent', 3),
                    max_retries=source_cfg.get('max_retries', 3),
                    request_delay=source_cfg.get('request_delay', 0.5)
                )
            else:
                source = SourceFactory.create_source(source_cfg)
            self.sources.append(source)

    def _create_strategy(self):
        strategy_name = self.config.strategy
        if strategy_name == 'normalization':
            return AsyncNormalizationStrategy()
        elif strategy_name == 'filter':
            return FilterStrategy(min_length=self.config.get('min_length', 5))
        else:
            raise ValueError(f"Неизвестная стратегия: {strategy_name}")

    async def run(self) -> str:
        self._create_sources()
        strategy = self._create_strategy()

        mode = self.config.processing_mode
        use_executor = mode in ('threads', 'processes')
        executor_type = 'thread' if mode == 'threads' else 'process' if mode == 'processes' else None


        app = HybridApp(
            sources=self.sources,
            async_strategy=strategy,
            presenter=self.presenter,
            use_executor=use_executor,
            executor_type=executor_type
        )

        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            await app.run()
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
            app.shutdown()

        self.last_result = output
        return output

    async def run_and_print(self):
        result = await self.run()
        print(result)
