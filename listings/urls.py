from django.urls import path

from listings import views
from listings.views import ListingDetailsView

urlpatterns = [
    path('listing/<int:pk>/', ListingDetailsView.as_view(), name='listing-detail'),
    path('add-listing/', views.AddListingView.as_view(), name='add-listing'),
]