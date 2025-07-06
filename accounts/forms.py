from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import forms

UserModel = get_user_model()

class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email']

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