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

# Import | Local Views
from .views import (
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookieStatusView,
    delete_cookie_view,
    get_cookie_view,
    set_cookie_view,
)

# =============================================================================
# URL Patterns
# =============================================================================

cookie_management_patterns = [
    path("set-cookie/", set_cookie_view, name="set_cookie_view"),
    path("get-cookie/", get_cookie_view, name="get_cookie_view"),
    path("delete-cookie/", delete_cookie_view, name="delete_cookie_view"),
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
    path("status/", CookieStatusView.as_view(), name="cookie_consent_status"),
    path(
        route="",
        view=CookieGroupListView.as_view(),
        name="cookie_consent_cookie_group_list",
    ),
]

# Consolidate all URL patterns
urlpatterns = cookie_management_patterns + cookie_consent_patterns
