# -*- coding: utf-8 -*-

"""
Check Cookie Existence View Class
=================================
"""

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

from .view_cookie_check_func import check_cookie_view


class CheckCookieView(View):
    """A class-based view that checks if a specific cookie exists."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return check_cookie_view(request)


__all__: list[str] = ["CheckCookieView"]
