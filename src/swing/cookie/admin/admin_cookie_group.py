# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Group Admin
==================

Admin configuration for CookieGroup model with inline cookies.

"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Import | Local
from .admin_cookie_inline import CookieInline

# NOTE: CookieConsentInline is intentionally not used here. CookieConsentModel
# tracks consent per user/session (with necessary/analytics/marketing flags),
# not per CookieGroupModel - there is no ForeignKey relating the two models,
# so it cannot be registered as an inline on CookieGroupAdmin.


class CookieGroupAdmin(admin.ModelAdmin):
    """Admin configuration for CookieGroup model with inline cookies."""

    list_display = [
        "varname",
        "name",
        "is_required_badge",
        "is_deletable_badge",
        "cookie_count",
        "ordering",
        "get_version",
    ]
    list_filter = [
        "is_required",
        "is_deletable",
    ]
    search_fields = [
        "varname",
        "name",
        "description",
    ]
    list_editable = ["ordering"]
    ordering = ["ordering", "name"]
    inlines = [CookieInline]
    fieldsets = [
        (
            None,
            {
                "fields": ("varname", "name", "description"),
            },
        ),
        (
            _("Behavior"),
            {
                "fields": ("is_required", "is_deletable", "ordering"),
            },
        ),
    ]

    @admin.display(description=_("Required"), boolean=True)
    def is_required_badge(self, obj):
        return obj.is_required

    @admin.display(description=_("Deletable"), boolean=True)
    def is_deletable_badge(self, obj):
        return obj.is_deletable

    @admin.display(description=_("Cookies"))
    def cookie_count(self, obj):
        count = obj.cookie_set.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            "#28a745" if count > 0 else "#6c757d",
            count,
        )


__all__: list[str] = ["CookieGroupAdmin"]
