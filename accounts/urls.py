from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views
from accounts.views import Login

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]