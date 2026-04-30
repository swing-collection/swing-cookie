# -*- coding: utf-8 -*-

"""
Cookie Group Decline View
=========================

View to decline cookie groups.

"""

# Import | Local
from ..utils.util import decline_cookies
from .view_cookie_group_base import CookieGroupBaseProcessView


class CookieGroupDeclineView(CookieGroupBaseProcessView):
    """
    View to decline CookieGroup.
    """

    def process(self, request, response, varname):
        decline_cookies(request, response, varname)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


__all__: list[str] = ["CookieGroupDeclineView"]
