# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Shared fixtures for swing.cookie tests.

Provides cookie group / cookie fixtures used across the view, model, and
admin test modules, plus cache hygiene so the `all_cookie_groups()` cache
(keyed globally, not per-test) never leaks stale data between tests.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.cookie.models import Cookie, CookieGroup
from swing.cookie.utils.cache import delete_cache


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def _clear_cookie_group_cache():
    """Clear the cookie-group cache before and after every test.

    ``all_cookie_groups()`` caches its result under a fixed cache key, so
    without this the cache would leak cookie groups created by one test
    into the next.
    """
    delete_cache()
    yield
    delete_cache()


@pytest.fixture
def necessary_group(db):
    """A required (non-optional) cookie group."""
    return CookieGroup.objects.create(
        name="necessary",
        varname="necessary",
        description="Required cookies.",
        is_required=True,
    )


@pytest.fixture
def analytics_group(db):
    """An optional cookie group used for analytics cookies."""
    return CookieGroup.objects.create(
        name="analytics",
        varname="analytics",
        description="Analytics cookies.",
        is_required=False,
    )


@pytest.fixture
def marketing_group(db):
    """An optional cookie group used for marketing cookies."""
    return CookieGroup.objects.create(
        name="marketing",
        varname="marketing",
        description="Marketing cookies.",
        is_required=False,
    )


@pytest.fixture
def analytics_cookie(analytics_group):
    """A single cookie belonging to the analytics group."""
    return Cookie.objects.create(
        cookiegroup=analytics_group,
        name="_ga",
        description="Google Analytics tracking cookie.",
        domain="example.com",
        value="dummy-value",
    )
