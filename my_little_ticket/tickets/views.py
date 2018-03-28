"""Views."""
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


@an_decorators.render_to('index.html')
def index(request):
    """Show the list of boards."""
    boards = models.Board.objects.all()
    return {'boards': boards}


@an_decorators.render_to('board.html')
def board(request, board_id):
    """Show a board."""
    board = shortcuts.get_object_or_404(models.Board, pk=board_id)
    tickets = models.Ticket.objects.filter(board=board)
    return {'board': board, 'tickets': tickets}
