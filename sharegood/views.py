from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
    DetailView,
    UpdateView
)

from sharegood.forms import LoginForm, RegisterForm, UserEditForm
from sharegood.models import Donation, Institution, CustomUser


class LandingPageView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        quantity = sum([donation.quantity for donation in donations])
        institutions = len(set([donation.institution_id for donation in
                                donations]))
        institution_list = Institution.objects.all()
        context = {
            'quantity': quantity,
            'institutions': institutions,
            'institution_list': institution_list
        }
        return render(request, self.template_name, context)


class AddDonationView(TemplateView):
    template_name = "form.html"


class Login(LoginView):
    form_class = LoginForm
    template_name = "login.html"


class RegisterView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data.get('email')
        user.save()
        return super(RegisterView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie utworzone!"


class ProfileView(UserPassesTestMixin, DetailView):
    """Powers a view to a user model details"""

    model = CustomUser
    template_name = 'profile.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        return self.request.user == self.get_object()


class UserEditView(LoginRequiredMixin, UpdateView):
    """Powers a form to edit a user model"""

    template_name = 'edit_profile.html'
    form_class = UserEditForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()
