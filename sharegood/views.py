from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView

from sharegood.forms import LoginForm, RegisterForm
from sharegood.models import Donation, Institution


class LandingPage(View):
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


class AddDonation(TemplateView):
    template_name = "form.html"


class Login(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = reverse_lazy('landing-page')


class Register(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data.get('email')
        user.save()
        return super(Register, self).form_valid(form)
