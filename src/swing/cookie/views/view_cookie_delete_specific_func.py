# -*- coding: utf-8 -*-

"""
Clear Specific Cookies View Function
====================================
"""

from django.http import HttpRequest, HttpResponse


def clear_specific_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    Clears all cookies that start with a specific prefix (e.g., "example_").
    """
    response = HttpResponse(content="Specific Cookies Cleared")
    prefix = "example_"
    cookies_to_clear: list[str] = [
        cookie for cookie in request.COOKIES if cookie.startswith(prefix)
    ]

    for cookie in cookies_to_clear:
        response.delete_cookie(cookie)

    return response


__all__: list[str] = ["clear_specific_cookies_view"]
