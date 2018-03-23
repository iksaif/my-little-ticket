"""Models."""

from django.db import models
from django.core import validators


_ID_VALIDATOR = validators.RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Board(models.Model):
    """A monitored component."""

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048, blank=True, null=True)
    link = models.URLField(max_length=1024)
    scoring_strategy = models.TextField(max_length=1028, blank=True, null=True)

    def __str__(self):
        return self.name
