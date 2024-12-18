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
from typing import Any, Dict

# Import | Libraries
from django.http import HttpResponse, HttpRequest
from django.views import View

# Import | Local Modules
from swing_cookie.models.model_cookie import CookieModel


# =============================================================================
# Function
# =============================================================================

def set_multiple_cookies_view(request: HttpRequest) -> HttpResponse:
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
    response = HttpResponse("Multiple Cookies Set")
    cookies_to_set = {
        "cookie_one": "value_one",
        "cookie_two": "value_two",
        "cookie_three": "value_three",
    }

    for name, value in cookies_to_set.items():
        response.set_cookie(name, value)

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
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        Handles GET requests and updates the cookie value.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
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
        response = HttpResponse("Multiple Cookies Set")
        cookies_to_set = {
            "cookie_one": "value_one",
            "cookie_two": "value_two",
            "cookie_three": "value_three",
        }

        for name, value in cookies_to_set.items():
            response.set_cookie(name, value)

        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "set_multiple_cookies_view",
    "SetMultipleCookiesView",
]
