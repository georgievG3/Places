from django.urls import path

from listings import views
from listings.views import ListingDetailsView, DeleteImageView

urlpatterns = [
    path('listing/<int:pk>/', ListingDetailsView.as_view(), name='listing-detail'),
    path('add-listing/', views.AddListingView.as_view(), name='add-listing'),
    path('my-listings/', views.UserListingsView.as_view(), name='my-listings'),
    path('edit-listing/<int:pk>/', views.EditListingView.as_view(), name='edit-listing'),
    path('delete-listing/<int:pk>/', views.DeleteListingView.as_view(), name='delete-listing'),
    path('delete-listing-image/<int:pk>/', DeleteImageView.as_view(), name='delete-listing-image'),
]