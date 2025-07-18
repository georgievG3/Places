from django.urls import path

from listings import views
from listings.views import ListingDetailsView, DeleteImageView

# urlpatterns = [
#     path('listing/<slug:slug>/', ListingDetailsView.as_view(), name='listing-detail'),
#     path('add-listing/', views.AddListingView.as_view(), name='add-listing'),
#     path('my-listings/', views.UserListingsView.as_view(), name='my-listings'),
#     path('edit-listing/<slug:slug>/', views.EditListingView.as_view(), name='edit-listing'),
#     path('delete-listing/<slug:slug>/', views.DeleteListingView.as_view(), name='delete-listing'),
#     path('delete-listing-image/<int:pk>/', DeleteImageView.as_view(), name='delete-listing-image'),
# ]

urlpatterns = [
    path('listing/<slug:slug>/', ListingDetailsView.as_view(), name='listing-detail'),
    path('add-listing/', views.AddListingView.as_view(), name='add-listing'),
    path('my-listings/', views.UserListingsView.as_view(), name='my-listings'),
    path('edit-listing/<slug:slug>/', views.EditListingView.as_view(), name='edit-listing'),
    path('delete-listing/<slug:slug>/', views.DeleteListingView.as_view(), name='delete-listing'),
    path('delete-listing-image/<int:pk>/', DeleteImageView.as_view(), name='delete-listing-image'),
]