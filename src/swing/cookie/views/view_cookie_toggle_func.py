# -*- coding: utf-8 -*-

"""
Toggle Cookie Value View Function
=================================
"""

from django.http import HttpRequest, HttpResponse


def toggle_cookie_value_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Toggles the value of "toggle_cookie" between "on" and "off".
    """
    current_value: str = request.COOKIES.get("toggle_cookie", "off")
    new_value = "on" if current_value == "off" else "off"
    response = HttpResponse(content=f"Cookie toggled to {new_value}")
    response.set_cookie(key="toggle_cookie", value=new_value)
    return response


__all__: list[str] = ["toggle_cookie_value_view"]
