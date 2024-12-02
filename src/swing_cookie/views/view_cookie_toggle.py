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

def toggle_cookie_value_view(request: HttpRequest) -> HttpResponse:
    """
    Toggle Cookie Value View Function
    =================================

    Toggles the value of "toggle_cookie" between "on" and "off".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie value has been toggled.
    """
    current_value = request.COOKIES.get("toggle_cookie", "off")
    new_value = "on" if current_value == "off" else "off"
    response = HttpResponse(f"Cookie toggled to {new_value}")
    response.set_cookie("toggle_cookie", new_value)
    return response


# =============================================================================
# Class
# =============================================================================

class ToggleCookieValueView(View):
    """
    Toggle Cookie Value View Class
    ==============================

    A class-based view that toggles the value of "toggle_cookie" between "on" 
    and "off".

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and toggles the cookie value.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to toggle the value of "toggle_cookie" between 
        "on" and "off".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie value has been toggled.
        """
        current_value = request.COOKIES.get("toggle_cookie", "off")
        new_value = "on" if current_value == "off" else "off"
        response = HttpResponse(f"Cookie toggled to {new_value}")
        response.set_cookie("toggle_cookie", new_value)
        return response



# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cookie_delete_view",
    "CookieDeleteView",
]
