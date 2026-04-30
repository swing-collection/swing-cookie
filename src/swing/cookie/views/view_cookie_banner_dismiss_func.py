# -*- coding: utf-8 -*-

"""
Dismiss Cookie Banner View Function
====================================
"""

from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _


def dismiss_cookie_banner_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Sets a cookie to indicate that the user has dismissed the cookie consent banner.
    """
    response = HttpResponse(content=_("Banner Dismissed"))
    response.set_cookie(
        key="cookie_banner_dismissed",
        value="true",
        max_age=31536000,  # 1 year
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    return response


__all__: list[str] = ["dismiss_cookie_banner_view"]
