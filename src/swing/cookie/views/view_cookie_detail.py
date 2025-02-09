# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Detail Views Module
==========================

This module provides views to retrieve detailed information about cookies
stored in the database.

It includes:
------------
- `view_cookie_details_view`: Function-based view to get cookie details.
- `ViewCookieDetailsView`: Class-based view to get cookie details.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict, List

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

# Import | Local Modules
from ..models.model_cookie import CookieModel

# =============================================================================
# Function
# =============================================================================


def view_cookie_details_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    View Cookie Details Function
    ============================

    Retrieves detailed information about a specific cookie.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        A response containing detailed information about the cookie
        or an error message if not found.
    """

    # Allow dynamic retrieval
    cookie_name: str = request.GET.get(
        "name",
        default="example_cookie",
    )

    try:
        cookie: CookieModel = CookieModel.objects.get(name=cookie_name)
        details: str = (
            f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain or 'N/A'}, "
            f"Path: {cookie.path}, Expires: {cookie.expires or 'Session'}, Secure: {cookie.secure}, "
            f"HTTPOnly: {cookie.httponly}"
        )
        return HttpResponse(content=details)

    except CookieModel.DoesNotExist:
        return HttpResponse(
            content=_(message="Cookie not found"),
            status=404,
        )


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

        # Allow dynamic retrieval
        cookie_name: str = request.GET.get(
            "name",
            default="example_cookie",
        )

        try:
            cookie: CookieModel = CookieModel.objects.get(name=cookie_name)
            details: str = (
                f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain or 'N/A'}, "
                f"Path: {cookie.path}, Expires: {cookie.expires or 'Session'}, Secure: {cookie.secure}, "
                f"HTTPOnly: {cookie.httponly}"
            )
            return HttpResponse(content=details)

        except CookieModel.DoesNotExist:
            return HttpResponse(
                content=_(message="Cookie not found"),
                status=404,
            )


# =============================================================================
# Module Exports
# =============================================================================

__all__: List[str] = [
    "view_cookie_details_view",
    "ViewCookieDetailsView",
]
