# -*- coding: utf-8 -*-

"""
Toggle Cookie Value View Class
==============================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_toggle_func import toggle_cookie_value_view


class ToggleCookieValueView(View):
    """A class-based view that toggles a cookie value between "on" and "off"."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return toggle_cookie_value_view(request)


__all__: list[str] = ["ToggleCookieValueView"]
