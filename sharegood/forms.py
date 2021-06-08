from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm, UserChangeForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Wprowadzone hasła się różnią.",

    }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {
            'required': 'Hasło nie może być puste!'
        }
        self.fields['password2'].error_messages = {
            'required': 'Potwierdzenie hasła nie może być puste!'
        }

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
        error_messages = {
            'email': {
                'unique': "Podany e-mail jest już zarejestrowany.",
                'required': "Musisz podać swój e-mail."
            }
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField()


class UserEditForm(UserChangeForm):
    """ Form to change user's personal data with password confirmation """

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['confirm_password'].error_messages = {
            'required': 'Hasło nie może być puste!'
        }

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'confirm_password')
        error_messages = {
            'email': {
                'unique': "Podany e-mail jest już zarejestrowany.",
                'required': "Musisz podać swój e-mail."
            },
        }

    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        confirm_password = cleaned_data.get("confirm_password")

        if not check_password(confirm_password, self.instance.password):
            if not self.errors:
                self.add_error('confirm_password', 'Podano błędne hasło.')
