"""Feature request strategy."""

from my_little_ticket.plugins import base


class FeatureRequestStrategy(base.Strategy):
    """FeatureRequestStrategy strategy.

    Uses votes to sort.
    """

    def __init__(self, params):
        """Constructor."""
        super(FeatureRequestStrategy, self).__init__(params)
        self.params = params

    def short_name(self):
        """See base.Strategy."""
        return "feature-request"

    def name(self):
        """See base.Strategy."""
        return "Feature request"

    def description(self):
        """Score based on votes."""
        return """
Feature request strategy. Uses the number of votes to determine a score.
The more voters, the higher the feature request will go.
        """

    def group(self, ticket):
        """See base.Strategy."""
        status = ticket.status or "unknown"

        if status.lower() in ["block", "blocked", "idle"]:
            return "Waiting"
        elif status.lower() in ["in progress"]:
            return "In Progress"
        elif status.lower() in ["closed", "fixed", "resolved"]:
            return "X Implemented"
        else:
            return "Feature Requests"

    def _get_votes(self, ticket):
        raw = ticket.raw or {}
        return raw.get("fields", {}).get("votes", {}).get("votes", 0)

    def status(self, ticket):
        """See base.Strategy."""
        score = self._get_votes(ticket)
        if score == 0:  # Nobody cares
            return self.STATUS_DANGER
        elif score <= 3:  # Some people
            return self.STATUS_WARNING
        elif score <= 6:  # At least a team
            return self.STATUS_INFO
        else:  # More than a team
            return self.STATUS_SUCCESS

    def score(self, ticket):
        """See base.Strategy."""
        score = self._get_votes(ticket)
        # Multiply by itself to make more differences between scores.
        return score * score
