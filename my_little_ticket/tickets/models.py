"""Models."""

from django.db import models
from django.core import validators

import jsonfield


_ID_VALIDATOR = validators.RegexValidator(
    r'^[a-zA-Z]+[0-9a-zA-Z-]*$', 'Only alphanumeric characters are allowed.')


class Source(models.Model):
    """A ticket source.

    This will usually be a filter for a ticket system.
    """

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True)
    link = models.URLField(max_length=1024, blank=True)
    py_module = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    params = models.TextField(max_length=1024, blank=True, null=True)
    params_json = jsonfield.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Board(models.Model):
    """A Ticket board."""

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048, blank=True, null=True)
    link = models.URLField(max_length=1024)
    scoring_strategy = models.TextField(max_length=1028, blank=True, null=True)
    sources = models.ManyToManyField(Source, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    word = models.CharField(max_length=64)

    def __str__(self):
        return self.word


class Ticket(models.Model):
    """A (cached) ticket."""

    class Meta:
        unique_together = (('external_id', 'source'),)

    external_id = models.CharField(max_length=64)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE,
                               related_name="source")
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE,
                              related_name="board")

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    refreshed_on = models.DateTimeField(auto_now=True)

    score = models.FloatField(default=0)

    summary = models.CharField(max_length=64)
    text = models.TextField(max_length=1024, blank=True, null=True)
    project = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    assignee = models.CharField(max_length=256)
    status = models.CharField(max_length=64)
    link = models.URLField(max_length=1024, blank=True)
    tags = models.ManyToManyField(Tag)

    # Raw data.
    raw = jsonfield.JSONField(null=True)

    def __str__(self):
        return "%s - %s" % (self.source, self.external_id)
