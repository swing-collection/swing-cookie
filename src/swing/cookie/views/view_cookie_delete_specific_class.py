# -*- coding: utf-8 -*-

"""
Clear Specific Cookies View Class
=================================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_delete_specific_func import clear_specific_cookies_view


class ClearSpecificCookiesView(View):
    """A class-based view that clears cookies based on certain criteria."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return clear_specific_cookies_view(request)


__all__: list[str] = ["ClearSpecificCookiesView"]
