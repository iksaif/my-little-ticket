"""Urls."""
from django.urls import path
from my_little_ticket.tickets import views

# pylama:ignore=W0611
# Add metrics to the registry
from my_little_ticket.tickets import metrics

# pylama:select=W0611


urlpatterns = [
    path("", views.index, name="index"),
    path(r"board/<slug:board_id>/", views.board, name="board"),
]
