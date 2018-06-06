"""Test for the default strategy plugin."""

import unittest

import uuid
from my_little_ticket.tickets.models import Ticket
from my_little_ticket.plugins import default


class MyTestCase(unittest.TestCase):
    """Tests for DefaultStrategy."""

    def test_basic(self):
        """Check if the default strategy works."""
        tickets = (
            Ticket(id=1, uuid=uuid.uuid4(), summary="Foo", text="Foo foo", link="http://bug/foo"),
            Ticket(id=2, uuid=uuid.uuid4(), summary="bar", text="bar bar", link="http://bug/bar"),
        )
        strategy = default.DefaultStrategy(params={})
        result = strategy.scores(tickets)
        self.assertEqual(len(result), len(tickets))
        strategy.group(tickets[0])
        strategy.status(tickets[0])


# FIXME: More tests here.


if __name__ == "__main__":
    unittest.main()
