from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from sharegood.models import Donation


class LandingPage(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        quantity = sum([donation.quantity for donation in donations])
        institutions = len(set([donation.institution_id for donation in
                                donations]))
        context = {
            'quantity': quantity,
            'institutions': institutions
        }
        return render(request, self.template_name, context)


class AddDonation(TemplateView):
    template_name = "form.html"


class Login(TemplateView):
    template_name = "login.html"


class Register(TemplateView):
    template_name = "register.html"
