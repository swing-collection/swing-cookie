# -*- coding: utf-8 -*-

"""
Cookie Group Accept View
========================

View to accept cookie groups.

"""

# Import | Local
from ..utils.util import accept_cookies
from .view_cookie_group_base import CookieGroupBaseProcessView


class CookieGroupAcceptView(CookieGroupBaseProcessView):
    """
    View to accept CookieGroup.
    """

    def process(self, request, response, varname):
        accept_cookies(request, response, varname)


__all__: list[str] = ["CookieGroupAcceptView"]
