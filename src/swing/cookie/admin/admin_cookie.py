# -*- coding: utf-8 -*-

"""
Cookie Admin
============

Admin configuration for Cookie model.

"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Cookie


class CookieAdmin(admin.ModelAdmin):
    """Admin configuration for Cookie model."""

    list_display = [
        "name",
        "group",
        "path",
        "domain",
        "secure_badge",
        "httponly_badge",
    ]
    list_filter = [
        "group",
        "secure",
        "httponly",
    ]
    search_fields = [
        "name",
        "domain",
        "group__varname",
        "group__name",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("name", "group", "value"),
            },
        ),
        (
            _("Cookie Settings"),
            {
                "fields": ("path", "domain", "expires"),
            },
        ),
        (
            _("Security"),
            {
                "fields": ("secure", "httponly"),
            },
        ),
    ]

    @admin.display(description=_("Secure"), boolean=True)
    def secure_badge(self, obj):
        return obj.secure

    @admin.display(description=_("HTTPOnly"), boolean=True)
    def httponly_badge(self, obj):
        return obj.httponly


__all__: list[str] = ["CookieAdmin"]
