# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Admin
====================

Admin configuration for CookieConsent model.

"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Import | Local


class CookieConsentAdmin(admin.ModelAdmin):
    """Admin configuration for CookieConsent model."""

    list_display = [
        "get_user_display",
        "consent_given",
        "necessary",
        "analytics",
        "marketing",
        "consent_date",
        "policy_version",
        "ip_address",
    ]
    list_filter = [
        "consent_given",
        "necessary",
        "analytics",
        "marketing",
        ("user", admin.EmptyFieldListFilter),
    ]
    search_fields = [
        "user__username",
        "user__email",
        "session_key",
        "ip_address",
    ]
    readonly_fields = [
        "user",
        "session_key",
        "necessary",
        "analytics",
        "marketing",
        "consent_given",
        "consent_date",
        "policy_version",
        "ip_address",
    ]
    date_hierarchy = "created_at"

    @admin.display(description=_("User/Session"))
    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username
        return (
            f"Session: {obj.session_key[:12]}..."
            if obj.session_key
            else "Unknown"
        )


__all__: list[str] = ["CookieConsentAdmin"]
