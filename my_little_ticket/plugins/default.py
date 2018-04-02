"""Default strategy."""

from my_little_ticket.plugins import base


class DefaultStrategy(base.Strategy):
    """Default strategy.
    TOTO.
    """

    def short_name(self):
        return "default"

    def name(self):
        return "Default"

    def description(self):
        return """TODO."""

    def score(self, ticket):
        # FIXME
        return 0
