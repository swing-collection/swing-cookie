# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.views.view_cookie_policy module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from types import SimpleNamespace

# Import | Libraries
import pytest
from django.urls import reverse

from swing.cookie.views.view_cookie_policy import CookiePolicyView

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookiePolicyViewGet:
    """Tests for GET requests against CookiePolicyView."""

    def test_renders_policy_template(self, client, analytics_group):
        """GET renders the policy.html template with a 200 status."""
        url = reverse("cookie_consent_policy")
        response = client.get(url)

        assert response.status_code == 200
        assert "swing_cookie/policy.html" in [
            t.name for t in response.templates
        ]

    def test_context_lists_groups_and_their_cookies(
        self, client, analytics_group, analytics_cookie
    ):
        """Context includes each group along with its nested cookies."""
        url = reverse("cookie_consent_policy")
        response = client.get(url)

        groups = response.context["cookie_groups"]
        varnames = [g["varname"] for g in groups]
        assert "analytics" in varnames

        analytics_data = next(g for g in groups if g["varname"] == "analytics")
        assert analytics_data["is_required"] is False
        cookie_names = [c["name"] for c in analytics_data["cookies"]]
        assert "_ga" in cookie_names

    def test_content_includes_cookie_name(
        self, client, analytics_group, analytics_cookie
    ):
        """Rendered HTML includes the individual cookie's name."""
        url = reverse("cookie_consent_policy")
        response = client.get(url)

        assert b"_ga" in response.content

    def test_no_cookie_groups_configured(self, client):
        """Policy page still renders when no cookie groups exist."""
        url = reverse("cookie_consent_policy")
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["cookie_groups"] == []
        assert b"No cookie categories have been configured." in response.content

    def test_real_cookie_has_no_max_age_and_shows_session(
        self, client, analytics_group, analytics_cookie
    ):
        """CookieModel has no `max_age` field, so duration always renders 'Session'."""
        url = reverse("cookie_consent_policy")
        response = client.get(url)

        analytics_data = next(
            g
            for g in response.context["cookie_groups"]
            if g["varname"] == "analytics"
        )
        assert analytics_data["cookies"][0]["duration"] == "Session"


class TestFormatDuration:
    """Unit tests for CookiePolicyView._format_duration().

    Exercised directly with a duck-typed object (rather than a real
    CookieModel instance, which has no ``max_age`` field) so the
    formatting logic itself is verified even though it's currently
    unreachable via the ORM.
    """

    def test_no_max_age_attribute_returns_session(self):
        view = CookiePolicyView()
        assert view._format_duration(SimpleNamespace()) == "Session"

    def test_zero_max_age_returns_session(self):
        view = CookiePolicyView()
        assert view._format_duration(SimpleNamespace(max_age=0)) == "Session"

    def test_seconds_only_returns_hours(self):
        view = CookiePolicyView()
        assert view._format_duration(SimpleNamespace(max_age=3600)) == "1 hour"
        assert view._format_duration(SimpleNamespace(max_age=7200)) == "2 hours"

    def test_days(self):
        view = CookiePolicyView()
        assert view._format_duration(SimpleNamespace(max_age=86400)) == "1 day"
        assert view._format_duration(SimpleNamespace(max_age=86400 * 5)) == "5 days"

    def test_months(self):
        view = CookiePolicyView()
        assert (
            view._format_duration(SimpleNamespace(max_age=86400 * 60)) == "2 months"
        )

    def test_years(self):
        view = CookiePolicyView()
        assert (
            view._format_duration(SimpleNamespace(max_age=86400 * 365)) == "1 year"
        )
        assert (
            view._format_duration(SimpleNamespace(max_age=86400 * 365 * 2))
            == "2 years"
        )
