from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.authentication_view, name='authenticate'),
]