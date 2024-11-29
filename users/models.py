import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


def phone_number_validator(number):
    regex = r"^998\d{9}$"
    if not re.match(regex, number):
        raise ValidationError(_("Phone number must be entered in the format: '998XXXXXXXX'."))
    return number


class User(AbstractUser):
    username = None
    phone = models.CharField(
        max_length=12, validators=[phone_number_validator],
        unique=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
        }
    )
    father_name = models.CharField(
        _("father name"),
        max_length=150,
        blank=True
    )
    language = models.CharField(
        _("language"),
        max_length=2,
        default="uz",
        choices=[("uz", "Uzbek"), ("ru", "Russian"), ("en", "English")]
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email",]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.father_name)
        return full_name.strip()
