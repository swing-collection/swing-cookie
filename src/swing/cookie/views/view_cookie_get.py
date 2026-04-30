# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Retrieval Views Module
=============================

This module contains views for retrieving cookie values, including both
function-based and class-based views.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Local Modules
from ..models import CookieModel

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

# =============================================================================
# Function
# =============================================================================


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Get Cookie View Function
    ========================

    Retrieves the value of a specific cookie named "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing the value of the "example_cookie".
    """
    cookie_value: str | None = request.COOKIES.get("example_cookie")
    return HttpResponse(content=f"Cookie Value: {cookie_value}")


# =============================================================================
# Class
# =============================================================================


class GetCookieView(View):
    """
    Get Cookie View Class
    =====================

    A class-based view that retrieves the value of a specific cookie named
    "example_cookie".

    Methods:
    --------
    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        Handles GET requests and updates the cookie value.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve the value of the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object containing the value of the "example_cookie".
        """
        cookie_value: str | None = request.COOKIES.get("example_cookie")
        return HttpResponse(content=f"Cookie Value: {cookie_value}")


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "get_cookie_view",
    "GetCookieView",
]
