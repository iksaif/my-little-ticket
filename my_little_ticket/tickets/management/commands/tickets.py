"""`tickets` commands."""

import logging

from django.core.management import base
from django.utils import timezone
from django.utils import module_loading

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
        plugin_class = module_loading.import_string(source.py_module)
        plugin = plugin_class(source.params)
        tickets = set(plugin.tickets().items())

        existing_tickets = set(
            models.Ticket.objects.filter(source=source).values_list("id", flat=True)
        )

        for ticket_id, ticket in tickets:
            self._save_ticket(source, ticket_id, ticket)

        updated_tickets = set([ticket_id for ticket_id, _ in tickets])

        outdated_tickets = existing_tickets - updated_tickets
        new_tickets = updated_tickets - existing_tickets
        updated_tickets -= new_tickets
        print("New: %s" % new_tickets)
        print("Updated: %s" % updated_tickets)
        print("Old: %s" % outdated_tickets)

        # Remove old tickets.
        models.Ticket.objects.filter(id__in=outdated_tickets).delete()
        return updated_tickets

    def _save_ticket(self, source, ticket_id, ticket):
        """Save a ticket."""
        try:
            tags = ticket.pop("tags", [])
            ticket_obj, created = models.Ticket.objects.update_or_create(
                id=ticket_id, source=source, defaults=ticket
            )
            for tag in tags:
                tag_obj, created = models.Tag.objects.update_or_create(word=tag)
                ticket_obj.tags.add(tag_obj)
        except Exception:
            msg = "Failed to save ticket with id #%s" % ticket_id
            logging.exception(msg)
            self.stderr.write(self.style.ERROR(msg))
        else:
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    "%s %s:%s config" % (action, source.name, ticket_obj.external_id)
                )
            )
