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
        self.max_age = params.get("max_age", 60 * 60 * 24 * 2)
        self.params = params

    def short_name(self):
        """Return the short name (id) for this strategy."""
        return "default"

    def name(self):
        """Return a human readable name for this strategy."""
        return "Default"

    def description(self):
        """Explains how this strategy works."""
        return """Default strategy: %s.""" % self.params

    def group(self, ticket):
        """Group tickets together."""
        status = ticket.status or ""
        if status.lower() in ["block", "blocked", "idle"]:
            return "Inactive"

        return ticket.project

    def status(self, ticket):
        """Score status for a given ticket."""
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
        """Score a ticket.

        Use the time since last update to compute a score.
        """
        now = time.time()
        return now - time.mktime(ticket.modified_on.timetuple())
