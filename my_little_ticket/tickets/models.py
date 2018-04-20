"""Models."""

import uuid

from django.utils import timezone
from django.db import models
from django.core import validators
from django.conf import settings
from django.utils import module_loading

import jsonfield


_ID_VALIDATOR = validators.RegexValidator(
    r'^[a-zA-Z]+[0-9a-zA-Z-]*$', 'Only alphanumeric characters are allowed.')


class Source(models.Model):
    """A ticket source.

    This will usually be a filter for a ticket system.
    """
    PLUGINS_CHOICES = ((s, s) for s in settings.MLT_PLUGINS)

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True)
    link = models.URLField(max_length=1024, blank=True)
    py_module = models.CharField(max_length=255, choices=PLUGINS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    params = jsonfield.JSONField(blank=True, null=True)

    success = models.PositiveIntegerField(default=0)
    failure = models.PositiveIntegerField(default=0)
    success_on = models.DateTimeField(null=True, blank=True)
    failure_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Board(models.Model):
    """A Ticket board."""
    STRATEGY_CHOICES = ((s, s) for s in settings.MLT_STRATEGIES)

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048, blank=True, null=True)
    link = models.URLField(max_length=1024)
    strategy_py_module = models.CharField(max_length=255, choices=STRATEGY_CHOICES)
    strategy_params = jsonfield.JSONField(blank=True, null=True)
    sources = models.ManyToManyField(Source, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def strategy(self):
        py_module = self.strategy_py_module or 'my_little_ticket.plugins.default.DefaultStrategy'
        strategy_class = module_loading.import_string(py_module)
        return strategy_class(self.strategy_params or {})


class Tag(models.Model):
    word = models.CharField(max_length=64)

    def __str__(self):
        return self.word


class Ticket(models.Model):
    """A (cached) ticket."""

    class Meta:
        unique_together = (('external_id', 'source'),)

    # A stable id for each individual event.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=64)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE,
                               related_name="source")

    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=timezone.now)
    refreshed_on = models.DateTimeField(auto_now=True)

    summary = models.CharField(max_length=64)
    text = models.TextField(max_length=1024, blank=True, null=True)
    project = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    assignee = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)
    link = models.URLField(max_length=1024, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # Raw data.
    raw = jsonfield.JSONField(null=True)

    def __str__(self):
        return "%s - %s" % (self.source, self.external_id)
