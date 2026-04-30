# -*- coding: utf-8 -*-

"""
Cookie Get Views
================

Re-exports from individual modules.

"""

from .view_cookie_get_class import GetCookieView
from .view_cookie_get_func import get_cookie_view

__all__: list[str] = ["get_cookie_view", "GetCookieView"]
