"""my-little-ticket Jira plugin."""
import logging
import jira

from my_little_ticket.plugins import base

from django.conf import settings


DEFAULT_JIRA_URL = getattr(settings, 'JIRA_URL', None)
DEFAULT_JIRA_USERNAME = getattr(settings, 'JIRA_USERNAME', None)
DEFAULT_JIRA_PASSWORD = getattr(settings, 'JIRA_PASSWORD', None)


class JiraPlugin(base.Plugin):
    """my-little-ticket Static plugin.

    params:
    ```python
    {
      'url': 'http://jira', // Url to root API.
      'username': 'foo',
      'password': 'bar',
      'jql': {},            // Get tickets matching this jql.
      'max_results': 5,     // Optional maximum number of tickets.
    }
    ```
    """

    def __init__(self, params=None):
        """Create an instance of the plugin."""
        super(JiraPlugin, self).__init__(params)
        if params is None:
            params = {}

        self._client = None
        self.max_results = params.get('max_results', 1000)

        if params:
            self.url = params.get('url', DEFAULT_JIRA_URL)
            self.username = params.get('username', DEFAULT_JIRA_USERNAME)
            self.password = params.get('password', DEFAULT_JIRA_PASSWORD)
            self.jql = params['jql']

    @property
    def short_name(self):
        """Return the short name."""
        return 'jira'

    @property
    def name(self):
        """Return the name."""
        return 'Jira'

    @property
    def description(self):
        """Return the description."""
        return 'Returns tickets from JIRA.'

    @property
    def link(self):
        """Return the link."""
        return 'https://github.com/iksaif/my-little-ticket'

    @property
    def client(self):
        """Get a JIRA client."""
        if not self._client:
            if self._params is None:
                return None

            basic_auth = (self.username, self.password)
            self._client = jira.JIRA(self.url, basic_auth=basic_auth, timeout=5)

        return self._client

    def tickets(self):
        """Return the tickets."""
        ret = {}

        if not self.client:
            return ret

        issues = self.client.search_issues(self.jql, maxResults=self.max_results)
        for issue in issues:
            ticket = self._to_ticket(issue)
            if ticket is not None:
                ret[ticket['id']] = ticket
        return ret

    def _to_ticket(self, issue):
        """Return a status or None."""
        logging.debug('Handling %s' % (issue.fields.summary))

        data = dict(issue.raw)
        data['me'] = data['self']
        data['issue'] = issue
        data['permalink'] = issue.permalink()
        del data['self']

        if 'description' in data['fields']:
            text = data['fields']['description']
        else:
            text = None
        status = base.Ticket(
            ext_id=issue.key,
            summary=issue.fields.summary,
            text=text,
            link=issue.permalink(),
            # FIXME: all fields.
        )
        return status
