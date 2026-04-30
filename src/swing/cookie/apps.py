# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Cookie Config App Configuration
=================================

This module contains the configuration settings for the Swing Cookie
Django app.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Import | Local Modules


# =============================================================================
# App Configuration
# =============================================================================


class SwingCookieConfig(AppConfig):
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

    name = "swing.cookie"
    verbose_name: str = _("Swing Cookie")
    default_auto_field: str = "django.db.models.AutoField"

    # def ready(self) -> None:
    #     """
    #     Ready Method
    #     ============

    #     This method is executed when the Django app is ready. It can be used
    #     to import signals, register tasks, or perform other setup actions.

    #     Returns:
    #     --------
    #     None

    #     """

    #     # Ensure signals are registered when the app is loaded
    #     import swing.cookie.signals


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "SwingCookieConfig",
]
