# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Update Cookie View Class
========================

A class-based view for updating cookies.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_update_func import update_cookie_view


class UpdateCookieView(View):
    """
    Update Cookie View Class
    ========================

    A class-based view that updates the value of cookies.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to update cookies.
        """
        return update_cookie_view(request)


__all__: list[str] = ["UpdateCookieView"]
