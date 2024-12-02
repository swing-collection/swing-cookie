# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Delete Views Module
==========================

This module contains views for managing cookies, including functions and
class-based views for deleting cookies.

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

def clear_specific_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    Clear Specific Cookies View Function
    ====================================

    Clears all cookies that start with a specific prefix (e.g., "example_").

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the specific cookies have been cleared.
    """
    response = HttpResponse("Specific Cookies Cleared")
    prefix = "example_"
    cookies_to_clear = [
        cookie for cookie in request.COOKIES if cookie.startswith(prefix)
    ]

    for cookie in cookies_to_clear:
        response.delete_cookie(cookie)

    return response

# =============================================================================
# Class
# =============================================================================

class ClearSpecificCookiesView(View):
    """
    Clear Specific Cookies View Class
    =================================

    A class-based view that clears cookies based on certain criteria, such as 
    those that start with a specific prefix (e.g., "example_").

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
        Handles GET requests to clear cookies that start with a specific prefix.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the specific cookies have been cleared.
        """
        response = HttpResponse("Specific Cookies Cleared")
        prefix = "example_"
        cookies_to_clear = [
            cookie for cookie in request.COOKIES if cookie.startswith(prefix)
        ]

        for cookie in cookies_to_clear:
            response.delete_cookie(cookie)

        return response



# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "clear_specific_cookies_view",
    "ClearSpecificCookiesView",
]
