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
# Function
# =============================================================================

def update_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Update Cookie View Function
    ===========================

    Updates the value of a specific cookie named "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been updated.
    """
    response = HttpResponse("Cookie Updated")
    # This value can be dynamic or retrieved from request data
    new_value = "updated_value"
    response.set_cookie("example_cookie", new_value)
    return response


# =============================================================================
# Class
# =============================================================================

class UpdateCookieView(View):
    """
    Update Cookie View Class
    ========================

    A class-based view that updates the value of a specific cookie named 
    "example_cookie".

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
        Handles GET requests to update the value of the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie has been updated.
        """
        response = HttpResponse("Cookie Updated")
        new_value = "updated_value"
        response.set_cookie("example_cookie", new_value)
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "update_cookie_view",
    "UpdateCookieView",
]
