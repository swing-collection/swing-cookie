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
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and deletes all cookies.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
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
    "cookie_delete_view",
    "CookieDeleteView",
]
