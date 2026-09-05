# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.models.model_cookie module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.cookie.models import Cookie, CookieModel

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookieModel:
    """Tests for the CookieModel class."""

    def test_str_includes_name_and_domain(self, analytics_group):
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            domain="example.com",
            value="v1",
        )
        assert str(cookie) == "_ga (example.com)"

    def test_str_with_no_domain(self, analytics_group):
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            value="v1",
        )
        assert str(cookie) == "_ga (No Domain)"

    def test_varname_property(self, analytics_group):
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            domain="example.com",
            value="v1",
        )
        assert cookie.varname == "analytics=_ga:example.com"

    def test_natural_key_includes_group_natural_key(self, analytics_group):
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            domain="example.com",
            value="v1",
        )
        assert cookie.natural_key() == ("_ga", "example.com", "analytics")

    def test_get_version_returns_created_at_isoformat(self, analytics_group):
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            value="v1",
        )
        assert cookie.get_version() == cookie.created_at.isoformat()

    def test_cookiegroup_field_relates_to_group(self, analytics_group):
        """Regression guard for the cookie.group -> cookiegroup field-name fix."""
        cookie = Cookie.objects.create(
            cookiegroup=analytics_group,
            name="_ga",
            value="v1",
        )
        assert cookie.cookiegroup_id == analytics_group.pk
        assert cookie in analytics_group.cookie_set.all()

    def test_alias_matches_model(self):
        assert Cookie is CookieModel
