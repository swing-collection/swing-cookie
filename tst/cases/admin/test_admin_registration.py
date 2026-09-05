# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.admin registration and configuration sanity.

These are basic "does the admin actually work" checks: models are
registered, and Django's admin system checks (E033/E035/E108/E116/E127/
E202, etc.) pass for every registered ModelAdmin. This catches field-name
typos (e.g. referencing a non-existent ``group`` attribute instead of the
real ``cookiegroup`` field) that would otherwise only surface at runtime
when an admin page is rendered.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from swing.cookie.admin import (
    CookieAdmin,
    CookieConsentAdmin,
    CookieGroupAdmin,
    CookiePolicyAdmin,
    LogItemAdmin,
)
from swing.cookie.models import (
    Cookie,
    CookieConsentModel,
    CookieGroup,
    CookiePolicyModel,
    LogItem,
)

pytestmark = pytest.mark.django_db


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True, scope="module")
def _register_admin():
    """Import the module that actually calls admin.site.register(...).

    swing.cookie.admin (the package __init__) only re-exports the
    ModelAdmin classes; the registration calls live in the sibling
    swing.cookie.admin.admin module.
    """
    import swing.cookie.admin.admin  # noqa: F401


# =============================================================================
# Tests
# =============================================================================


class TestAdminRegistration:
    """Models are registered with the default admin site.

    LogItem's registration is conditional on
    ``COOKIE_CONSENT_LOG_ENABLED`` (see swing/cookie/admin/admin.py), and
    the test settings module runs with that flag off, so it is verified
    separately below rather than in this always-on list.
    """

    @pytest.mark.parametrize(
        "model",
        [Cookie, CookieGroup, CookieConsentModel, CookiePolicyModel],
    )
    def test_model_is_registered(self, model):
        assert model in admin.site._registry

    def test_log_item_not_registered_when_logging_disabled(self, settings):
        assert settings.COOKIE_CONSENT_LOG_ENABLED is False
        assert LogItem not in admin.site._registry


class TestAdminSystemChecks:
    """Django's admin system checks must pass for every ModelAdmin.

    Checked against a throwaway AdminSite (with every ModelAdmin
    registered, regardless of the COOKIE_CONSENT_LOG_ENABLED flag) so
    field-name typos are caught even for conditionally-registered admins
    like LogItemAdmin.
    """

    def test_no_admin_check_errors(self):
        site = admin.AdminSite(name="swing_cookie_check")
        site.register(Cookie, CookieAdmin)
        site.register(CookieGroup, CookieGroupAdmin)
        site.register(CookieConsentModel, CookieConsentAdmin)
        site.register(CookiePolicyModel, CookiePolicyAdmin)
        site.register(LogItem, LogItemAdmin)

        errors = site.check(None)
        assert errors == []


class TestCookieAdminChangelist:
    """Smoke-test the Cookie admin changelist actually renders."""

    def test_changelist_renders(self, client, analytics_group):
        Cookie.objects.create(cookiegroup=analytics_group, name="_ga", value="v1")
        admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="pw"
        )
        client.force_login(admin_user)

        response = client.get("/admin/cookie/cookiemodel/")

        assert response.status_code == 200
        assert b"_ga" in response.content


class TestCookieConsentAdminChangelist:
    """Smoke-test the CookieConsent admin changelist renders (regression guard).

    Prior to the field-name fix, list_display/list_filter/readonly_fields
    referenced 'accepted'/'created'/'cookie_group', none of which exist on
    CookieConsentModel, and would raise FieldDoesNotExist when rendering.
    """

    def test_changelist_renders(self, client):
        admin_user = get_user_model().objects.create_superuser(
            username="admin2", email="admin2@example.com", password="pw"
        )
        CookieConsentModel.objects.create(user=admin_user, consent_given=True)
        client.force_login(admin_user)

        response = client.get("/admin/cookie/cookieconsentmodel/")

        assert response.status_code == 200


class TestCookieGroupAdminChangelist:
    """Smoke-test the CookieGroup admin changelist (with its Cookie inline)."""

    def test_changelist_and_change_view_render(self, client, analytics_group):
        admin_user = get_user_model().objects.create_superuser(
            username="admin3", email="admin3@example.com", password="pw"
        )
        client.force_login(admin_user)

        list_response = client.get("/admin/cookie/cookiegroupmodel/")
        assert list_response.status_code == 200

        change_response = client.get(
            f"/admin/cookie/cookiegroupmodel/{analytics_group.pk}/change/"
        )
        assert change_response.status_code == 200
