import itertools


class App:
    def __init__(self, sources, strategy, presenter):
        self.sources = sources
        self.strategy = strategy
        self.presenter = presenter

    def run(self):

        source_iters = [source.fetch() for source in self.sources]

        combined = itertools.chain.from_iterable(source_iters)

        received_stats = {}
        def count_received(iterable):
            for item in iterable:
                src = item.metadata.get('source', 'unknown')
                received_stats[src] = received_stats.get(src, 0) + 1
                yield item

        counted_input = count_received(combined)

        processed_iter = self.strategy.process(counted_input)

        self.presenter.display_results(processed_iter, received_stats)
