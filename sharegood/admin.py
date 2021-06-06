from django.contrib import admin

from sharegood.models import Category, Donation, Institution, CustomUser

admin.site.register(Category)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institution_type')
    search_fields = ('name', 'categories', 'institution_type')
    readonly_fields = ('id',)


admin.site.register(Institution, InstitutionAdmin)


class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'institution', 'quantity', 'pick_up_date', 'city')
    search_fields = ('institution', 'categories', 'pick_up_date', 'city',
                     'user')
    readonly_fields = ('id',)


admin.site.register(Donation, DonationAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    readonly_fields = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
