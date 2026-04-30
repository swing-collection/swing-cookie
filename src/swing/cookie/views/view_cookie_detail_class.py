# -*- coding: utf-8 -*-

"""
Cookie Detail View Class
========================

A class-based view for retrieving cookie details.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_detail_func import view_cookie_details_view


class ViewCookieDetailsView(View):
    """
    View Cookie Details View Class
    ==============================

    A class-based view that retrieves detailed information about cookies
    dynamically based on request parameters.

    Methods:
    --------
    get : Handle GET requests to retrieve cookie details.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve cookie details.
        """
        return view_cookie_details_view(request)


__all__: list[str] = ["ViewCookieDetailsView"]
