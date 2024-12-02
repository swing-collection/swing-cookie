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
from typing import Any, Dict, Optional

# Import | Libraries
from django.http import HttpResponse, HttpRequest
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
    original_cookie_value = request.COOKIES.get("example_cookie")
    if original_cookie_value:
        response = HttpResponse("Cookie Copied")
        response.set_cookie("copied_cookie", original_cookie_value)
        return response
    return HttpResponse("Original cookie not found")


# =============================================================================
# Class
# =============================================================================

class CopyCookieView(View):
    """
    Copy Cookie View Class
    ======================

    A class-based view that copies the value of "example_cookie" to a new cookie 
    named "copied_cookie".

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and copies the cookie value.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
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
        original_cookie_value = request.COOKIES.get("example_cookie")
        if original_cookie_value:
            response = HttpResponse("Cookie Copied")
            response.set_cookie("copied_cookie", original_cookie_value)
            return response
        return HttpResponse("Original cookie not found")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "get_cookie_view",
    "GetCookieView",
]