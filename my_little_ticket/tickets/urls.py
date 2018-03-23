"""Urls."""
from django.urls import path
from my_little_ticket.tickets import views

urlpatterns = [
    path('', views.index, name='index'),
]
