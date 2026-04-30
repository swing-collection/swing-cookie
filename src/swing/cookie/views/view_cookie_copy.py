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
# Functions
# =============================================================================


def copy_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Copy Cookie View Function
    =========================

    Copies the value of "example_cookie" to a new cookie named "copied_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been copied.
    """
    original_cookie_value: str | None = request.COOKIES.get("example_cookie")
    if original_cookie_value:
        response = HttpResponse(content="Cookie Copied")
        response.set_cookie(key="copied_cookie", value=original_cookie_value)
        return response
    return HttpResponse(content="Original cookie not found")


# =============================================================================
# Class
# =============================================================================


class CopyCookieView(View):
    """
    Copy Cookie View Class
    ======================

    A class-based view that copies the value of "example_cookie" to a
    new cookie named "copied_cookie".

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
        Handles GET requests to copy the value of "example_cookie" to a new
        cookie.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie has been copied.
        """
        original_cookie_value: str | None = request.COOKIES.get(
            "example_cookie"
        )
        if original_cookie_value:
            response = HttpResponse(content="Cookie Copied")
            response.set_cookie(
                key="copied_cookie",
                value=original_cookie_value,
            )
            return response
        return HttpResponse(content="Original cookie not found")


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "copy_cookie_view",
    "CopyCookieView",
]
