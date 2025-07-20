from django.urls import path

from reservations.views import reserve_listing_view, UserReservationsView, UserReservationDeleteView

urlpatterns = [
    path('reserve/<slug:slug>/', reserve_listing_view, name='reserve_listing'),
    path('my-reservations/', UserReservationsView.as_view(), name='my_reservations'),
    path('delete-reservation/<int:pk>/', UserReservationDeleteView.as_view(), name='delete_user_reservation'),
]