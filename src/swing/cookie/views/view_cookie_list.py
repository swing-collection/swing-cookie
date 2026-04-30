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
from typing import Any

# Import | Local Modules
from ..models import CookieModel

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

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
    cookies: dict[str, str] = request.COOKIES
    cookies_list: str = ", ".join(
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
        cookies: dict[str, str] = request.COOKIES
        cookies_list: str = ", ".join(
            [f"{key}: {value}" for key, value in cookies.items()]
        )
        return HttpResponse(content=f"Cookies: {cookies_list}")


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "list_cookies_view",
    "ListCookiesView",
]
