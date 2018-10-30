"""Test trello."""
import httmock
import os

from django import test

from my_little_ticket.plugins import trello


@httmock.urlmatch(netloc=r"(.*\.)?trello\.com")
def _trello_mock(url, request):
    if url.path == "/1/members/me/boards/":
        filename = "spec_trello_boards.json"
    elif url.path == "/1/boards/120xsa321sdpasd/dateLastActivity":
        filename = "spec_trello_lastactivity.json"
    elif url.path == "/1/boards/120xsa321sdpasd":
        filename = "spec_trello_board.json"
    elif url.path == "/1/boards/120xsa321sdpasd/cards/":
        filename = "spec_trello_cards.json"
    elif url.path == "/1/cards/5bd8baa50cb8fb4737d32733":
        filename = "spec_trello_card.json"
    else:
        raise Exception(url)

    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()


class TrelloPluginTests(test.TestCase):
    """Test the plugins."""

    def test_all(self):
        """Basic test."""
        with httmock.HTTMock(_trello_mock):
            p = trello.TrelloPlugin()
            tickets = sorted(p.tickets().values())
            ticket = tickets[0]

            self.assertEqual(ticket["summary"], "test")

    def test_one_board(self):
        """Test with some settings."""
        with httmock.HTTMock(_trello_mock):
            p = trello.TrelloPlugin(
                {"board_id": "120xsa321sdpasd", "include_closed": True}
            )
            tickets = sorted(p.tickets().values())
            ticket = tickets[0]

            self.assertEqual(ticket["summary"], "test")
