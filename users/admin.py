from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("phone", "email", "first_name", "last_name", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("phone", "first_name", "last_name", "father_name", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'father_name', 'language')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name", "last_name", "email", 'father_name', 'language'
                )
            }
        )
    )


