# -*- coding: utf-8 -*-

"""
Cookie Consent App Configuration
=================================

This module contains the configuration settings for the Cookie Consent Django app.
"""

# =============================================================================
# Imports
# =============================================================================

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# =============================================================================
# App Configuration
# =============================================================================

class CookieConfig(AppConfig):
    """
    Cookie Consent App Configuration
    =================================

    Configures the `cookie_consent` app, including its name, verbose name,
    and default auto field type.

    Attributes:
    -----------
    name : str
        The internal name of the app.
    verbose_name : str
        The human-readable name of the app, used in the Django admin.
    default_auto_field : str
        The default field type for primary keys in models.
    """

    name = "swing_cookie"
    verbose_name = _("Swing Cookie")
    default_auto_field = "django.db.models.AutoField"

    def ready(self) -> None:
        """
        Ready Method
        ============

        This method is executed when the Django app is ready. It can be used
        to import signals, register tasks, or perform other setup actions.

        Returns:
        --------
        None
        """
        import cookie_consent.signals  # Ensure signals are registered when the app is loaded


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "CookieConfig",
]
