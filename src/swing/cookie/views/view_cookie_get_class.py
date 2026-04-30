# -*- coding: utf-8 -*-

"""
Get Cookie View Class
=====================

A class-based view that retrieves cookie values dynamically.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_get_func import get_cookie_view


class GetCookieView(View):
    """
    Get Cookie View Class
    =====================

    A class-based view that retrieves cookie values dynamically.

    Methods:
    --------
    get : Handle GET requests to retrieve cookies.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve a cookie.
        """
        return get_cookie_view(request)


__all__: list[str] = ["GetCookieView"]
