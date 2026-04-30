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
from typing import Any

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local Modules
from ..models import CookieModel

# =============================================================================
# Function
# =============================================================================


def cookie_delete_view(request: HttpRequest) -> HttpResponse:
    """
    Cookie Delete View Function
    ===========================

    Deletes a specific cookie named "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been deleted.
    """
    response = HttpResponse(content="Cookie Deleted")
    response.delete_cookie(key="example_cookie")
    return response


# =============================================================================
# Class
# =============================================================================


class CookieDeleteView(View):
    """
    Cookie Delete View Class
    ========================

    A class-based view that deletes a specific cookie named "example_cookie".

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
        Handles GET requests to delete the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie has been deleted.
        """
        response = HttpResponse(content="Cookie Deleted")
        response.delete_cookie(key="example_cookie")
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "cookie_delete_view",
    "CookieDeleteView",
]
