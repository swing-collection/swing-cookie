# -*- coding: utf-8 -*-
from typing import List

from django.contrib import admin

from ..conf import settings
from ..models import Cookie, CookieGroup, LogItem


class CookieAdmin(admin.ModelAdmin):
    """ """

    list_display: List[str] = [
        "varname",
        "name",
        "cookiegroup",
        "path",
        "domain",
        "get_version",
    ]
    search_fields: List[str] = [
        "name",
        "domain",
        "cookiegroup__varname",
        "cookiegroup__name",
    ]
    readonly_fields: List[str] = [
        "varname",
    ]
    list_filter: List[str] = [
        "cookiegroup",
    ]


class CookieGroupAdmin(admin.ModelAdmin):
    """ """

    list_display: List[str] = [
        "varname",
        "name",
        "is_required",
        "is_deletable",
        "get_version",
    ]
    search_fields: List[str] = [
        "varname",
        "name",
    ]
    list_filter: List[str] = [
        "is_required",
        "is_deletable",
    ]


class LogItemAdmin(admin.ModelAdmin):
    """ """

    list_display: List[str] = [
        "action",
        "cookiegroup",
        "version",
        "created",
    ]
    list_filter: List[str] = [
        "action",
        "cookiegroup",
    ]
    readonly_fields: List[str] = [
        "action",
        "cookiegroup",
        "version",
        "created",
    ]
    date_hierarchy = "created"


admin.site.register(
    model_or_iterable=Cookie,
    admin_class=CookieAdmin,
)
admin.site.register(
    model_or_iterable=CookieGroup,
    admin_class=CookieGroupAdmin,
)
if settings.COOKIE_CONSENT_LOG_ENABLED:
    admin.site.register(
        model_or_iterable=LogItem,
        admin_class=LogItemAdmin,
    )
    admin.site.register(
        model_or_iterable=LogItem,
        admin_class=LogItemAdmin,
    )
