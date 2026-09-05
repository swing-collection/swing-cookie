# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Copy Cookie View Function
=========================
"""

from django.http import HttpRequest, HttpResponse


def copy_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Copies the value of "example_cookie" to a new cookie named "copied_cookie".
    """
    original_cookie_value: str | None = request.COOKIES.get("example_cookie")
    if original_cookie_value:
        response = HttpResponse(content="Cookie Copied")
        response.set_cookie(key="copied_cookie", value=original_cookie_value)
        return response
    return HttpResponse(content="Original cookie not found")


__all__: list[str] = ["copy_cookie_view"]
