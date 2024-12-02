# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Set Views Module
=======================



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
# Functions
# =============================================================================

def check_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Check Cookie Existence View Function
    ====================================

    Checks if a specific cookie named "example_cookie" exists.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating whether the cookie exists or not.
    """
    cookie_exists = "example_cookie" in request.COOKIES
    if cookie_exists:
        return HttpResponse("Cookie exists")
    else:
        return HttpResponse("Cookie does not exist")


# =============================================================================
# Classes
# =============================================================================

class CheckCookieView(View):
    """
    Check Cookie Existence View Class
    =================================

    A class-based view that checks if a specific cookie named "example_cookie" 
    exists.

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
        Handles GET requests to check if the "example_cookie" exists.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating whether the cookie exists or not.
        """
        cookie_exists = "example_cookie" in request.COOKIES
        if cookie_exists:
            return HttpResponse("Cookie exists")
        else:
            return HttpResponse("Cookie does not exist")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "check_cookie_view",
    "CheckCookieView",
]
