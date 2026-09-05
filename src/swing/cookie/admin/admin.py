# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Admin Configuration
==================================

Registers all admin classes with Django admin site.

"""

from django.contrib import admin

from ..conf import settings
from ..models import (
    Cookie,
    CookieConsentModel,
    CookieGroup,
    CookiePolicyModel,
    LogItem,
)
from .admin_cookie import CookieAdmin
from .admin_cookie_consent import CookieConsentAdmin
from .admin_cookie_group import CookieGroupAdmin
from .admin_cookie_policy import CookiePolicyAdmin
from .admin_log_item import LogItemAdmin

# Register models with admin site
admin.site.register(Cookie, CookieAdmin)
admin.site.register(CookieGroup, CookieGroupAdmin)
admin.site.register(CookieConsentModel, CookieConsentAdmin)
admin.site.register(CookiePolicyModel, CookiePolicyAdmin)

if settings.COOKIE_CONSENT_LOG_ENABLED:
    admin.site.register(LogItem, LogItemAdmin)
