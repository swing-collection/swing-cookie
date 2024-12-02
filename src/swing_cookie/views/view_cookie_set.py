# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Set Views Module
=======================

This module contains views for setting cookie values, including both 
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
from .models import Cookie


# =============================================================================
# Function
# =============================================================================

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Set Cookie View Function
    ========================

    Sets a specific cookie named "example_cookie" and saves it to the database.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been set.
    """
    response = HttpResponse("Cookie Set")
    cookie = Cookie(
        name="example_cookie",
        value="example_value",
        domain=request.get_host(),
        path="/",
        expires=None,
        secure=False,
        httponly=True
    )
    cookie.save()
    response.set_cookie(
        key=cookie.name,
        value=cookie.value,
        domain=cookie.domain,
        path=cookie.path,
        expires=cookie.expires,
        secure=cookie.secure,
        httponly=cookie.httponly
    )
    return response


# =============================================================================
# Class
# =============================================================================

class SetCookieView(View):
    """
    Set Cookie View Class
    =====================

    A class-based view that sets a specific cookie named "example_cookie" and
    saves it to the database.

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and sets the cookie.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to set the "example_cookie".

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the cookie has been set.
        """
        response = HttpResponse("Cookie Set")
        cookie = Cookie(
            name="example_cookie",
            value="example_value",
            domain=request.get_host(),
            path="/",
            expires=None,
            secure=False,
            httponly=True
        )
        cookie.save()
        response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            domain=cookie.domain,
            path=cookie.path,
            expires=cookie.expires,
            secure=cookie.secure,
            httponly=cookie.httponly
        )
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "set_cookie_view",
    "SetCookieView",
]
