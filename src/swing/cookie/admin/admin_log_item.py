# -*- coding: utf-8 -*-

"""
Log Item Admin
==============

Admin configuration for consent audit log.

"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import LogItem


class LogItemAdmin(admin.ModelAdmin):
    """Admin configuration for consent audit log."""

    list_display = [
        "timestamp",
        "action",
        "cookiegroup",
        "get_user_display",
        "version",
        "ip_address",
    ]
    list_filter = [
        "action",
        "cookiegroup",
        ("user", admin.EmptyFieldListFilter),
    ]
    search_fields = [
        "user__username",
        "session_key",
        "ip_address",
        "user_agent",
    ]
    readonly_fields = [
        "action",
        "cookiegroup",
        "user",
        "session_key",
        "ip_address",
        "user_agent",
        "version",
        "timestamp",
    ]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    @admin.display(description=_("User/Session"))
    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username
        return (
            f"Session: {obj.session_key[:12]}..."
            if obj.session_key
            else "Unknown"
        )

    def has_add_permission(self, request):
        return False  # Logs are created programmatically only

    def has_change_permission(self, request, obj=None):
        return False  # Logs are immutable


__all__: list[str] = ["LogItemAdmin"]
