# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Set Cookie View Class
=====================

A class-based view that sets cookies dynamically.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_set_func import set_cookie_view


class SetCookieView(View):
    """
    Set Cookie View Class
    =====================

    A class-based view that sets cookies dynamically.

    Methods:
    --------
    get, post : Handle requests to set cookies.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to set a cookie.
        """
        return set_cookie_view(request)

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles POST requests to set a cookie.
        """
        return set_cookie_view(request)


__all__: list[str] = ["SetCookieView"]
