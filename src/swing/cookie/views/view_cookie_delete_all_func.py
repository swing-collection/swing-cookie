# -*- coding: utf-8 -*-

"""
Delete All Cookies View Function
================================
"""

from django.http import HttpRequest, HttpResponse


def delete_all_cookies_view(request: HttpRequest) -> HttpResponse:
    """
    Deletes all cookies present in the request.
    """
    response = HttpResponse(content="All Cookies Deleted")
    for cookie in request.COOKIES:
        response.delete_cookie(key=cookie)
    return response


__all__: list[str] = ["delete_all_cookies_view"]
