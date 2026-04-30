# -*- coding: utf-8 -*-

"""
View Cookie Expiry View Function
================================
"""

from django.http import HttpRequest, HttpResponse

# Import | Local
from ..models import CookieModel


def view_cookie_expiry_view(request: HttpRequest) -> HttpResponse:
    """
    Retrieves the expiry date of a specific cookie named "example_cookie".
    """
    cookie_value: str | None = request.COOKIES.get("example_cookie")
    if cookie_value:
        cookie = CookieModel.objects.get(name="example_cookie")
        return HttpResponse(content=f"Cookie Expires On: {cookie.expires}")
    return HttpResponse(content="Cookie not found")


__all__: list[str] = ["view_cookie_expiry_view"]
