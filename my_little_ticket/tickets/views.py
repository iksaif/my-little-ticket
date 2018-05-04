"""Views."""
import collections
from django import shortcuts
from annoying import decorators as an_decorators
from my_little_ticket.tickets import models
from my_little_ticket.tickets import serializers


from rest_framework import viewsets
from rest_framework import permissions


class BoardsViewSet(viewsets.ReadOnlyModelViewSet):
    """API view for Boards with expanded statuses."""

    queryset = models.Board.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.BoardSerializer


class SourcesViewSet(viewsets.ReadOnlyModelViewSet):
    """API view for Sources with expanded statuses."""

    queryset = models.Source.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.SourceSerializer


class TicketsViewSet(viewsets.ReadOnlyModelViewSet):
    """API view for Tickets with expanded statuses."""

    queryset = models.Ticket.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.TicketSerializer


@an_decorators.render_to("index.html")
def index(request):
    """Show the list of boards."""
    boards = models.Board.objects.all()
    return {"boards": boards}


@an_decorators.render_to("board.html")
def board(request, board_id):
    """Show a board."""
    board = shortcuts.get_object_or_404(models.Board, pk=board_id)
    tickets = set()
    for source in board.sources.all():
        tickets |= set(models.Ticket.objects.filter(source=source))

    # TODO: Move elsewhere.
    strategy = board.strategy()
    groups = collections.defaultdict(list)
    for ticket in tickets:
        ticket.strategy_score = strategy.score(ticket)
        ticket.strategy_status = strategy.status(ticket)
        ticket.strategy_group = strategy.group(ticket)
        groups[ticket.strategy_group].append(ticket)

    # Sort everything.
    for group, tickets in list(groups.items()):
        tickets = sorted(tickets, key=lambda t: t.strategy_score, reverse=True)
        groups[group] = tickets

    groups = sorted(list(groups.items()), key=lambda k: k[0])
    return {"board": board, "groups": groups}
