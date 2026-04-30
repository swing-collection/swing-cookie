# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Demo URL Patterns
==========================

Defines URL patterns for the demo project. This includes:

- Admin panel routes for managing the application.
- Routes for the `swing_hello` app, including a default route.

"""

# =============================================================================
# Imports
# =============================================================================

from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLResolver

# Import | Local
# Import | Local Modules
from . import views

# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns: list[URLResolver] = [
    # Admin
    path(
        route="admin/",
        view=admin.site.urls,
    ),
    # Demo pages
    path(
        route="",
        view=views.home_view,
        name="demo_home",
    ),
    path(
        route="analytics/",
        view=views.analytics_page,
        name="demo_analytics",
    ),
    path(
        route="preferences/",
        view=views.preferences_page,
        name="demo_preferences",
    ),
    # Cookie consent URLs
    path(
        route="cookie-consent/",
        view=include(arg="swing.cookie.urls"),
    ),
]
