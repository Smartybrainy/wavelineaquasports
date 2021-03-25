from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    phone_number = models.BigIntegerField(unique=True)
    country_code = models.IntegerField(default=234)
    full_name = models.CharField(
        _('full_name'), max_length=100, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('is_active'), default=False)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    phone_number_verified = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'country_code']

    class Meta:
        ordering = ('email',)
        verbose_name = _('user',)
        verbose_name_plural = _('users',)

    def get_short_name(self):
        if self.full_name != '':
            return self.full_name
        elif self.email != '':
            return self.email
        return self.phone_number

    def __str__(self):
        return self.email
