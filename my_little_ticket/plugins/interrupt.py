"""Interrupt strategy."""

import time
import humanize
from my_little_ticket.plugins import base


class InterruptStrategy(base.Strategy):
    """Default strategy.

    Simply uses the time since last update to compute a score
    and status.

    Params:
        max_age: maximum age in seconds before switching to `STATUS_DANGER`.
    """

    def __init__(self, params):
        """Constructor."""
        super(InterruptStrategy, self).__init__(params)
        self.params = params
        # Default to three days (this way it's not all red on monday).
        self.max_age = params.get("max_age", 60 * 60 * 24 * 3)

    def short_name(self):
        """See base.Strategy."""
        return "interrupt"

    def name(self):
        """See base.Strategy."""
        return "Interrupt"

    def description(self):
        """See base.Strategy."""
        return """
Interrupt strategy.
<ul>
<li>Max age: %ss</li>
<li><span class="badge badge-danger">danger</span> >%s</li>
<li><span class="badge badge-warning">warning</span> >%s</li>
<li><span class="badge badge-info">info</span> >%s</li>
<li><span class="badge badge-success">success</span> less</li>
<ul/>
        """ % (
            self.max_age,
            humanize.naturaltime(self.max_age),
            humanize.naturaltime(self.max_age * 0.75),
            humanize.naturaltime(self.max_age * 0.25),
        )

    def _is_blocked(self, ticket):
        """Return true if blocked."""
        status = ticket.status or "unknown"
        return status.lower() in ["block", "blocked", "idle"]

    def group(self, ticket):
        """Return group for a ticket."""
        tags = [tag.word for tag in ticket.tags.all()]
        if self._is_blocked(ticket):
            return "Waiting"
        elif "alert" in tags:
            return "Alerts"
        else:
            return "Tickets"

    def status(self, ticket):
        """Return status for a ticket."""
        delta = time.time() - time.mktime(ticket.modified_on.timetuple())
        # Make sure higher priority tickets have higher factors.
        priority_factors = {"Blocker": 4, "Critical": 4, "Major": 2}
        delta *= priority_factors.get(ticket.priority, 1)
        if self._is_blocked(ticket):
            # Static status for blocked tickets.
            return self.STATUS_INFO
        elif delta > self.max_age:
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
        # TODO:
        # - take comments into account instead of modifications
        # - ignore comments starting with "note:" or "fyi:"
        now = time.time()
        return now - time.mktime(ticket.modified_on.timetuple())
