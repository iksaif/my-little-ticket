"""API to create plugins and some utilities."""
import abc
import uuid

from datetime import datetime


# TODO: make that a named tuple with an as_dict() method.
class Ticket(dict):
    """Simple class to create tickets."""

    NAMESPACE = uuid.UUID('{27d04f51-793d-40da-a2cf-dd03fb606947}')

    def __init__(self, ext_id, summary, text, link,
                 project=None, type=None, assignee=None,
                 status=None, tags=None, raw=None,
                 created_on=None, modified_on=None, refreshed_on=None):
        """Initialize a ticket.

        See my_little_tickets.tickets.models.Ticket for details about
        arguments.
        """
        s = self

        s['id'] = uuid.uuid5(uuid.NAMESPACE_URL, str(link))
        s['ext_id'] = ext_id
        s['summary'] = summary
        s['text'] = text
        s['project'] = project
        s['type'] = type
        s['assignee'] = assignee
        s['status'] = status
        s['link'] = link
        s['tags'] = set(tags or [])
        s['raw'] = raw
        s['created_on'] = created_on
        s['modified_on'] = modified_on
        s['refreshed_on'] = refreshed_on or datetime.now()

    def __hash__(self):
        return hash(self['id'])


class Plugin(object):
    """Abstract class for plugins."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, params=None):
        """Create the plugin instance.

        Args:
          params: dict(string, any)
        """
        self._params = params

    @property
    @abc.abstractmethod
    def short_name(self):
        """Return the short_name of the plugin.

        It must contain only alphanumeric characters.
        """
        return None

    @property
    @abc.abstractmethod
    def name(self):
        """Return the name of the plugin."""
        return None

    @property
    def description(self):
        """Return a description."""
        return None

    @property
    def link(self):
        """Return a link."""
        return None

    @abc.abstractmethod
    def tickets(self):
        """Return a list of tickets.

        Return:
          dict(uuid.UUID: my_litle_ticket.plugins.base.Ticket).
        """
        return {}


class Strategy(object):
    """Abstract class for strategies."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, param=None):
        """Create the plugin instance.

        Args:
          param: dict(string, any)
        """
        self._param = param

    @property
    @abc.abstractmethod
    def short_name(self):
        """Return the short_name of the plugin.

        It must contain only alphanumeric characters.
        """
        return None

    @property
    @abc.abstractmethod
    def name(self):
        """Return the name of the plugin."""
        return None

    @property
    def description(self):
        """Return a description."""
        return None

    @property
    def link(self):
        """Return a link."""
        return None

    @abc.abstractmethod
    def score(self, ticket):
        """Return a score for a given ticket."""
        return 0

    def scores(self, tickets):
        """Return a map of ticket -> score.

        Override if you want to do something smarter for a full list of tickets.
        """
        return {ticket: self.score(ticket) for ticket in tickets}
