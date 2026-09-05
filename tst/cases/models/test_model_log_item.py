# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.models.model_log_item module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from swing.cookie.models import ACTION_ACCEPTED, LogItem

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestLogItemModel:
    """Tests for the LogItem model."""

    def test_str_includes_user_action_and_group(self, analytics_group):
        user = get_user_model().objects.create_user(username="alice", password="pw")
        log = LogItem.objects.create(
            action=ACTION_ACCEPTED,
            cookiegroup=analytics_group,
            user=user,
        )
        assert "alice" in str(log)
        assert "accepted" in str(log)
        assert analytics_group.name in str(log)

    def test_str_for_anonymous_session(self, analytics_group):
        log = LogItem.objects.create(
            action=ACTION_ACCEPTED,
            cookiegroup=analytics_group,
            session_key="sess123",
        )
        assert "Anonymous" in str(log)
        assert "sess123" in str(log)


class TestLogConsentClassmethod:
    """Tests for LogItem.log_consent()."""

    def test_records_ip_user_agent_and_version(self, analytics_group):
        user = get_user_model().objects.create_user(username="bob", password="pw")
        request = RequestFactory().get(
            "/",
            REMOTE_ADDR="198.51.100.7",
            HTTP_USER_AGENT="pytest-agent",
        )
        request.user = user

        log = LogItem.log_consent(
            action=ACTION_ACCEPTED,
            cookiegroup=analytics_group,
            request=request,
        )

        assert log.ip_address == "198.51.100.7"
        assert log.user_agent == "pytest-agent"
        assert log.user == user
        assert log.version == analytics_group.get_version()

    def test_explicit_user_overrides_request_user(self, analytics_group):
        request_user = get_user_model().objects.create_user(
            username="req_user", password="pw"
        )
        explicit_user = get_user_model().objects.create_user(
            username="explicit_user", password="pw"
        )
        request = RequestFactory().get("/")
        request.user = request_user

        log = LogItem.log_consent(
            action=ACTION_ACCEPTED,
            cookiegroup=analytics_group,
            request=request,
            user=explicit_user,
        )

        assert log.user == explicit_user

    def test_works_without_request(self, analytics_group):
        log = LogItem.log_consent(
            action=ACTION_ACCEPTED,
            cookiegroup=analytics_group,
            session_key="sess456",
        )
        assert log.session_key == "sess456"
        assert log.ip_address is None
