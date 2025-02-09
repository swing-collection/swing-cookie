# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Banner Views Module
==========================


This module provides views for handling the dismissal of the cookie consent
banner.

It includes:
------------
- `dismiss_cookie_banner_view`: Function-based view to set a cookie when the
    user dismisses the banner.
- `DismissCookieBannerView`: Class-based view to handle cookie banner
    dismissal.


"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

# Import | Local Modules
from ..models.model_cookie import CookieModel

# =============================================================================
# Function
# =============================================================================


def dismiss_cookie_banner_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Dismiss Cookie Banner Function
    ==============================

    Sets a cookie to indicate that the user has dismissed the cookie consent banner.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        A response indicating that the banner has been dismissed.
    """
    response = HttpResponse(content=_(message="Banner Dismissed"))
    response.set_cookie(
        key="cookie_banner_dismissed",
        value="true",
        max_age=31536000,  # 1 year
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    return response


# =============================================================================
# Class
# =============================================================================


class DismissCookieBannerView(View):
    """
    Dismiss Cookie Banner Class
    ===========================

    A class-based view that sets a cookie when the user dismisses the cookie consent banner.

    Methods:
    --------
    get(request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        Handles GET requests and sets a cookie indicating the banner has been dismissed.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to set a cookie indicating the banner has been dismissed.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            A response indicating that the banner has been dismissed.
        """
        response = HttpResponse(content=_(message="Banner Dismissed"))
        response.set_cookie(
            key="cookie_banner_dismissed",
            value="true",
            max_age=31536000,  # 1 year
            secure=True,
            httponly=True,
            samesite="Lax",
        )
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "dismiss_cookie_banner_view",
    "DismissCookieBannerView",
]
