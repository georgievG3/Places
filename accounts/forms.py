from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from accounts.models import Profile

UserModel = get_user_model()

class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(AppUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].error_messages = {
            'required': 'Моля, въведи имейл адрес.',
            'invalid': 'Невалиден имейл адрес.',
            'unique': 'Този имейл адрес вече е зает.'
        }

        self.fields['password1'].error_messages = {
            'required': 'Моля, въведи парола.',
            'password_too_short': 'Паролата е прекалено кратка.',
            'password_too_common': 'Паролата е прекалено често използвана.',
            'password_entirely_numeric': 'Паролата не може да бъде само числа.'
        }

        self.fields['password2'].error_messages = {
            'required': 'Моля, потвърди паролата.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролите не съвпадат.")
        return password2


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AuthForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "Моля, въведете правилен имейл и парола."
        ),
        "inactive": ("Този акаунт не е активен.."),
    }


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'profile_details','date_of_birth']

        labels = {
            'profile_picture': 'Профилна снимка',
            'phone_number': 'Телефонен номер',
            'profile_details': 'Детайли за профила',
            'date_of_birth': 'Дата на раждане',
        }


class ProfileEditForm(ProfileBaseForm):
    first_name = forms.CharField(label='Име', max_length=30, required=False)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']

        if commit:
            self.user.save()
            profile.save()

        return profile
