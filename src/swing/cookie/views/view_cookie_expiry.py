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
from typing import Any, Dict, List

# Import | Local Modules
from cookie.models.model_cookie import CookieModel

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

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
    cookie_value: str | None = request.COOKIES.get("example_cookie")
    if cookie_value:
        cookie = CookieModel.objects.get(name="example_cookie")
        return HttpResponse(content=f"Cookie Expires On: {cookie.expires}")
    return HttpResponse(content="Cookie not found")


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
            cookie = CookieModel.objects.get(name="example_cookie")
            return HttpResponse(content=f"Cookie Expires On: {cookie.expires}")
        return HttpResponse(content="Cookie not found")


# =============================================================================
# Module Exports
# =============================================================================

__all__: List[str] = [
    "view_cookie_expiry_view",
    "ViewCookieExpiryView",
]
