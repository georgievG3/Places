from django.urls import path

from reservations.views import reserve_listing

urlpatterns = [
    path('reserve/<slug:slug>/', reserve_listing, name='reserve_listing'),
]