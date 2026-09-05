# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Inline Admin
===========================

Inline admin for viewing consent records.

"""

from django.contrib import admin

# Import | Local
from ..models import CookieConsentModel


class CookieConsentInline(admin.TabularInline):
    """
    Inline admin for viewing consent records.
    """

    model = CookieConsentModel
    extra = 0
    fields = ["user", "session_key", "consent_given", "created_at", "ip_address"]
    readonly_fields = [
        "user",
        "session_key",
        "consent_given",
        "created_at",
        "ip_address",
    ]
    can_delete = False
    max_num = 0  # Don't allow adding new records via inline

    def has_add_permission(self, request, obj=None):
        return False


__all__: list[str] = ["CookieConsentInline"]
