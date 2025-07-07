from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import AppUserCreationForm, AuthForm, ProfileEditForm
from accounts.models import Profile

UserModel = get_user_model()
# Create your views here.
class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        if response.status_code in [301, 302]:
            login(self.request, self.object)

        return response


class Login(LoginView):
    authentication_form = AuthForm


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileEditView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'
    success_url = reverse_lazy('profile-details')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def profile_delete_view(request):
    return render(request, 'accounts/profile-delete-page.html')
