# -*- coding: utf-8 -*-

"""
Dismiss Cookie Banner View Class
================================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_banner_dismiss_func import dismiss_cookie_banner_view


class DismissCookieBannerView(View):
    """A class-based view that handles cookie banner dismissal."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return dismiss_cookie_banner_view(request)


__all__: list[str] = ["DismissCookieBannerView"]
