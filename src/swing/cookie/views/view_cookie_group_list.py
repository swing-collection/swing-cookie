# -*- coding: utf-8 -*-

"""
Cookie Group List View
======================

Display all cookie groups.

"""

from django.views.generic import ListView

from ..models import CookieGroup


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup


__all__: list[str] = ["CookieGroupListView"]
