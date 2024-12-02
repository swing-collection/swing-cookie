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

def list_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    List Cookies View Function
    ==========================

    Lists all cookies present in the request.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing a list of all cookies and their values.
    """
    cookies = request.COOKIES
    cookies_list = ", ".join(
        [f"{key}: {value}" for key, value in cookies.items()]
    )
    return HttpResponse(f"Cookies: {cookies_list}")


# =============================================================================
# Class
# =============================================================================

class ListCookiesView(View):
    """
    List Cookies View Class
    =======================

    A class-based view that lists all cookies present in the request.

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
        Handles GET requests to list all cookies present in the request.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object containing a list of all cookies and their values.
        """
        cookies = request.COOKIES
        cookies_list = ", ".join(
            [f"{key}: {value}" for key, value in cookies.items()]
        )
        return HttpResponse(f"Cookies: {cookies_list}")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "list_cookies_view",
    "ListCookiesView",
]
