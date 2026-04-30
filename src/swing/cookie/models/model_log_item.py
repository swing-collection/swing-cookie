# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Log Item Model Module
=====================

This module provides the `LogItem` model for tracking cookie consent
actions. It creates an audit trail of when users accept or decline
cookie groups.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Optional, TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local
from .model_cookie_group import CookieGroupModel

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    from django.http import HttpRequest


# =============================================================================
# Constants
# =============================================================================

ACTION_ACCEPTED = "accepted"
ACTION_DECLINED = "declined"

ACTION_CHOICES = [
    (ACTION_ACCEPTED, _("Accepted")),
    (ACTION_DECLINED, _("Declined")),
]


# =============================================================================
# Class
# =============================================================================


class LogItem(models.Model):
    """
    Log Item Model
    ==============

    Records consent actions (accept/decline) for cookie groups.
    This provides an audit trail for GDPR compliance.

    Attributes:
    -----------
    action : str
        The action taken (accepted or declined).
    cookiegroup : CookieGroup
        The cookie group for which consent was given/withdrawn.
    user : User | None
        The authenticated user (if any).
    session_key : str | None
        The session key for anonymous users.
    ip_address : str | None
        The IP address of the user.
    user_agent : str | None
        The user agent string of the browser.
    timestamp : datetime
        The timestamp when the action was taken.
    version : str | None
        The cookie group version at the time of consent.
    """

    action = models.CharField(
        _("Action"),
        max_length=10,
        choices=ACTION_CHOICES,
        help_text=_("The consent action taken by the user."),
    )

    cookiegroup = models.ForeignKey(
        CookieGroupModel,
        verbose_name=_("Cookie Group"),
        on_delete=models.CASCADE,
        related_name="log_items",
        help_text=_("The cookie group for which consent was given."),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cookie_consent_logs",
        help_text=_("The authenticated user who gave consent (if any)."),
    )

    session_key = models.CharField(
        _("Session Key"),
        max_length=40,
        blank=True,
        null=True,
        db_index=True,
        help_text=_("The session key for anonymous users."),
    )

    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        blank=True,
        null=True,
        help_text=_("The IP address of the user."),
    )

    user_agent = models.TextField(
        _("User Agent"),
        blank=True,
        null=True,
        help_text=_("The user agent string of the browser."),
    )

    version = models.CharField(
        _("Version"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_(
            "The cookie group version at the time of consent. "
            "Used to verify valid consent for specific cookie versions."
        ),
    )

    timestamp = models.DateTimeField(
        _("Timestamp"),
        auto_now_add=True,
        db_index=True,
        help_text=_("The timestamp when the action was taken."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the LogItem model.
        """

        verbose_name = _("Consent Log")
        verbose_name_plural = _("Consent Logs")
        ordering = ["-timestamp"]
        indexes = [
            models.Index(
                fields=["user", "cookiegroup"],
                name="logitem_user_group_idx",
            ),
            models.Index(
                fields=["session_key", "cookiegroup"],
                name="logitem_session_group_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Returns a string representation of the log item.

        Returns:
        --------
        str
            A human-readable description of the consent action.
        """
        user_str = (
            self.user.username
            if self.user
            else f"Anonymous ({self.session_key or 'no session'})"
        )
        return f"{user_str} {self.action} {self.cookiegroup.name}"

    @classmethod
    def log_consent(
        cls,
        action: str,
        cookiegroup: CookieGroupModel,
        request: Optional["HttpRequest"] = None,
        user: Optional["AbstractUser"] = None,
        session_key: Optional[str] = None,
    ) -> "LogItem":
        """
        Creates a log entry for a consent action.

        Parameters:
        -----------
        action : str
            The action taken (ACTION_ACCEPTED or ACTION_DECLINED).
        cookiegroup : CookieGroupModel
            The cookie group for which consent was given.
        request : HttpRequest | None
            The HTTP request object (for extracting IP and user agent).
        user : User | None
            The authenticated user (overrides request.user if provided).
        session_key : str | None
            The session key (overrides request.session.session_key if provided).

        Returns:
        --------
        LogItem
            The created log entry.
        """
        ip_address = None
        user_agent = None
        resolved_user = user
        resolved_session_key = session_key

        if request:
            # Extract IP address
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(",")[0].strip()
            else:
                ip_address = request.META.get("REMOTE_ADDR")

            # Extract user agent
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

            # Use request user if not explicitly provided
            if resolved_user is None and hasattr(request, "user"):
                if request.user.is_authenticated:
                    resolved_user = request.user

            # Use request session if not explicitly provided
            if resolved_session_key is None and hasattr(request, "session"):
                resolved_session_key = request.session.session_key

        return cls.objects.create(
            action=action,
            cookiegroup=cookiegroup,
            user=resolved_user,
            session_key=resolved_session_key,
            ip_address=ip_address,
            user_agent=user_agent,
            version=cookiegroup.get_version(),
        )


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "ACTION_ACCEPTED",
    "ACTION_DECLINED",
    "ACTION_CHOICES",
    "LogItem",
]
