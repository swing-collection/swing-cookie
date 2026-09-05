# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Policy Admin
===================

Admin configuration for CookiePolicy model.

"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Import | Local


class CookiePolicyAdmin(admin.ModelAdmin):
    """Admin configuration for CookiePolicy model."""

    list_display = [
        "version",
        "is_active_badge",
        "effective_date",
        "created_at",
    ]
    list_filter = [
        "is_active",
    ]
    search_fields = [
        "version",
        "content",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    fieldsets = [
        (
            None,
            {
                "fields": ("version", "is_active", "effective_date"),
            },
        ),
        (
            _("Policy Content"),
            {
                "fields": ("content",),
                "classes": ("wide",),
            },
        ),
    ]

    @admin.display(description=_("Active"), boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


__all__: list[str] = ["CookiePolicyAdmin"]
