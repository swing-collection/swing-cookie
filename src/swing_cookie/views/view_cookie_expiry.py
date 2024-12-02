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

def view_cookie_expiry_view(request: HttpRequest) -> HttpResponse:
    """
    View Cookie Expiry Date View Function
    =====================================

    Retrieves the expiry date of a specific cookie named "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing the expiry date of the cookie.
    """
    cookie_value = request.COOKIES.get("example_cookie")
    if cookie_value:
        cookie = Cookie.objects.get(name="example_cookie")
        return HttpResponse(f"Cookie Expires On: {cookie.expires}")
    return HttpResponse("Cookie not found")


# =============================================================================
# Class
# =============================================================================

class ViewCookieExpiryView(View):
    """
    View Cookie Expiry Date View Class
    ==================================

    A class-based view that retrieves the expiry date of a specific cookie 
    named "example_cookie".

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and returns the expiry date of the cookie.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve the expiry date of the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object containing the expiry date of the cookie.
        """
        cookie_value = request.COOKIES.get("example_cookie")
        if cookie_value:
            cookie = Cookie.objects.get(name="example_cookie")
            return HttpResponse(f"Cookie Expires On: {cookie.expires}")
        return HttpResponse("Cookie not found")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cookie_delete_view",
    "CookieDeleteView",
]
