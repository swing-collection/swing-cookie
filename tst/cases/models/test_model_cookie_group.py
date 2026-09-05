# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.models.model_cookie_group module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.cookie.models import Cookie, CookieGroup, CookieGroupModel

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookieGroupModel:
    """Tests for the CookieGroupModel class."""

    def test_str_returns_name(self):
        group = CookieGroup.objects.create(name="analytics", varname="analytics")
        assert str(group) == str(group.name)

    def test_save_title_cases_name(self):
        group = CookieGroup.objects.create(name="analytics", varname="analytics")
        assert group.name == "Analytics"

    def test_save_auto_generates_varname(self):
        group = CookieGroup.objects.create(name="Ad Tracking", varname="")
        assert group.varname == "ad_tracking"

    def test_natural_key(self):
        group = CookieGroup.objects.create(name="analytics", varname="analytics")
        assert group.natural_key() == ("analytics",)

    def test_get_version_falls_back_to_updated_at(self):
        group = CookieGroup.objects.create(name="analytics", varname="analytics")
        assert group.get_version() == group.updated_at.isoformat()

    def test_get_version_uses_latest_cookie(self):
        group = CookieGroup.objects.create(name="analytics", varname="analytics")
        cookie = Cookie.objects.create(
            cookiegroup=group, name="_ga", value="v1"
        )
        assert group.get_version() == cookie.updated_at.isoformat()

    def test_for_json_serializes_group_and_cookies(self):
        group = CookieGroup.objects.create(
            name="analytics",
            varname="analytics",
            description="Analytics cookies.",
            is_required=False,
        )
        Cookie.objects.create(
            cookiegroup=group, name="_ga", domain="example.com", value="v1"
        )

        data = group.for_json()

        assert data["varname"] == "analytics"
        assert data["is_required"] is False
        assert len(data["cookies"]) == 1
        assert data["cookies"][0]["name"] == "_ga"
        assert data["cookies"][0]["domain"] == "example.com"

    def test_alias_matches_model(self):
        assert CookieGroup is CookieGroupModel
