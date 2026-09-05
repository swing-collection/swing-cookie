# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Admin
============

Admin configuration for Cookie model.

"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Import | Local


class CookieAdmin(admin.ModelAdmin):
    """Admin configuration for Cookie model."""

    list_display = [
        "name",
        "cookiegroup",
        "path",
        "domain",
        "secure_badge",
        "httponly_badge",
    ]
    list_filter = [
        "cookiegroup",
        "secure",
        "httponly",
    ]
    search_fields = [
        "name",
        "domain",
        "cookiegroup__varname",
        "cookiegroup__name",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("name", "cookiegroup", "value"),
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
