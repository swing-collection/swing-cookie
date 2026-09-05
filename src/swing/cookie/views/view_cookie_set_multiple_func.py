# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Set Multiple Cookies View Function
==================================
"""

from django.http import HttpRequest, HttpResponse


def set_multiple_cookies_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Sets multiple cookies in a single response.
    """
    response = HttpResponse(content="Multiple Cookies Set")
    cookies_to_set: dict[str, str] = {
        "cookie_one": "value_one",
        "cookie_two": "value_two",
        "cookie_three": "value_three",
    }

    for name, value in cookies_to_set.items():
        response.set_cookie(key=name, value=value)

    return response


__all__: list[str] = ["set_multiple_cookies_view"]
