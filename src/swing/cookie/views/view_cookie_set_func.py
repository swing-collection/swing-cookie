# -*- coding: utf-8 -*-

"""
Set Cookie View Function
========================

Sets a cookie dynamically based on request parameters.

"""

from django.http import HttpRequest, HttpResponse, JsonResponse

from ..models import CookieModel


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Set Cookie View Function
    ========================

    Sets a cookie dynamically based on request parameters.

    Query Parameters (GET) or Form Data (POST):
    -------------------------------------------
    name : str (required)
        The name of the cookie to set.
    value : str (optional, default: "")
        The value to store in the cookie.
    path : str (optional, default: "/")
        The path for which the cookie is valid.
    secure : bool (optional, default: False)
        Whether the cookie should only be sent over HTTPS.
    httponly : bool (optional, default: True)
        Whether the cookie should be inaccessible to JavaScript.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        JSON response with the cookie details or error message.
    """
    # Get parameters from POST or GET
    params = request.POST if request.method == "POST" else request.GET

    name = params.get("name")
    if not name:
        return JsonResponse(
            {"error": "Cookie name is required", "param": "name"},
            status=400,
        )

    value = params.get("value", "")
    path = params.get("path", "/")
    secure = params.get("secure", "").lower() in ("true", "1", "yes")
    httponly = params.get("httponly", "true").lower() not in (
        "false",
        "0",
        "no",
    )
    domain = params.get("domain") or None

    # Check if cookie already exists
    cookie, created = CookieModel.objects.get_or_create(
        name=name,
        domain=domain,
        defaults={
            "value": value,
            "path": path,
            "secure": secure,
            "httponly": httponly,
        },
    )

    if not created:
        # Update existing cookie
        cookie.value = value
        cookie.path = path
        cookie.secure = secure
        cookie.httponly = httponly
        cookie.save()

    response = JsonResponse(
        {
            "success": True,
            "cookie": {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "httponly": cookie.httponly,
            },
            "created": created,
        }
    )

    # Set the actual cookie in the response
    response.set_cookie(
        key=cookie.name,
        value=cookie.value,
        domain=cookie.domain,
        path=cookie.path,
        expires=cookie.expires,
        secure=cookie.secure,
        httponly=cookie.httponly,
    )

    return response


__all__: list[str] = ["set_cookie_view"]
