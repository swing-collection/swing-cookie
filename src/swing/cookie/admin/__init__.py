# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Admin
====================

Re-exports all admin classes from individual modules.

"""

from .admin_cookie import CookieAdmin
from .admin_cookie_consent import CookieConsentAdmin
from .admin_cookie_consent_inline import CookieConsentInline
from .admin_cookie_group import CookieGroupAdmin
from .admin_cookie_inline import CookieInline
from .admin_cookie_policy import CookiePolicyAdmin
from .admin_log_item import LogItemAdmin

__all__: list[str] = [
    "CookieAdmin",
    "CookieConsentAdmin",
    "CookieConsentInline",
    "CookieGroupAdmin",
    "CookieInline",
    "CookiePolicyAdmin",
    "LogItemAdmin",
]
