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

def dismiss_cookie_banner_view(request: HttpRequest) -> HttpResponse:
    """
    Dismiss Cookie Banner View Function
    ===================================

    Sets a cookie to indicate that the user has dismissed the cookie consent 
    banner.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the banner has been dismissed.
    """
    response = HttpResponse("Banner Dismissed")
    response.set_cookie("cookie_banner_dismissed", "true")
    return response


# =============================================================================
# Class
# =============================================================================

class DismissCookieBannerView(View):
    """
    Dismiss Cookie Banner View Class
    ================================

    A class-based view that sets a cookie to indicate that the user has 
    dismissed the cookie consent banner.

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and sets the cookie.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        """
        Handles GET requests to set a cookie indicating the banner has been 
        dismissed.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
            HttpResponse
        The response object indicating that the banner has been dismissed.
    """
    response = HttpResponse("Banner Dismissed")
    response.set_cookie("cookie_banner_dismissed", "true")
    return response

# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "cookie_delete_view",
    "CookieDeleteView",
]
