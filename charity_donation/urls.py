"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from sharegood import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', views.LandingPageView.as_view(), name='landing-page'),
    path('donate/', views.AddDonationView.as_view(), name='add-donation'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.UserEditView.as_view(), name='edit-profile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('change_password/', views.UserPasswordChangeView.as_view(),
         name='change-password')

]
