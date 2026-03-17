class AppConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sources_config = []
            cls._instance.strategy_name = "normalization"
        return cls._instance

    def load(self, config_dict: dict):
        self.sources_config = config_dict.get('sources', [])
        self.strategy_name = config_dict.get('strategy', 'normalization')
    @property
    def sources(self):
        return self.sources_config
    @property
    def strategy(self):
        return self.strategy_name