# -*- coding: utf-8 -*-

"""
List Cookies View Function
==========================

Lists all cookies present in the request.

"""

from django.http import HttpRequest, HttpResponse


def list_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    List Cookies View Function
    ==========================

    Lists all cookies present in the request.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object containing a list of all cookies and their values.
    """
    cookies: dict[str, str] = request.COOKIES
    cookies_list: str = ", ".join(
        [f"{key}: {value}" for key, value in cookies.items()]
    )
    return HttpResponse(f"Cookies: {cookies_list}")


__all__: list[str] = ["list_cookies_view"]
