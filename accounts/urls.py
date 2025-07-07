from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views
from accounts.views import Login, ProfileEditView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', views.profile_delete_view, name='profile-delete'),
    ]))
]