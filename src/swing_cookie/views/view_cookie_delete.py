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



# =============================================================================
# Function
# =============================================================================

def cookie_delete_view(request: HttpRequest) -> HttpResponse:
    """
    Cookie Delete View Function
    ===========================

    Deletes a specific cookie named 'example_cookie'.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been deleted.
    """
    response = HttpResponse("Cookie Deleted")
    response.delete_cookie('example_cookie')
    return response


# =============================================================================
# Class
# =============================================================================

class CookieDeleteView(View):
    """
    Cookie Delete View Class
    ========================

    A class-based view that deletes a specific cookie named 'example_cookie'.

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and deletes the cookie.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        """
        Handles GET requests to delete the 'example_cookie'.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie has been deleted.
        """
        response = HttpResponse("Cookie Deleted")
        response.delete_cookie('example_cookie')
        return response



# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cookie_delete_view",
    "CookieDeleteView",
]
