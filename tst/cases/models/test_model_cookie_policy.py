# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for swing.cookie.models.model_cookie_policy module.
"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Libraries
import pytest

from swing.cookie.models import CookiePolicyModel

pytestmark = pytest.mark.django_db


# =============================================================================
# Tests
# =============================================================================


class TestCookiePolicyModel:
    """Tests for the CookiePolicyModel class."""

    def test_str_includes_version(self):
        policy = CookiePolicyModel.objects.create(version="v1", content="...")
        assert str(policy) == "Cookie Policy vV1"

    def test_save_normalizes_version(self):
        policy = CookiePolicyModel.objects.create(version="  v1  ", content="...")
        assert policy.version == "V1"

    def test_default_is_active_true(self):
        policy = CookiePolicyModel.objects.create(version="v1", content="...")
        assert policy.is_active is True
