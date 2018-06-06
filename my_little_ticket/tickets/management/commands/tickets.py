"""`tickets` commands."""

import logging

from django.core.management import base
from django.utils import timezone

from my_little_ticket.tickets import models


class Command(base.BaseCommand):
    """Load plugins from settings."""

    help = "Handle tickets"

    def add_arguments(self, _):
        """Add arguments."""
        pass

    def handle(self, *args, **options):
        """Run the command."""
        self.stdout.write("Syncing tickets...")
        sources = models.Source.objects.all()
        for source in sources:
            self.sync_source(source)

    def sync_source(self, source):
        """Fetch tickets for one source."""
        now = timezone.now()
        tickets = set()

        try:
            self.stdout.write(self.style.SUCCESS("Syncing  %s" % source))
            tickets = self.sync_source_safe(source)
        except Exception:
            msg = "Failed to sync %s" % source
            logging.exception(msg)
            self.stderr.write(self.style.ERROR(msg))
            source.failure += 1
            source.failure_on = timezone.now()
            source.save()
        else:
            source.success += 1
            source.success_on = now
            source.save()
        return tickets

    def sync_source_safe(self, source):
        """Fetch ticket for one source, without exception handling."""
        plugin = source.plugin()
        tickets = set(plugin.tickets().items())

        existing_tickets = set(
            models.Ticket.objects.filter(source=source).values_list("id", flat=True)
        )
        updated_tickets = set()
        new_tickets = set()

        for ticket_id, ticket in tickets:
            ticket_obj, created = self._save_ticket(source, ticket_id, ticket)
            if not ticket_obj:
                continue
            if created:
                new_tickets.add(ticket_obj.id)
            else:
                updated_tickets.add(ticket_obj.id)

        outdated_tickets = existing_tickets - updated_tickets
        print("New: %s" % new_tickets)
        print("Updated: %s" % updated_tickets)
        print("Old: %s" % outdated_tickets)

        # Remove old tickets.
        models.Ticket.objects.filter(id__in=outdated_tickets).delete()
        return updated_tickets

    def _save_ticket(self, source, ticket_id, ticket):
        """Save a ticket."""
        ticket_obj = None
        created = False
        try:
            tags = ticket.pop("tags", [])
            ticket_obj, created = models.Ticket.objects.update_or_create(
                uuid=ticket_id, source=source, defaults=ticket
            )
            for tag in tags:
                tag_obj, created = models.Tag.objects.update_or_create(word=tag)
                ticket_obj.tags.add(tag_obj)
            ticket_obj.save()
        except Exception:
            msg = "Failed to save ticket with id #%s (%s)" % (
                ticket_id, ticket_obj.id if ticket_obj else None)
            logging.exception(msg)
            self.stderr.write(self.style.ERROR(msg))
        else:
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    "%s %s:%s config" % (action, source.name, ticket_obj.external_id)
                )
            )
        return ticket_obj, created
