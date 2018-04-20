"""Test jira."""
import httmock
import os

from django import test

from my_little_ticket.plugins import jira


@httmock.urlmatch(netloc=r"(.*\.)?jira\.foo")
def _jira_mock(url, request):
    if url.path == "/rest/api/2/serverInfo":
        filename = "spec_jira_handshake.json"
    elif url.path == "/rest/api/2/field":
        filename = "spec_jira_fields.json"
    elif url.path == "/rest/api/2/search":
        filename = "spec_jira_search.json"
    else:
        raise Exception(url)

    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()


class JiraPluginTests(test.TestCase):
    """Test the plugins."""

    _JIRA_URL = "http://jira.foo"

    def test_base(self):
        """Basic test."""
        p = jira.JiraPlugin()
        self.assertFalse(p.tickets())

    def test_all(self):
        """Test with some settings."""
        with httmock.HTTMock(_jira_mock):
            p = jira.JiraPlugin(
                {
                    "url": self._JIRA_URL,
                    "username": "foo",
                    "password": "bar",
                    "defcon": lambda _: 3,
                    "jql": "FOO-1",
                }
            )
            tickets = sorted(p.tickets().values())
            ticket = tickets[0]

            self.assertEqual(ticket["summary"], "Test")
