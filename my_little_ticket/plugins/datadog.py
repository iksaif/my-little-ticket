"""my-little-ticket Datadog plugin."""
import logging
import time

import datadog

from my_little_ticket.plugins import base

from django.conf import settings


DEFAULT_DATADOG_API_HOST = getattr(settings, "DATADOG_API_HOST", None)
DEFAULT_DATADOG_APP_KEY = getattr(settings, "DATADOG_APP_KEY", None)
DEFAULT_DATADOG_API_KEY = getattr(settings, "DATADOG_API_KEY", None)

# TODO: There could also be one for events (as monitors create events).


class MonitorPlugin(base.Plugin):
    """my-little-ticket Datadog plugin.

    This is not super useful yet, it's probably a better idea to plugin datadog monitors
    to jira or trello and fetch status from there.

    params:
    ```python
    {
      'api_host': 'https://api.datadoghq.com', // Url to root API.
      'api_key': '',        // API Key
      'app_key': '',        // API Key
      'params': {},         // Get tickets matching these params (see Datadog API).
    }
    ```
    """

    def __init__(self, params=None):
        """Create an instance of the plugin."""
        super(MonitorPlugin, self).__init__(params)
        if params is None:
            params = {}

        self._api = None

        self.api_host = params.get("api_host", DEFAULT_DATADOG_API_HOST)
        self.api_key = params.get("api_key", DEFAULT_DATADOG_API_KEY)
        self.app_key = params.get("app_key", DEFAULT_DATADOG_APP_KEY)
        if "params" in params:
            self.params = params["params"]
        else:
            self.params = {}

    @property
    def short_name(self):
        """Return the short name."""
        return "datadog"

    @property
    def name(self):
        """Return the name."""
        return "Datadog"

    @property
    def description(self):
        """Return the description."""
        return "Returns monitors from Datadog."

    @property
    def link(self):
        """Return the link."""
        # TODO: Fill ?q= from self.params
        return "%s/monitors/manage" % self.api_host

    @property
    def api(self):
        """Get a Datadog api."""
        if not self._api:
            # This isn't super nice if somebody else in the same
            # process is uinsg it...
            datadog.initialize(
                api_key=self.api_key, app_key=self.app_key, api_host=self.api_host
            )
            self._api = datadog.api

        return self._api

    def tickets(self):
        """Return the tickets."""
        ret = {}

        if not self.api:
            return ret

        monitors = self.api.Monitor.get_all(**self.params)
        for monitor in monitors:
            ticket = self._to_ticket(monitor)
            if ticket is not None:
                ret[ticket["uuid"]] = ticket
        return ret

    def _to_ticket(self, monitor):
        """Return a status or None."""
        logging.debug("Handling %s" % (monitor))

        tags = list(monitor["tags"])
        assignee = None
        priority = None
        summary = monitor["name"]
        text = monitor["message"]
        status = monitor["overall_state"]
        created_on = monitor["created"]
        updated_on = monitor["modified"]

        ticket = base.Ticket(
            ext_id=monitor["id"],
            summary=summary,
            text=text,
            link="https://%s/monitors/%d" % (self.api_host, monitor["id"]),
            project=str(monitor["org_id"]),
            type=monitor["type"],
            assignee=assignee,
            status=status,
            priority=priority,
            tags=tags,
            created_on=created_on,
            modified_on=updated_on,
            raw=monitor,
        )
        return ticket

    def info(self, ticket):
        """Return info that might be interesting for this ticket."""
        data = {}
        return data
