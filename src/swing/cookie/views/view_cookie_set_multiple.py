# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Set Views Module
=======================

This module contains views for setting cookie values, including both
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


def set_multiple_cookies_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Set Multiple Cookies View Function
    ==================================

    Sets multiple cookies in a single response.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that multiple cookies have been set.
    """
    response = HttpResponse(content="Multiple Cookies Set")
    cookies_to_set: dict[str, str] = {
        "cookie_one": "value_one",
        "cookie_two": "value_two",
        "cookie_three": "value_three",
    }

    for name, value in cookies_to_set.items():
        response.set_cookie(key=name, value=value)

    return response


# =============================================================================
# Class
# =============================================================================


class SetMultipleCookiesView(View):
    """
    Set Multiple Cookies View Class
    ===============================

    A class-based view that sets multiple cookies in a single response.

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
        Handles GET requests to set multiple cookies.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that multiple cookies have been set.
        """
        response = HttpResponse(content="Multiple Cookies Set")
        cookies_to_set: dict[str, str] = {
            "cookie_one": "value_one",
            "cookie_two": "value_two",
            "cookie_three": "value_three",
        }

        for name, value in cookies_to_set.items():
            response.set_cookie(key=name, value=value)

        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "set_multiple_cookies_view",
    "SetMultipleCookiesView",
]
