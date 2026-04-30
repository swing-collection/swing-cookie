# -*- coding: utf-8 -*-

"""
Cookie Inline Admin
===================

Inline admin for editing cookies within a cookie group.

"""

from django.contrib import admin

# Import | Local
from ..models import Cookie


class CookieInline(admin.TabularInline):
    """
    Inline admin for editing cookies within a cookie group.
    """

    model = Cookie
    extra = 1
    fields = ["name", "path", "domain", "secure", "httponly"]
    show_change_link = True


__all__: list[str] = ["CookieInline"]
