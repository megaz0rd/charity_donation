import datetime
import re
import phonenumbers
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm, UserChangeForm, PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

from sharegood.models import Institution, Category


class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Wprowadzone hasła się różnią.'),

    }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {
            'required': _('Hasło nie może być puste!')
        }
        self.fields['password2'].error_messages = {
            'required': _('Potwierdzenie hasła nie może być puste!')
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
                'unique': _('Podany e-mail jest już zarejestrowany.'),
                'required': _('Musisz podać swój e-mail.')
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


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True,
                                   widget=forms.PasswordInput(),
                                   error_messages={
                                       'required': 'Podaj stare hasło!'
                                   })
    new_password1 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(),
                                    error_messages={
                                        'required': 'Nowe hasło nie może być '
                                                    'puste!'
                                    })
    new_password2 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(),
                                    error_messages={
                                        'required': 'Potwierdzenie nowego '
                                                    'hasła nie może być puste!'
                                    })

    class Meta:
        model = get_user_model()
        fields = (
            'old_password',
            'new_password1',
            'new_password2'
        )


class AddDonationFormStepOne(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class AddDonationFormStepTwo(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'min': 1,
            'step': 1
        })
    )


class AddDonationFormStepThree(forms.Form):

    def __init__(self, *args, **kwargs):
        cat = kwargs['initial']['categories']
        self.institution = forms.ModelChoiceField(
            queryset=Institution.objects.filter(categories__in=[c for c in
                                                                cat]),
            widget=forms.RadioSelect())
        self.declared_fields['institution'] = self.institution
        super(AddDonationFormStepThree, self).__init__(*args, **kwargs)


class AddDonationFormStepFour(forms.Form):
    address = forms.CharField(max_length=256)
    city = forms.CharField(max_length=64)
    zip_code = forms.CharField(max_length=6)
    phone_number = forms.CharField(max_length=13)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(max_length=256)

    def clean_pick_up_date(self):
        date = self.cleaned_data['pick_up_date']
        if date < datetime.date.today():
            raise forms.ValidationError("Nie możesz wybrać daty z przeszłości")
        return date

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if not re.match(r"^\d\d-\d\d\d$", zip_code):
            raise forms.ValidationError("Niepoprawny format kodu pocztowego")
        return zip_code

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phonenumbers.is_valid_number(phonenumbers.parse(phone_number,
                                                               "PL")):
            raise forms.ValidationError(_("Niepoprawny numer telefonu"))
        return phone_number


class AddDonationFormStepFive(forms.Form):
    pass
