# -*- coding: utf-8 -*-

"""
Get Cookie View Function
========================

Retrieves cookie values dynamically based on query parameters.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse

# Import | Local
from ..models import CookieModel


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Get Cookie View Function
    ========================

    Retrieves the value of a cookie dynamically based on query parameters.

    Query Parameters:
    -----------------
    name : str (required)
        The name of the cookie to retrieve.
    source : str (optional, default: "request")
        Where to look for the cookie:
        - "request": Browser cookies in the request
        - "database": Cookie definitions stored in database
        - "both": Check both sources

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    JsonResponse
        JSON response with cookie value and metadata.
    """
    name = request.GET.get("name")
    if not name:
        return JsonResponse(
            {"error": "Cookie name is required", "param": "name"},
            status=400,
        )

    source = request.GET.get("source", "request")

    result: dict[str, Any] = {
        "name": name,
        "found": False,
    }

    # Check browser cookies
    if source in ("request", "both"):
        browser_value = request.COOKIES.get(name)
        if browser_value is not None:
            result["found"] = True
            result["browser_value"] = browser_value

    # Check database
    if source in ("database", "both"):
        try:
            cookie = CookieModel.objects.get(name=name)
            result["found"] = True
            result["database"] = {
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "httponly": cookie.httponly,
                "expires": (
                    cookie.expires.isoformat() if cookie.expires else None
                ),
            }
        except CookieModel.DoesNotExist:
            if source == "database":
                result["database"] = None

    return JsonResponse(result)


__all__: list[str] = ["get_cookie_view"]
