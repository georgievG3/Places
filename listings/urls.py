from django.urls import path

from listings import views

urlpatterns = [
    path('', views.listing_page_view, name='listing-page'),
    path('add-listing/', views.AddListingView.as_view(), name='add-listing'),
]