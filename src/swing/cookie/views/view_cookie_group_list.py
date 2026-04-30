# -*- coding: utf-8 -*-

"""
Cookie Group List View
======================

Display all cookie groups.

"""

from django.views.generic import ListView

# Import | Local
from ..models import CookieGroup


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup
    template_name = "swing_cookie/cookiegroup_list.html"


__all__: list[str] = ["CookieGroupListView"]
