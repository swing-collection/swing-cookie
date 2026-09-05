# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Detail View Function
===========================

Retrieves detailed information about a specific cookie.

"""

from django.http import HttpRequest, HttpResponse, JsonResponse

# Import | Local
from ..models.model_cookie import CookieModel


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
                "group": (
                    cookie.cookiegroup.varname if cookie.cookiegroup else None
                ),
            }
        )

    except CookieModel.DoesNotExist:
        return JsonResponse(
            {"error": "Cookie not found", "name": cookie_name},
            status=404,
        )


__all__: list[str] = ["view_cookie_details_view"]
