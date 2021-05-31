from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

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


class Login(TemplateView):
    template_name = "login.html"


class Register(CreateView):
    model = get_user_model()
    fields = ['email', 'password', 'first_name', 'last_name']
    template_name = "register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.username = form.cleaned_data.get('email')
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        return super(Register, self).form_valid(form)
