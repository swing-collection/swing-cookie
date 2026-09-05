# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Set Views
================

Re-exports from individual modules.

"""

from .view_cookie_set_class import SetCookieView
from .view_cookie_set_func import set_cookie_view

__all__: list[str] = ["set_cookie_view", "SetCookieView"]
