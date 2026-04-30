# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent URL Configuration
================================

This module defines URL patterns for managing cookies, including setting,
getting, and deleting cookies, as well as handling user consent.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Django Libraries
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

# Import | Local
# Import | Local Views
from .views import (
    CookieConsentWithdrawView,
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookieStatusView,
)
from .views.view_cookie_delete import cookie_delete_view
from .views.view_cookie_get import get_cookie_view
from .views.view_cookie_set import set_cookie_view

# =============================================================================
# URL Patterns
# =============================================================================

cookie_management_patterns = [
    path("set-cookie/", set_cookie_view, name="set_cookie_view"),
    path("get-cookie/", get_cookie_view, name="get_cookie_view"),
    path("delete-cookie/", cookie_delete_view, name="cookie_delete_view"),
]

cookie_consent_patterns = [
    path(
        route="accept/",
        view=csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept_all",
    ),
    re_path(
        route=r"^accept/(?P<varname>[\w-]+)/$",
        view=csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept",
    ),
    re_path(
        route=r"^decline/(?P<varname>[\w-]+)/$",
        view=csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline",
    ),
    path(
        route="decline/",
        view=csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline_all",
    ),
    path(
        route="withdraw/",
        view=csrf_exempt(CookieConsentWithdrawView.as_view()),
        name="cookie_consent_withdraw",
    ),
    path("status/", CookieStatusView.as_view(), name="cookie_consent_status"),
    path(
        route="",
        view=CookieGroupListView.as_view(),
        name="cookie_consent_cookie_group_list",
    ),
]

# Consolidate all URL patterns
urlpatterns = cookie_management_patterns + cookie_consent_patterns
