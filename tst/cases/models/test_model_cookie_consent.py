# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.models.model_cookie_consent module.
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

from swing.cookie.models import CookieConsentModel, CookiePolicyModel

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookieConsentModelBasics:
    """Basic field / __str__ behavior."""

    def test_str_for_authenticated_user(self):
        user = get_user_model().objects.create_user(username="alice", password="pw")
        consent = CookieConsentModel.objects.create(user=user, consent_given=True)
        assert "alice" in str(consent)
        assert "True" in str(consent)

    def test_str_for_anonymous_session(self):
        consent = CookieConsentModel.objects.create(
            session_key="abc123", consent_given=False
        )
        assert "Anonymous" in str(consent)
        assert "abc123" in str(consent)

    def test_requires_user_or_session_constraint(self):
        """CheckConstraint requires either a user or a session_key."""
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                CookieConsentModel.objects.create()


class TestUpdateConsent:
    """Tests for CookieConsentModel.update_consent()."""

    def test_update_consent_sets_fields(self):
        user = get_user_model().objects.create_user(username="bob", password="pw")
        consent = CookieConsentModel.objects.create(user=user)

        consent.update_consent(necessary=True, analytics=True, marketing=False)

        consent.refresh_from_db()
        assert consent.necessary is True
        assert consent.analytics is True
        assert consent.marketing is False
        assert consent.consent_given is True

    def test_update_consent_all_false_means_consent_not_given(self):
        user = get_user_model().objects.create_user(username="carl", password="pw")
        consent = CookieConsentModel.objects.create(user=user)

        consent.update_consent(necessary=False, analytics=False, marketing=False)

        assert consent.consent_given is False


class TestHasGivenFullConsent:
    """Tests for CookieConsentModel.has_given_full_consent()."""

    def test_true_when_all_categories_accepted(self):
        user = get_user_model().objects.create_user(username="dan", password="pw")
        consent = CookieConsentModel.objects.create(
            user=user, necessary=True, analytics=True, marketing=True
        )
        assert consent.has_given_full_consent() is True

    def test_false_when_any_category_declined(self):
        user = get_user_model().objects.create_user(username="eve", password="pw")
        consent = CookieConsentModel.objects.create(
            user=user, necessary=True, analytics=False, marketing=True
        )
        assert consent.has_given_full_consent() is False


class TestNeedsReconsent:
    """Tests for CookieConsentModel.needs_reconsent()."""

    def test_true_when_no_policy_version_set(self):
        user = get_user_model().objects.create_user(username="fay", password="pw")
        consent = CookieConsentModel.objects.create(user=user)
        assert consent.needs_reconsent() is True

    def test_false_when_policy_version_matches_latest_active(self):
        user = get_user_model().objects.create_user(username="gus", password="pw")
        policy = CookiePolicyModel.objects.create(
            version="v1", content="...", is_active=True
        )
        consent = CookieConsentModel.objects.create(
            user=user, policy_version=policy
        )
        assert consent.needs_reconsent() is False

    def test_true_when_newer_policy_published(self):
        user = get_user_model().objects.create_user(username="hank", password="pw")
        old_policy = CookiePolicyModel.objects.create(
            version="v1", content="...", is_active=True
        )
        consent = CookieConsentModel.objects.create(
            user=user, policy_version=old_policy
        )
        CookiePolicyModel.objects.create(version="v2", content="...", is_active=True)

        assert consent.needs_reconsent() is True

    def test_false_when_no_active_policy_exists_at_all(self):
        """If a policy_version is set but nothing is active anymore, don't
        force reconsent (there's nothing newer to reconsent to)."""
        user = get_user_model().objects.create_user(username="hazel", password="pw")
        policy = CookiePolicyModel.objects.create(
            version="v1", content="...", is_active=False
        )
        consent = CookieConsentModel.objects.create(
            user=user, policy_version=policy
        )
        assert consent.needs_reconsent() is False


class TestGetOrCreateForRequest:
    """Tests for CookieConsentModel.get_or_create_for_request()."""

    def test_creates_record_for_authenticated_user(self):
        user = get_user_model().objects.create_user(username="ivy", password="pw")
        request = RequestFactory().get("/")
        request.user = user

        consent, created = CookieConsentModel.get_or_create_for_request(request)

        assert created is True
        assert consent.user == user

    def test_reuses_record_for_same_authenticated_user(self):
        user = get_user_model().objects.create_user(username="jan", password="pw")
        request = RequestFactory().get("/")
        request.user = user

        first, _ = CookieConsentModel.get_or_create_for_request(request)
        second, created = CookieConsentModel.get_or_create_for_request(request)

        assert created is False
        assert first.pk == second.pk

    def test_records_ip_from_x_forwarded_for(self):
        user = get_user_model().objects.create_user(username="kim", password="pw")
        request = RequestFactory().get(
            "/", HTTP_X_FORWARDED_FOR="203.0.113.5, 10.0.0.1"
        )
        request.user = user

        consent, _ = CookieConsentModel.get_or_create_for_request(request)

        assert consent.ip_address == "203.0.113.5"

    def test_updates_ip_when_it_changes(self):
        user = get_user_model().objects.create_user(username="liam", password="pw")
        request = RequestFactory().get("/", REMOTE_ADDR="10.0.0.1")
        request.user = user
        CookieConsentModel.get_or_create_for_request(request)

        request2 = RequestFactory().get("/", REMOTE_ADDR="10.0.0.2")
        request2.user = user
        consent, created = CookieConsentModel.get_or_create_for_request(request2)

        assert created is False
        assert consent.ip_address == "10.0.0.2"

    def test_creates_record_for_anonymous_session(self):
        """Anonymous visitors get a session-keyed consent record."""
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.backends.db import SessionStore

        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.session = SessionStore()

        consent, created = CookieConsentModel.get_or_create_for_request(request)

        assert created is True
        assert consent.user is None
        assert consent.session_key == request.session.session_key

    def test_reuses_record_for_same_anonymous_session(self):
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.backends.db import SessionStore

        session = SessionStore()
        session.create()

        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.session = session

        first, _ = CookieConsentModel.get_or_create_for_request(request)

        request2 = RequestFactory().get("/")
        request2.user = AnonymousUser()
        request2.session = session
        second, created = CookieConsentModel.get_or_create_for_request(request2)

        assert created is False
        assert first.pk == second.pk
