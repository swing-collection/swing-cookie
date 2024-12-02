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

# Import | Local Modules
from swing_cookie.models.model_cookie import CookieModel


# =============================================================================
# Function
# =============================================================================

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Get Cookie View Function
    ========================

    Retrieves the value of a specific cookie named "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing the value of the "example_cookie".
    """
    cookie_value: Optional[str] = request.COOKIES.get("example_cookie")
    return HttpResponse(f"Cookie Value: {cookie_value}")


# =============================================================================
# Class
# =============================================================================

class GetCookieView(View):
    """
    Get Cookie View Class
    =====================

    A class-based view that retrieves the value of a specific cookie named 
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
        Handles GET requests to retrieve the value of the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object containing the value of the "example_cookie".
        """
        cookie_value: Optional[str] = request.COOKIES.get("example_cookie")
        return HttpResponse(f"Cookie Value: {cookie_value}")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "get_cookie_view",
    "GetCookieView",
]
