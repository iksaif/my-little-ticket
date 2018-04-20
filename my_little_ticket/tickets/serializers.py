"""Serializers for defcon.status."""
from rest_framework import serializers
from my_little_ticket.tickets import models


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Boards."""

    class Meta:
        """Configuration."""

        model = models.Board
        fields = "__all__"


# TODO: Display tickets here.


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Plugin."""

    class Meta:
        """Configuration."""

        model = models.Ticket
        # TODO:
        # - Filter by board
        # - Fix raw (JSONField)
        # - Display tags
        # fields = '__all__'
        exclude = ("raw", "tags")


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for PluginInstance."""

    class Meta:
        """Configuration."""

        model = models.Source
        # TODO:
        # - Fix raw (JSONField)
        # fields = '__all__'
        exclude = ("params_json",)
