# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.views.view_cookie_group_list module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookieGroupListViewGet:
    """Tests for GET requests against CookieGroupListView."""

    def test_renders_cookiegroup_list_template(
        self, client, necessary_group, analytics_group
    ):
        """GET renders the cookiegroup_list.html template with a 200 status."""
        url = reverse("cookie_consent_cookie_group_list")
        response = client.get(url)

        assert response.status_code == 200
        assert "swing_cookie/cookiegroup_list.html" in [
            t.name for t in response.templates
        ]

    def test_lists_all_cookie_groups_including_required(
        self, client, necessary_group, analytics_group
    ):
        """Unlike the cache-backed helper, the ListView shows ALL groups."""
        url = reverse("cookie_consent_cookie_group_list")
        response = client.get(url)

        object_list = list(response.context["object_list"])
        names = {g.varname for g in object_list}
        assert names == {"necessary", "analytics"}

    def test_empty_state_message(self, client):
        """An empty queryset renders the 'no cookie groups' message."""
        url = reverse("cookie_consent_cookie_group_list")
        response = client.get(url)

        assert response.status_code == 200
        assert b"No cookie groups configured." in response.content

    def test_required_group_has_no_accept_decline_forms(
        self, client, necessary_group
    ):
        """Required groups don't render accept/decline forms.

        Note: base.html's <style> block always contains the
        `.cookie-consent-accept`/`.cookie-consent-decline` CSS selectors,
        so the assertion must look for the actual `<form class="...">`
        markup rather than the bare class-name substring.
        """
        url = reverse("cookie_consent_cookie_group_list")
        response = client.get(url)

        assert b'<form class="cookie-consent-accept"' not in response.content
        assert b'<form class="cookie-consent-decline"' not in response.content

    def test_optional_group_renders_accept_and_decline_forms(
        self, client, analytics_group
    ):
        """Optional groups render both accept and decline forms."""
        url = reverse("cookie_consent_cookie_group_list")
        response = client.get(url)

        assert b'<form class="cookie-consent-accept"' in response.content
        assert b'<form class="cookie-consent-decline"' in response.content
