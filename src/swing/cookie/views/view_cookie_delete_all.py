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
from typing import Any

# Import | Local Modules
from ..models import CookieModel

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

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
    response = HttpResponse(content="All Cookies Deleted")
    for cookie in request.COOKIES:
        response.delete_cookie(key=cookie)
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
        response = HttpResponse(content="All Cookies Deleted")
        for cookie in request.COOKIES:
            response.delete_cookie(key=cookie)
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "delete_all_cookies_view",
    "DeleteAllCookiesView",
]
