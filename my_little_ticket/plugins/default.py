"""Default strategy."""

import time
from my_little_ticket.plugins import base


class DefaultStrategy(base.Strategy):
    """Default strategy.

    Simply uses the time since last update to compute a score
    and status.

    Params:
        max_age: maximum age in seconds before switching to `STATUS_DANGER`.
    """

    def __init__(self, params):
        """Constructor."""
        super(DefaultStrategy, self).__init__(params)
        # Default to two days.
        self.max_age = params.get('max_age', 60 * 60 * 24 * 2)

    def short_name(self):
        return "default"

    def name(self):
        return "Default"

    def description(self):
        return """Default strategy."""

    def group(self, ticket):
        """Simple grouping."""
        if ticket.status.lower() in ['block', 'blocked', 'idle']:
            return 'Inactive'
        return ticket.project

    def status(self, ticket):
        """Simple score status."""
        delta = time.time() - time.mktime(ticket.modified_on.timetuple())
        if delta > self.max_age:
            return self.STATUS_DANGER
        elif delta > self.max_age * 0.75:
            return self.STATUS_WARNING
        elif delta > self.max_age * 0.25:
            return self.STATUS_INFO
        else:
            return self.STATUS_SUCCESS

    def score(self, ticket):
        """Simple score strategy.

        Use the time since last update to compute a score.
        """
        now = time.time()
        return now - time.mktime(ticket.modified_on.timetuple())
