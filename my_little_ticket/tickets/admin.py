"""Admin classes for my_little_ticket.status."""
from django.contrib import admin
from my_little_ticket.tickets import models


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    """Admin for Source."""

    list_display = ("name", "description", "link")


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin for Board."""

    list_display = ("name", "description", "link")


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin for Ticket."""

    list_display = ("external_id", "summary", "source", "created_on", "modified_on")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag."""

    list_display = ("word",)
