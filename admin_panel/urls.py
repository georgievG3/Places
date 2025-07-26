from django.urls import path

from admin_panel import views

urlpatterns = [
    path('pending/', views.PendingListingsView.as_view(), name='pending_listings'),
    path('pending/listing/<slug:slug>/review/', views.ReviewListingView.as_view(), name='review-listing'),
    path('approve-listing/<slug:slug>/', views.ApproveListingView.as_view(), name='approve-listing'),
    path('add-blog-post/', views.create_blog_post, name='add-blog-post'),
]