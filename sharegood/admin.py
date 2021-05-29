from django.contrib import admin

from sharegood.models import Category, Donation, Institution

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
