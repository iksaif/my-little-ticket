"""Test for the default strategy plugin."""

import unittest

from my_little_ticket.plugins import base
from my_little_ticket.plugins import default

class MyTestCase(unittest.TestCase):
    def test_basic(self):
        tickets = (
            base.Ticket('foo', 'Foo', 'Foo foo', 'http://bug/foo'),
            base.Ticket('bar', 'bar', 'bar bar', 'http://bug/bar')
        )
        strategy = default.DefaultStrategy()
        result = strategy.scores(tickets)
        self.assertEqual(len(result), len(tickets))
        # FIXME: More tests here.


if __name__ == '__main__':
    unittest.main()
