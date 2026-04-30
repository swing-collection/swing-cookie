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
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

# Import | Local
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

    Query Parameters:
    -----------------
    name : str (required)
        The name of the cookie to retrieve details for.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    JsonResponse
        JSON response containing detailed information about the cookie
        or an error message if not found.
    """
    cookie_name = request.GET.get("name")

    if not cookie_name:
        return JsonResponse(
            {"error": "Cookie name is required", "param": "name"},
            status=400,
        )

    try:
        cookie: CookieModel = CookieModel.objects.get(name=cookie_name)
        return JsonResponse(
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "expires": (
                    cookie.expires.isoformat() if cookie.expires else None
                ),
                "secure": cookie.secure,
                "httponly": cookie.httponly,
                "group": cookie.group.varname if cookie.group else None,
            }
        )

    except CookieModel.DoesNotExist:
        return JsonResponse(
            {"error": "Cookie not found", "name": cookie_name},
            status=404,
        )


# =============================================================================
# Class
# =============================================================================


class ViewCookieDetailsView(View):
    """
    View Cookie Details View Class
    ==============================

    A class-based view that retrieves detailed information about cookies
    dynamically based on request parameters.

    Methods:
    --------
    get : Handle GET requests to retrieve cookie details.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to retrieve cookie details.
        """
        return view_cookie_details_view(request)


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "view_cookie_details_view",
    "ViewCookieDetailsView",
]
