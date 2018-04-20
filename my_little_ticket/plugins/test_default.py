"""Test for the default strategy plugin."""

import unittest

from my_little_ticket.tickets.models import Ticket
from my_little_ticket.plugins import default


class MyTestCase(unittest.TestCase):
    def test_basic(self):
        tickets = (
            Ticket(id='foo', summary='Foo', text='Foo foo', link='http://bug/foo'),
            Ticket(id='bar', summary='bar', text='bar bar', link='http://bug/bar')
        )
        strategy = default.DefaultStrategy(params={})
        result = strategy.scores(tickets)
        self.assertEqual(len(result), len(tickets))
        # FIXME: More tests here.


if __name__ == '__main__':
    unittest.main()
