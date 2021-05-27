from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    class InstitutionType(models.TextChoices):
        FOUNDATION = 'FUND', _('Fundacja')
        NON_GOV = 'NGOV', _('Organizacja pozarządowa')
        CHARITY = 'CHAR', _('Zbiórka lokalna')

    name = models.CharField(max_length=128)
    description = models.TextField()
    institution_type = models.CharField(max_length=4,
                                        choices=InstitutionType.choices,
                                        default=InstitutionType.FOUNDATION)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=13)
    pick_up_date = models.DateField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
