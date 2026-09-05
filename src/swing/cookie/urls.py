# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent URL Configuration
================================

This module defines URL patterns for managing cookies, including setting,
getting, and deleting cookies, as well as handling user consent.

All views are class-based following Django best practices.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Django Libraries
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

# Import | Local Views
from .views import (
    ConsentExportView,
    ConsentUpdateView,
    CookieBannerView,
    CookieConsentWithdrawView,
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookiePolicyView,
    CookiePreferencesView,
    CookieStatusView,
)

# =============================================================================
# URL Patterns
# =============================================================================

# Cookie consent management patterns
cookie_consent_patterns = [
    # Banner view - renders the cookie banner
    path(
        route="banner/",
        view=CookieBannerView.as_view(),
        name="cookie_consent_banner",
    ),
    # Policy page - detailed cookie information
    path(
        route="policy/",
        view=CookiePolicyView.as_view(),
        name="cookie_consent_policy",
    ),
    # Update consent (AJAX endpoint)
    path(
        route="update/",
        view=csrf_exempt(ConsentUpdateView.as_view()),
        name="cookie_consent_update",
    ),
    # Accept all cookies
    path(
        route="accept/",
        view=csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept_all",
    ),
    # Accept specific cookie group
    re_path(
        route=r"^accept/(?P<varname>[\w-]+)/$",
        view=csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept",
    ),
    # Decline specific cookie group
    re_path(
        route=r"^decline/(?P<varname>[\w-]+)/$",
        view=csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline",
    ),
    # Decline all optional cookies
    path(
        route="decline/",
        view=csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline_all",
    ),
    # Withdraw all consent
    path(
        route="withdraw/",
        view=csrf_exempt(CookieConsentWithdrawView.as_view()),
        name="cookie_consent_withdraw",
    ),
    # Get current consent status
    path(
        route="status/",
        view=CookieStatusView.as_view(),
        name="cookie_consent_status",
    ),
    # Manage granular preferences
    path(
        route="preferences/",
        view=csrf_exempt(CookiePreferencesView.as_view()),
        name="cookie_consent_preferences",
    ),
    # Export consent data (GDPR)
    path(
        route="export/",
        view=ConsentExportView.as_view(),
        name="cookie_consent_export",
    ),
    # List all cookie groups (management page)
    path(
        route="",
        view=CookieGroupListView.as_view(),
        name="cookie_consent_cookie_group_list",
    ),
]

# Consolidate all URL patterns
urlpatterns = cookie_consent_patterns
