# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Delete Views Module
==========================


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

def delete_all_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    Delete All Cookies View Function
    ================================

    Deletes all cookies present in the request.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that all cookies have been deleted.
    """
    response = HttpResponse("All Cookies Deleted")
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response


# =============================================================================
# Class
# =============================================================================

class DeleteAllCookiesView(View):
    """
    Delete All Cookies View Class
    =============================

    A class-based view that deletes all cookies present in the request.

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
        Handles GET requests to delete all cookies present in the request.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that all cookies have been deleted.
        """
        response = HttpResponse("All Cookies Deleted")
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "delete_all_cookies_view",
    "DeleteAllCookiesView",
]
