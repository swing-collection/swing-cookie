# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Model Module
===========================

This module defines the `CookieConsentModel`, which tracks user consent
for different categories of cookies (e.g., necessary, analytics, marketing).

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local


# =============================================================================
# Class
# =============================================================================

# Ensures compatibility with custom User models
User: type[AbstractUser] = get_user_model()


class CookieConsentModel(models.Model):
    """
    Cookie Consent Model
    ====================

    Tracks user consent status for different types of cookies.

    Attributes:
    -----------
    user : User
        The user who provided the consent.
    necessary : bool
        Whether the user consented to necessary cookies.
    analytics : bool
        Whether the user consented to analytics cookies.
    marketing : bool
        Whether the user consented to marketing cookies.
    consent_given : bool
        Whether the user has given overall consent.
    consent_date : datetime
        The timestamp when consent was last updated.
    created_at : datetime
        The timestamp when the consent record was created.
    updated_at : datetime
        The timestamp when the consent record was last updated.

    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cookie_consent",
        verbose_name=_("User"),
        help_text=_("The user who provided the cookie consent."),
    )

    necessary = models.BooleanField(
        _("Necessary"),
        default=True,
        help_text=_("Consent for necessary cookies."),
    )

    analytics = models.BooleanField(
        _("Analytics"),
        default=False,
        help_text=_("Consent for analytics cookies."),
    )

    marketing = models.BooleanField(
        _("Marketing"),
        default=False,
        help_text=_("Consent for marketing cookies."),
    )

    consent_given = models.BooleanField(
        _("Consent Given"),
        default=False,
        help_text=_("Indicates if the user has given overall cookie consent."),
    )

    consent_date = models.DateTimeField(
        _("Consent Date"),
        auto_now_add=True,
        help_text=_("The timestamp when the user last updated their consent."),
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        help_text=_("The timestamp when the consent record was created."),
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
        help_text=_("The timestamp when the consent record was last updated."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the `CookieConsentModel` class.
        """

        verbose_name: str = _("Cookie Consent")
        verbose_name_plural: str = _("Cookie Consents")
        ordering: list[str] = ["-created_at"]

    def __str__(self) -> str:
        """
        Returns a string representation of the user's consent status.

        Returns:
        --------
        str
            The user's username and their consent status.
        """
        return f"{self.user.username} - Consent Given: {self.consent_given}"

    def update_consent(
        self,
        necessary: bool,
        analytics: bool,
        marketing: bool,
    ) -> None:
        """
        Updates the user's cookie consent preferences.

        Parameters:
        -----------
        necessary : bool
            Whether the user consents to necessary cookies.
        analytics : bool
            Whether the user consents to analytics cookies.
        marketing : bool
            Whether the user consents to marketing cookies.

        Returns:
        --------
        None
        """
        self.necessary: bool = necessary
        self.analytics: bool = analytics
        self.marketing: bool = marketing
        self.consent_given: bool = necessary or analytics or marketing
        self.save()

    def has_given_full_consent(self) -> bool:
        """
        Checks if the user has given consent to all cookie categories.

        Returns:
        --------
        bool
            True if consent is given for all categories, otherwise False.
        """
        return self.necessary and self.analytics and self.marketing


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieConsentModel",
]
