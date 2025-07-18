from django.urls import path

from reservations.views import reserve_listing_view, UserReservationsView

urlpatterns = [
    path('reserve/<slug:slug>/', reserve_listing_view, name='reserve_listing'),
    path('my-reservations/', UserReservationsView.as_view(), name='my_reservations'),
]