# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Set Multiple Cookies View Class
===============================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_set_multiple_func import set_multiple_cookies_view


class SetMultipleCookiesView(View):
    """A class-based view that sets multiple cookies in a single response."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return set_multiple_cookies_view(request)


__all__: list[str] = ["SetMultipleCookiesView"]
