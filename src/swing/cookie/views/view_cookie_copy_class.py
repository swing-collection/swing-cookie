# -*- coding: utf-8 -*-

"""
Copy Cookie View Class
======================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_copy_func import copy_cookie_view


class CopyCookieView(View):
    """A class-based view that copies a cookie to a new cookie."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return copy_cookie_view(request)


__all__: list[str] = ["CopyCookieView"]
