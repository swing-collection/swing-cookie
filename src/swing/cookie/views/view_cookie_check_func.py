# -*- coding: utf-8 -*-

"""
Check Cookie Existence View Function
====================================
"""

from django.http import HttpRequest, HttpResponse


def check_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Checks if a specific cookie named "example_cookie" exists.
    """
    cookie_exists: bool = "example_cookie" in request.COOKIES
    if cookie_exists:
        return HttpResponse(content="Cookie exists")
    else:
        return HttpResponse(content="Cookie does not exist")


__all__: list[str] = ["check_cookie_view"]
