from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
    DetailView,
    UpdateView,
    ListView
)

from sharegood.forms import (
    RegisterForm,
    LoginForm,
    UserEditForm,
    UserPasswordChangeForm
)
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


class UserEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Powers a form to edit a user model"""

    template_name = 'edit_profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('landing-page')

    def get_object(self):
        return self.request.user

    def get_success_message(self, cleaned_data):
        return "Twoje dane zostały zmienione!"


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """Powers a form to edit a user's password"""

    template_name = 'registration/change_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('landing-page')

    def get_success_message(self, cleaned_data):
        return "Twoje hasło zostało zmienione!"


class DonationListView(LoginRequiredMixin, View):
    """Powers a view to a list of user's donations"""

    template_name = 'donations.html'

    def get(self, request, *args, **kwargs):
        """Create new field 'my_dt' on model Donation to filter by combined
        two other model's fields: Date and Time Field. Pass the results to
        context."""
        user_donations = Donation.objects.annotate(
            my_dt=ExpressionWrapper(F('pick_up_date') + F('pick_up_time'),
                                    output_field=DateTimeField())).filter(
            user=request.user)

        picked_up = user_donations.filter(my_dt__lt=timezone.now())
        ordered = user_donations.filter(my_dt__gt=timezone.now())
        context = {
            'picked_up': picked_up,
            'ordered': ordered
        }
        return render(request, self.template_name, context)


class DonationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Powers a view to a donation's details"""

    model = Donation
    template_name = 'donation_detail.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """Forbidden access to the view if object Donation not belong to
        request.user """
        return self.request.user == self.get_object().user
