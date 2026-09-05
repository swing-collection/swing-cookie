# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.views.view_cookie_banner module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest
from django.urls import reverse

from swing.cookie.conf import settings

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookieBannerViewGet:
    """Tests for GET requests against CookieBannerView."""

    def test_renders_banner_template(self, client, analytics_group):
        """GET renders the banner.html template with a 200 status."""
        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert response.status_code == 200
        assert "swing_cookie/banner.html" in [
            t.name for t in response.templates
        ]

    def test_context_contains_cookie_groups(self, client, analytics_group):
        """Context exposes the optional cookie groups."""
        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert "analytics" in response.context["cookie_groups"]
        assert "analytics" in response.context["consent_status"]

    def test_required_group_not_in_optional_groups(
        self, client, necessary_group, analytics_group
    ):
        """Required groups are excluded from the (optional) cookie_groups map."""
        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert "necessary" not in response.context["cookie_groups"]
        assert "analytics" in response.context["cookie_groups"]

    def test_show_banner_true_when_no_consent_cookie(
        self, client, analytics_group
    ):
        """Banner shows when the visitor has made no choice yet."""
        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert response.context["show_banner"] is True
        assert b"cookie-consent-banner" in response.content

    def test_show_banner_false_when_group_accepted(
        self, client, analytics_group
    ):
        """Banner is hidden once the visitor has accepted a group."""
        version = analytics_group.get_version()
        client.cookies[settings.COOKIE_CONSENT_NAME] = f"analytics={version}"

        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert response.context["show_banner"] is False
        assert response.context["consent_status"]["analytics"]["accepted"] is True

    def test_show_banner_false_when_group_declined(
        self, client, analytics_group
    ):
        """Banner is hidden once the visitor has declined a group."""
        client.cookies[settings.COOKIE_CONSENT_NAME] = (
            f"analytics={settings.COOKIE_CONSENT_DECLINE}"
        )

        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert response.context["show_banner"] is False
        assert response.context["consent_status"]["analytics"]["declined"] is True

    def test_no_cookie_groups_configured(self, client):
        """Banner still renders (but stays hidden-by-content) with no groups."""
        url = reverse("cookie_consent_banner")
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["cookie_groups"] in (None, {})
