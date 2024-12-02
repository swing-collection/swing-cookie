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

def view_cookie_details_view(request: HttpRequest) -> HttpResponse:
    """
    View Cookie Details View Function
    =================================

    Retrieves detailed information about a specific cookie named 
    "example_cookie".

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing detailed information about the cookie.
    """
    try:
        cookie = Cookie.objects.get(name="example_cookie")
        details = f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain}, " \
                  f"Path: {cookie.path}, Expires: {cookie.expires}, Secure: {cookie.secure}, " \
                  f"HTTPOnly: {cookie.httponly}"
        return HttpResponse(f"Cookie Details: {details}")
    except Cookie.DoesNotExist:
        return HttpResponse("Cookie not found")


# =============================================================================
# Class
# =============================================================================

class ViewCookieDetailsView(View):
    """
    View Cookie Details View Class
    ==============================
    A class-based view that retrieves detailed information about a specific 
    cookie named "example_cookie".

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and returns detailed information about the cookie.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve detailed information about the 
        "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object containing detailed information about the cookie.
        """
        try:
            cookie = Cookie.objects.get(name="example_cookie")
            details = f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain}, " \
                    f"Path: {cookie.path}, Expires: {cookie.expires}, Secure: {cookie.secure}, " \
                    f"HTTPOnly: {cookie.httponly}"
            return HttpResponse(f"Cookie Details: {details}")
        except Cookie.DoesNotExist:
            return HttpResponse("Cookie not found")

# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cookie_delete_view",
    "CookieDeleteView",
]
