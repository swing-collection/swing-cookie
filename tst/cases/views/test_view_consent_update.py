# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.views.view_consent_update module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import json

# Import | Libraries
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from swing.cookie.conf import settings as cookie_settings
from swing.cookie.models import CookieConsentModel

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests - Form-encoded (QueryDict) requests
# =============================================================================


class TestConsentUpdateViewFormData:
    """POST with regular form data goes through the QueryDict.dict() path."""

    def test_consent_all_accepts_every_optional_group(
        self, client, analytics_group, marketing_group
    ):
        """`consent=all` accepts every configured optional group."""
        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert set(data["updated"]) == {"analytics", "marketing"}

    def test_individual_preferences_single_values_not_lists(
        self, client, analytics_group, marketing_group
    ):
        """Regression test for the request.POST.dict() fix.

        A naive `dict(request.POST)` would yield list values (e.g.
        ``{"analytics": ["true"]}``), which breaks the
        ``isinstance(accepted, str)`` string-to-bool coercion. Using
        ``request.POST.dict()`` must yield plain scalar values instead.
        """
        url = reverse("cookie_consent_update")
        response = client.post(
            url,
            data={"analytics": "true", "marketing": "false"},
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert set(data["updated"]) == {"analytics", "marketing"}

    def test_required_group_cannot_be_declined(
        self, client, necessary_group, analytics_group
    ):
        """Required groups can't be toggled through this endpoint at all.

        ``all_cookie_groups()`` (the source of truth for this view) only
        ever returns optional cookie groups, so a required group's varname
        is simply not recognized here regardless of what value is posted.
        """
        url = reverse("cookie_consent_update")
        response = client.post(
            url, data={"necessary": "false", "analytics": "true"}
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "necessary" not in data["updated"]
        assert "analytics" in data["updated"]

    def test_response_sets_consent_cookie(
        self, client, analytics_group
    ):
        """The final JSON response must carry the updated consent cookie.

        `accept_cookies`/`decline_cookies` write the consent cookie onto the
        intermediate response object built inside the view; whatever is
        finally returned to the client must preserve that Set-Cookie header
        so the browser (and subsequent requests, e.g. the banner view) sees
        the recorded choice.
        """
        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 200
        assert cookie_settings.COOKIE_CONSENT_NAME in response.cookies
        cookie_value = response.cookies[cookie_settings.COOKIE_CONSENT_NAME].value
        assert "analytics=" in cookie_value

    def test_essential_only_declines_optional_groups(
        self, client, necessary_group, analytics_group
    ):
        """`consent=essential` declines every optional group.

        Required groups are never candidates for accept/decline here since
        ``all_cookie_groups()`` excludes them entirely - only optional
        groups are ever iterated, so this mode's practical effect is
        "decline everything optional".
        """
        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "essential"})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert cookie_settings.COOKIE_CONSENT_NAME in response.cookies
        cookie_value = response.cookies[cookie_settings.COOKIE_CONSENT_NAME].value
        assert "analytics=declined" in cookie_value

    def test_unknown_varname_is_ignored(self, client, analytics_group):
        """Preferences for a varname with no matching cookie group are ignored."""
        url = reverse("cookie_consent_update")
        response = client.post(url, data={"does_not_exist": "true"})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["updated"] == []


# =============================================================================
# Tests - JSON requests
# =============================================================================


class TestConsentUpdateViewJson:
    """POST with an application/json body."""

    def test_json_body_consent_all(self, client, analytics_group):
        """A JSON body is parsed and processed identically to form data."""
        url = reverse("cookie_consent_update")
        response = client.post(
            url,
            data=json.dumps({"consent": "all"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "analytics" in data["updated"]

    def test_json_body_with_real_booleans_not_strings(
        self, client, analytics_group, marketing_group
    ):
        """JSON bodies carry real bool values (not the string 'true'/'false').

        This exercises the branch where `isinstance(accepted, str)` is
        False, so the value is used as-is rather than coerced.
        """
        url = reverse("cookie_consent_update")
        response = client.post(
            url,
            data=json.dumps({"analytics": True, "marketing": False}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert set(data["updated"]) == {"analytics", "marketing"}

    def test_invalid_json_returns_400(self, client):
        """Malformed JSON returns a 400 with an error payload."""
        url = reverse("cookie_consent_update")
        response = client.post(
            url,
            data="{not valid json",
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.content)
        assert "error" in data


# =============================================================================
# Tests - No cookie groups configured
# =============================================================================


class TestConsentUpdateViewNoGroups:
    """Behavior when no cookie groups exist at all."""

    def test_returns_400_when_no_groups_configured(self, client):
        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 400
        data = json.loads(response.content)
        assert data["error"] == "No cookie groups configured"


# =============================================================================
# Tests - Consent persistence (DB logging)
# =============================================================================


class TestConsentUpdateViewPersistence:
    """Verify consent is persisted to CookieConsentModel for known visitors."""

    def test_authenticated_user_consent_is_persisted(
        self, client, analytics_group, marketing_group, settings
    ):
        """Consent for a logged-in user is written to CookieConsentModel."""
        settings.COOKIE_CONSENT_LOG_ENABLED = True
        user = get_user_model().objects.create_user(
            username="alice", password="pw"
        )
        client.force_login(user)

        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 200

        consent = CookieConsentModel.objects.get(user=user)
        assert consent.necessary is True
        assert consent.analytics is True
        assert consent.marketing is True
        assert consent.consent_given is True
        assert consent.consent_date is not None

    def test_anonymous_session_consent_is_persisted(
        self, client, analytics_group, settings
    ):
        """Consent for an anonymous visitor is keyed by their session."""
        settings.COOKIE_CONSENT_LOG_ENABLED = True

        # Force a session to exist (and its cookie to be sent back) before
        # posting, mirroring how a real browser would already have a
        # session from an earlier page view.
        session = client.session
        session.save()
        session_key = session.session_key

        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 200

        consent = CookieConsentModel.objects.get(session_key=session_key)
        assert consent.analytics is True
        assert consent.consent_given is True

    def test_disabling_log_updates_still_succeeds(
        self, client, analytics_group, settings
    ):
        """When logging is disabled, the endpoint still responds successfully."""
        settings.COOKIE_CONSENT_LOG_ENABLED = False

        url = reverse("cookie_consent_update")
        response = client.post(url, data={"consent": "all"})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
