# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
View Cookie Expiry View Class
=============================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_expiry_func import view_cookie_expiry_view


class ViewCookieExpiryView(View):
    """A class-based view that retrieves the expiry date of a cookie."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return view_cookie_expiry_view(request)


__all__: list[str] = ["ViewCookieExpiryView"]
