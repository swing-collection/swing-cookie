# -*- coding: utf-8 -*-

"""
List Cookies View Class
=======================

A class-based view for listing all cookies.

"""

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

from .view_cookie_list_func import list_cookies_view


class ListCookiesView(View):
    """
    List Cookies View Class
    =======================

    A class-based view that lists all cookies present in the request.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to list all cookies present in the request.
        """
        return list_cookies_view(request)


__all__: list[str] = ["ListCookiesView"]
