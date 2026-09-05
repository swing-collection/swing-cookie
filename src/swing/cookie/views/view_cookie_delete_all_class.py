# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Delete All Cookies View Class
=============================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_delete_all_func import delete_all_cookies_view


class DeleteAllCookiesView(View):
    """A class-based view that deletes all cookies present in the request."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return delete_all_cookies_view(request)


__all__: list[str] = ["DeleteAllCookiesView"]
