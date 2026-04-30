# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Model Module
===========================

This module defines the `CookieConsentModel`, which tracks user consent
for different categories of cookies (e.g., necessary, analytics, marketing).

Supports both authenticated and anonymous users.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Import | Local
from .model_cookie_policy import CookiePolicyModel

if TYPE_CHECKING:
    from django.http import HttpRequest


# =============================================================================
# Class
# =============================================================================


class CookieConsentModel(models.Model):
    """
    Cookie Consent Model
    ====================

    Tracks user consent status for different types of cookies.
    Supports both authenticated and anonymous users.

    Attributes:
    -----------
    user : User | None
        The user who provided the consent (for authenticated users).
    session_key : str | None
        The session key for anonymous users.
    policy_version : CookiePolicyModel | None
        The policy version the user consented to.
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
    ip_address : str | None
        The IP address when consent was given.
    created_at : datetime
        The timestamp when the consent record was created.
    updated_at : datetime
        The timestamp when the consent record was last updated.

    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cookie_consent",
        verbose_name=_("User"),
        null=True,
        blank=True,
        help_text=_("The authenticated user who provided consent."),
    )

    session_key = models.CharField(
        _("Session Key"),
        max_length=40,
        blank=True,
        null=True,
        db_index=True,
        help_text=_("The session key for anonymous users."),
    )

    policy_version = models.ForeignKey(
        CookiePolicyModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consents",
        verbose_name=_("Policy Version"),
        help_text=_(
            "The cookie policy version the user consented to. "
            "When a new policy is published, users may need to re-consent."
        ),
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
        default=timezone.now,
        help_text=_("The timestamp when the user last updated their consent."),
    )

    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        blank=True,
        null=True,
        help_text=_("The IP address when consent was given."),
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
        constraints = [
            models.CheckConstraint(
                condition=models.Q(user__isnull=False)
                | models.Q(session_key__isnull=False),
                name="consent_requires_user_or_session",
            ),
        ]
        indexes = [
            models.Index(
                fields=["session_key"],
                name="consent_session_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Returns a string representation of the user's consent status.

        Returns:
        --------
        str
            The user's identifier and their consent status.
        """
        if self.user:
            identifier = self.user.username
        else:
            identifier = f"Anonymous ({self.session_key or 'no session'})"
        return f"{identifier} - Consent Given: {self.consent_given}"

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
        self.necessary = necessary
        self.analytics = analytics
        self.marketing = marketing
        self.consent_given = necessary or analytics or marketing
        self.consent_date = timezone.now()
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

    def needs_reconsent(self) -> bool:
        """
        Checks if the user needs to re-consent due to a new policy version.

        Returns:
        --------
        bool
            True if a newer policy version exists, otherwise False.
        """
        if not self.policy_version:
            return True
        latest_policy = (
            CookiePolicyModel.objects.filter(is_active=True)
            .order_by("-version")
            .first()
        )
        if not latest_policy:
            return False
        return latest_policy.pk != self.policy_version.pk

    @classmethod
    def get_or_create_for_request(
        cls,
        request: "HttpRequest",
    ) -> tuple["CookieConsentModel", bool]:
        """
        Gets or creates a consent record for the current request.

        Works for both authenticated and anonymous users.

        Parameters:
        -----------
        request : HttpRequest
            The current HTTP request.

        Returns:
        --------
        tuple[CookieConsentModel, bool]
            A tuple of (consent_record, created).
        """
        # Extract IP address
        ip_address = None
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        if hasattr(request, "user") and request.user.is_authenticated:
            # Authenticated user
            consent, created = cls.objects.get_or_create(
                user=request.user,
                defaults={
                    "ip_address": ip_address,
                },
            )
        else:
            # Anonymous user - use session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key

            consent, created = cls.objects.get_or_create(
                session_key=session_key,
                user__isnull=True,
                defaults={
                    "ip_address": ip_address,
                },
            )

        # Update IP if changed
        if not created and consent.ip_address != ip_address:
            consent.ip_address = ip_address
            consent.save(update_fields=["ip_address"])

        return consent, created


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieConsentModel",
]
