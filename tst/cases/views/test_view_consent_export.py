# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.views.view_consent_export module.
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
from django.utils import timezone

from swing.cookie.models import CookieConsentModel, LogItem

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestConsentExportViewAuthenticated:
    """GET requests for an authenticated user."""

    def test_returns_expected_payload_schema(self, client, analytics_group):
        """Payload matches the real CookieConsentModel schema (no made-up fields)."""
        user = get_user_model().objects.create_user(
            username="alice", password="pw"
        )
        CookieConsentModel.objects.create(
            user=user,
            necessary=True,
            analytics=True,
            marketing=False,
            consent_given=True,
            consent_date=timezone.now(),
            ip_address="127.0.0.1",
        )
        client.force_login(user)

        url = reverse("cookie_consent_export")
        response = client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)

        assert data["user"] == "alice"
        assert len(data["consent_records"]) == 1
        record = data["consent_records"][0]

        # Real schema fields.
        assert set(record.keys()) == {
            "necessary",
            "analytics",
            "marketing",
            "consent_given",
            "consent_date",
            "created",
            "policy_version",
            "ip_address",
        }
        assert record["necessary"] is True
        assert record["analytics"] is True
        assert record["marketing"] is False
        assert record["consent_given"] is True
        assert record["ip_address"] == "127.0.0.1"

        # These made-up fields from the old (buggy) payload must be gone.
        assert "group" not in record
        assert "accepted" not in record

    def test_includes_audit_log_entries(self, client, analytics_group):
        """Audit log entries are included and reference the cookie group varname."""
        user = get_user_model().objects.create_user(
            username="bob", password="pw"
        )
        LogItem.objects.create(
            action="accepted",
            cookiegroup=analytics_group,
            user=user,
            version=analytics_group.get_version(),
        )
        client.force_login(user)

        url = reverse("cookie_consent_export")
        response = client.get(url)

        data = json.loads(response.content)
        assert len(data["audit_log"]) == 1
        entry = data["audit_log"][0]
        assert entry["action"] == "accepted"
        assert entry["cookie_group"] == "analytics"

    def test_only_returns_records_for_the_requesting_user(self, client):
        """A user only sees their own consent records, not another user's."""
        user_a = get_user_model().objects.create_user(username="a", password="pw")
        user_b = get_user_model().objects.create_user(username="b", password="pw")
        CookieConsentModel.objects.create(user=user_a, consent_given=True)
        CookieConsentModel.objects.create(user=user_b, consent_given=True)

        client.force_login(user_b)
        url = reverse("cookie_consent_export")
        response = client.get(url)

        data = json.loads(response.content)
        assert len(data["consent_records"]) == 1


class TestConsentExportViewAnonymous:
    """GET requests for anonymous visitors, keyed by session."""

    def test_anonymous_without_session_returns_empty_records(self, client):
        """No session key yet -> no consent records, no error."""
        url = reverse("cookie_consent_export")
        response = client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["user"] is None
        assert data["consent_records"] == []
        assert data["audit_log"] == []

    def test_anonymous_with_session_returns_matching_records(self, client):
        """A consent record tied to the current session is returned."""
        session = client.session
        session.save()
        session_key = session.session_key

        CookieConsentModel.objects.create(
            session_key=session_key,
            consent_given=True,
            necessary=True,
        )

        url = reverse("cookie_consent_export")
        response = client.get(url)

        data = json.loads(response.content)
        assert data["session_key"] == session_key
        assert len(data["consent_records"]) == 1
