"""my-little-ticket Trello plugin."""
import logging

import trello

from my_little_ticket.plugins import base

from django.conf import settings


DEFAULT_TRELLO_API_KEY = getattr(settings, "TRELLO_API_KEY", None)
DEFAULT_TRELLO_API_SECRET = getattr(settings, "TRELLO_API_SECRET", None)


class TrelloPlugin(base.Plugin):
    """my-little-ticket Trello plugin.

    params:
    ```python
    {
      'api_key': '--secret--',        // API Key
      'api_secret': '--secret--',     // API Secret
      'board_id': 'as124DD',          // Board ID
      'include_closed': False,        // Include closed cards
    }
    ```
    """

    def __init__(self, params=None):
        """Create an instance of the plugin."""
        super(TrelloPlugin, self).__init__(params)
        if params is None:
            params = {}

        self._client = None

        self.api_key = params.get("api_key", DEFAULT_TRELLO_API_KEY)
        self.api_secret = params.get("api_secret", DEFAULT_TRELLO_API_SECRET)
        self.board_id = params.get("board_id", None)
        self.include_closed = params.get("include_closed", False)
        self.members = {}
        if "params" in params:
            self.params = params["params"]
        else:
            self.params = {}

    @property
    def short_name(self):
        """Return the short name."""
        return "trello"

    @property
    def name(self):
        """Return the name."""
        return "Trello"

    @property
    def description(self):
        """Return the description."""
        return "Returns cards from Trello."

    @property
    def link(self):
        """Return the link."""
        return "https://trello.com/b/%s" % self.board_id

    @property
    def client(self):
        """Get a Trello api."""
        if not self._client:
            # This isn't super nice if somebody else in the same
            # process is uinsg it...
            self._client = trello.TrelloClient(
                api_key=self.api_key, api_secret=self.api_secret
            )

        return self._client

    def member(self, member_id):
        """Get the member for this member id."""
        if member_id not in self.members:
            self.members[member_id] = self.client.get_member(member_id)
        return self.members[member_id]

    def tickets(self):
        """Return the tickets."""
        if not self.client:
            return {}

        if self.board_id:
            boards = [self.client.get_board(self.board_id)]
        else:
            boards = self.client.list_boards()

        tickets = {}
        for board in boards:
            tickets.update(self._tickets_for_board(board))
        return tickets

    def _tickets_for_board(self, board):
        ret = {}
        if self.include_closed:
            cards = board.all_cards()
        else:
            cards = board.open_cards()
        for card in cards:
            ticket = self._to_ticket(board, card)
            if ticket is not None:
                ret[ticket["uuid"]] = ticket
        return ret

    def _to_ticket(self, board, card):
        """Return a status or None."""
        logging.debug("Handling %s" % (card))

        labels = card.labels or []

        tags = []
        for label in labels:
            if label.name:
                tags.append(label.name)
            else:
                tags.append(label.color)
        if len(labels) == 1:
            priority = labels[0].color
        else:
            priority = None

        assignee = None
        if card.member_id:
            member = self.member(card.member_id[0])
            if member:
                assignee = member.full_name

        status = "Closed" if card.closed else "Open"
        created_on = card.created_date
        updated_on = card.date_last_activity

        raw = self.client.fetch_json("/cards/" + card.id)

        ticket = base.Ticket(
            ext_id=card.short_id,
            summary=card.name,
            text=card.description,
            link=card.url,
            project=board.name,
            type="Card",
            assignee=assignee,
            status=status,
            priority=priority,
            tags=tags,
            created_on=created_on,
            modified_on=updated_on,
            raw=raw,
        )
        return ticket

    def info(self, ticket):
        """Return info that might be interesting for this ticket."""
        data = {}
        return data
