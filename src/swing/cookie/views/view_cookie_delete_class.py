# -*- coding: utf-8 -*-

"""
Cookie Delete View Class
========================

A class-based view that deletes cookies dynamically.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_delete_func import cookie_delete_view


class CookieDeleteView(View):
    """
    Cookie Delete View Class
    ========================

    A class-based view that deletes cookies dynamically.

    Methods:
    --------
    get, post, delete : Handle requests to delete cookies.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """Handles GET requests to delete a cookie."""
        return cookie_delete_view(request)

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """Handles POST requests to delete a cookie."""
        return cookie_delete_view(request)

    def delete(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """Handles DELETE requests to delete a cookie."""
        return cookie_delete_view(request)


__all__: list[str] = ["CookieDeleteView"]
