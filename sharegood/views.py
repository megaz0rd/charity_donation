from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    FormView, 
    TemplateView
)
## Uncomment line below for switch from AjaxForm to Session Wizard
# from formtools.wizard.views import SessionWizardView 

from sharegood.forms import (
    # Comment line below for switch from AjaxForm to Session Wizard
    AddDonationSingleForm,
    ## Uncomment lines below for switch from AjaxForm to Session Wizard
    # AddDonationFormStepOne,
    # AddDonationFormStepTwo,
    # AddDonationFormStepThree,
    # AddDonationFormStepFour,
    # AddDonationFormStepFive,
    LoginForm,
    RegisterForm,
    UserEditForm,
    UserPasswordChangeForm, 
)
from sharegood.models import (
    Category,
    CustomUser,
    Donation,
    Institution
)
## Comment line below if switched from AjaxForm to Session Wizard
from sharegood.mixins import AjaxFormMixin

class LandingPageView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        quantity = sum([donation.quantity for donation in donations])
        institutions = len(set([donation.institution_id for donation in
                                donations]))

        foundations = Institution.objects.filter(institution_type='FUND')
        found_paginator = Paginator(foundations, 5)
        ngos = Institution.objects.filter(institution_type='NGOV')
        ngos_paginator = Paginator(ngos, 5)
        charity = Institution.objects.filter(institution_type='CHAR')
        charity_paginator = Paginator(charity, 5)

        page_number = request.GET.get('foundations')
        foundations = found_paginator.get_page(page_number)
        page_number = request.GET.get('page2')
        ngos = ngos_paginator.get_page(page_number)
        page_number = request.GET.get('page3')
        charities = charity_paginator.get_page(page_number)

        context = {
            'quantity': quantity,
            'institutions': institutions,
            'foundations': foundations,
            'ngos': ngos,
            'charities': charities
        }
        return render(request, self.template_name, context)

## Uncomment this view for multistep form powered by SessionWizard
# class AddDonationView(SessionWizardView):
#     template_name = "form.html"
#     form_list = (
#         AddDonationFormStepOne,
#         AddDonationFormStepTwo,
#         AddDonationFormStepThree,
#         AddDonationFormStepFour,
#         AddDonationFormStepFive
#     )
#
#     def get_context_data(self, form, **kwargs):
#         context = super(AddDonationView, self).get_context_data(form, **kwargs)
#         context['categories'] = Category.objects.all()
#         context['institutions'] = Institution.objects.all()
#         return context
#
#     def get(self, request, *args, **kwargs):
#         try:
#             return self.render(self.get_form())
#         except KeyError:
#             return super().get(request, *args, **kwargs)
#
#     def get_form_initial(self, step):
#         if step == '2':
#             step0data = self.get_cleaned_data_for_step('0')
#             if step0data:
#                 categories = step0data.get('categories', '')
#                 return self.initial_dict.get(step, {'categories': categories})
#         return self.initial_dict.get(step, {})
#
#     def done(self, form_list, **kwargs):
#         form_data = [form.cleaned_data for form in form_list]
#         categories = form_data[0]['categories']
#         donation = Donation.objects.create(
#             quantity=form_data[1]['quantity'],
#             institution=form_data[2]['institution'],
#             address=form.cleaned_data['address'],
#             city=form.cleaned_data['city'],
#             zip_code=form.cleaned_data['zip_code'],
#             phone_number=form.cleaned_data['phone_number'],
#             pick_up_date=form.cleaned_data['pick_up_date'],
#             pick_up_time=form.cleaned_data['pick_up_time'],
#             pick_up_comment=form.cleaned_data['pick_up_comment'],
#             user=self.request.user
#         )
#         donation.categories.set(categories)
#         return render(self.request, 'form-confirmation.html', {'form_data': [
#             form.cleaned_data for form in form_list]})

## Comment this view for switch from AjaxForm to SessionWizard
class AddDonationView(AjaxFormMixin, CreateView):
    """Powers the multistep form with jQuery"""

    model = Donation
    template_name = "form.html"
    form_class = AddDonationSingleForm
    success_url = "/formsubmited/"

    def get_context_data(self, **kwargs):
        """Pass the category and institution objects to handle the individual steps of the form"""
        context = super(AddDonationView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['institutions'] = Institution.objects.all()
        return context

    def form_valid(self, form):
        """If form is valid set request.user for object and save"""
        form.instance.user = self.request.user
        form.save()
        return super(AddDonationView, self).form_valid(form)


class DonationSuccess(TemplateView):
    template_name = "form-confirmation.html"


class Login(LoginView):
    """Powers a form to authenticate and log in a user"""

    form_class = LoginForm
    template_name = "login.html"


class RegisterView(SuccessMessageMixin, CreateView):
    """Powers a form to create a user"""

    model = get_user_model()
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Set provieded email as username"""

        user = form.save(commit=False)
        user.username = form.cleaned_data.get('email')
        user.save()
        return super(RegisterView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie utworzone!"


class ProfileView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
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
            'ordered': ordered,
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
