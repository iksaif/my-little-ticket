"""tickets metrics."""

import time
import prometheus_client

from django.conf import settings
from my_little_ticket.tickets import models


class TicketsCollector(object):
    """Collector to export tickets metrics."""

    def __init__(self, registry=prometheus_client.REGISTRY):
        """Create a new tickets collector."""
        self._first = True
        if registry:
            registry.register(self)

    def collect(self):
        """Collect all metrics."""
        if self._first:
            # Avoid collecting when running from manage.py.
            self._first = False
            return []

        metrics = []

        labels = ["id", "name"]
        success_on = prometheus_client.core.GaugeMetricFamily(
            "source_success_on", "Last success for this source", labels=labels
        )
        failure_on = prometheus_client.core.GaugeMetricFamily(
            "source_failure_on", "Last failure for this source", labels=labels
        )
        success = prometheus_client.core.CounterMetricFamily(
            "source_success_total", "Success counter per source", labels=labels
        )
        failure = prometheus_client.core.CounterMetricFamily(
            "source_failure_total", "failure counter per source", labels=labels
        )
        for source in models.Source.objects.all():
            labels = [str(source.id), source.name]
            timestamp = time.mktime(
                source.success_on.timetuple()
            ) if source.success_on else 0
            success_on.add_metric(labels, timestamp)
            timestamp = time.mktime(
                source.failure_on.timetuple()
            ) if source.failure_on else 0
            failure_on.add_metric(labels, timestamp)
            success.add_metric(labels, source.success)
            failure.add_metric(labels, source.failure)
        metrics.extend([success_on, failure_on, success, failure])

        return metrics


if getattr(settings, "TICKETS_METRICS", True):
    tickets_collector = TicketsCollector()
