from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('Email address'), unique=True)


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Kategorie')


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Instytucje')


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=13)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.institution.name

    class Meta:
        ordering = ('pick_up_date', 'pick_up_time')
        verbose_name_plural = _('Donacje')
